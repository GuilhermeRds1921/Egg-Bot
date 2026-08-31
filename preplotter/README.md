# Pré-Plotter EggBot

Módulo Python para controlar o EggBot via Arduino UNO (firmware EggDuino) pela linha de comando.

## Rápido Começo

### Instalação

```bash
pip install -r ../requirements.txt
```

### Uso Básico

Modo simulação (seguro, sem movimento):
```bash
python3 -m preplotter.main --port /dev/ttyACM0
```

Teste de movimento validado:
```bash
python3 -m preplotter.main --port /dev/ttyACM0 --run --test reference
```

## Módulos

- **planner.py** — Cálculo automático de movimento (distância euclidiana, duração)
- **eggduino.py** — Comunicação serial com Arduino (EggDuino)
- **main.py** — Interface CLI e coordenação dos testes

## Testes Integrados

```bash
# Teste 1: Referência (SM,2000,0,800)
python3 -m preplotter.main --port /dev/ttyACM0 --run --test reference

# Teste 2: Retorno
python3 -m preplotter.main --port /dev/ttyACM0 --run --test return

# Teste 3: Eixo do braço
python3 -m preplotter.main --port /dev/ttyACM0 --run --test arm

# Teste 4: Diagonal (ambos eixos)
python3 -m preplotter.main --port /dev/ttyACM0 --run --test diagonal

# Todos os testes
python3 -m preplotter.main --port /dev/ttyACM0 --run --test all
```

## Movimento Customizado

```bash
python3 -m preplotter.main \
  --port /dev/ttyACM0 \
  --run \
  --start-rotation 0 \
  --start-arm 0 \
  --end-rotation 500 \
  --end-arm 300 \
  --speed 200
```

## Documentação Completa

Veja [../docs/preplotter.md](../docs/preplotter.md)
