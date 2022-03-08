import pygame
def cut(surface, x, y, width, height):
    image = surface.copy()
    rect = pygame.Rect(x, y, width, height)
    image.set_clip(rect)
    croppedImg = surface.subsurface(image.get_clip())
    return croppedImg.copy()

class Font:
    def __init__(self, path, fontSize):
        self.spacing = 1
        fontPic = pygame.image.load(path).convert()
        self.fontWidth = fontPic.get_width()
        self.fontHeight = fontPic.get_height()
        self.dictionary = {}
        self.wordDict = {}
        width = 0
        self.charOrder = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';', '%']
        self.charCount = 0
        self.totalCharWidth = 0
        self.wordWidth = []
        for x in range(self.fontWidth):
            color = fontPic.get_at((x, 0))
            if color[0] == 127:
                letterPic = cut(fontPic, x - width, 0, width, self.fontHeight)
                letterPic = pygame.transform.scale(letterPic, (int(letterPic.get_width() * (fontSize/4)), int(letterPic.get_height() * (fontSize/4))))
                letterPic.set_colorkey((0, 0, 0))
                self.dictionary[self.charOrder[self.charCount]] = letterPic.copy()
                self.charCount += 1
                width = 0
            else:
                 width += 1

    def render(self, surf, string, coords):
        xOffset = 0
        for i in string:
            if i != " ":
                surf.blit(self.dictionary[i], (coords[0] + xOffset, coords[1]))
                xOffset += self.dictionary[i].get_width()
            else: xOffset += self.dictionary["A"].get_width()        

    def renderLines(self, surf, y, gap, lst):
        yOffset = 0
        x = 0
        surfWidth = surf.get_width()
        widthCenter = surfWidth/2
        for word in lst:
           wordWidth = self.dictionary["A"].get_width() * len(word)
           wordWidthCenter = wordWidth/2
           self.render(surf, word, (widthCenter - wordWidthCenter, y + yOffset))
           yOffset += self.fontHeight + gap
           xOffset = 0
           
