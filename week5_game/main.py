"""
Изначально у вас есть HP. Когда игрок бестолку бродит по полю, его HP и Score понемногу падает.
Сначала HP и EXP можно набирать за счет магии союзников и ловлей мышей.
К рыцарям, дракону, змее подходите с осторожностью, они отнимают много HP, но прибавляют больше опыта или очков,
и наоборот, в зависимости от их вида.
Особенно опасайтесь молний. Молния губит слабого героя и помогает сильному.
Серьезные фичи брать можно, но только когда есть HP.
Если HP падает до 0, игра заканчивается.
Удачи!
"""

import pygame
import os
import Objects
import ScreenEngine as SE
import Logic
import Service

HEIGHT = 800
WIDTH = 1200
SCREEN_DIM = (WIDTH, HEIGHT)

pygame.init()
gameDisplay = pygame.display.set_mode(SCREEN_DIM)
pygame.display.set_caption("Knight in Underworld!")
KEYBOARD_CONTROL = True

pygame.mixer.music.load('SuperMario.mp3')
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play()


if not KEYBOARD_CONTROL:
    import numpy as np
    answer = np.zeros(4, dtype=float)

base_stats = {
    "strength": 20,
    "endurance": 20,
    "intelligence": 5,
    "luck": 5
}


def create_game(sprite_size, is_new):
    global hero, engine, drawer, iteration
    if is_new:
        hero = Objects.Hero(base_stats, Service.create_sprite(
            os.path.join("texture", "Hero.png"), sprite_size))
        engine = Logic.GameEngine()
        Service.service_init(sprite_size)
        Service.reload_game(engine, hero)
        drawer = SE.GameSurface((1200, 800), pygame.SRCALPHA, (0, 680),
                                    SE.ProgressBar((1200, 220), (850, 0),
                                                   SE.InfoWindow((350, 800), (0, 0),
                                                                 SE.HelpWindow((700, 500), pygame.SRCALPHA, (0, 0),
                                                                        SE.GameOver((850, 680), pygame.SRCALPHA, (0, 0),
                                                                                SE.ScreenHandle((0, 0)))))))
    else:
        engine.sprite_size = sprite_size
        hero.sprite = Service.create_sprite(
            os.path.join("texture", "Hero.png"), sprite_size)
        Service.service_init(sprite_size, False)

    Logic.GameEngine.sprite_size = sprite_size

    drawer.connect_engine(engine)

    iteration = 0


size = 50
create_game(size, True)

while engine.working:

    if KEYBOARD_CONTROL:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                engine.working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    engine.show_help = not engine.show_help
                    if engine.show_help:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.play()

                if event.key == pygame.K_KP_PLUS:
                    size = size + 1
                    create_game(size, False)
                if event.key == pygame.K_KP_MINUS:
                    size = size - 1
                    create_game(size, False)
                if event.key == pygame.K_r:
                    create_game(size, True)
                if event.key == pygame.K_ESCAPE:
                    engine.working = False
                if engine.game_process:
                    if event.key == pygame.K_UP:
                        engine.move_up()
                        iteration += 1
                    elif event.key == pygame.K_DOWN:
                        engine.move_down()
                        iteration += 1
                    elif event.key == pygame.K_LEFT:
                        engine.move_left()
                        iteration += 1
                    elif event.key == pygame.K_RIGHT:
                        engine.move_right()
                        iteration += 1
                else:
                    if event.key == pygame.K_RETURN:
                        create_game()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                engine.working = False
        if engine.game_process:
            actions = [
                engine.move_right,
                engine.move_left,
                engine.move_up,
                engine.move_down,
            ]
            answer = np.random.randint(0, 100, 4)
            prev_score = engine.score
            move = actions[np.argmax(answer)]()
            state = pygame.surfarray.array3d(gameDisplay)
            reward = engine.score - prev_score
            print(reward)
        else:
            create_game()

    gameDisplay.blit(drawer, (0, 0))
    drawer.draw(gameDisplay)

    pygame.display.update()

pygame.display.quit()
pygame.quit()
exit(0)
