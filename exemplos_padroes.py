#!/usr/bin/env python3
"""
Exemplos de uso da geração de padrões com o preplotter.

Demonstra como usar PatternGenerator para criar padrões customizados
e executá-los no Arduino.
"""

from preplotter.main import PrePlotter
from preplotter.patterns import PatternGenerator


def exemplo_1_senoide_customizada():
    """Exemplo 1: Senoide com parâmetros customizados."""
    print("\n" + "="*60)
    print("EXEMPLO 1: Senoide Customizada")
    print("="*60)
    print("Cria uma onda senoidal com amplitude maior e mais pontos")
    
    # Gerar segmentos de padrão
    segments = PatternGenerator.sine_wave(
        rotation_start=0,
        rotation_end=3200,
        amplitude=600,      # ← Amplitude maior
        speed=200,          # ← Velocidade menor = mais precisão
        num_points=128,     # ← Mais pontos = padrão mais suave
        vertical_offset=300
    )
    
    print(f"\n✓ Gerados {len(segments)} segmentos")
    print(f"✓ Primeiro segmento: {segments[0]}")
    print(f"✓ Último segmento: {segments[-1]}")
    print("\nPara executar no Arduino:")
    print("  python3 -m preplotter.main --port /dev/ttyACM0 --run --pattern sine")


def exemplo_2_multiplos_padroes():
    """Exemplo 2: Executar múltiplos padrões em sequência."""
    print("\n" + "="*60)
    print("EXEMPLO 2: Múltiplos Padrões em Sequência")
    print("="*60)
    
    padroes = [
        ("Senoide", PatternGenerator.sine_wave(num_points=32)),
        ("Círculo", PatternGenerator.circle(num_points=64)),
        ("Espiral", PatternGenerator.spiral(num_points=128)),
    ]
    
    print("\nPadrões a executar:")
    for nome, segments in padroes:
        print(f"  • {nome}: {len(segments)} segmentos")


def exemplo_3_padroes_artisticos():
    """Exemplo 3: Criando padrões artísticos."""
    print("\n" + "="*60)
    print("EXEMPLO 3: Padrões Artísticos")
    print("="*60)
    
    # Senoide com múltiplos períodos
    print("\n1. Multi-Senoide (2 períodos):")
    multi_sine = PatternGenerator.multi_sine_wave(
        rotation_start=0,
        rotation_end=3200,
        amplitude=400,
        speed=250,
        num_periods=2,
        num_points=128
    )
    print(f"   ✓ {len(multi_sine)} segmentos")
    print(f"   ✓ Usa ambos os eixos para criar padrão complexo")
    
    # Espiral com parâmetros customizados
    print("\n2. Espiral Expandindo:")
    spiral = PatternGenerator.spiral(
        rotation_start=0,
        rotation_end=3200,
        arm_start=50,
        arm_end=1200,
        speed=300,
        num_points=256,
        num_turns=5  # ← Mais voltas que o padrão padrão
    )
    print(f"   ✓ {len(spiral)} segmentos")
    print(f"   ✓ Começa pequeno (50) e expande até 1200")
    
    # Estrela grande
    print("\n3. Estrela Grande:")
    star = PatternGenerator.star(
        center_rotation=1600,
        center_arm=400,
        outer_radius=450,
        inner_radius=100,
        speed=300,
        num_points=5
    )
    print(f"   ✓ {len(star)} segmentos")
    print(f"   ✓ Estrela geométrica perfeita")


def exemplo_4_entender_linearsegment():
    """Exemplo 4: Entender a estrutura LineSegment."""
    print("\n" + "="*60)
    print("EXEMPLO 4: Entendendo LineSegment")
    print("="*60)
    
    # Pegar um padrão
    segments = PatternGenerator.circle(num_points=4)
    
    print("\nEstrutura de um LineSegment:")
    print("  LineSegment(start_rotation, start_arm, end_rotation, end_arm, speed)")
    
    for i, seg in enumerate(segments):
        print(f"\nSegmento {i+1}:")
        print(f"  Inicial: rotation={seg.start_rotation:.1f}, arm={seg.start_arm:.1f}")
        print(f"  Final:   rotation={seg.end_rotation:.1f}, arm={seg.end_arm:.1f}")
        print(f"  Velocidade: {seg.speed} steps/s")


def exemplo_5_calcular_duracao():
    """Exemplo 5: Calcular duração de execução."""
    print("\n" + "="*60)
    print("EXEMPLO 5: Calcular Duração de Execução")
    print("="*60)
    
    import math
    
    padroes = {
        "Senoide": PatternGenerator.sine_wave(num_points=64),
        "Espiral": PatternGenerator.spiral(num_points=256),
        "Círculo": PatternGenerator.circle(num_points=128),
    }
    
    print("\nDuração estimada de cada padrão:\n")
    
    for nome, segments in padroes.items():
        tempo_total = 0
        
        for seg in segments:
            # Calcular distância euclidiana
            delta_rot = seg.end_rotation - seg.start_rotation
            delta_arm = seg.end_arm - seg.start_arm
            distance = math.sqrt(delta_rot**2 + delta_arm**2)
            
            # Calcular duração
            if seg.speed > 0:
                duration_ms = (distance / seg.speed) * 1000
                tempo_total += duration_ms / 1000.0
        
        print(f"  {nome}:")
        print(f"    • Segmentos: {len(segments)}")
        print(f"    • Tempo estimado: {tempo_total:.1f}s ({tempo_total/60:.1f} min)")


def exemplo_6_combinar_padroes():
    """Exemplo 6: Combinar múltiplos padrões."""
    print("\n" + "="*60)
    print("EXEMPLO 6: Combinar Múltiplos Padrões")
    print("="*60)
    
    from preplotter.patterns import LineSegment
    
    # Criar lista vazia
    pattern_completo = []
    
    # Adicionar círculo
    pattern_completo.extend(
        PatternGenerator.circle(num_points=32)
    )
    
    # Adicionar espiral
    pattern_completo.extend(
        PatternGenerator.spiral(num_points=64)
    )
    
    print(f"\n✓ Padrão combinado:")
    print(f"  • Círculo: 32 segmentos")
    print(f"  • Espiral: 64 segmentos")
    print(f"  • Total: {len(pattern_completo)} segmentos")
    print(f"\nPrimeiro segmento: {pattern_completo[0]}")
    print(f"Segmento de transição: {pattern_completo[31]}")
    print(f"Último segmento: {pattern_completo[-1]}")


if __name__ == "__main__":
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "Exemplos de Uso - PatternGenerator" + " "*11 + "║")
    print("╚" + "="*58 + "╝")
    
    exemplo_1_senoide_customizada()
    exemplo_2_multiplos_padroes()
    exemplo_3_padroes_artisticos()
    exemplo_4_entender_linearsegment()
    exemplo_5_calcular_duracao()
    exemplo_6_combinar_padroes()
    
    print("\n" + "="*60)
    print("PRÓXIMOS PASSOS")
    print("="*60)
    print("""
1. Conectar Arduino ao computador
2. Escolher um padrão da CLI:
   
   python3 -m preplotter.main --port /dev/ttyACM0 --run --pattern sine
   python3 -m preplotter.main --port /dev/ttyACM0 --run --pattern circle
   python3 -m preplotter.main --port /dev/ttyACM0 --run --pattern spiral

3. Ou criar padrão customizado:
   
   from preplotter.patterns import PatternGenerator
   segments = PatternGenerator.sine_wave(amplitude=600, num_points=128)
   # Executar com preplotter.plot_line() para cada segmento

Documentação: docs/preplotter.md
Testes: TESTE_PADROES_RESULTADO.md
""")
    print("="*60 + "\n")
