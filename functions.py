import pygame
def width(img):
    return img.get_width()

def height(img):
    return img.get_height()

def cut(surface, x, y, width, height):
    image = surface.copy()
    rect = pygame.Rect(x, y, width, height)
    image.set_clip(rect)
    croppedImg = surface.subsurface(image.get_clip())
    return croppedImg.copy()