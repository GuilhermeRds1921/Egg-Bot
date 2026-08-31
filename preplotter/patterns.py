"""
patterns.py

Padrões predefinidos para desenho (senoide, quadrado, espiral, etc).

Cada padrão retorna uma lista de tuplas (start, end, speed) que podem
ser executadas sequencialmente com plot_line().
"""

import math
from typing import List, Tuple, NamedTuple


class LineSegment(NamedTuple):
    """Representa um segmento de linha."""
    start_rotation: float
    start_arm: float
    end_rotation: float
    end_arm: float
    speed: float


class PatternGenerator:
    """Gerador de padrões de desenho."""

    @staticmethod
    def sine_wave(
        rotation_start: float = 0,
        rotation_end: float = 3200,
        amplitude: float = 400,
        speed: float = 300,
        num_points: int = 64,
        vertical_offset: float = 0
    ) -> List[LineSegment]:
        """
        Gera uma senoide (onda).

        Args:
            rotation_start: Posição inicial em rotação (steps)
            rotation_end: Posição final em rotação (steps)
            amplitude: Amplitude da onda em passos do braço
            speed: Velocidade do desenho (steps/segundo)
            num_points: Número de pontos para discretizar a onda
            vertical_offset: Deslocamento vertical (posição base do braço)

        Returns:
            Lista de segmentos de linha
        """
        segments = []

        for i in range(num_points - 1):
            # Parâmetro t de 0 a 1
            t0 = i / (num_points - 1)
            t1 = (i + 1) / (num_points - 1)

            # Calcular posição em rotação
            rot_start = rotation_start + t0 * (rotation_end - rotation_start)
            rot_end = rotation_start + t1 * (rotation_end - rotation_start)

            # Calcular posição em braço usando senoide
            # 1 período completo de senoide (0 a 2π)
            arm_start = vertical_offset + amplitude * math.sin(2 * math.pi * t0)
            arm_end = vertical_offset + amplitude * math.sin(2 * math.pi * t1)

            segments.append(
                LineSegment(
                    start_rotation=rot_start,
                    start_arm=arm_start,
                    end_rotation=rot_end,
                    end_arm=arm_end,
                    speed=speed
                )
            )

        return segments

    @staticmethod
    def multi_sine_wave(
        rotation_start: float = 0,
        rotation_end: float = 3200,
        amplitude: float = 400,
        speed: float = 300,
        num_periods: int = 2,
        num_points: int = 128,
        vertical_offset: float = 0
    ) -> List[LineSegment]:
        """
        Gera múltiplos períodos de senoide (onda múltipla).

        Args:
            rotation_start: Posição inicial em rotação
            rotation_end: Posição final em rotação
            amplitude: Amplitude da onda
            speed: Velocidade do desenho
            num_periods: Quantos períodos de senoide (0 a 2π*num_periods)
            num_points: Número de pontos para discretizar
            vertical_offset: Deslocamento vertical

        Returns:
            Lista de segmentos de linha
        """
        segments = []

        for i in range(num_points - 1):
            t0 = i / (num_points - 1)
            t1 = (i + 1) / (num_points - 1)

            rot_start = rotation_start + t0 * (rotation_end - rotation_start)
            rot_end = rotation_start + t1 * (rotation_end - rotation_start)

            # Múltiplos períodos
            arm_start = vertical_offset + amplitude * math.sin(2 * math.pi * t0 * num_periods)
            arm_end = vertical_offset + amplitude * math.sin(2 * math.pi * t1 * num_periods)

            segments.append(
                LineSegment(
                    start_rotation=rot_start,
                    start_arm=arm_start,
                    end_rotation=rot_end,
                    end_arm=arm_end,
                    speed=speed
                )
            )

        return segments

    @staticmethod
    def spiral(
        rotation_start: float = 0,
        rotation_end: float = 3200,
        arm_start: float = 0,
        arm_end: float = 1000,
        speed: float = 300,
        num_points: int = 128,
        num_turns: int = 3
    ) -> List[LineSegment]:
        """
        Gera uma espiral.

        Args:
            rotation_start: Posição inicial em rotação
            rotation_end: Posição final em rotação
            arm_start: Posição inicial em braço
            arm_end: Posição final em braço
            speed: Velocidade do desenho
            num_points: Número de pontos para discretizar
            num_turns: Número de voltas da espiral

        Returns:
            Lista de segmentos de linha
        """
        segments = []

        for i in range(num_points - 1):
            t0 = i / (num_points - 1)
            t1 = (i + 1) / (num_points - 1)

            # Rotação
            rot_start = rotation_start + t0 * (rotation_end - rotation_start)
            rot_end = rotation_start + t1 * (rotation_end - rotation_start)

            # Braço (avança linearmente)
            arm_val_start = arm_start + t0 * (arm_end - arm_start)
            arm_val_end = arm_start + t1 * (arm_end - arm_start)

            # Adiciona ondulação senoidal
            arm_val_start += 200 * math.sin(2 * math.pi * t0 * num_turns)
            arm_val_end += 200 * math.sin(2 * math.pi * t1 * num_turns)

            segments.append(
                LineSegment(
                    start_rotation=rot_start,
                    start_arm=arm_val_start,
                    end_rotation=rot_end,
                    end_arm=arm_val_end,
                    speed=speed
                )
            )

        return segments

    @staticmethod
    def square(
        center_rotation: float = 1600,
        center_arm: float = 400,
        size: float = 300,
        speed: float = 300
    ) -> List[LineSegment]:
        """
        Gera um quadrado.

        Args:
            center_rotation: Centro em rotação
            center_arm: Centro em braço
            size: Tamanho do quadrado (semi-diagonal)
            speed: Velocidade do desenho

        Returns:
            Lista de segmentos de linha (4 lados)
        """
        # Vértices do quadrado
        v1 = (center_rotation - size, center_arm - size)
        v2 = (center_rotation + size, center_arm - size)
        v3 = (center_rotation + size, center_arm + size)
        v4 = (center_rotation - size, center_arm + size)

        segments = []

        # Lado 1: v1 → v2
        segments.append(LineSegment(v1[0], v1[1], v2[0], v2[1], speed))

        # Lado 2: v2 → v3
        segments.append(LineSegment(v2[0], v2[1], v3[0], v3[1], speed))

        # Lado 3: v3 → v4
        segments.append(LineSegment(v3[0], v3[1], v4[0], v4[1], speed))

        # Lado 4: v4 → v1
        segments.append(LineSegment(v4[0], v4[1], v1[0], v1[1], speed))

        return segments

    @staticmethod
    def circle(
        center_rotation: float = 1600,
        center_arm: float = 400,
        radius: float = 300,
        speed: float = 300,
        num_points: int = 64
    ) -> List[LineSegment]:
        """
        Gera um círculo.

        Args:
            center_rotation: Centro em rotação
            center_arm: Centro em braço
            radius: Raio do círculo
            speed: Velocidade do desenho
            num_points: Número de pontos para discretizar

        Returns:
            Lista de segmentos de linha
        """
        segments = []

        for i in range(num_points):
            angle_start = 2 * math.pi * i / num_points
            angle_end = 2 * math.pi * (i + 1) / num_points

            rot_start = center_rotation + radius * math.cos(angle_start)
            rot_end = center_rotation + radius * math.cos(angle_end)

            arm_start = center_arm + radius * math.sin(angle_start)
            arm_end = center_arm + radius * math.sin(angle_end)

            segments.append(
                LineSegment(rot_start, arm_start, rot_end, arm_end, speed)
            )

        return segments

    @staticmethod
    def star(
        center_rotation: float = 1600,
        center_arm: float = 400,
        outer_radius: float = 400,
        inner_radius: float = 150,
        speed: float = 300,
        num_points: int = 5
    ) -> List[LineSegment]:
        """
        Gera uma estrela.

        Args:
            center_rotation: Centro em rotação
            center_arm: Centro em braço
            outer_radius: Raio externo (pontas)
            inner_radius: Raio interno (vales)
            speed: Velocidade do desenho
            num_points: Número de pontas

        Returns:
            Lista de segmentos de linha
        """
        segments = []
        total_points = num_points * 2

        for i in range(total_points):
            angle_start = 2 * math.pi * i / total_points
            angle_end = 2 * math.pi * (i + 1) / total_points

            # Alterna entre raio externo e interno
            if i % 2 == 0:
                r_start = outer_radius
                r_end = inner_radius
            else:
                r_start = inner_radius
                r_end = outer_radius

            rot_start = center_rotation + r_start * math.cos(angle_start)
            rot_end = center_rotation + r_end * math.cos(angle_end)

            arm_start = center_arm + r_start * math.sin(angle_start)
            arm_end = center_arm + r_end * math.sin(angle_end)

            segments.append(
                LineSegment(rot_start, arm_start, rot_end, arm_end, speed)
            )

        return segments
