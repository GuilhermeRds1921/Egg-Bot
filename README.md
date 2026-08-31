# EggBot

![Arduino](https://img.shields.io/badge/Arduino-Uno-149ddd?style=for-the-badge) ![Python](https://img.shields.io/badge/Python-3.7%2B-3776AB?style=for-the-badge) ![Serial](https://img.shields.io/badge/Serial-9600%20baud-0A0A0A?style=for-the-badge) ![Robótica](https://img.shields.io/badge/Robótica-EggBot-ff5a5f?style=for-the-badge)

> Projeto EggBot para desenho e pintura em ovos, com controle via Arduino/firmware EggDuino e interface CLI em Ubuntu.

Este README reúne a documentação principal do projeto em um único lugar. Ele centraliza:
- visão geral do projeto
- hardware e arquitetura
- uso do pré-plotter
- padrões disponíveis
- testes reais
- convenção de commits

A pasta EggDuino fica isolada e não foi alterada.

---

## Sumário

- [Visão geral](#visão-geral)
- [Status atual](#status-atual)
- [Arquitetura](#arquitetura)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Pré-requisitos](#pré-requisitos)
- [Instalação rápida](#instalação-rápida)
- [Uso do pré-plotter](#uso-do-pré-plotter)
- [Padrões disponíveis](#padrões-disponíveis)
- [Testes validos no hardware](#testes-validos-no-hardware)
- [Comandos úteis](#comandos-úteis)
- [Convenção de commits](#convenção-de-commits)
- [Regras de contribuição](#regras-de-contribuição)

---

## Visão geral

O EggBot é um robô demonstrativo para desenhar ou pintar ovos. O projeto combina:
- estrutura mecânica
- motores passo a passo
- Arduino UNO
- firmware EggDuino
- comunicação serial
- lógica de planejamento de movimento em Python

A parte de software do projeto foi organizada em um pré-plotter sem interface gráfica, executado em Ubuntu via terminal.

---

## Status atual

✅ Hardware original validado
- Arduino UNO + CNC Shield
- 2 motores NEMA 17
- Firmware EggDuino instalado e funcionando

✅ Comunicação serial validada
- comando `SM,2000,0,800` funcionou corretamente
- protocolo EggDuino está operacional

✅ Pré-plotter Python em Ubuntu implementado
- CLI via terminal
- teste de movimento em modo real e simulação
- geração de padrões matemáticos

✅ Padrões geométricos testados no hardware real
- senoide
- espiral
- círculo

⏳ Etapas futuras
- importação de SVG
- controle de servo pen up/down
- integração com ESP32

---

## Arquitetura

A arquitetura do sistema pode ser entendida em quatro camadas:

- Mecânica: suporte do ovo, suporte da caneta, estrutura do robô
- Eletrônica: Arduino UNO, CNC Shield, drivers e motores
- Firmware: EggDuino, responsável pela execução dos movimentos
- Software: Python para planejamento, serial e CLI

### Fluxo de operação

```text
Ubuntu / Python
    ↓
pré-plotter CLI
    ↓
serial /dev/ttyACM0
    ↓
firmware EggDuino
    ↓
2 motores passo a passo
```

---

## Estrutura do repositório

```text
Egg-Bot/
├── README.md                       # documentação central do projeto
├── COMO_USAR_COM_GPT.md            # guia de uso com IA (opcional/complementar)
├── TESTE_ARDUINO_RESULTADO.md      # relatório de testes reais
├── TESTE_PADROES_RESULTADO.md      # relatório de padrões
├── RESUMO_PADROES.md               # resumo rápido
├── exemplos_padroes.py             # exemplos de padrões
├── eggbot.py                      # software principal do projeto
├── eggbot_conf.py                 # configuração do sistema
├── requirements.txt               # dependências Python
├── preplotter/                    # módulo de pré-plotter
│   ├── __init__.py
│   ├── planner.py
│   ├── eggduino.py
│   ├── patterns.py
│   ├── main.py
│   └── README.md
├── docs/
│   └── preplotter.md
└── EggDuino/                      # pasta de firmware/implementação externa
    └── (não alterada neste projeto de documentação/uso)
```

> A pasta EggDuino permanece como exceção e não é alvo de mudanças nesta padronização.

---

## Pré-requisitos

- Python 3.7+
- Ubuntu Linux
- Arduino UNO conectado por USB
- firmware EggDuino carregado no Arduino
- acesso à porta serial do Arduino

### Permissões do Ubuntu

```bash
sudo usermod -aG dialout $USER
```

Depois faça logout/login ou reinicie a sessão.

---

## Instalação rápida

```bash
cd ~/Documentos/Github/Egg-Bot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Se quiser instalar apenas a dependência principal:

```bash
pip install pyserial
```

---

## Uso do pré-plotter

### Modo seguro (sem movimento real)

```bash
python3 -m preplotter.main --port /dev/ttyACM0
```

### Teste de referência

```bash
python3 -m preplotter.main --port /dev/ttyACM0 --run --test reference
```

### Teste de retorno

```bash
python3 -m preplotter.main --port /dev/ttyACM0 --run --test return
```

### Teste do eixo do braço

```bash
python3 -m preplotter.main --port /dev/ttyACM0 --run --test arm
```

### Teste diagonal

```bash
python3 -m preplotter.main --port /dev/ttyACM0 --run --test diagonal
```

### Todos os testes

```bash
python3 -m preplotter.main --port /dev/ttyACM0 --run --test all
```

### Movimento customizado

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

### Ajuda da CLI

```bash
python3 -m preplotter.main --help
```

---

## Padrões disponíveis

O sistema possui geradores de padrões para desenho por segmentos.

### Lista de padrões

| Padrão | Comando | Descrição |
|---|---|---|
| Senoide | `--pattern sine` | onda senoidal do topo à base do ovo |
| Multi-senoide | `--pattern multi-sine` | dois períodos de senoide |
| Espiral | `--pattern spiral` | espiral expandindo |
| Quadrado | `--pattern square` | teste geométrico |
| Círculo | `--pattern circle` | calibração e simetria |
| Estrela | `--pattern star` | desenho estelar |

### Exemplos

#### Senoide

```bash
python3 -m preplotter.main --port /dev/ttyACM0 --run --pattern sine
```

#### Espiral

```bash
python3 -m preplotter.main --port /dev/ttyACM0 --run --pattern spiral
```

#### Círculo

```bash
python3 -m preplotter.main --port /dev/ttyACM0 --run --pattern circle
```

#### Exemplo de uso em Python

```python
from preplotter.patterns import PatternGenerator

segments = PatternGenerator.sine_wave(
    rotation_start=0,
    rotation_end=3200,
    amplitude=500,
    speed=250,
    num_points=64,
    vertical_offset=200,
)

print(f"Gerados {len(segments)} segmentos")
```

---

## Testes validos no hardware

Os testes abaixo foram executados no Arduino real com firmware EggDuino e todos passaram.

### Teste 1: referência

```bash
python3 -m preplotter.main --port /dev/ttyACM0 --run --test reference
```

Resultado esperado: movimento de `SM,2000,0,800`

### Teste 2: retorno

```bash
python3 -m preplotter.main --port /dev/ttyACM0 --run --test return
```

Resultado esperado: movimento de `SM,2000,0,-800`

### Teste 3: braço

```bash
python3 -m preplotter.main --port /dev/ttyACM0 --run --test arm
```

### Teste 4: diagonal

```bash
python3 -m preplotter.main --port /dev/ttyACM0 --run --test diagonal
```

### Teste 5: padrão senoide

```bash
python3 -m preplotter.main --port /dev/ttyACM0 --run --pattern sine
```

Resultado: padrão de linha senoidal do topo à base do ovo executado com sucesso.

---

## Comandos úteis

### Verificar portas USB

```bash
ls /dev/tty*
```

### Ver a ajuda

```bash
python3 -m preplotter.main --help
```

### Rodar a suíte de exemplos

```bash
python3 exemplos_padroes.py
```

### Ver a versão do firmware

```bash
python3 -m preplotter.main --port /dev/ttyACM0 --run --test reference
```

---

## Convenção de commits

O projeto usa uma convenção simples e padronizada, inspirada em Conventional Commits, para manter um histórico limpo e legível.

### Estrutura

```text
<tipo>(<escopo>): <descrição curta>
```

### Tipos permitidos

- `feat`: nova funcionalidade
- `fix`: correção de bug
- `docs`: documentação
- `refactor`: refatoração sem mudança funcional
- `test`: testes
- `chore`: manutenção e configurações
- `perf`: melhoria de performance

### Exemplos

```bash
git commit -m "feat(preplotter): add sine wave pattern support"
git commit -m "fix(serial): handle invalid EggDuino response"
git commit -m "docs(readme): centralize project instructions in root README"
git commit -m "test(patterns): validate spiral and circle generation"
```

### Regras

- usar verbo no imperativo: `add`, `fix`, `update`, `remove`
- manter a mensagem curta e clara
- escopo opcional, mas recomendado
- separar corpo e descrição quando necessário

### Template local

O repositório está configurado com um template de commit para facilitar o padrão.

```bash
git config --local commit.template .gitmessage
```

O template contém:

```text
<type>(<scope>): <subject>

<body>
```

---

## Regras de contribuição

- manter o README raiz como fonte principal de uso
- documentar mudanças de comportamento e comandos
- não alterar a pasta `EggDuino` sem necessidade explícita
- testar no hardware antes de fechar mudanças relevantes
- usar commits compatíveis com a convenção acima

---

## Observações finais

Este projeto foi organizado para funcionar de forma simples no Ubuntu, com foco em:
- estabilidade serial
- validação real do hardware
- facilidade de uso por linha de comando
- expansão de padrões de desenho

O README raiz agora funciona como ponto central de referência do projeto.
