# Projeto  pitfall-atari
### FPRO/MIEIC, 2019/20
### Luísa Marques (up201907565@fe.up.pt)
### 1MIEIC04

#### Objetivo

Criar um clone do Pitfall Atari 2600 em Pygame

#### Descrição

*---Pitfall é um dos maiores clássicos do Atari 2600  e um dos jogos mais populares dos anos 80, que moldou as bases dos jogos de avnetura.---*

#### UI

![UI](pitfall.jpg)

### Pacotes

- Pygame

#### Tarefas

1. **NIVEIS**
   1. os níveis são naturalmente uma lista, sendo que cada nível é por si também uma lista dum dicionário com os objetos.
      * sugestão: cada nível é uma grelha 16x12, que é convertida para objetos em pixels.
```
levels = [
   # coordinates are defined as a 16x12 grid
    [{'obj': 'hole', 'gx': 5, 'gy': 10}, {'obj': 'snake', 'gx': 2, 'gy': 5}],
    ...,
    ...,
]
current_level = levels[0]
# convert grid coordinates to screen coordinates
objects = [{'x': 800*o['gx']/16, 'y': 600*o['gy']/12, **o} for o in current_level]
```
1. **NIVEIS (cont.)**
   1. desenhamos os nossos objetos (desenhar os objetos)
      * sugestão: tamanho da janela=800x600, tamanho de cada imagem do objeto será múltiplo de 50 (e.g. cobra=50x50, buraco=350x50, jogador=25x100).
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
