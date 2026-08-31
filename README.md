# EggBot

![Arduino](https://img.shields.io/badge/Arduino-Uno-149ddd?style=for-the-badge) ![Python](https://img.shields.io/badge/Python-3.7%2B-3776AB?style=for-the-badge) ![Serial](https://img.shields.io/badge/Serial-9600%20baud-0A0A0A?style=for-the-badge) ![Robótica](https://img.shields.io/badge/Robótica-EggBot-ff5a5f?style=for-the-badge)

> Projeto EggBot para desenho e pintura em ovos com Arduino, firmware EggDuino e pré-plotter em Python para Ubuntu.

Este repositório reúne o software principal e a documentação de uso do projeto. A pasta EggDuino foi mantida como exceção e não foi alterada neste fluxo de documentação.

---

## Visão geral

O EggBot é um robô demonstrativo para desenhar e pintar ovos. O sistema combina:

- estrutura mecânica
- dois motores de passo
- Arduino UNO
- firmware EggDuino
- comunicação serial via USB
- planejamento de movimento em Python
- execução por linha de comando sem interface gráfica

A parte de software foi organizada como um pré-plotter CLI para controlar o robô de forma segura e reproduzível.

---

## Status atual

✅ Hardware validado
- Arduino UNO + CNC Shield
- 2 motores NEMA 17
- firmware EggDuino funcionando

✅ Comunicação serial validada
- comando `SM,2000,0,800` executado corretamente
- protocolo EggDuino operacional

✅ Pré-plotter funcional em Ubuntu
- CLI em terminal
- modo simulação e modo execução real
- cálculo automático de movimento
- geração de padrões geométricos

✅ Padrões testados no hardware real
- senoide
- espiral
- círculo

⏳ Próximos passos
- importação de SVG
- pen up/down via servo
- integração com ESP32

---

## Estrutura do repositório

```text
Egg-Bot/
├── README.md               # documentação principal do projeto
├── eggbot.py               # software principal
├── eggbot_conf.py          # configurações do projeto
├── requirements.txt        # dependências Python
├── preplotter/             # módulo do pré-plotter
│   ├── __init__.py
│   ├── planner.py
│   ├── eggduino.py
│   ├── patterns.py
│   ├── main.py
│   └── README.md
├── .gitmessage            # template de commits
├── EggDuino/               # firmware/implementação externa (exceção)
└── outros arquivos locais de apoio
```

> A pasta EggDuino permanece fora do escopo desta padronização.

---

## Pré-requisitos

- Python 3.7+
- Ubuntu Linux
- Arduino UNO conectado por USB
- firmware EggDuino carregado no Arduino
- permissão de acesso à porta serial

### Permissões do Ubuntu

```bash
sudo usermod -aG dialout $USER
```

Depois reinicie a sessão ou faça logout/login.

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

## Como usar o pré-plotter

### Modo seguro

```bash
python3 -m preplotter.main --port /dev/ttyACM0
```

Sem `--run`, o sistema apenas simula e não move os motores.

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

O pré-plotter também gera padrões matemáticos para desenho sequencial.

| Padrão | Comando | Descrição |
|---|---|---|
| Senoide | `--pattern sine` | onda senoidal do topo à base do ovo |
| Multi-senoide | `--pattern multi-sine` | dois períodos de senoide |
| Espiral | `--pattern spiral` | espiral expandindo |
| Quadrado | `--pattern square` | desenho geométrico simples |
| Círculo | `--pattern circle` | calibração e simetria |
| Estrela | `--pattern star` | padrão estelar |

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

---

## Testes no hardware

Os testes abaixo foram executados no Arduino real com o firmware EggDuino e passaram com sucesso.

### Teste 1: referência

```bash
python3 -m preplotter.main --port /dev/ttyACM0 --run --test reference
```

Resultado esperado: `SM,2000,0,800`

### Teste 2: retorno

```bash
python3 -m preplotter.main --port /dev/ttyACM0 --run --test return
```

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

Resultado: linha senoidal do topo à base do ovo executada com sucesso.

---

## Comandos úteis

### Ver portas USB

```bash
ls /dev/tty*
```

### Ver ajuda

```bash
python3 -m preplotter.main --help
```

### Rodar exemplos

```bash
python3 exemplos_padroes.py
```

---

## Convenção de commits

O projeto usa uma convenção simples e padronizada, inspirada em Conventional Commits.

### Estrutura

```text
<tipo>(<escopo>): <descrição curta>
```

### Tipos recomendados

- `feat`: nova funcionalidade
- `fix`: correção de bug
- `docs`: documentação
- `refactor`: refatoração
- `test`: testes
- `chore`: manutenção
- `perf`: performance

### Exemplos

```bash
git commit -m "feat(preplotter): add sine wave pattern support"
git commit -m "fix(serial): handle invalid EggDuino response"
git commit -m "docs(readme): centralize project instructions"
git commit -m "test(patterns): validate spiral and circle generation"
```

### Regras

- usar verbo no imperativo
- manter a mensagem curta e clara
- usar escopo quando fizer sentido
- manter histórico consistente

---

## Regras de contribuição

- manter o README principal como ponto central de referência
- documentar mudanças de comportamento e comando
- não alterar a pasta EggDuino sem necessidade explícita
- validar no hardware em mudanças relevantes
- seguir a convenção de commits acima

---

## Observações finais

Este projeto foi organizado para funcionar de forma simples no Ubuntu, com foco em:

- estabilidade serial
- validação real do hardware
- facilidade de uso em linha de comando
- expansão de padrões de desenho

O README principal agora centraliza as instruções do projeto e deixa a base de uso clara para desenvolvimento e uso futuro.
