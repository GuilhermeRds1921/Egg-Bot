"""
planner.py

Módulo de planejamento de movimento.

Responsável por:
- Receber coordenadas de início e fim (rotation, arm)
- Calcular delta de movimentos
- Calcular duração baseada em distância e velocidade
- Retornar comando de movimento estruturado
"""

import math
from dataclasses import dataclass


@dataclass
class MoveCommand:
    """Representa um comando de movimento estruturado."""
    rotation_steps: int
    arm_steps: int
    duration_ms: int

    def __str__(self):
        return f"MoveCommand(rot={self.rotation_steps}, arm={self.arm_steps}, dur={self.duration_ms}ms)"


class LinePlanner:
    """Planejador de linhas de movimento."""

    # Limites de segurança
    MAX_STEPS_PER_COMMAND = 100000  # Máximo de passos por comando
    MIN_SPEED = 1                   # Velocidade mínima (steps/s)
    MIN_DURATION_MS = 10            # Duração mínima (ms)

    @staticmethod
    def plan_line(
        start_rotation: float,
        start_arm: float,
        end_rotation: float,
        end_arm: float,
        speed: float
    ) -> MoveCommand:
        """
        Planeja um movimento de linha reta entre dois pontos.

        Args:
            start_rotation: Posição inicial do eixo de rotação (em steps)
            start_arm: Posição inicial do eixo do braço (em steps)
            end_rotation: Posição final do eixo de rotação (em steps)
            end_arm: Posição final do eixo do braço (em steps)
            speed: Velocidade do movimento (steps/segundo)

        Returns:
            MoveCommand: Comando estruturado com passos e duração

        Raises:
            ValueError: Se parâmetros de entrada forem inválidos
        """

        # Validações de entrada
        if speed <= 0:
            raise ValueError(f"Speed deve ser positivo, recebido: {speed}")

        # Calcular deltas
        rotation_delta = end_rotation - start_rotation
        arm_delta = end_arm - start_arm

        # Calcular distância euclidiana
        distance = math.sqrt(rotation_delta**2 + arm_delta**2)

        # Se a distância é zero, comando trivial
        if distance == 0:
            return MoveCommand(
                rotation_steps=0,
                arm_steps=0,
                duration_ms=LinePlanner.MIN_DURATION_MS
            )

        # Calcular duração em segundos
        duration_seconds = distance / speed

        # Converter para milissegundos
        duration_ms = int(duration_seconds * 1000)

        # Garantir duração mínima
        if duration_ms < LinePlanner.MIN_DURATION_MS:
            duration_ms = LinePlanner.MIN_DURATION_MS

        # Validar limites de passos
        if abs(rotation_delta) > LinePlanner.MAX_STEPS_PER_COMMAND:
            raise ValueError(
                f"Rotation delta ({rotation_delta}) excede limite "
                f"({LinePlanner.MAX_STEPS_PER_COMMAND})"
            )
        if abs(arm_delta) > LinePlanner.MAX_STEPS_PER_COMMAND:
            raise ValueError(
                f"Arm delta ({arm_delta}) excede limite "
                f"({LinePlanner.MAX_STEPS_PER_COMMAND})"
            )

        return MoveCommand(
            rotation_steps=int(rotation_delta),
            arm_steps=int(arm_delta),
            duration_ms=duration_ms
        )

    @staticmethod
    def calculate_distance(rotation_delta: float, arm_delta: float) -> float:
        """Calcula distância euclidiana entre dois pontos."""
        return math.sqrt(rotation_delta**2 + arm_delta**2)
