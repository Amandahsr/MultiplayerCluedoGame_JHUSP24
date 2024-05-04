import pygame

# This is the debug function that will be used to display information on the screen

pygame.init()
font = pygame.font.Font(None, 24)


def debug(info, x=10, y=10):
    display_surf = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, "White")
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pygame.draw.rect(display_surf, "Black", debug_rect)
    display_surf.blit(debug_surf, debug_rect)
