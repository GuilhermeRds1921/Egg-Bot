"""
eggduino.py

Módulo de comunicação serial com Arduino (EggDuino).

Responsável por:
- Abrir e gerenciar conexão serial
- Enviar/receber comandos
- Validar protocolos
- Controlar motores e movimento
"""

import serial
import time
import logging
from typing import Optional


# Configuração de logging
logger = logging.getLogger(__name__)


class EggDuinoSerial:
    """Gerenciador de comunicação serial com Arduino (EggDuino)."""

    # Configuração serial padrão
    DEFAULT_BAUDRATE = 9600
    DEFAULT_TIMEOUT = 2.0
    COMMAND_TERMINATOR = "\r"

    # Espera entre comandos (ms)
    COMMAND_DELAY_MS = 50

    def __init__(
        self,
        port: str = "/dev/ttyACM0",
        baudrate: int = DEFAULT_BAUDRATE,
        timeout: float = DEFAULT_TIMEOUT
    ):
        """
        Inicializa gerenciador serial.

        Args:
            port: Porta serial (ex: /dev/ttyACM0 ou /dev/ttyUSB0)
            baudrate: Taxa de baud (padrão 9600)
            timeout: Timeout de leitura (segundos)
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None
        self.connected = False

    def connect(self) -> bool:
        """
        Abre conexão serial.

        Returns:
            bool: True se conexão foi bem-sucedida
        """
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            time.sleep(2)  # Aguardar Arduino reiniciar após conexão
            self.connected = True
            logger.info(f"[SERIAL] Conectado a {self.port} @ {self.baudrate} baud")
            return True
        except serial.SerialException as e:
            logger.error(f"[SERIAL] Erro ao conectar: {e}")
            self.connected = False
            return False

    def disconnect(self) -> bool:
        """
        Fecha conexão serial.

        Returns:
            bool: True se desconexão foi bem-sucedida
        """
        if self.serial and self.serial.is_open:
            try:
                self.serial.close()
                self.connected = False
                logger.info("[SERIAL] Desconectado")
                return True
            except serial.SerialException as e:
                logger.error(f"[SERIAL] Erro ao desconectar: {e}")
                return False
        return True

    def send_command(self, command: str, read_response: bool = True) -> Optional[str]:
        """
        Envia comando e opcionalmente lê resposta.

        Args:
            command: Comando a enviar (sem terminador)
            read_response: Se deve ler resposta

        Returns:
            str: Resposta recebida (se read_response=True), None caso contrário
        """
        if not self.connected or not self.serial:
            logger.error("[SERIAL] Não conectado")
            return None

        try:
            # Enviar comando com terminador
            full_command = command + self.COMMAND_TERMINATOR
            self.serial.write(full_command.encode())
            logger.debug(f"[SERIAL] > {command}")

            # Pequeno delay
            time.sleep(self.COMMAND_DELAY_MS / 1000.0)

            # Ler resposta se solicitado
            response = None
            if read_response:
                response = self.serial.readline().decode().strip()
                if response:
                    logger.debug(f"[SERIAL] < {response}")

            return response

        except serial.SerialException as e:
            logger.error(f"[SERIAL] Erro ao enviar comando: {e}")
            return None

    def detect_eggduino(self) -> bool:
        """
        Detecta se EggDuino está respondendo.

        Envia comando 'v' e verifica resposta.

        Returns:
            bool: True se EggDuino respondeu
        """
        if not self.connected:
            return False

        try:
            response = self.send_command("v", read_response=True)
            if response and len(response) > 0:
                logger.info(f"[SERIAL] EggDuino detectado: {response}")
                return True
            else:
                logger.warning("[SERIAL] Nenhuma resposta do EggDuino")
                return False
        except Exception as e:
            logger.error(f"[SERIAL] Erro ao detectar EggDuino: {e}")
            return False

    def enable_motors(self) -> bool:
        """
        Habilita os motores.

        Envia comando EM,1

        Returns:
            bool: True se comando foi bem-sucedido
        """
        response = self.send_command("EM,1", read_response=True)
        if response:
            logger.info("[MOTOR] Motores habilitados")
            return True
        logger.warning("[MOTOR] Erro ao habilitar motores")
        return False

    def disable_motors(self) -> bool:
        """
        Desabilita os motores.

        Envia comando EM,0

        Returns:
            bool: True se comando foi bem-sucedido
        """
        response = self.send_command("EM,0", read_response=True)
        if response:
            logger.info("[MOTOR] Motores desabilitados")
            return True
        logger.warning("[MOTOR] Erro ao desabilitar motores")
        return False

    def move(
        self,
        duration_ms: int,
        arm_steps: int,
        rotation_steps: int
    ) -> bool:
        """
        Envia comando de movimento.

        Formato: SM,<duration_ms>,<arm_steps>,<rotation_steps>

        Args:
            duration_ms: Duração do movimento em milissegundos
            arm_steps: Passos do eixo do braço (pode ser negativo)
            rotation_steps: Passos do eixo de rotação (pode ser negativo)

        Returns:
            bool: True se comando foi bem-sucedido
        """
        command = f"SM,{duration_ms},{arm_steps},{rotation_steps}"
        response = self.send_command(command, read_response=True)
        if response:
            logger.info(f"[MOVE] {command}")
            return True
        logger.warning(f"[MOVE] Erro ao executar movimento: {command}")
        return False

    def wait_for_move(self, duration_ms: int) -> None:
        """
        Aguarda conclusão de um movimento.

        Args:
            duration_ms: Duração estimada do movimento (ms)
        """
        wait_seconds = (duration_ms / 1000.0) + 0.5  # Adicionar margem
        logger.info(f"[WAIT] Aguardando {wait_seconds:.1f}s")
        time.sleep(wait_seconds)
