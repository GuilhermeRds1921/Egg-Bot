# EggBot

![Arduino](https://img.shields.io/badge/Arduino-Uno-149ddd?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.7%2B-3776AB?style=for-the-badge)
![Serial](https://img.shields.io/badge/Serial-9600%20baud-0A0A0A?style=for-the-badge)

[![EggBot](https://github.com/GuilhermeRds1921/Egg-Bot/blob/main/capa.jpeg?raw=true)](https://github.com/GuilhermeRds1921/Egg-Bot/blob/main/capa.jpeg)

## Sobre o projeto

EggBot desenvolvido para desenho em ovos utilizando **Arduino UNO**, motores de passo e firmware **EggDuino**.

O projeto inclui um pré-plotter desenvolvido em **Python**, responsável por planejar movimentos e enviar comandos ao Arduino diretamente pela porta serial.

O sistema funciona sem interface gráfica e pode ser controlado completamente pelo terminal.

### Principais tecnologias

* Arduino UNO
* CNC Shield
* Motores NEMA 17
* EggDuino
* Python
* PySerial
* Comunicação serial
* Planejamento de movimento

---

## Funcionamento

```text
Python
   ↓
Pré-plotter
   ↓
Comunicação Serial
   ↓
Arduino UNO
   ↓
EggDuino
   ↓
Motores de Passo
   ↓
EggBot
```

O pré-plotter converte coordenadas e padrões geométricos em comandos compatíveis com o protocolo EggDuino.

---

## Estrutura

```text
Egg-Bot/
├── eggbot.py
├── eggbot_conf.py
├── requirements.txt
├── preplotter/
│   ├── planner.py
│   ├── eggduino.py
│   ├── patterns.py
│   └── main.py
├── EggDuino/
└── README.md
```

---

## Instalação

```bash
git clone https://github.com/GuilhermeRds1921/Egg-Bot.git
cd Egg-Bot

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

No Linux, pode ser necessário permitir acesso à porta serial:

```bash
sudo usermod -aG dialout $USER
```

---

## Execução

### Simulação

```bash
python3 -m preplotter.main --port /dev/ttyACM0
```

### Teste no hardware

```bash
python3 -m preplotter.main \
  --port /dev/ttyACM0 \
  --run \
  --test diagonal
```

### Executar padrão

```bash
python3 -m preplotter.main \
  --port /dev/ttyACM0 \
  --run \
  --pattern sine
```

Padrões disponíveis incluem:

* senoide
* espiral
* círculo
* quadrado
* estrela

---

## Status

* ✅ Arduino e motores validados
* ✅ Comunicação serial funcionando
* ✅ Controle por linha de comando
* ✅ Geração de padrões geométricos
* ✅ Testes realizados no hardware
* ⏳ Importação de SVG
* ⏳ Controle da caneta por servo
* ⏳ Integração futura com ESP32

---

## Referências

* [EggDuino — plex3r](https://github.com/plex3r/EggDuino)
* [EggBot — Evil Mad Scientist](https://github.com/evil-mad/EggBot)
* [Referência de montagem — YouTube](https://www.youtube.com/watch?v=F3q-DkTBnXs)
* [Modelo mecânico — Thingiverse](https://www.thingiverse.com/thing:3431363)

---

## Créditos

O firmware EggDuino e os projetos utilizados como referência pertencem aos seus respectivos autores.

Este repositório documenta as adaptações, integração do hardware e desenvolvimento do pré-plotter em Python realizados para este projeto.
