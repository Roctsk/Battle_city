import pygame
import sys

pygame.init()

WIDTH,HEIGHT = 1000 ,800

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Battle_city")

BG_COLOR =(30,30,30)


play_img = pygame.image.load("img/button_play.png").convert_alpha()
skin_img = pygame.image.load("img/button_skins.png").convert_alpha()
setting_img = pygame.image.load("img/button_settings.png").convert_alpha()

chest_img= pygame.image.load("img/chest.png").convert_alpha()


play_rect = play_img.get_rect(center=(WIDTH // 2 ,HEIGHT // 2 - 50))
skin_rect = skin_img.get_rect(center=(WIDTH // 2 - 250  ,HEIGHT // 2 - 50))
setting_rect = setting_img.get_rect(center=(WIDTH // 2 + 250 ,HEIGHT // 2 - 50))


chest_img = pygame.transform.scale(chest_img, (
    int(chest_img.get_width() * 1.2),
    int(chest_img.get_height() * 1.2)
))

chest_rect = chest_img.get_rect()
chest_rect.bottomleft = (5 , HEIGHT - 20)

game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if play_rect.collidepoint(mouse_pos):
                print("Гра почалася")
            elif skin_rect.collidepoint(mouse_pos):
                print("Вибір скіна")
            elif setting_rect.collidepoint(mouse_pos):
                print("Налаштування")
            elif chest_rect.collidepoint(mouse_pos):
                print("Ти відкриваєш сундук")
            
    

    screen.fill((0, 0, 0))

    screen.blit(play_img,play_rect)
    screen.blit(skin_img,skin_rect)
    screen.blit(setting_img,setting_rect)
    screen.blit(chest_img,chest_rect)

    pygame.display.flip()


pygame.quit()
sys.exit()
                           