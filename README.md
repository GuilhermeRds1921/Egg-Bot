# EggBot IoT Plotter

![Arduino](https://img.shields.io/badge/Arduino-Uno-149ddd?style=for-the-badge)
![ESP32](https://img.shields.io/badge/ESP32-IoT-E7352C?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-Plotter-3776AB?style=for-the-badge)
![Web](https://img.shields.io/badge/Web-Interface-61DAFB?style=for-the-badge)

[![EggBot](https://github.com/GuilhermeRds1921/Egg-Bot/blob/main/imagem01.jpeg?raw=true)](https://github.com/GuilhermeRds1921/Egg-Bot/blob/main/imagem01.jpeg)

## Sobre o projeto

Este projeto tem como objetivo transformar um **EggBot** em um sistema IoT completo para desenho automático em ovos.

O EggBot e o firmware EggDuino já fornecem a base mecânica e o controle dos motores. O foco deste repositório é desenvolver a camada de software necessária para permitir que uma pessoa envie uma imagem por uma interface web e o sistema converta essa imagem em movimentos que possam ser executados pelo robô.

A proposta final é criar um fluxo semelhante ao de um plotter ou impressora 3D:

```text
Imagem
  ↓
Interface Web
  ↓
Processamento / Fatiamento
  ↓
Geração de trajetória
  ↓
G-code / comandos do EggDuino
  ↓
ESP32
  ↓
Arduino UNO
  ↓
EggDuino
  ↓
Motores
  ↓
Desenho no ovo
```

## Objetivo

Desenvolver um **plotter para superfícies ovais** capaz de transformar imagens em trajetórias compatíveis com o EggBot.

O sistema deverá permitir:

* enviar imagens pela interface web;
* processar e simplificar a imagem;
* converter a imagem em linhas e trajetórias;
* adaptar as coordenadas para a superfície do ovo;
* gerar comandos compatíveis com o firmware EggDuino;
* visualizar ou validar o resultado antes da execução;
* iniciar o desenho remotamente;
* acompanhar o estado da impressão.

## Arquitetura

O projeto será dividido em três componentes principais.

### ESP32

Responsável pela camada IoT do sistema.

Funções previstas:

* criar uma rede Wi-Fi local;
* hospedar a interface web;
* receber imagens e configurações;
* controlar o processo de plotagem;
* realizar a comunicação com o Arduino UNO.

### Arduino UNO + EggDuino

Responsável pelo controle físico do EggBot.

O Arduino recebe os comandos de movimento e controla:

* motor de rotação do ovo;
* motor responsável pelo movimento da caneta;
* futuramente, servo para levantar e abaixar a caneta.

### Plotter

Responsável por transformar a imagem enviada pelo usuário em movimentos executáveis pelo EggBot.

O processamento deverá seguir aproximadamente:

```text
Imagem
  ↓
Conversão para escala de cinza
  ↓
Detecção / vetorização de linhas
  ↓
Simplificação da geometria
  ↓
Geração de coordenadas
  ↓
Planejamento da trajetória
  ↓
Conversão para comandos
```

## Fluxo esperado

O usuário deverá conseguir acessar o EggBot pelo celular ou computador:

```text
Celular / Notebook
       ↓ Wi-Fi
      ESP32
       ↓
 Interface Web
       ↓
 Upload da imagem
       ↓
 Processamento
       ↓
 Pré-visualização
       ↓
 Gerar trajetória
       ↓
 Iniciar desenho
       ↓
 Arduino + EggDuino
       ↓
      EggBot
```

A ideia é que o sistema funcione de forma independente, sem necessidade de manter um computador conectado ao robô.

## Status

Atualmente:

* ✅ estrutura mecânica do EggBot;
* ✅ Arduino UNO;
* ✅ EggDuino funcionando;
* ✅ motores controlados pelo firmware;
* ✅ comunicação serial validada;
* ✅ pré-plotter inicial em Python;
* ✅ geração de trajetórias geométricas simples;
* ⏳ processamento de imagens;
* ⏳ vetorização;
* ⏳ geração de G-code/comandos;
* ⏳ servidor no ESP32;
* ⏳ interface web;
* ⏳ comunicação ESP32 ↔ Arduino;
* ⏳ controle completo da plotagem.

## Tecnologias

* ESP32
* Arduino UNO
* EggDuino
* Python
* C / C++
* HTML / CSS / JavaScript
* Comunicação serial
* Wi-Fi
* IoT
* Processamento de imagens
* G-code
* Planejamento de trajetória

## Referências

* [EggDuino — plex3r](https://github.com/plex3r/EggDuino)
* [EggBot — Evil Mad Scientist](https://github.com/evil-mad/EggBot)
* [Referência de montagem — YouTube](https://www.youtube.com/watch?v=F3q-DkTBnXs)
* [Modelo mecânico — Thingiverse](https://www.thingiverse.com/thing:3431363)

## Créditos

O EggBot e o firmware EggDuino são projetos utilizados como base para o desenvolvimento.

O foco deste repositório é a implementação da camada de **plotagem, processamento de imagens, geração de trajetórias, comunicação IoT e interface web** necessária para transformar o hardware existente em um sistema autônomo de desenho em ovos.
