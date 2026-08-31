#!/usr/bin/env python3
"""
main.py

Pré-plotter para EggBot via Arduino + EggDuino.

CLI com argparse para executar movimentos simples de teste
e demonstração do sistema.

Uso:
    python3 main.py [--port /dev/ttyACM0] [--run] [--test-name]
"""

import argparse
import logging
import sys
from .eggduino import EggDuinoSerial
from .planner import LinePlanner, MoveCommand
from .patterns import PatternGenerator


# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)


class PrePlotter:
    """Controlador principal do pré-plotter."""

    def __init__(self, port: str = "/dev/ttyACM0", baudrate: int = 9600):
        """Inicializa pré-plotter."""
        self.port = port
        self.baudrate = baudrate
        self.eggduino = EggDuinoSerial(port=port, baudrate=baudrate)
        self.current_rotation = 0.0
        self.current_arm = 0.0

    def connect(self) -> bool:
        """Conecta ao Arduino."""
        logger.info(f"[PREPLOTTER] port={self.port}, baud={self.baudrate}")
        return self.eggduino.connect()

    def disconnect(self) -> bool:
        """Desconecta do Arduino."""
        return self.eggduino.disconnect()

    def validate_connection(self) -> bool:
        """Valida que EggDuino está respondendo."""
        if not self.eggduino.detect_eggduino():
            logger.error("[PREPLOTTER] Falha ao detectar EggDuino")
            return False
        logger.info("[SERIAL] EggDuino detectado")
        return True

    def prepare(self) -> bool:
        """Prepara o sistema (conecta, valida, habilita motores)."""
        logger.info("\n[PREPLOTTER] === Inicializando ===\n")

        if not self.connect():
            return False

        if not self.validate_connection():
            return False

        if not self.eggduino.enable_motors():
            return False

        logger.info("[PREPLOTTER] Sistema pronto\n")
        return True

    def cleanup(self) -> bool:
        """Limpa o sistema (desabilita motores, desconecta)."""
        logger.info("\n[PREPLOTTER] === Finalizando ===\n")

        self.eggduino.disable_motors()
        return self.disconnect()

    def plot_line(
        self,
        start_rotation: float,
        start_arm: float,
        end_rotation: float,
        end_arm: float,
        speed: float
    ) -> bool:
        """
        Executa plotagem de uma linha.

        Args:
            start_rotation: Posição inicial rotação
            start_arm: Posição inicial braço
            end_rotation: Posição final rotação
            end_arm: Posição final braço
            speed: Velocidade (steps/segundo)

        Returns:
            bool: True se execução foi bem-sucedida
        """
        logger.info("[PLAN]")
        logger.info(f"start: rotation={start_rotation} arm={start_arm}")
        logger.info(f"end:   rotation={end_rotation} arm={end_arm}\n")

        try:
            move_cmd = LinePlanner.plan_line(
                start_rotation=start_rotation,
                start_arm=start_arm,
                end_rotation=end_rotation,
                end_arm=end_arm,
                speed=speed
            )

            # Log do plano
            distance = LinePlanner.calculate_distance(
                move_cmd.rotation_steps,
                move_cmd.arm_steps
            )
            logger.info(f"rotation_delta={move_cmd.rotation_steps}")
            logger.info(f"arm_delta={move_cmd.arm_steps}")
            logger.info(f"distance={distance:.0f}")
            logger.info(f"duration_ms={move_cmd.duration_ms}\n")

            # Executar movimento
            if not self.eggduino.move(
                move_cmd.duration_ms,
                move_cmd.arm_steps,
                move_cmd.rotation_steps
            ):
                logger.error("[PLOT] Erro ao executar movimento")
                return False

            # Aguardar conclusão
            self.eggduino.wait_for_move(move_cmd.duration_ms)

            # Atualizar posição atual
            self.current_rotation = end_rotation
            self.current_arm = end_arm

            logger.info("[PLOT] Movimento concluído\n")
            return True

        except ValueError as e:
            logger.error(f"[PLAN] Erro de validação: {e}")
            return False

    def test_reference_move(self) -> bool:
        """Teste 1: Referência já validada (SM,2000,0,800)."""
        logger.info("=" * 50)
        logger.info("TESTE 1: Movimento de Referência")
        logger.info("Esperado: SM,2000,0,800")
        logger.info("=" * 50)
        logger.info("")

        return self.plot_line(
            start_rotation=0,
            start_arm=0,
            end_rotation=800,
            end_arm=0,
            speed=400
        )

    def test_return_move(self) -> bool:
        """Teste 2: Retorno ao ponto inicial."""
        logger.info("=" * 50)
        logger.info("TESTE 2: Movimento de Retorno")
        logger.info("Esperado: SM,2000,0,-800")
        logger.info("=" * 50)
        logger.info("")

        return self.plot_line(
            start_rotation=800,
            start_arm=0,
            end_rotation=0,
            end_arm=0,
            speed=400
        )

    def test_arm_axis(self) -> bool:
        """Teste 3: Eixo do braço."""
        logger.info("=" * 50)
        logger.info("TESTE 3: Eixo do Braço")
        logger.info("=" * 50)
        logger.info("")

        # Movimento positivo do braço
        if not self.plot_line(
            start_rotation=0,
            start_arm=0,
            end_rotation=0,
            end_arm=800,
            speed=400
        ):
            return False

        # Retorno do braço
        logger.info("\n[TESTE] Aguardando antes de retorno...")
        import time
        time.sleep(1)

        return self.plot_line(
            start_rotation=0,
            start_arm=800,
            end_rotation=0,
            end_arm=0,
            speed=400
        )

    def test_diagonal_move(self) -> bool:
        """Teste 4: Movimento diagonal (sincronização de eixos)."""
        logger.info("=" * 50)
        logger.info("TESTE 4: Movimento Diagonal")
        logger.info("Ambos eixos se movem simultaneamente")
        logger.info("=" * 50)
        logger.info("")

        return self.plot_line(
            start_rotation=0,
            start_arm=0,
            end_rotation=800,
            end_arm=400,
            speed=400
        )

    def execute_pattern(self, segments) -> bool:
        """
        Executa uma sequência de segmentos de padrão.

        Args:
            segments: Lista de LineSegment do padrão

        Returns:
            bool: True se execução foi bem-sucedida
        """
        logger.info(f"[PADRÃO] Executando {len(segments)} segmentos\n")

        for i, segment in enumerate(segments):
            logger.info(f"[PADRÃO] Segmento {i+1}/{len(segments)}")

            if not self.plot_line(
                start_rotation=segment.start_rotation,
                start_arm=segment.start_arm,
                end_rotation=segment.end_rotation,
                end_arm=segment.end_arm,
                speed=segment.speed
            ):
                logger.error(f"[PADRÃO] Erro no segmento {i+1}")
                return False

        logger.info(f"[PADRÃO] ✓ Padrão concluído\n")
        return True

    def pattern_sine_wave(self) -> bool:
        """Padrão: Onda Senoide (do topo à base do ovo)."""
        logger.info("=" * 60)
        logger.info("PADRÃO: Onda Senoide")
        logger.info("Descrição: Traça uma onda senoidal do topo à base do ovo")
        logger.info("=" * 60)
        logger.info("")

        segments = PatternGenerator.sine_wave(
            rotation_start=0,
            rotation_end=3200,
            amplitude=500,
            speed=250,
            num_points=64,
            vertical_offset=200
        )

        return self.execute_pattern(segments)

    def pattern_multi_sine_wave(self) -> bool:
        """Padrão: Múltiplas Ondas Senoides."""
        logger.info("=" * 60)
        logger.info("PADRÃO: Múltiplas Ondas Senoides")
        logger.info("Descrição: Traça 2 períodos de senoide")
        logger.info("=" * 60)
        logger.info("")

        segments = PatternGenerator.multi_sine_wave(
            rotation_start=0,
            rotation_end=3200,
            amplitude=400,
            speed=250,
            num_periods=2,
            num_points=128,
            vertical_offset=300
        )

        return self.execute_pattern(segments)

    def pattern_spiral(self) -> bool:
        """Padrão: Espiral."""
        logger.info("=" * 60)
        logger.info("PADRÃO: Espiral")
        logger.info("Descrição: Traça uma espiral de dentro para fora")
        logger.info("=" * 60)
        logger.info("")

        segments = PatternGenerator.spiral(
            rotation_start=0,
            rotation_end=3200,
            arm_start=100,
            arm_end=1000,
            speed=300,
            num_points=256,
            num_turns=4
        )

        return self.execute_pattern(segments)

    def pattern_square(self) -> bool:
        """Padrão: Quadrado."""
        logger.info("=" * 60)
        logger.info("PADRÃO: Quadrado")
        logger.info("Descrição: Traça um quadrado")
        logger.info("=" * 60)
        logger.info("")

        segments = PatternGenerator.square(
            center_rotation=1600,
            center_arm=400,
            size=300,
            speed=300
        )

        return self.execute_pattern(segments)

    def pattern_circle(self) -> bool:
        """Padrão: Círculo."""
        logger.info("=" * 60)
        logger.info("PADRÃO: Círculo")
        logger.info("Descrição: Traça um círculo")
        logger.info("=" * 60)
        logger.info("")

        segments = PatternGenerator.circle(
            center_rotation=1600,
            center_arm=400,
            radius=300,
            speed=300,
            num_points=128
        )

        return self.execute_pattern(segments)

    def pattern_star(self) -> bool:
        """Padrão: Estrela."""
        logger.info("=" * 60)
        logger.info("PADRÃO: Estrela")
        logger.info("Descrição: Traça uma estrela de 5 pontas")
        logger.info("=" * 60)
        logger.info("")

        segments = PatternGenerator.star(
            center_rotation=1600,
            center_arm=400,
            outer_radius=400,
            inner_radius=150,
            speed=300,
            num_points=5
        )

        return self.execute_pattern(segments)


def parse_arguments():
    """Parse dos argumentos da linha de comando."""
    parser = argparse.ArgumentParser(
        description="EggBot Pré-Plotter - Plotter sem interface gráfica para Ubuntu"
    )

    parser.add_argument(
        "--port",
        type=str,
        default="/dev/ttyACM0",
        help="Porta serial (padrão: /dev/ttyACM0)"
    )

    parser.add_argument(
        "--baud",
        type=int,
        default=9600,
        help="Taxa de baud (padrão: 9600)"
    )

    parser.add_argument(
        "--run",
        action="store_true",
        help="Autoriza execução de movimento (segurança)"
    )

    parser.add_argument(
        "--test",
        type=str,
        choices=["reference", "return", "arm", "diagonal", "all"],
        default="reference",
        help="Teste a executar (padrão: reference)"
    )

    parser.add_argument(
        "--start-rotation",
        type=float,
        default=None,
        help="Posição inicial rotação (custom)"
    )

    parser.add_argument(
        "--start-arm",
        type=float,
        default=None,
        help="Posição inicial braço (custom)"
    )

    parser.add_argument(
        "--end-rotation",
        type=float,
        default=None,
        help="Posição final rotação (custom)"
    )

    parser.add_argument(
        "--end-arm",
        type=float,
        default=None,
        help="Posição final braço (custom)"
    )

    parser.add_argument(
        "--speed",
        type=float,
        default=400,
        help="Velocidade em steps/segundo (padrão: 400)"
    )

    parser.add_argument(
        "--pattern",
        type=str,
        choices=["sine", "multi-sine", "spiral", "square", "circle", "star"],
        default=None,
        help="Padrão de desenho predefinido"
    )

    return parser.parse_args()


def main():
    """Função principal."""
    args = parse_arguments()

    # Verificar autorização de execução
    if not args.run:
        logger.warning("\n[AVISO] Modo de simulação (nenhum movimento será executado)")
        logger.warning("[AVISO] Use --run para autorizar execução real\n")
        logger.info("Exemplo:")
        logger.info("  python3 -m preplotter.main --port /dev/ttyACM0 --run --test reference\n")
        return 0

    # Criar e inicializar pré-plotter
    plotter = PrePlotter(port=args.port, baudrate=args.baud)

    try:
        # Preparar sistema
        if not plotter.prepare():
            logger.error("[PREPLOTTER] Falha na preparação")
            return 1

        # Executar teste ou movimento custom
        success = False

        if args.pattern:
            # Executar padrão
            if args.pattern == "sine":
                success = plotter.pattern_sine_wave()
            elif args.pattern == "multi-sine":
                success = plotter.pattern_multi_sine_wave()
            elif args.pattern == "spiral":
                success = plotter.pattern_spiral()
            elif args.pattern == "square":
                success = plotter.pattern_square()
            elif args.pattern == "circle":
                success = plotter.pattern_circle()
            elif args.pattern == "star":
                success = plotter.pattern_star()

        elif args.start_rotation is not None:
            # Movimento customizado
            if args.end_rotation is None or args.end_arm is None:
                logger.error("[CLI] Faltam parâmetros para movimento customizado")
                logger.error("[CLI] Use: --start-rotation, --start-arm, --end-rotation, --end-arm")
                return 1

            success = plotter.plot_line(
                start_rotation=args.start_rotation,
                start_arm=args.start_arm or 0.0,
                end_rotation=args.end_rotation,
                end_arm=args.end_arm,
                speed=args.speed
            )

        elif args.test == "reference":
            success = plotter.test_reference_move()
        elif args.test == "return":
            success = plotter.test_return_move()
        elif args.test == "arm":
            success = plotter.test_arm_axis()
        elif args.test == "diagonal":
            success = plotter.test_diagonal_move()
        elif args.test == "all":
            success = (
                plotter.test_reference_move() and
                plotter.test_return_move() and
                plotter.test_arm_axis() and
                plotter.test_diagonal_move()
            )

        if not success:
            logger.error("[PREPLOTTER] Erro durante execução")
            return 1

        logger.info("[PREPLOTTER] ✓ Executado com sucesso")
        return 0

    except KeyboardInterrupt:
        logger.warning("\n[PREPLOTTER] Interrompido pelo usuário")
        return 1

    except Exception as e:
        logger.error(f"[PREPLOTTER] Erro não esperado: {e}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        # Sempre limpar ao sair
        plotter.cleanup()


if __name__ == "__main__":
    sys.exit(main())
