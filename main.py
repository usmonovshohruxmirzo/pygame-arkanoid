import pygame
import sys
import random
import math
from game_objects import Paddle, Ball, Brick, PowerUp, Laser, Particle, Firework

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PyGame Arkanoid")

BG_COLOR = pygame.Color('grey12')
BRICK_COLORS = [(178, 34, 34), (255, 165, 0), (255, 215, 0), (50, 205, 50)]

title_font = pygame.font.Font(None, 70)
game_font = pygame.font.Font(None, 40)
message_font = pygame.font.Font(None, 30)

mute = False
def load_sound(file):
    try:
        return pygame.mixer.Sound(file)
    except:
        return type('', (), {'play': lambda self: None})()

bounce_sound = load_sound('bounce.wav')
brick_break_sound = load_sound('brick_break.wav')
game_over_sound = load_sound('game_over.wav')
laser_sound = load_sound('laser.wav')

paddle = Paddle(screen_width, screen_height)
ball = Ball(screen_width, screen_height)

def pattern_1():
    return [Brick(col * 80 + 5, row * 25 + 50, 75, 20, BRICK_COLORS[row % 4]) for row in range(6) for col in range(10)]

def pattern_2():
    return [Brick((screen_width // 2) - (row * 40) + col * 80, row * 25 + 50, 75, 20, BRICK_COLORS[row % 4]) for row in range(6) for col in range(row + 1)]

def pattern_3():
    return [Brick(col * 80 + 5, row * 25 + 50, 75, 20, BRICK_COLORS[row % 4]) for row in range(6) for col in range(10) if (row + col) % 2 == 0]

def pattern_4():
    return [Brick(col * 80 + 5, row * 25 + 50, 75, 20, BRICK_COLORS[row % 4]) for row in range(6) for col in range(10) if row in [0, 5] or col in [0, 9]]

def pattern_5():
    return [Brick(col * 80 + 5, row * 25 + 50, 75, 20, BRICK_COLORS[row % 4]) for row in range(6) for col in range(row + 1)]

def pattern_6():
    return [Brick(col * 80 + row * 40 + 5, row * 25 + 50, 75, 20, BRICK_COLORS[row % 4]) for row in range(6) for col in range(10 - row)]

def pattern_7():
    return [Brick(col * 80 + 5, row * 25 + 50, 75, 20, BRICK_COLORS[row % 4]) for row in range(6) for col in range(10) if (row % 2 == 0 and col % 3 != 1) or (row % 2 == 1 and col % 3 == 1)]

def pattern_8():
    return [Brick(col * 80 + 5, row * 25 + 50, 75, 20, BRICK_COLORS[row % 4]) for row in range(6) for col in range(10) if col % 2 == 0]

def pattern_9():
    return [Brick(col * 80 + 5, row * 25 + 50, 75, 20, BRICK_COLORS[row % 4]) for row in range(6) if row % 2 == 0 for col in range(10)]

def pattern_10():
    return [Brick(random.randint(0, 9) * 80 + 5, random.randint(0, 5) * 25 + 50, 75, 20, random.choice(BRICK_COLORS)) for _ in range(30)]

levels = [pattern_1, pattern_2, pattern_3, pattern_4, pattern_5,
          pattern_6, pattern_7, pattern_8, pattern_9, pattern_10]

current_level, chosen_level = 0, 0
bricks = []

power_ups, lasers, particles, fireworks = [], [], [], []
game_state = 'title_screen'
score, lives = 0, 3
display_message, message_timer, firework_timer = "", 0, 0

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
                    ball.reset()
                    score, lives = 0, 3
                    power_ups.clear(); lasers.clear(); particles.clear(); fireworks.clear()
                    game_state = 'playing'
                elif event.key == pygame.K_0:  # Level 10
                    chosen_level = 9
                    current_level = chosen_level
                    bricks = levels[current_level]()
                    paddle.reset()
                    ball.reset()
                    score, lives = 0, 3
                    power_ups.clear(); lasers.clear(); particles.clear(); fireworks.clear()
                    game_state = 'playing'

            elif game_state in ['game_over', 'you_win']:
                if event.key == pygame.K_SPACE:
                    game_state = 'title_screen'

            elif game_state == 'playing':
                if event.key == pygame.K_f and paddle.has_laser:
                    lasers.append(Laser(paddle.rect.centerx - 30, paddle.rect.top))
                    lasers.append(Laser(paddle.rect.centerx + 30, paddle.rect.top))
                    if not mute: laser_sound.play()
                if event.key == pygame.K_m:
                    mute = not mute
                if ball.is_glued and event.key == pygame.K_SPACE:
                    ball.is_glued = False

    screen.fill(BG_COLOR)

    if game_state == 'title_screen':
        title_surface = title_font.render("ARKANOID", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(screen_width / 2, screen_height / 2 - 50))
        screen.blit(title_surface, title_rect)
        start_surface = game_font.render("Press SPACE to Start", True, (255, 255, 255))
        start_rect = start_surface.get_rect(center=(screen_width / 2, screen_height / 2 + 20))
        screen.blit(start_surface, start_rect)
        mute_surface = message_font.render("Press M to Mute/Unmute in-game", True, (255, 255, 255))
        mute_rect = mute_surface.get_rect(center=(screen_width / 2, screen_height / 2 + 60))
        screen.blit(mute_surface, mute_rect)

    elif game_state == 'level_select':
        select_surface = title_font.render("Select Level (1-9 or 0 for 10)", True, (255, 255, 255))
        select_rect = select_surface.get_rect(center=(screen_width / 2, screen_height / 2 - 100))
        screen.blit(select_surface, select_rect)

    elif game_state == 'playing':
        paddle.update()
        keys = pygame.key.get_pressed()
        ball_status, collision_object = ball.update(paddle, keys[pygame.K_SPACE])

        if ball_status == 'lost':
            lives -= 1
            if lives <= 0:
                game_state = 'game_over'
                if not mute: game_over_sound.play()
            else:
                ball.reset()
                paddle.reset()
        elif collision_object in ['wall', 'paddle']:
            if not mute: bounce_sound.play()
            for _ in range(5):
                particles.append(Particle(ball.rect.centerx, ball.rect.centery, (255, 255, 0), 1, 3, 1, 3, 0))

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
                                             random.choice(['grow', 'laser', 'glue', 'slow'])))
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
                    ball.activate_power_up(power_up.type)
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

        paddle.draw(screen)
        ball.draw(screen)
        for brick in bricks:
            brick.draw(screen)
        for power_up in power_ups:
            power_up.draw(screen)
        for laser in lasers:
            laser.draw(screen)

        score_text = game_font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        lives_text = game_font.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(lives_text, (screen_width - lives_text.get_width() - 10, 10))
        level_text = game_font.render(f"Level: {current_level + 1}", True, (255, 255, 255))
        screen.blit(level_text, (screen_width // 2 - 50, 10))

        if mute:
            muted_text = message_font.render("MUTED", True, (255, 0, 0))
            screen.blit(
                muted_text,
                (screen_width - muted_text.get_width() - 10, screen_height - muted_text.get_height() - 10)
            )

    elif game_state in ['game_over', 'you_win']:
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

        message = "GAME OVER" if game_state == 'game_over' else "YOU WIN!"
        text_surface = game_font.render(message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(screen_width / 2, screen_height / 2 - 20))
        screen.blit(text_surface, text_rect)
        restart_surface = game_font.render("Press SPACE to return to Title", True, (255, 255, 255))
        restart_rect = restart_surface.get_rect(center=(screen_width / 2, screen_height / 2 + 30))
        screen.blit(restart_surface, restart_rect)

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
