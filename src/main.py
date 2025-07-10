import pygame
import sys
import random
import math
from game_objects import Paddle, Ball, Brick, PowerUp, Laser, Particle, Firework

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen_width, screen_height = 850, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PyGame Arkanoid")

cover_image = pygame.image.load("../assets/images/graphics/start.png").convert_alpha()
cover_image = pygame.transform.scale(cover_image, (screen_width, screen_height))

game_bg_image = pygame.image.load("../assets/images/graphics/field.png").convert()
game_bg_image = pygame.transform.scale(game_bg_image, (screen_width, screen_height))

paddle_image = pygame.image.load("../assets/images/graphics/paddle.png").convert_alpha()

BG_COLOR = pygame.Color('grey12')
BRICK_COLORS = [(178, 34, 34), (255, 165, 0), (255, 215, 0), (50, 205, 50)]

title_font = pygame.font.Font(None, 70)
game_font = pygame.font.Font(None, 40)
message_font = pygame.font.Font(None, 30)

mute = False
def load_sound(file):
    try:
        s = pygame.mixer.Sound(file)
        print(f"Loaded sound: {file}")
        return s
    except Exception as e:
        print(f"Failed to load sound: {file} ({e})")
        class DummySound:
            def play(self): pass
            def stop(self): pass
        return DummySound()

bounce_sound = load_sound('../assets/sounds/bounce.wav')
brick_break_sound = load_sound('../assets/sounds/brick_break.wav')
game_over_sound = load_sound('../assets/sounds/game_over.wav')
laser_sound = load_sound('../assets/sounds/laser.wav')
win_sound = load_sound('../assets/sounds/win.mp3')

edge_left_img = pygame.image.load("../assets/images/graphics/edge_left.png").convert_alpha()
edge_right_img = pygame.image.load("../assets/images/graphics/edge_right.png").convert_alpha()
left_new_height = int(edge_left_img.get_height() * 0.924)
right_new_height = int(edge_right_img.get_height() * 0.924)
edge_left_img = pygame.transform.scale(edge_left_img, (edge_left_img.get_width(), left_new_height))
edge_right_img = pygame.transform.scale(edge_right_img, (edge_right_img.get_width(), right_new_height))
edge_top_img = pygame.image.load("../assets/images/graphics/edge_top.png").convert_alpha()
edge_top_img = pygame.transform.scale(edge_top_img, (screen_width, edge_top_img.get_height()))

left_offset = edge_left_img.get_width()
right_offset = edge_right_img.get_width()
top_offset = edge_top_img.get_height()

paddle = Paddle(screen_width, screen_height, left_offset, right_offset)
balls = [Ball(screen_width, screen_height, left_offset, right_offset, top_offset)]

brick_texture_map = {
    (178, 34, 34): "../assets/images/graphics/bricks/brick_red.png",
    (255, 165, 0): "../assets/images/graphics/bricks/brick_yellow.png",
    (255, 215, 0): "../assets/images/graphics/bricks/brick_pink.png",
    (50, 205, 50): "../assets/images/graphics/bricks/brick_blue.png",
}

def level_1():
    return [Brick(left_offset + col * 80 + 5, top_offset + row * 25 + 40, 75, 20, BRICK_COLORS[row % 4], brick_texture_map[BRICK_COLORS[row % 4]]) for row in range(6) for col in range(10)]

def level_2():
    return [Brick(left_offset + (screen_width - left_offset - right_offset) // 2 - (row * 40) + col * 80, top_offset + row * 25 + 40, 75, 20, BRICK_COLORS[row % 4], brick_texture_map[BRICK_COLORS[row % 4]]) for row in range(6) for col in range(row + 1)]

def level_3():
    return [Brick(left_offset + col * 80 + 5, top_offset + row * 25 + 40, 75, 20, BRICK_COLORS[row % 4], brick_texture_map[BRICK_COLORS[row % 4]]) for row in range(6) for col in range(10) if (row + col) % 2 == 0]

def level_4():
    return [Brick(left_offset + col * 80 + 5, top_offset + row * 25 + 40, 75, 20, BRICK_COLORS[row % 4], brick_texture_map[BRICK_COLORS[row % 4]]) for row in range(6) for col in range(10) if row in [0, 5] or col in [0, 9]]

def level_5():
    return [Brick(left_offset + col * 80 + 5, top_offset + row * 25 + 40, 75, 20, BRICK_COLORS[row % 4], brick_texture_map[BRICK_COLORS[row % 4]]) for row in range(6) for col in range(row + 1)]

def level_6():
    return [Brick(left_offset + col * 80 + row * 40 + 5, top_offset + row * 25 + 40, 75, 20, BRICK_COLORS[row % 4], brick_texture_map[BRICK_COLORS[row % 4]]) for row in range(6) for col in range(10 - row)]

def level_7():
    return [Brick(left_offset + col * 80 + 5, top_offset + row * 25 + 40, 75, 20, BRICK_COLORS[row % 4], brick_texture_map[BRICK_COLORS[row % 4]]) for row in range(6) for col in range(10) if (row % 2 == 0 and col % 3 != 1) or (row % 2 == 1 and col % 3 == 1)]

def level_8():
    return [Brick(left_offset + col * 80 + 5, top_offset + row * 25 + 40, 75, 20, BRICK_COLORS[row % 4], brick_texture_map[BRICK_COLORS[row % 4]]) for row in range(6) for col in range(10) if col % 2 == 0]

def level_9():
    return [Brick(left_offset + col * 80 + 5, top_offset + row * 25 + 40, 75, 20, BRICK_COLORS[row % 4], brick_texture_map[BRICK_COLORS[row % 4]]) for row in range(6) if row % 2 == 0 for col in range(10)]

def level_10():
    return [Brick(left_offset + random.randint(0, 9) * 80 + 5, top_offset + random.randint(0, 5) * 25 + 40, 75, 20, random.choice(BRICK_COLORS), brick_texture_map[random.choice(BRICK_COLORS)]) for _ in range(30)]

levels = [level_1, level_2, level_3, level_4, level_5,
          level_6, level_7, level_8, level_9, level_10]

current_level, chosen_level = 0, 0
bricks = []

power_ups, lasers, particles, fireworks = [], [], [], []
game_state = 'title_screen'
score, lives = 0, 3
display_message, message_timer, firework_timer = "", 0, 0
paused = False

level_images = []
for i in range(10):
    img = pygame.image.load(f"../assets/images/levels/level_{i+1}.png").convert_alpha()
    img = pygame.transform.scale(img, (100, 60))
    level_images.append(img)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game_state == 'title_screen':
                if event.key == pygame.K_SPACE:
                    game_state = 'level_select'

            elif game_state == 'level_select':
                if pygame.K_1 <= event.key <= pygame.K_9:
                    chosen_level = event.key - pygame.K_1
                    current_level = chosen_level
                    bricks = levels[current_level]()
                    paddle.reset()
                    balls = [Ball(screen_width, screen_height, left_offset, right_offset, top_offset)]
                    score, lives = 0, 3
                    power_ups.clear(); lasers.clear(); particles.clear(); fireworks.clear()
                    game_state = 'playing'
                elif event.key == pygame.K_0:
                    chosen_level = 9
                    current_level = chosen_level
                    bricks = levels[current_level]()
                    paddle.reset()
                    balls = [Ball(screen_width, screen_height, left_offset, right_offset, top_offset)]
                    score, lives = 0, 3
                    power_ups.clear(); lasers.clear(); particles.clear(); fireworks.clear()
                    game_state = 'playing'

            elif game_state in ['game_over', 'you_win']:
                if event.key == pygame.K_SPACE:
                    game_state = 'title_screen'
                    score, lives = 0, 3

                if game_state == 'you_win' and current_level < len(levels) - 1 and event.key == pygame.K_RETURN:
                    current_level += 1
                    chosen_level = current_level
                    bricks = levels[current_level]()
                    paddle.reset()
                    balls = [Ball(screen_width, screen_height, left_offset, right_offset, top_offset)]
                    lives = 3
                    power_ups.clear(); lasers.clear(); particles.clear(); fireworks.clear()
                    game_state = 'playing'

            elif game_state == 'playing':
                if event.key == pygame.K_f and paddle.has_laser and paddle.laser_cooldown <= 0:
                    lasers.append(Laser(paddle.rect.centerx - 30, paddle.rect.top))
                    lasers.append(Laser(paddle.rect.centerx + 30, paddle.rect.top))
                    paddle.laser_cooldown = 15
                    if not mute: laser_sound.play()
                if event.key == pygame.K_m:
                    mute = not mute
                if any(ball.is_glued for ball in balls) and event.key == pygame.K_SPACE:
                    for ball in balls:
                        if ball.is_glued:
                            ball.is_glued = False
                if event.key == pygame.K_p:
                    paused = not paused
                if paused:
                    continue

    screen.fill(BG_COLOR)

    if game_state == 'title_screen':
        screen.blit(cover_image, (0, 0))
        
        start_text = "Press SPACE to Start"
        start_surface = game_font.render(start_text, True, (255, 255, 255))
        button_gap = 20
        start_rect = start_surface.get_rect()
        base_x = 40
        base_y = screen_height - (start_rect.height + button_gap) - 40
        start_rect.topleft = (base_x, base_y)
        screen.blit(start_surface, start_rect)
        mute_icon_y = base_y + start_rect.height + button_gap + 10
        if mute:
            mute_icon = pygame.image.load("../assets/images/graphics/mute.png").convert_alpha()
        else:
            mute_icon = pygame.image.load("../assets/images/graphics/speaker.png").convert_alpha()
        mute_icon = pygame.transform.scale(mute_icon, (48, 48))
        screen.blit(mute_icon, (base_x, mute_icon_y))


    elif game_state == 'level_select':
        select_surface = title_font.render("Select Level", True, (255, 255, 255))
        select_rect = select_surface.get_rect(center=(screen_width / 2, 60))
        screen.blit(select_surface, select_rect)
        instruction_text = "(Click a level to select)"
        instruction_surface = message_font.render(instruction_text, True, (255, 255, 255))
        instruction_rect = instruction_surface.get_rect(center=(screen_width / 2, 100))
        screen.blit(instruction_surface, instruction_rect)

        num_levels = 10
        cols = 5
        rows = 2
        box_width = 130
        box_height = 100
        padding_x = 40
        padding_y = 40
        start_x = (screen_width - (box_width + padding_x) * cols + padding_x) // 2
        start_y = 150

        level_boxes = []

        for i in range(num_levels):
            col = i % cols
            row = i // cols
            x = start_x + col * (box_width + padding_x)
            y = start_y + row * (box_height + padding_y)

            rect = pygame.Rect(x, y, box_width, box_height)
            level_boxes.append((rect, i))

            pygame.draw.rect(screen, (200, 200, 200), rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 3)

            image = level_images[i]
            img_rect = image.get_rect(center=(x + box_width // 2, y + box_height // 2 - 10))
            screen.blit(image, img_rect)

            level_text = message_font.render(f"Level {i+1}", True, (0, 0, 0))
            text_rect = level_text.get_rect(center=(x + box_width // 2, y + box_height - 15))
            screen.blit(level_text, text_rect)

        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            for rect, level_index in level_boxes:
                if rect.collidepoint(mouse_pos):
                    chosen_level = level_index
                    current_level = chosen_level
                    bricks = levels[current_level]()
                    paddle.reset()
                    balls = [Ball(screen_width, screen_height, left_offset, right_offset, top_offset)]
                    score, lives = 0, 3
                    power_ups.clear(); lasers.clear(); particles.clear(); fireworks.clear()
                    game_state = 'playing'
                    break

    elif game_state == 'playing':
        if paused:
            pause_surface = title_font.render("PAUSED", True, (255, 255, 255))
            pause_rect = pause_surface.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(pause_surface, pause_rect)
            pygame.display.flip()
            clock.tick(60)
            continue
        left_y = (screen_height - edge_left_img.get_height()) // 2
        right_y = (screen_height - edge_right_img.get_height()) // 2
        screen.blit(edge_left_img, (0, left_y))
        screen.blit(edge_right_img, (screen_width - edge_right_img.get_width(), right_y))
        top_x = edge_left_img.get_width()
        top_width = screen_width - edge_left_img.get_width() - edge_right_img.get_width()
        edge_top_scaled = pygame.transform.scale(edge_top_img, (top_width, edge_top_img.get_height()))
        screen.blit(edge_top_scaled, (top_x, 0))

        paddle.update()
        keys = pygame.key.get_pressed()

        balls_to_remove = []
        for ball in balls:
            ball_status, collision_object = ball.update(paddle, keys[pygame.K_SPACE])
            if ball_status == 'lost':
                balls_to_remove.append(ball)
            elif collision_object in ['wall', 'paddle']:
                if not mute: bounce_sound.play()
                for _ in range(5):
                    particles.append(Particle(ball.rect.centerx, ball.rect.centery, (255, 255, 0), 1, 3, 1, 3, 0))

        for ball in balls_to_remove:
            balls.remove(ball)

        if len(balls) == 0:
            lives -= 1
            if lives <= 0:
                game_state = 'game_over'
                if not mute: game_over_sound.play()
            else:
                balls = [Ball(screen_width, screen_height, left_offset, right_offset, top_offset)]
                paddle.reset()

        for ball in balls:
            for brick in bricks[:]:
                if ball.rect.colliderect(brick.rect):
                    ball.speed_y *= -1
                    for _ in range(15):
                        particles.append(Particle(brick.rect.centerx, brick.rect.centery, brick.color, 1, 4, 1, 4, 0.05))
                    bricks.remove(brick)
                    score += 10
                    if not mute: brick_break_sound.play()
                    if random.random() < 0.3:
                        power_ups.append(PowerUp(brick.rect.centerx, brick.rect.centery,
                                                 random.choice(['grow', 'laser', 'glue', 'slow', 'multi', 'life', 'shrink'])))
                    break

        for power_up in power_ups[:]:
            power_up.update()
            if power_up.rect.top > screen_height:
                power_ups.remove(power_up)
            elif paddle.rect.colliderect(power_up.rect):
                display_message = power_up.PROPERTIES[power_up.type]['message']
                message_timer = 120
                if power_up.type in ['grow', 'laser', 'glue']:
                    paddle.activate_power_up(power_up.type)
                elif power_up.type == 'slow':
                    for ball in balls:
                        ball.activate_power_up(power_up.type)
                elif power_up.type == 'multi':
                    new_balls = []
                    for ball in balls:
                        new_ball = Ball(screen_width, screen_height, left_offset, right_offset, top_offset)
                        new_ball.rect.center = ball.rect.center
                        new_ball.speed_x = -ball.speed_x
                        new_ball.speed_y = ball.speed_y
                        new_balls.append(new_ball)
                    balls.extend(new_balls)
                elif power_up.type == 'life':
                    lives += 1
                elif power_up.type == 'shrink':
                    paddle.shrink()
                power_ups.remove(power_up)

        for laser in lasers[:]:
            laser.update()
            if laser.rect.bottom < 0:
                lasers.remove(laser)
            else:
                for brick in bricks[:]:
                    if laser.rect.colliderect(brick.rect):
                        for _ in range(10):
                            particles.append(Particle(brick.rect.centerx, brick.rect.centery, brick.color, 1, 3, 1, 3, 0.05))
                        bricks.remove(brick)
                        lasers.remove(laser)
                        score += 10
                        if not mute: brick_break_sound.play()
                        break

        if not bricks:
            game_state = 'you_win'
            if not mute:
                win_sound.stop()
                win_sound.play()

        paddle.draw(screen)
        for ball in balls:
            ball.draw(screen)
        for brick in bricks:
            brick.draw(screen)
        for power_up in power_ups:
            power_up.draw(screen)
        for laser in lasers:
            laser.draw(screen)

        score_text = game_font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (25, 20))
        lives_text = game_font.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(lives_text, (screen_width - lives_text.get_width() - 25, 20))
        level_text = game_font.render(f"Level: {current_level + 1}", True, (255, 255, 255))
        screen.blit(level_text, (screen_width // 2 - 50, 20))

        if mute:
            mute_icon = pygame.image.load("../assets/images/graphics/mute.png").convert_alpha()
        else:
            mute_icon = pygame.image.load("../assets/images/graphics/speaker.png").convert_alpha()
        mute_icon = pygame.transform.scale(mute_icon, (30, 30))
        screen.blit(mute_icon, (screen_width - mute_icon.get_width() - 30, screen_height - mute_icon.get_height() - 20))

    elif game_state in ['game_over', 'you_win']:
        if game_state == 'game_over':
            pass
        
        if game_state == 'you_win':
            firework_timer -= 1
            if firework_timer <= 0:
                fireworks.append(Firework(screen_width, screen_height))
                firework_timer = random.randint(20, 50)
            for firework in fireworks[:]:
                firework.update()
                if firework.is_dead():
                    fireworks.remove(firework)
            for firework in fireworks:
                firework.draw(screen)
        
        if game_state in ['game_over', 'you_win']:
            score_surface = game_font.render(f"Score: {score}", True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(screen_width / 2, 80))
            screen.blit(score_surface, score_rect)
            if game_state == 'game_over':
                message = "GAME OVER"
            else:
                message = "YOU WIN!"
            big_font = pygame.font.Font(None, 100)
            text_surface = big_font.render(message, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(screen_width / 2, screen_height / 2))
            screen.blit(text_surface, text_rect)

        restart_surface = game_font.render("Press SPACE to return to Title", True, (255, 255, 255))
        restart_rect = restart_surface.get_rect(center=(screen_width / 2, screen_height / 2 + 100))
        screen.blit(restart_surface, restart_rect)

        if game_state == 'you_win' and current_level < len(levels) - 1:
            next_level_surface = game_font.render("Press ENTER to play next level", True, (255, 255, 255))
            next_level_rect = next_level_surface.get_rect(center=(screen_width / 2, screen_height / 2 + 150))
            screen.blit(next_level_surface, next_level_rect)


    if message_timer > 0:
        message_timer -= 1
        message_surface = message_font.render(display_message, True, (255, 255, 255))
        message_rect = message_surface.get_rect(center=(screen_width / 2, screen_height - 60))
        screen.blit(message_surface, message_rect)

    for particle in particles[:]:
        particle.update()
        if particle.size <= 0:
            particles.remove(particle)
    for particle in particles:
        particle.draw(screen)

    pygame.display.flip()
    clock.tick(60)
