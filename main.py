import pygame
import sys

pygame.init()

WIDTH,HEIGHT = 1021 ,831

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


tile_map = [
    [1, 1, 1, 0, 0, 2, 2, 0, 0, 1,2, 0, 0, 1,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 2, 12, 0, 0, 1,1 ],
    [0, 0, 1, 0, 0, 0, 1, 0, 0, 0,2, 0, 0, 1,1],
    [0, 2, 2, 0, 1, 1, 0, 0, 0, 0,2, 0, 0, 1,1],
    [1, 1, 1, 0, 0, 2, 2, 0, 0, 1,2, 0, 0, 1,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 1, 1],
    [0, 0, 1, 0, 0, 0, 1, 0, 0, 0,2, 0, 0, 1,1],
    [0, 2, 2, 0, 1, 1, 0, 0, 0, 0,2, 0, 0, 1,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 2, 12, 0, 0, 1, 1],
    [0, 0, 1, 0, 0, 0, 1, 0, 0, 0,2, 0, 0, 1,1],
    [0, 0, 1, 0, 0, 0, 1, 0, 0, 0,2, 0, 0, 1,1],
    [0, 2, 2, 0, 1, 1, 0, 0, 0, 0,2, 0, 0, 1,1]
]

tile_images = {
    0: pygame.transform.scale(
        pygame.image.load("img/Tile/tile_0000.png").convert_alpha(),
        (128, 128)
    ),
    1: pygame.transform.scale(
        pygame.image.load("img/Tile/tile_0001.png").convert_alpha(),
        (128, 128)
    ),
    2: pygame.transform.scale(
        pygame.image.load("img/Tile/tile_0000.png").convert_alpha(),
        (128, 128)
    )
}



TILE_SIZE = 64 

player_tank = pygame.image.load("img/blue_tank.png").convert_alpha()
player_tank = pygame.transform.scale(player_tank,(64,64))

player_rect = player_tank.get_rect(topleft=(TILE_SIZE,TILE_SIZE *5))

direction = "UP" 
tank_speed = 5

#Зврвз буду робити кулю

bullet_img = pygame.image.load("img/bullet.png").convert_alpha()
bullet_img = pygame.transform.scale(bullet_img,(16,16))

class Bullet:
    def __init__(self,x,y,direction):
        self.speed = 5
        self.direction = direction

        if direction == "UP":
            self.image = pygame.transform.rotate(bullet_img, -90) 
        elif direction == "DOWN":
            self.image = pygame.transform.rotate(bullet_img, 90) 
        elif direction == "LEFT":
            self.image = pygame.transform.rotate(bullet_img,-180)
        elif direction == "RIGHT":
             self.image = bullet_img 

        self.rect = self.image.get_rect(center=(x,y))
    
    def update(self):
        if self.direction == "UP":
            self.rect.y -= self.speed
        elif self.direction == "DOWN":
            self.rect.y += self.speed
        elif self.direction == "LEFT":
            self.rect.x -= self.speed
        elif self.direction == "RIGHT":
            self.rect.x += self.speed

    def draw(self,surface):
        surface.blit(self.image , self.rect)

def get_bullet_spawn(player_rect, direction):
    offset = 20
    if direction == "UP":
        return player_rect.centerx, player_rect.top - offset
    elif direction == "DOWN":
        return player_rect.centerx, player_rect.bottom + offset
    elif direction == "LEFT":
        return player_rect.left - offset, player_rect.centery
    elif direction == "RIGHT":
        return player_rect.right + offset, player_rect.centery

        
            
        
        

menu = True
bullets = []

game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if play_rect.collidepoint(mouse_pos):
                print("Гра почалася")
                menu = False
            elif skin_rect.collidepoint(mouse_pos):
                print("Вибір скіна")
            elif setting_rect.collidepoint(mouse_pos):
                print("Налаштування")
            elif chest_rect.collidepoint(mouse_pos):
                print("Ти відкриваєш сундук")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not menu:
                bullet_x, bullet_y = get_bullet_spawn(player_rect, direction)
                bullet = Bullet(bullet_x, bullet_y, direction)
                bullets.append(bullet)


        

    screen.fill((0, 0, 0))

    if menu:
        screen.blit(play_img,play_rect)
        screen.blit(skin_img,skin_rect)
        screen.blit(setting_img,setting_rect)
        screen.blit(chest_img,chest_rect)
    else:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            if player_rect.top - tank_speed >= 0:
                player_rect.y -= tank_speed
                direction = "UP" 
        elif keys[pygame.K_DOWN]:
            if player_rect.bottom + tank_speed <= HEIGHT:
                player_rect.y += tank_speed
                direction = "DOWN" 
        elif keys[pygame.K_LEFT]:
            if player_rect.left- tank_speed >= 0:
                player_rect.x -= tank_speed
                direction = "LEFT" 
        elif keys[pygame.K_RIGHT]:
            if player_rect.right + tank_speed <= WIDTH:
                player_rect.x += tank_speed
                direction = "RIGHT" 
        for y, row in enumerate(tile_map):
            for x, tile_id in enumerate(row):
                tile_img = tile_images.get(tile_id)
                if tile_img:
                    screen.blit(tile_img, (x * TILE_SIZE, y * TILE_SIZE))

        if direction == "UP":
            rotate_tank = player_tank
        elif direction == "DOWN" :
            rotate_tank = pygame.transform.rotate(player_tank,180)
        elif direction == "LEFT" :
            rotate_tank = pygame.transform.rotate(player_tank,90)
        elif direction == "RIGHT" :
            rotate_tank = pygame.transform.rotate(player_tank,-90)
        for bullet in bullets[:]:
            bullet.update()
            print(f"Куля у позиції: {bullet.rect.topleft}")
            if (bullet.rect.right < 0 or bullet.rect.left > WIDTH or
                bullet.rect.bottom < 0 or bullet.rect.top > HEIGHT):
                bullets.remove(bullet)
            else:
                bullet.draw(screen)
        screen.blit(rotate_tank,player_rect)
   
    pygame.display.flip()


pygame.quit()
sys.exit()
                           