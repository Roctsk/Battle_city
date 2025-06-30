import pygame
import sys
import os
from maps import tile_maps
import random

import json
import os

SAVE_FILE = "save_data.json"

def save_crystals(count):
    data = {"crystals": count}
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_crystals():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            return data.get("crystals", 0)
    return 0


pygame.init()
pygame.mixer.init()

shoot_sound = pygame.mixer.Sound("Music/shoot.mp3")
hit_sound = pygame.mixer.Sound("Music/hit.mp3")
move_sound = pygame.mixer.Sound("Music/move.mp3")

pygame.mixer.music.load("Music/fon.mp3")
pygame.mixer.music.set_volume(0.5)
move_sound.set_volume(0.3)

crystal_count = load_crystals()
chest_open_sound = pygame.mixer.Sound("Music/open_chest.mp3")

clock = pygame.time.Clock()


WIDTH, HEIGHT = 1180, 740

small_font = pygame.font.SysFont("arial", 28)
back_text = small_font.render("← Назад", True, (255, 255, 255))
back_rect = back_text.get_rect(topleft=(50, HEIGHT - 70))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle_city")

BG_COLOR = (30, 30, 30)

play_img = pygame.image.load("img/button_play.png").convert_alpha()
skin_img = pygame.image.load("img/button_skins.png").convert_alpha()
setting_img = pygame.image.load("img/button_settings.png").convert_alpha()

chest_img = pygame.image.load("img/chest.png").convert_alpha()


LEVEL_IMG_SIZE = 180
LEVELS_PER_ROW = 3
LEVEL_BUTTON_SIZE = 100  
BUTTON_SPACING = 20



total_grid_width = LEVELS_PER_ROW *LEVEL_BUTTON_SIZE + (LEVELS_PER_ROW -1) * BUTTON_SPACING
total_grid_height = LEVELS_PER_ROW *LEVEL_BUTTON_SIZE + (LEVELS_PER_ROW -1) * BUTTON_SPACING
levels_img_x = (WIDTH - total_grid_width) // 2
levels_img_y = (HEIGHT - total_grid_height) // 2


exit_img = pygame.image.load("img/exit.png")
exit_img = pygame.transform.scale(exit_img,(120,120))
exit_rect = exit_img.get_rect(topright=(WIDTH - 5, 5))


level_buttons = []
for row in range(LEVELS_PER_ROW):
    for col in range(LEVELS_PER_ROW):
        rect = pygame.Rect(
            levels_img_x + col * (LEVEL_BUTTON_SIZE + BUTTON_SPACING),
            levels_img_y + row * (LEVEL_BUTTON_SIZE + BUTTON_SPACING),
            LEVEL_BUTTON_SIZE,
            LEVEL_BUTTON_SIZE
        )
        level_buttons.append(rect)

level_images = []
for i in range(1, 10):
    img = pygame.image.load(f"Img/{i}.png").convert_alpha()
    img = pygame.transform.scale(img, (LEVEL_BUTTON_SIZE, LEVEL_BUTTON_SIZE))
    level_images.append(img)

play_rect = play_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
skin_rect = skin_img.get_rect(center=(WIDTH // 2 - 250, HEIGHT // 2 - 50))
setting_rect = setting_img.get_rect(center=(WIDTH // 2 + 250, HEIGHT // 2 - 50))
background_img = pygame.transform.scale(pygame.image.load("img/background.jpg").convert(), (WIDTH, HEIGHT))
level_select_bg = pygame.transform.scale(
    pygame.image.load("img/level_select_bg.png").convert(),
    (WIDTH, HEIGHT)
)

chest_img = pygame.transform.scale(chest_img, (
    int(chest_img.get_width() * 1.2),
    int(chest_img.get_height() * 1.2)
))
chest_rect = chest_img.get_rect()
chest_rect.bottomleft = (5, HEIGHT - 20)

show_level_select = False
current_tile_map = None  



tile_images = {
    0: pygame.transform.scale(
        pygame.image.load("img/Tile/tile_0000.png").convert_alpha(),
        (100, 100)
    ),
    1: pygame.transform.scale(
        pygame.image.load("img/Tile/tile_0024.png").convert_alpha(),
        (128, 128)
    ),
    2: pygame.transform.scale(
        pygame.image.load("img/Tile/tile_0001.png").convert_alpha(),
        (100, 100)
    ),
    3: pygame.transform.scale(
        pygame.image.load("img/Tile/tile_0004.png").convert_alpha(),
        (100, 100)
    ),
    4: pygame.transform.scale(
        pygame.image.load("img/Tile/tile_0005.png").convert_alpha(),
        (100, 100)
    ),
    5: pygame.transform.scale(
        pygame.image.load("img/Tile/tile_0006.png").convert_alpha(),
        (100, 100)
    ),
    6: pygame.transform.scale(
        pygame.image.load("img/Tile/tile_0263.png").convert_alpha(),
        (100, 100)
    ),
    7: pygame.transform.scale(
        pygame.image.load("img/Tile/tile_0263.png").convert_alpha(),
        (100, 100)
    ),
    8: pygame.transform.scale(
        pygame.image.load("img/Tile/tile_0287.png").convert_alpha(),
        (100, 100)
    ),
}

TILE_SIZE = 64

player_tank = pygame.image.load("img/blue_tank.png").convert_alpha()
player_tank = pygame.transform.scale(player_tank, (64, 64))
player_rect = player_tank.get_rect(topleft=(TILE_SIZE, TILE_SIZE * 5))

auto_tank = pygame.image.load("img/red_tank.png").convert_alpha()
auto_tank = pygame.transform.scale(auto_tank, (64, 64))


auto_rect = auto_tank.get_rect(topleft=(WIDTH - TILE_SIZE * 2, TILE_SIZE))
auto_direction = "DOWN"



direction = "UP"
tank_speed = 5
   
bullet_img = pygame.image.load("img/bullet.png").convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (16, 16))


class Bullet:
    def __init__(self, x, y, direction):
        self.speed = 5
        self.direction = direction

        if direction == "UP":
            self.image = pygame.transform.rotate(bullet_img, -90)
        elif direction == "DOWN":
            self.image = pygame.transform.rotate(bullet_img, 90)
        elif direction == "LEFT":
            self.image = pygame.transform.rotate(bullet_img, -180)
        elif direction == "RIGHT":
            self.image = bullet_img

        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        if self.direction == "UP":
            self.rect.y -= self.speed
        elif self.direction == "DOWN":
            self.rect.y += self.speed
        elif self.direction == "LEFT":
            self.rect.x -= self.speed
        elif self.direction == "RIGHT":
            self.rect.x += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)


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
    

skin_images = [
    pygame.image.load("img/skin_1.png").convert_alpha(),
    pygame.image.load("img/skin_2.png").convert_alpha(),
    pygame.image.load("img/skin_3.png").convert_alpha(),

]

skin_images = [pygame.transform.scale(img, (300, 300)) for img in skin_images]

skin_prices = [100, 200, 300] 

crystal_img = pygame.image.load("img/almaz.png").convert_alpha()
crystal_img = pygame.transform.scale(crystal_img, (40, 32))

skin_rects = []
total_width = len(skin_images) * 180 + (len(skin_images) - 1) * 100
start_x = WIDTH // 2 - 180 - total_width // 2
y_pos = HEIGHT // 2 - 200

for i, img in enumerate(skin_images):
    rect = img.get_rect(topleft=(start_x + i * (300 + 100), y_pos))
    skin_rects.append(rect)


current_level_index = 0

menu = True
bullets = []

auto_bullets = []
auto_shoot_timer = 0
ENEMY_SHOOT_INTERVAL = 120  

player_health = 3
auto_health = 3

move_channel = pygame.mixer.Channel(1)
shoot_channel = pygame.mixer.Channel(2)
mouse_pos = (0, 0)
load_level = False  
setting_menu = False

volume = 0.5
slider_dragging = False
slider_x = 300
slider_y = 200
slider_width = 400
slider_height = 10

skin_menu = False

game = True
while game: 
    clock.tick(60)  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            if setting_menu and back_rect.collidepoint(mouse_pos):
                setting_menu = False
                menu = True
            if setting_menu:
                slider_dragging = False

            if setting_menu and slider_dragging:
                rel_x = mouse_pos[0] - slider_x
                rel_x = max(0, min(rel_x, slider_width)) 
                volume = rel_x / slider_width
                pygame.mixer.music.set_volume(volume)
            if menu:

                if play_rect.collidepoint(mouse_pos):
                    pygame.mixer.music.stop()
                    menu = False
                    show_level_select = True
                elif setting_rect.collidepoint(mouse_pos):
                    menu = False
                    setting_menu = True
                elif skin_rect.collidepoint(mouse_pos):
                    menu = False
                    skin_menu = True 
                elif chest_rect.collidepoint(mouse_pos):
                    save_crystals(crystal_count)
                    chest_open_sound.play()
                    gained_crystals = random.randint(1, 10) 
                    crystal_count += gained_crystals
                    print(f"Випало {gained_crystals} кристалів! Всього: {crystal_count}")
                elif back_rect.collidepoint(mouse_pos):
                    setting_menu = False
                    menu = True
            elif back_rect.collidepoint(mouse_pos):
                    skin_menu = False
                    menu = True

            elif show_level_select:
                for i, rect in enumerate(level_buttons):
                    if rect.collidepoint(mouse_pos):
                        if 0 <= i < len(tile_maps):
                            current_level_index = i
                            current_tile_map = tile_maps[current_level_index]
                            show_level_select = False
                            menu = False
                            print(f" Завантажено карту рівня {current_level_index + 1}")
                        else:
                            print(f" Рівень {i + 1} не знайдено")

            else:
                if exit_rect.collidepoint(mouse_pos):
                    menu = True
                    current_tile_map = None
                    show_level_select = False
                    bullets.clear()



        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x, bullet_y = get_bullet_spawn(player_rect, direction)
                new_bullet = Bullet(bullet_x, bullet_y, direction)
                bullets.append(new_bullet)
                shoot_channel.play(shoot_sound)


    if menu:
        screen.blit(background_img, (0, 0))
        screen.blit(play_img, play_rect)
        screen.blit(skin_img, skin_rect)
        screen.blit(setting_img, setting_rect)
        screen.blit(chest_img, chest_rect)
        screen.blit(crystal_img, (10, 10))

        font = pygame.font.SysFont("arial", 28)
        crystal_text = font.render(str(crystal_count), True, (255, 255, 255))
        screen.blit(crystal_text, (10 + crystal_img.get_width() + 5, 12))
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("Music/fon.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

    elif setting_menu:
        screen.fill((50, 50, 70))  

        font = pygame.font.SysFont("arial", 36)
        small_font = pygame.font.SysFont("arial", 28)

        settings_text = font.render("Налаштування", True, (255, 255, 255))
        screen.blit(settings_text, (WIDTH // 2 - settings_text.get_width() // 2, 50))

        pygame.draw.rect(screen, (200, 200, 200), (slider_x, slider_y, slider_width, slider_height))
        
        knob_x = slider_x + int(volume * slider_width)
        pygame.draw.circle(screen, (255, 0, 0), (knob_x, slider_y + slider_height // 2), 12)

        volume_text = small_font.render("Гучність музики", True, (255, 255, 255))
        screen.blit(volume_text, (slider_x, slider_y - 40))

        back_text = small_font.render("← Назад", True, (255, 255, 255))
        back_rect = back_text.get_rect(topleft=(50, HEIGHT - 70))
        screen.blit(back_text, back_rect)

        lang_text = small_font.render("Мова: [UA] [EN] [PL]", True, (200, 200, 200))
        screen.blit(lang_text, (slider_x, slider_y + 80))
    elif show_level_select:
        screen.blit(level_select_bg, (0, 0))
        for i, rect in enumerate(level_buttons):
            if i < len(level_images):
                screen.blit(level_images[i], rect.topleft)
    elif skin_menu:
        screen.fill((40,40,60))
        
        title = pygame.font.SysFont("arial", 48).render("Скіни", True, (255, 215, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))


        for i, img in enumerate(skin_images):

            pygame.draw.rect(screen, (0, 200, 255), skin_rects[i].inflate(20, 20), border_radius=10)

            screen.blit(img, skin_rects[i])

            font = pygame.font.SysFont("arial", 26)
            price = skin_prices[i]
            price_text = font.render(str(price), True, (255, 255, 0))

            text_x = skin_rects[i].centerx - 20
            text_y = skin_rects[i].bottom + 10

            crystal_x = text_x + price_text.get_width() + 10
            crystal_y = text_y - 5

            screen.blit(price_text, (text_x, text_y))
            screen.blit(crystal_img, (crystal_x, crystal_y))

        screen.blit(back_text,back_rect)


    else:
        keys = pygame.key.get_pressed()
        moving = False


        if keys[pygame.K_UP] and player_rect.top - tank_speed >= 0:
            player_rect.y -= tank_speed
            direction = "UP"
            moving = True
        elif keys[pygame.K_DOWN] and player_rect.bottom + tank_speed <= HEIGHT:
            player_rect.y += tank_speed
            direction = "DOWN"
            moving = True
        elif keys[pygame.K_LEFT] and player_rect.left - tank_speed >= 0:
            player_rect.x -= tank_speed
            direction = "LEFT"
            moving = True
        elif keys[pygame.K_RIGHT] and player_rect.right + tank_speed <= WIDTH:
            player_rect.x += tank_speed
            direction = "RIGHT"
            moving = True

        
        if moving:
            if not move_channel.get_busy():
                move_channel.play(move_sound, loops=-1)
        else:
            move_channel.stop()

        if current_tile_map is not None:
            for y, row in enumerate(current_tile_map):
                for x, tile_id in enumerate(row):
                    tile_img = tile_images.get(tile_id)
                    if tile_img:
                        screen.blit(tile_img, (x * TILE_SIZE, y * TILE_SIZE))

        if direction == "UP":
            rotate_tank = player_tank
        elif direction == "DOWN":
            rotate_tank = pygame.transform.rotate(player_tank, 180)
        elif direction == "LEFT":
            rotate_tank = pygame.transform.rotate(player_tank, 90)
        elif direction == "RIGHT":
            rotate_tank = pygame.transform.rotate(player_tank, -90)


        if direction == "UP":
            rotate_auto = auto_tank
        elif direction == "DOWN":
            rotate_auto = pygame.transform.rotate(auto_tank, 180)
        elif direction == "LEFT":
            rotate_auto = pygame.transform.rotate(auto_tank, 90)
        elif direction == "RIGHT":
            rotate_auto = pygame.transform.rotate(auto_tank, -90)

        for bullet in bullets[:]:
            bullet.update()
            if bullet.rect.colliderect(auto_rect):
                print("В ворога влучино")
                bullets.remove(bullet)
                hit_sound.play()
                auto_health -= 1
                print(f"Здоров'я гравця: {auto_health}")
                if auto_health <= 0:
                 print("Ворог знищений!")
            elif (bullet.rect.right < 0 or bullet.rect.left > WIDTH or
                bullet.rect.bottom < 0 or bullet.rect.top > HEIGHT):
                bullets.remove(bullet)
            else:
                bullet.draw(screen)

        if load_level:
            if current_level_index < len(tile_maps):
                current_tile_map = tile_maps[current_level_index]
                auto_health = 3
                player_health = 3
                auto_rect.topleft = (WIDTH - TILE_SIZE * 2, TILE_SIZE)
                player_rect.topleft = (TILE_SIZE, TILE_SIZE * 5)
                bullets.clear()
                auto_bullets.clear()
                print(f"✅ Переходимо до рівня {current_level_index + 1}")
                load_level = False
            else:
                print("🎉 Гру пройдено!")
                game = False
                continue



        if auto_health <= 0:
            print("Ворог знищений!")
            current_level_index += 1
            load_level = True  
        for bullet in auto_bullets[:]:
            bullet.update()
            if bullet.rect.colliderect(player_rect):
                print("Гравець підбитий ворогом!")
                auto_bullets.remove(bullet)
                hit_sound.play()
                player_health -= 1
                print(f"Здоров'я гравця: {player_health}")
                if player_health <= 0:
                    print(" Гравець програв!")
                    game = False
            elif (bullet.rect.right < 0 or bullet.rect.left > WIDTH or
                bullet.rect.bottom < 0 or bullet.rect.top > HEIGHT):
                auto_bullets.remove(bullet)
            else:
                bullet.draw(screen)


        screen.blit(exit_img,exit_rect)
        screen.blit(rotate_tank, player_rect)
        screen.blit(rotate_auto,auto_rect)

        if auto_rect.y < player_rect.y:
            auto_rect.y += 1
            auto_direction = "DOWN"
        elif auto_rect.y > player_rect.y:
            auto_rect.y -= 1
            auto_direction = "UP"
        elif auto_rect.x < player_rect.x:
            auto_rect.x += 1
            auto_direction = "RIGHT"
        elif auto_rect.x > player_rect.x:
            auto_rect.x -= 1
            auto_direction = "LEFT"


        auto_shoot_timer += 1
        if auto_shoot_timer >= ENEMY_SHOOT_INTERVAL:
            bullet_x, bullet_y = get_bullet_spawn(auto_rect, auto_direction)
            auto_bullets.append(Bullet(bullet_x, bullet_y, auto_direction))
            shoot_channel.play(shoot_sound)
            auto_shoot_timer = 0

    pygame.display.flip()

pygame.quit()
sys.exit()