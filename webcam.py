#!/usr/bin/python

import sys
import pygame
import pygame.camera
pygame.init()
pygame.camera.init()

size = width, height = 640, 480
cam = pygame.camera.Camera("/dev/video0", (640, 480), "VVV")
cam.start()
cam.set_controls(hflip = True, vflip = False)
black = 0, 0, 0
screen = pygame.display.set_mode(size)
thresholded = pygame.surface.Surface(size, 0, screen)
running = 1


while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: running = 0

    image = cam.get_image()
    screen.fill(black)
    crect = (width / 2 - 15, height / 2 - 15, 30, 30)
    avg = pygame.transform.average_color(image, crect)
    pygame.transform.threshold(screen, image, avg, (30, 30, 30), (0, 0, 0), 2)
    
    pygame.draw.rect(screen, (255, 0, 0), crect, 4)
    pygame.display.flip()

while 1:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: sys.exit()
    
    screen.fill(black)
    image = cam.get_image()
    screen.blit(image, (0, 0))
    mask = pygame.mask.from_threshold(image, avg, (30, 30, 30))
    connected = mask.connected_component()
    if mask.count() > 100:
        coord = mask.centroid()
        pygame.draw.circle(screen, (0, 255, 0), coord, max(min(50, mask.count() / 400), 5))
    
    pygame.display.flip()
