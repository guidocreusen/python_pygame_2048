#function to create and antialiased rounded rectangle
import pygame

def AAfilledRoundedRect(rect,color,radius=0.4):

    """
    AAfilledRoundedRect(rect,color,radius=0.4)

    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect         = pygame.Rect(rect)
    color        = pygame.Color(*color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = pygame.Surface(rect.size,pygame.SRCALPHA)

    circle       = pygame.Surface([min(rect.size)*3]*2,pygame.SRCALPHA)
    pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)

    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

    rectangle.fill(color,special_flags=pygame.BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=pygame.BLEND_RGBA_MIN)

    return rectangle

#if __name__ == "__main__":
#    scr = pygame.display.set_mode((300,300))
#    scr.fill((255,255,255))
#
#    surf = AAfilledRoundedRect((0, 0, 50, 100), (0,255,0))
#    scr.blit(surf, (125,100))
#    
#    pygame.display.flip()
#    while pygame.event.wait().type != pygame.QUIT: pass