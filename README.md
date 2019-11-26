# Projeto  pitfall-atari
### FPRO/MIEIC, 2019/20
### Luísa Marques (up201907565@fe.up.pt)
### 1MIEIC04

#### Objetivo

Criar um clone do Pitfall Atari 2600 em Pygame

#### Descrição

*---Pitfall é um dos maiores clássicos do Atari 2600  e um dos jogos mais populares dos anos 80, que moldou as bases dos jogos de avnetura.---*

#### UI

![UI](https://github.com/fpro-feup/public/blob/master/assigns/ui.png)

### Pacotes

- Pygame

#### Tarefas

1. **NIVEIS**
   1. lista de tuplos (objeto, pos_x)
   1. desenhamos os nossos objetos (desenhar os objetos)
   1. desenhamos o fundo: arvores, plataforma, abismo
1. **JOGADOR**
   1. desenhar o jogador: pos_x, pos_y
   1. controlo esquerda-direita
   1. tecla space: salto_tempo = 50
   1. quando nao salta gravidade: pos_y += vel_y
   1. parar gravidade quando existe plataforma
1. **INTERACÇÃO**
   1. bounding-box entre tronco-jogador, jogador-objeto
   1. escada
1. **LIANA**
   1. movimento trignometrico dentro de certos limites

### 11/2019
