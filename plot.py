import pygame
import time
import random
import math

screen_width = 500
screen_height = 500
sx = -5
ex = 5
sy = -5
ey = 5
scale_x = screen_width/(ex-sx)
scale_y = screen_height/(sy-ey)

ticx = 0.5
ticy = 0.5
gridx = 2
gridy = 1
ticsize = 5

colorF = pygame.Color(0, 0, 255)
colorG = pygame.Color(255, 0, 255)
colorOXY = pygame.Color(0, 0, 0)
colorBG = pygame.Color(255, 255, 255)
colorgrid = pygame.Color(200, 200, 200)

N = 100

Fs = [(lambda x: x**2, (0,0,255)),
      (lambda x: math.sin(x), (255,0,255)),
      (lambda x: math.exp(x), (0,255,0))]

hilights = [False for p in Fs]

def mapX(x):
    return int((x - sx) * scale_x)

def revmapX(x):
    return x/scale_x + sx

def mapY(y):
    return int((y - ey)*scale_y)

def revmapY(y):
    return y/scale_y + ey

def mapP(p):
    return (mapX(p[0]), mapY(p[1]))

def mapPb(p):
    return ((p[0] - sx) * scale_x, (p[1] - ey) * scale_y)

mouseP = (0,0)
mouseX = 0
mouseY = 0
mouseRP = (0,0)
mouseRX = 0
mouseRY = 0

pygame.init()

font = pygame.font.Font(pygame.font.get_default_font(), 12)
screen = pygame.display.set_mode([screen_width, screen_height])


def draw():
    screen.fill(colorBG)

    x = gridx
    maxX = max(abs(sx), abs(ex))
    if gridx != 0:
        while x <= maxX:
            pygame.draw.line(screen, colorgrid, (mapX(x), 0), (mapX(x), screen_height))
            pygame.draw.line(screen, colorgrid, (mapX(-x), 0), (mapX(-x), screen_height))
            x += gridx

    y = gridy
    maxY = max(abs(sy), abs(ey))
    while y <= maxY:
        pygame.draw.line(screen, colorgrid, (0, mapY(y)), (screen_width, mapY(y)))
        pygame.draw.line(screen, colorgrid, (0, mapY(-y)), (screen_width, mapY(-y)))
        y += gridy

    pygame.draw.line(screen, colorOXY, mapP((sx, 0)), mapP((ex, 0)))
    pygame.draw.line(screen, colorOXY, mapP((0, sy)), mapP((0, ey)))

    x = ticx
    while x <= maxX:
        pygame.draw.line(screen, colorOXY, (mapX(x), mapY(0) - ticsize), (mapX(x), mapY(0) + ticsize))
        pygame.draw.line(screen, colorOXY, (mapX(-x), mapY(0) - ticsize), (mapX(-x), mapY(0) + ticsize))
        x += ticx

    y = ticy
    while y <= maxY:
        pygame.draw.line(screen, colorOXY, (mapX(0) - ticsize, mapY(y)), (mapX(0) + ticsize, mapY(y)))
        pygame.draw.line(screen, colorOXY, (mapX(0) - ticsize, mapY(-y)), (mapX(0) + ticsize, mapY(-y)))
        y += ticy

    for fun, hilight in zip(Fs, hilights):
        f, color = fun
        listP = list(range(N))
        for i in range(N):
            x = (i/N * (ex - sx)) + sx
            listP[i] = mapPb((x, f(x)))

        pygame.draw.aalines(screen, (255, 215, 0) if hilight else color, False, listP, 1)

    screen.blit(font.render(str((round(mouseRX, 2), round(mouseRY, 2))), True, (0, 0, 0), (200, 200, 200, 200)), dest = (mouseX + 10, mouseY))

    pygame.display.flip()

draw()

kw,ka,ks,kd,kn,km = False, False, False, False, False, False
clock = pygame.time.Clock()
frame = 0
while True:
    frame += 1
    if frame == 30: frame = 0
    dt = clock.tick(30) / 100
    mouseP = pygame.mouse.get_pos()
    mouseX = mouseP[0]
    mouseY = mouseP[1]
    mouseRX = revmapX(mouseX)
    mouseRY = revmapY(mouseY)
    mouseRP = (mouseRX, mouseRY)
    hilights = [abs(mapY(f(mouseRX))-mouseY) < 5 for f, c in Fs]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            kd |= event.key == pygame.K_d
            ka |= event.key == pygame.K_a
            kw |= event.key == pygame.K_w
            ks |= event.key == pygame.K_s

            kn |= event.key == pygame.K_n
            km |= event.key == pygame.K_m
        if event.type == pygame.KEYUP:
            kd &= event.key != pygame.K_d
            ka &= event.key != pygame.K_a
            kw &= event.key != pygame.K_w
            ks &= event.key != pygame.K_s

            kn &= event.key != pygame.K_n
            km &= event.key != pygame.K_m
    if kw:
        sy += ticy * dt
        ey += ticy * dt
    if ks:
        sy -= ticy * dt
        ey -= ticy * dt
    if ka:
        sx -= ticx * dt
        ex -= ticx * dt
    if kd:
        sx += ticx * dt
        ex += ticx * dt
    if frame % 10 == 0:
        if km: gridx *= 2
        if kn: gridx /= 2
    draw()
pygame.quit()
