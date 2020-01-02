import pygame
import math

pygame.display.set_caption("Pitfall Atari")
icon = pygame.image.load("imagens/icon.png")
pygame.display.set_icon(icon)

#initialize the pygame
pygame.init()

#create the screen

screen = pygame.display.set_mode((800,600))
screen_im = pygame.image.load("imagens/background.png")


imagens = {
    'homem': pygame.image.load("imagens/boneco.png"),
    'wall': pygame.image.load("imagens/muro.png"),
    'tronco': pygame.image.load("imagens/tronco.png"),
    'croc': pygame.image.load("imagens/crocordilo.png"),
    'escada': pygame.image.load("imagens/escadas.png"),
    'homem_salto': pygame.image.load("imagens/homemsalto.png"),
    'lagoa_azul':pygame.image.load("imagens/lagoaazul.png"),
    'buraco':pygame.image.load("imagens/buraco.png"),
    'lagoa_negra':pygame.image.load("imagens/lagoanegra.png"),
    'liana': pygame.image.load("imagens/liana.png"),
}

levels = [
[
    {'obj':'wall','gx':12.5, 'gy':9.15},
    {'obj':'escada','gx':7,'gy':7.48},
    {'obj':'tronco','gx':12,'gy':7.2},
    {'obj':'homem', 'gx':1, 'gy':6},
],
[ 
    {'obj':'wall','gx':12.5, 'gy':9.15},
    {'obj':'escada','gx':7,'gy':7.48},
    {'obj':'buraco', 'gx': 3, 'gy':7.48},
    {'obj':'buraco', 'gx': 10.5, 'gy':7.48},
    {'obj':'tronco','gx':10,'gy':7.2},
    {'obj':'tronco','gx':11,'gy':7.2},
    {'obj':'homem', 'gx':1, 'gy':6},

],
[
    {'obj': 'wall', 'gx': 12.5, 'gy': 9.15},
    {'obj': 'lagoa_negra', 'gx':5, 'gy':7.5} ,
    {"obj": "liana", "gx":8, "gy":3, "theta": 0},
    {'obj': 'tronco', 'gx': 5, 'gy': 7.2},
    {"obj": 'homem', "gx":1,"gy":6},

],
[
    {'obj': 'wall', 'gx': 12.5, 'gy': 9.15},   
    {'obj':'lagoa_azul', 'gx':5, "gy":7.5},
    {'obj': 'croc', 'gx': 5.5, 'gy': 7.5},
    {'obj': 'croc', 'gx': 7.5, 'gy': 7.5},
    {'obj': 'croc', 'gx': 9.5, 'gy': 7.5},
    {'obj': 'tronco', 'gx': 5, 'gy': 7.2},
    {"obj": 'homem', "gx":1,"gy":6}, 
],
[
    {'obj': 'wall', 'gx': 12.5, 'gy': 9.15},
    {'obj': 'tronco', 'gx': 5, 'gy': 7.2},
    {'obj': 'croc', 'gx': 7, 'gy': 7},
    {"obj": 'homem', "gx":1,"gy":6}, 

],
[ 
    {'obj': 'wall', 'gx': 12.5, 'gy': 9.15},
    {'obj': 'tronco', 'gx': 5, 'gy': 8},
    {'obj': 'croc', 'gx': 7, 'gy': 7},
    {"obj": 'homem', "gx":1,"gy":6}, 
    
], 
[
    {'obj': 'wall', 'gx': 12.5, 'gy': 9.15},
    {'obj': 'tronco', 'gx': 5, 'gy': 8},
    {'obj': 'croc', 'gx': 7, 'gy': 7},
    {"obj": 'homem', "gx":1,"gy":6}, 
],
[
    {'obj': 'wall', 'gx': 12.5, 'gy': 9.15},
    {'obj': 'tronco', 'gx': 5, 'gy': 8},
    {'obj': 'croc', 'gx': 7, 'gy': 7},
    {"obj": 'homem', "gx":1,"gy":6}, 
],
[
    {'obj': 'wall', 'gx': 12.5, 'gy': 9.15},
    {'obj': 'tronco', 'gx': 5, 'gy': 8},
    {'obj': 'croc', 'gx': 7, 'gy': 7},
    {"obj": 'homem', "gx":1,"gy":6}, 
]
]

def overlaps(x1, y1, w1, h1, x2, y2, w2, h2):
    return not (x1+w1 < x2 or x1 > x2+w2 or y1+h1 < y2 or y1 > y2+h2)

def collision(o1, o2):
    img1 = imagens[o1['obj']]
    img2 = imagens[o2['obj']]
    return overlaps(o1['x'], o1['y'], img1.get_width(), img1.get_height(),
                    o2['x'], o2['y'], img2.get_width(), img2.get_height())

def mudar_nivel(nivel):
    global current_level, objects, homem
    current_level = levels[nivel%len(levels)]
    objects = [{'x': 800*o['gx']/16, 'y': 600*o['gy']/12,
                'w': imagens[o['obj']].get_width(),
                'h': imagens[o['obj']].get_height(), **o} for o in current_level]
    homem = [o for o in objects if o['obj'] == 'homem'][0]
   
LARGURA_LIANA = 300
THETA0_LIANA = 60*math.pi/180
LIANA_G = 4*10

colisao = False
current_level = None
objects = None
homem = None
jumptime = 0
jumpdir = 0
falling = False
buraco_falling = False
plataforma = 6
climbing = False
waiting = False

nivel = 0
mudar_nivel(nivel)

#game loop
running = True
clock = pygame.time.Clock()
while running:
    dt = clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    
    
    screen.blit(screen_im,(0,0))
    # EVENTOS
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        running = False
        
    if keys[pygame.K_RIGHT] and not (falling or jumptime > 0 and not collision):
        if waiting:
            jumpdir = 1
            jumptime = 10 
            climbing = False
            plataforma = 6
            waiting = False
        elif not climbing:
            homem['x'] += 0.2*dt
            
    if keys[pygame.K_LEFT] and not (falling or jumptime > 0 and not collision):
        if waiting:
            jumpdir = -1 
            jumptime = 10 
            climbing = False
            plataforma = 6
            waiting = False
        elif not climbing:
            homem['x'] -= 0.2*dt
  
    if keys[pygame.K_SPACE]:
        if 12*homem['y']/600 >= plataforma:
            jumptime = 10
            if keys[pygame.K_RIGHT]:
                jumpdir = 1
            elif keys[pygame.K_LEFT]:
                jumpdir = -1
            else:
                jumpdir = 0

    if jumptime != 0:
        jumptime -= 1
        if jumptime == 0:
            falling = True
        homem['y'] -= 0.1*dt
        homem['x'] += 0.2*dt*jumpdir

    if falling:
        homem['y'] += 0.1*dt
        if 12*homem['y']/600 >= plataforma:
            falling = False
            buraco_falling = False
        if not buraco_falling:
            homem['x'] += 0.2*dt*jumpdir

    if homem['x'] > 800:
        nivel += 1
        if nivel == len(levels):
            nivel = 0
        mudar_nivel(nivel)
        homem['x'] = -homem['w']
    elif homem['x'] + homem['w'] < 0:
        nivel -= 1
        homem['x'] = 700
        if nivel < 0:
            nivel = len(levels)-1
        mudar_nivel(nivel)
    # FISICA
    for obj in objects:
        if obj['obj'] == 'tronco' and nivel != 0:
            obj['x'] -= 1.5
        if obj['obj'] == 'liana':
            # https://pt.wikipedia.org/wiki/Equa%C3%A7%C3%A3o_do_p%C3%AAndulo
            t = pygame.time.get_ticks()/1000
            g = LIANA_G
            l = LARGURA_LIANA
            obj['theta'] = THETA0_LIANA*math.cos(math.sqrt(g/l)*t)

    # COLISÕES
    colidiu_escada = False
    for obj in objects:
        if obj['obj'] == 'wall':
            if collision(homem, obj) :
                if homem['x'] < obj['x']:
                    homem['x'] = obj['x'] - homem['w']
                else:
                    homem['x'] = obj['x'] - obj['w']
                    
        if obj['obj'] in ('escada', 'buraco'):
            if homem['x'] > obj['x'] and homem['x']+homem['w'] < obj['x']+obj['w'] and plataforma == 6 and not falling and jumptime == 0:
                plataforma = 10
                falling = True
                buraco_falling = True
                
        if obj['obj'] in ['lagoa_negra', 'lagoa_azul']:
            if collision(obj, homem):
                homem['y'] += 1
                    
        if obj['obj'] == 'escada':
            if homem['x'] > obj['x'] and homem['x'] + homem['w'] < obj['x'] + obj['w'] and plataforma == 10:
                colidiu_escada = True
                if keys[pygame.K_UP] and not(falling or jumptime > 0):
                    climbing = True
                    if homem['y'] > 600*6/12:
                        homem['y'] -= 0.2*dt
                        waiting = False
                    else:
                        waiting = True
                        #climbing = False
                        #plataforma = 6
        if obj['obj']== 'tronco':
            if collision(obj, homem):
                colisao = True
                #if colisao == True:
                 #   homem['y'] = 345
                
                
            else:colisao = False
            
            if obj['x']<0:
                obj['x'] = 800

    # DESENHO    
    for o in objects:
        if o['obj'] == 'liana':
            pos_i = (o['x'], o['y'])
            pos_f = (o['x']+math.cos(math.pi/2-o['theta'])*LARGURA_LIANA,
                     o['y']+math.sin(math.pi/2-o['theta'])*LARGURA_LIANA)
            pygame.draw.line(screen, pygame.Color('brown'), pos_i, pos_f, 3)          
        elif o['obj'] != 'homem':
            img = imagens[o['obj']]
            screen.blit(img, (o['x'], o['y']))
                
    if jumptime != 0 or (falling and not homem['y'] < 600*plataforma/12 - homem['h']) or colisao: 
        screen.blit(imagens['homem_salto'], (o['x'], o['y']))
    else:
        screen.blit(imagens['homem'], (o['x'], o['y']))
    
    
    pygame.display.update()
    
pygame.quit()
