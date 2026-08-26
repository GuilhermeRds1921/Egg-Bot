# EggBot

![Arduino](https://img.shields.io/badge/Arduino-Robotnik-149ddd?style=for-the-badge) ![C++](https://img.shields.io/badge/C%2B%2B-Robotnik-149ddd?style=for-the-badge) ![Robótica](https://img.shields.io/badge/Robótica-Robotnik-149ddd?style=for-the-badge) ![Controle de movimento](https://img.shields.io/badge/Controle%20de%20movimento-Robotnik-149ddd?style=for-the-badge) ![Divulgação científica](https://img.shields.io/badge/Divulgação%20científica-Robotnik-149ddd?style=for-the-badge)

> Robô demonstrativo para pintura e desenho em ovos, usado como projeto de robótica, controle de movimento e divulgação científica.

<p align="center">
  <img src="eggbot.jpg" alt="EggBot utilizado para pintar ou desenhar em um ovo" width="400" />
</p>

<p align="center">
  <a href="https://www.youtube.com/watch?v=F3q-DkTBnXs"><strong>Ver vídeo de demonstração no YouTube</strong></a>
</p>

## Sumário

- [Visão geral](#visão-geral)
- [Objetivos](#objetivos)
- [Principais recursos](#principais-recursos)
- [Arquitetura do projeto](#arquitetura-do-projeto)
- [Hardware](#hardware)
- [Software](#software)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Como usar](#como-usar)
- [Aplicação em divulgação científica](#aplicação-em-divulgação-científica)
- [Demonstração em vídeo](#demonstração-em-vídeo)
- [Continuidade do projeto](#continuidade-do-projeto)
- [Referências](#referências)
- [Licença](#licença)

## Visão geral

O **EggBot** é um projeto de robótica voltado à pintura ou desenho em ovos. A proposta consiste em controlar o movimento do objeto e da ferramenta de desenho para criar padrões, formas ou ilustrações sobre uma superfície curva.

No contexto da **Robotnik**, o EggBot funciona como um protótipo de demonstração muito visual para apresentar conceitos de programação, controle de movimento, motores, montagem mecânica, eletrônica embarcada e integração entre software e hardware.

Este repositório faz parte da organização **Robotnik - DAINF-PB**, projeto de extensão do DAINF da UTFPR - Campus Pato Branco voltado à robótica, prototipagem e divulgação científica.

## Objetivos

- Documentar o funcionamento geral do EggBot utilizado pela Robotnik.
- Registrar componentes, arquivos, dependências e referências do projeto.
- Facilitar manutenção, reaproveitamento e continuidade por novos integrantes.
- Servir como material de apoio para oficinas, eventos e demonstrações de robótica.
- Apresentar de forma prática a relação entre movimento controlado, desenho e programação.

## Principais recursos

- Pintura ou desenho em ovos.
- Demonstração visual de robótica aplicada.
- Controle de movimento em mais de um eixo.
- Integração entre estrutura mecânica, motores, eletrônica e software.
- Possibilidade de uso em escolas, feiras, oficinas e eventos acadêmicos.

## Arquitetura do projeto

A arquitetura pode ser entendida em quatro camadas principais:

| Camada | Função |
|---|---|
| Mecânica | Estrutura física, suporte do ovo, suporte da caneta/ferramenta e acoplamentos. |
| Eletrônica | Microcontrolador, drivers/módulos de acionamento, motores, alimentação e conexões. |
| Software embarcado | Código responsável por movimentação, sequência de desenho e acionamento dos atuadores. |
| Demonstração | Uso do protótipo em eventos, oficinas e ações de divulgação científica. |

## Hardware

> Ajustar esta lista conforme a versão real do protótipo disponível no repositório.

- Estrutura mecânica do EggBot
- Suporte para ovo ou objeto oval
- Suporte para caneta ou ferramenta de marcação
- Microcontrolador compatível com o código do projeto
- Motores e/ou servomotores conforme a montagem
- Módulos de acionamento, quando aplicável
- Fonte de alimentação adequada
- Jumpers, conectores, parafusos e suportes mecânicos

## Software

> Ajustar esta lista conforme o código real do projeto.

- C/C++ em ambiente Arduino ou compatível
- Bibliotecas de controle de motores/servos, quando aplicável
- Código de movimentação e sequência de desenho
- Arquivos auxiliares de configuração ou padrões de desenho, se existirem

## Estrutura do repositório

> Esta seção deve ser atualizada conforme a organização real dos arquivos.

Sugestão de estrutura:

```txt
docs/
  assets/
    capa-eggbot.jpg
src/
  codigo-principal/
README.md
LICENSE
```

## Como usar

> Esta seção deve ser ajustada conforme a versão atual do código e da montagem.

1. Clone o repositório:

```bash
git clone URL_DO_REPOSITORIO_EGGBOT
cd EggBot
```

2. Confira a documentação de montagem mecânica e elétrica.
3. Verifique a alimentação e as conexões dos motores/atuadores.
4. Instale as dependências do ambiente usado no projeto.
5. Carregue o código no microcontrolador.
6. Faça testes sem o ovo primeiro, observando o movimento dos eixos.
7. Ajuste posição da caneta, pressão e fixação do ovo.
8. Execute uma demonstração simples antes de usar padrões mais complexos.

## Aplicação em divulgação científica

O EggBot é um projeto interessante para divulgação científica porque transforma conceitos técnicos em uma demonstração visual e intuitiva. Durante uma apresentação, é possível explicar como comandos de software se transformam em movimento físico, como a mecânica limita ou viabiliza o desenho, e como a eletrônica faz a ponte entre programação e ação.

Esse tipo de protótipo ajuda estudantes e visitantes a perceberem que robótica não se limita a robôs humanoides ou veículos: ela também pode aparecer em máquinas de desenho, automação criativa, dispositivos de fabricação e ferramentas educacionais.

## Demonstração em vídeo

Vídeo de demonstração informado para o projeto:

[https://www.youtube.com/watch?v=F3q-DkTBnXs](https://www.youtube.com/watch?v=F3q-DkTBnXs)

## Continuidade do projeto

Sugestões para evolução:

- Adicionar fotos reais da montagem.
- Adicionar diagrama elétrico.
- Documentar pinos utilizados no microcontrolador.
- Registrar dependências e versão das bibliotecas.
- Criar exemplos de padrões simples de desenho.
- Incluir vídeos curtos de funcionamento.
- Documentar problemas comuns, como desalinhamento, pressão excessiva da caneta ou escorregamento do ovo.
- Criar uma versão em artigo técnico a partir do arquivo LaTeX deste pacote.

## Referências

- Vídeo de demonstração do projeto: [EggBot no YouTube](https://www.youtube.com/watch?v=F3q-DkTBnXs)
- Documentação interna do projeto Robotnik, quando disponível.
- Referências adicionais devem ser adicionadas conforme os materiais realmente utilizados no repositório.

## Organização

**Robotnik - DAINF-PB**  
Departamento Acadêmico de Informática - UTFPR, Campus Pato Branco.

Repositório: adicionar URL do repositório quando estiver criado ou confirmado.

## Licença

Consulte o arquivo `LICENSE` deste repositório. Quando o projeto usar materiais derivados ou adaptados de terceiros, mantenha os créditos e as licenças originais indicados nas referências.
