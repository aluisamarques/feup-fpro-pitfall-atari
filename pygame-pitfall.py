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
    'homem':pygame.image.load('imagens/6d.png'),
    'wall': pygame.image.load("imagens/muro.png"),
    'tronco': pygame.image.load("imagens/tronco.png"),
    'tronco_1': pygame.image.load("imagens/tronco.png"),
    'tronco_2': pygame.image.load("imagens/tronco.png"),
    'croc': pygame.image.load("imagens/crocodilo.png"),
    'escada': pygame.image.load("imagens/escadas.png"),
    'homem_salto': pygame.image.load("imagens/player_jump.png"),
    'lagoa_azul':pygame.image.load("imagens/lagoaazul.png"),
    'buraco':pygame.image.load("imagens/buraco.png"),
    'lagoa_negra':pygame.image.load("imagens/lagoanegra.png"),
    'gato': pygame.image.load('imagens/gato.png'),
    'homem_salto_e': pygame.image.load('imagens/3.png'),
    'liana': pygame.image.load('imagens/liana.png'),
}

imagens_direita = [
    pygame.image.load('imagens/6d.png'),
    pygame.image.load('imagens/1d.png'),
    pygame.image.load('imagens/2d.png'),
    pygame.image.load('imagens/4d.png'),
    pygame.image.load('imagens/5d.png'),]

imagens_esquerda = [
    pygame.image.load('imagens/1.png'),
    pygame.image.load('imagens/2.png'),
    pygame.image.load('imagens/4.png'),
    pygame.image.load('imagens/5.png'),
    pygame.image.load('imagens/6.png'),]

levels = [
[
    {'obj':'wall','gx':12.5, 'gy':9.15},
    {'obj':'escada','gx':7,'gy':7.48},
    {'obj':'tronco','gx':12,'gy':7.4},
    {'obj':'homem', 'gx':1, 'gy':6},
],
[ 
    {'obj':'wall','gx':12.5, 'gy':9.15},
    {'obj':'escada','gx':7,'gy':7.48},
    {'obj':'buraco', 'gx': 3, 'gy':7.48},
    {'obj':'buraco', 'gx': 10.5, 'gy':7.48},
    {'obj':'tronco','gx':10,'gy':7.2},
    {'obj':'tronco_1','gx':14,'gy':7.2},
    {'obj':'homem', 'gx':1, 'gy':6},
],
[
    {'obj': 'lagoa_negra', 'gx':5, 'gy':7.5} ,
    {"obj": "liana", "gx":8, "gy":2, "theta": 0},
    {'obj': 'tronco', 'gx': 5, 'gy': 7.2},
    {'obj':'gato', 'gx':1, 'gy':10.65},
    {"obj": 'homem', "gx":1,"gy":6},
],
[
    {'obj':'lagoa_azul', 'gx':5, "gy":7.5},
    {'obj': 'croc', 'gx': 6, 'gy': 7.5},
    {'obj': 'croc', 'gx': 8.2, 'gy': 7.5},
    {'obj': 'croc', 'gx': 10, 'gy': 7.5},
    {'obj':'gato', 'gx':1, 'gy':10.65},
    {"obj": 'homem', "gx":1,"gy":6}, 
],
[
    {'obj': 'wall', 'gx': 2, 'gy': 9.15},
    {'obj':'buraco', 'gx': 12, 'gy':7.48},
    {'obj':'buraco', 'gx': 5, 'gy':7.48},
    {'obj':'escada','gx':9,'gy':7.48},
    {'obj': 'tronco', 'gx': 5, 'gy': 7.5},
    {'obj': 'tronco_1', 'gx': 7, 'gy': 7.5},
    {'obj': 'tronco_2', 'gx': 9, 'gy': 7.5},
    {"obj": 'homem', "gx":1,"gy":6}, 
],
]

def overlaps(x1, y1, w1, h1, x2, y2, w2, h2):
    return not (x1+w1 < x2 or x1 > x2+w2 or y1+h1 < y2 or y1 > y2+h2)

def collision(o1, o2):
    img1 = imagens[o1['obj']]
    img2 = imagens[o2['obj']]
    return overlaps(o1['x'], o1['y'], img1.get_width(), img1.get_height(),
                    o2['x'], o2['y'], img2.get_width(), img2.get_height())

def mudar_nivel(nivel):
    global current_level, objects, homem, liana, gato
    current_level = levels[nivel%len(levels)]
    objects = [{'x': 800*o['gx']/16, 'y': 600*o['gy']/12,
                'w': imagens[o['obj']].get_width(),
                'h': imagens[o['obj']].get_height(), **o} for o in current_level]
    homem = [o for o in objects if o['obj'] == 'homem'][0]
    lianas = [o for o in objects if o['obj'] == 'liana']
    liana = lianas[0] if lianas else None
   
LARGURA_LIANA = 250
THETA0_LIANA = 60*math.pi/180
LIANA_G = 4*10
ANIM_TIME = 50
SCORE = 0

colisao = False
current_level = None
objects = None
homem = None
liana = None
jumptime = 0
jumpdir = 0
plataforma = 6
gato = 1
dir = 2
buraco_falling = False
status = None
old_theta = 0
score = 500
vidas = 3
font = pygame.font.Font(None,30)

anim_time = pygame.time.get_ticks()

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
    
    #EVENTOS
    texto = font.render(str(score),100,(255,255,255))
    texto_1 = font.render(str(vidas),100,(255,255,255))
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        running = False
    
    if keys[pygame.K_RIGHT] and not (status == 'falling' or status == 'lagoa' or jumptime > 0 and not collision):
        dir = 0
        if status == 'waiting':
            jumpdir = 1
            jumptime = 10
            plataforma = 6
            status = None
        elif status != 'climbing':
            homem['x'] += 0.2*dt
        if pygame.time.get_ticks()- anim_time > ANIM_TIME and status == None:
            imagens_direita = imagens_direita[1:] + [imagens_direita[0]]
            anim_time = pygame.time.get_ticks()
            imagens['homem'] = imagens_direita[0]
  
    if keys[pygame.K_LEFT] and not (status == 'falling' or status == 'lagoa' or jumptime > 0 and not collision):
        dir = 1
        if status == 'waiting':
            jumpdir = -1 
            jumptime = 10
            plataforma = 6
            status = None
        elif status != 'climbing':
            homem['x'] -= 0.2*dt
        if  pygame.time.get_ticks() - anim_time > ANIM_TIME and status == None:
            imagens_esquerda = imagens_esquerda[1:] + [imagens_esquerda[0]]
            anim_time = pygame.time.get_ticks()
            imagens['homem'] = imagens_esquerda[0]
  
    if keys[pygame.K_SPACE] and not status == 'lagoa':
        if 12*homem['y']/600 >= plataforma and status is None:
            jumptime = 10
            if keys[pygame.K_RIGHT]:
                jumpdir = 1
            elif keys[pygame.K_LEFT]:
                jumpdir = -1
            else:
                jumpdir = 0
    
    if keys[pygame.K_DOWN] :
        if status == 'liana':
            jumpdir = -1 if liana['theta'] - old_theta < 0 else 1
            status = 'falling'

    if jumptime != 0:
        jumptime -= 1
        if jumptime == 0:
            status = 'falling'
        homem['y'] -= 0.1*dt
        homem['x'] += 0.1*dt*jumpdir

    if status == 'falling':
        homem['y'] += 0.1*dt
        if 12*homem['y']/600 >= plataforma:
            status = None
            buraco_falling = False
        if not buraco_falling:
            homem['x'] += 0.2*dt*jumpdir

    if homem['x'] + homem['w'] >= 800:
        if plataforma == 10:
            homem['x'] = 740
    if homem['x'] > 800:
            nivel += 1
            if nivel == len(levels):
                nivel = 0
            mudar_nivel(nivel)
            homem['x'] = -homem['w']
    elif homem['x'] + homem['w'] < 0:
        if plataforma == 10:
            homem['x'] = 0
        else:
            nivel -= 1
            homem['x'] = 700
            if nivel < 0:
                nivel = len(levels)-1
            mudar_nivel(nivel)
            
    if gato == 0:
        imagens['gato'] = pygame.image.load('imagens/gato_2.png')
    if gato == 1:
        imagens['gato'] = pygame.image.load('imagens/gato.png')
        
    if score < 0:
        score = SCORE
    
    if vidas == 0:
        nivel = 0
        mudar_nivel(nivel)
        vidas = 3
        
    if status != None:
        if dir == 0:
            imagens['homem'] = pygame.image.load('imagens/6d.png')
        if dir == 1:
            imagens['homem'] = pygame.image.load('imagens/6.png')
    
    # FISICA
    for obj in objects:
        if obj['obj'] in ['tronco','tronco_1', 'tronco_2'] and nivel != 0:
            obj['x'] -= 2.5
            
        if obj['obj'] == 'gato':
            if gato == 1:
                obj['x'] += 1.5 
            if gato == 0:
                obj['x'] -= 1.5
                
        if obj['obj'] == 'liana':
            # https://pt.wikipedia.org/wiki/Equa%C3%A7%C3%A3o_do_p%C3%AAndulo
            t = pygame.time.get_ticks()/1000
            g = LIANA_G
            l = LARGURA_LIANA
            old_theta = obj['theta']
            obj['theta'] = THETA0_LIANA*math.cos(math.sqrt(g/l)*t)

    # COLISÕES
    crocodilo = False    
    for obj in objects:
        if obj['obj'] == 'croc':
            if collision(obj, homem):
                crocodilo = True

    for obj in objects:
        if obj['obj'] == 'wall':
            if collision(homem, obj) :
                if homem['x'] < obj['x']:
                    homem['x'] = obj['x'] - homem['w'] - 40
                else:
                    homem['x'] = obj['x'] + obj['w'] + 40
                    
            for obj1 in objects:
                if obj1['obj'] == 'gato':
                    if collision(obj1, obj):
                        gato = 0
                    
        if obj['obj'] in ('escada', 'buraco'):
            if homem['x'] > obj['x'] and homem['x']+homem['w'] < obj['x']+obj['w'] and plataforma == 6 and status != 'falling' and jumptime == 0:
                plataforma = 10
                status = 'falling'
                buraco_falling = True
                score -= 10
                if score < 0:
                    score = SCORE
                
        if obj['obj'] in ['lagoa_negra', 'lagoa_azul']:
            if homem['x'] >= obj['x'] and homem['x']+homem['w'] <= obj['x']+obj['w'] and \
                    homem['y']+homem['h'] > obj['y'] and \
                    status != 'liana' and status != 'falling' and not crocodilo:
                status = 'lagoa'
                homem['y'] += 0.1*dt
                if status == 'lagoa' and homem['y'] > 405:
                    score -= round(0.2*dt)
                    vidas -= 1
                    if score < 0 or vidas <0:
                        score = SCORE
                        vidas = SCORE
                    homem['x'] = 50
                    homem['y'] = 50
                    status = None
                    while homem['y'] < 300:
                        homem['y'] += 0.1
                     
        if obj['obj'] == 'escada':
            if homem['x'] > obj['x'] and homem['x'] + homem['w'] < obj['x'] + obj['w'] and plataforma == 10:
                if keys[pygame.K_UP] and not(status == 'falling' or jumptime > 0):
                    status = 'climbing'
                    if homem['y'] > 600*6/12:
                        homem['y'] -= 0.2*dt
                    else:
                        status = 'waiting'
                        
        if obj['obj'] in ['tronco_1','tronco_2','tronco']:
            colisao = collision(obj, homem)
            if obj['x'] < 0:
                obj['x'] = 800
            if colisao  and status != 'liana' and status != 'jumping':
                score -= round(0.03*dt)
                if score < 0:
                    score = SCORE
        
        if obj['obj'] == 'gato':
            if collision(obj, homem):
                score -= round(0.03*dt)
                if score < 0 :
                    score = SCORE
            if obj['x'] + obj['w']> 800:
                gato = 0
            if obj['x'] < 0:
                gato = 1
        
    # testar colisao jogador e liana
    mao_x = homem['x'] + 25/2
    mao_y = homem['y'] + 25
    if liana and status != 'falling' and (mao_x-liana['x'])**2+(mao_y-liana['y'])**2 <= LARGURA_LIANA**2:
        dx = mao_x - liana['x']
        dy = mao_y - liana['y']
        theta_homem = math.pi/2 - math.atan2(dy, dx)
        if abs(theta_homem-abs(liana['theta'])) < 0.9 :
            status = 'liana'
            jumptime = 0
    if status == 'liana':
        homem['x'] = liana['x']+math.cos(math.pi/2-liana['theta'])*LARGURA_LIANA-25/2
        homem['y'] = liana['y']+math.sin(math.pi/2-liana['theta'])*LARGURA_LIANA-25

    # DESENHO
    screen.blit(screen_im,(0,0))
    screen.blit(texto, (50,30))
    screen.blit(texto_1,(50,50))
    for o in objects:
        if o['obj'] == 'liana':
            pos_i = (o['x'], o['y'])
            pos_f = (o['x']+math.cos(math.pi/2-o['theta'])*LARGURA_LIANA,
                     o['y']+math.sin(math.pi/2-o['theta'])*LARGURA_LIANA)
            pygame.draw.line(screen, pygame.Color('brown'), pos_i, pos_f, 6)
        
        elif o['obj'] != 'homem':
            img = imagens[o['obj']]
            screen.blit(img, (o['x'], o['y']))      
        
    if jumptime != 0 or (status == 'falling' and not homem['y'] < 600*plataforma/12 - homem['h']) or (colisao and status == None): 
        if dir==0:
            screen.blit(imagens['homem_salto'], (o['x'], o['y']))
        if dir == 1:
            screen.blit(imagens['homem_salto_e'], (o['x'],o['y']))
    else:
        img = imagens['homem']
        screen.blit(img, (o['x'] - img.get_width()/2 + o['w']/2, o['y'] - img.get_height() + o['h']))
    pygame.display.update()
    
pygame.quit()
