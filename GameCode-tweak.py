import pygame
import sys
import random

SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1000
SCREEN_TITLE = "Dziki wunsz"
WHITE = (255, 255, 255, 0)
BLUE = (52, 110, 157)
YELLOW = (255, 222, 86)

clock = pygame.time.Clock()


class Game:
    tick_rate = 10
    is_game_over = False

    def __init__(self, height, width, title):

        self.height = height
        self.width = width
        self.title = title

        self.SCREEN = pygame.display.set_mode(size=(width, height))
        self.SCREEN.fill(BLUE)
        pygame.display.set_caption(SCREEN_TITLE)

    def start(self, screen, game="Dziki wąż", bgcol=BLUE, fgcol=YELLOW):
        self.SCREEN.fill(BLUE)
        pygame.display.update()
        font = pygame.font.Font(None, 40)
        msg = "Naciśnij dowolny klawisz, żeby zacząć grę " + game
        text = font.render(msg, 1, fgcol)
        text_pos = text.get_rect()
        text_pos.center = screen.get_rect().center
        screen.blit(text, text_pos)
        pygame.display.update(text_pos)
        pygame.event.pump()
        event = pygame.event.wait()
        while not event.type == pygame.KEYDOWN:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(bgcol, text_pos)
        self.SCREEN.fill(BLUE)
        pygame.display.update(text_pos)

    def lose(self, screen, score, fgcol=YELLOW):
        name = ""
        font = pygame.font.Font(None, 64)
        text1 = font.render("KONIEC GRY", 1, fgcol)
        scr = screen.get_rect().center
        textpos1 = text1.get_rect()
        textpos1.center = scr
        screen.blit(text1, textpos1)
        pygame.display.update()
        pygame.time.wait(2000)

        self.SCREEN.fill(BLUE)
        pygame.display.update()

        text2 = font.render("Podaj swoje imię i naciśnij ENTER ", 1, fgcol)
        scr = screen.get_rect().center
        textpos2 = text2.get_rect()
        textpos2.center = scr
        screen.blit(text2, textpos2)
        pygame.display.update()
        pygame.time.wait(2000)

        while True:
            for evt in pygame.event.get():
                if evt.type == pygame.KEYDOWN:
                    if evt.unicode.isalpha():
                        name += evt.unicode
                    elif evt.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif evt.key == pygame.K_RETURN:
                        leaderboard = open("leaderboard.csv", "a")
                        leaderboard.write((str(score) + "," + name + "\n"))
                        leaderboard.close()
                        self.run_game()
                elif evt.type == pygame.QUIT:
                    return
            screen.fill(BLUE)
            block = font.render(name, True, (255, 255, 255))
            rect = block.get_rect()
            rect.center = screen.get_rect().center
            screen.blit(block, rect)
            pygame.display.flip()

            # self.run_game()
        # pygame.display.update()

    def run_game(self):
        points = 0
        self.start(self.SCREEN)
        is_game_over = False
        # is_game_over = True
        pygame.display.update()


        snake = Snake("headm.png", 500, 500, 50, 50)

        yum = Yum("mousem.png", random.randint(0, 900), random.randint(0, 900), 50, 50)

        def yum_disappear():
            yum.x_pos = 2000
            yum.y_pos = 2000

        def yum_reappear():
            yum.x_pos = random.randint(0, 900)
            yum.y_pos = random.randint(0, 900)

        reappearing = pygame.USEREVENT + 1
        pygame.time.set_timer(reappearing, 5000)

        while not is_game_over:
            snake.update()
            snake.x_positions.insert(0, snake.x_pos)
            snake.y_positions.insert(0, snake.y_pos)

            segments = []
            for a in range(1, snake.length + 1):
                # segments.insert(0, Segment("seg.png", snake.x_positions[a], snake.y_positions[a], 100, 100))
                segments.insert(0, Segment("segm.png", snake.x_positions[a], snake.y_positions[a], 50, 50))

            if snake.collision(yum):
                yum_disappear()
                snake.length += 1
                points += 100

            for s in segments:
                if s.collision(snake):
                    is_game_over = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_game_over = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        snake.to_right()

                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        snake.to_left()

                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        snake.to_down()

                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        snake.to_up()

                elif event.type == reappearing:
                    if yum.y_pos == 2000:
                        yum_reappear()

            self.SCREEN.fill(BLUE)
            snake.draw(self.SCREEN)
            yum.draw(self.SCREEN)
            for s in segments:
                s.draw(self.SCREEN)
            font = pygame.font.Font(None, 36)
            text = font.render("Wynik: " + str(points), 1, WHITE)
            self.SCREEN.blit(text, (0, 0))
            pygame.display.update()
            clock.tick(self.tick_rate)

        self.lose(self.SCREEN, points)


class GameObject:
    def __init__(self, image_path, x, y, height, width):
        self.image = pygame.image.load(image_path)

        self.x_pos = x
        self.y_pos = y
        self.height = height
        self.width = width

    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))


class Snake(GameObject):
    # SPEED = 100
    SPEED = 50
    direction = 0
    change_to = direction
    length = 1
    x_positions = [100, ]
    y_positions = [500, ]

    if len(x_positions) > 30:
        x_positions.pop(-1)
    if len(y_positions) > 30:
        y_positions.pop(-1)

    def update(self):
        if self.change_to == 2 and self.direction != 3:
            self.direction = 2
        if self.change_to == 3 and self.direction != 2:
            self.direction = 3
        if self.change_to == 1 and self.direction != 0:
            self.direction = 1
        if self.change_to == 0 and self.direction != 1:
            self.direction = 0

        if self.direction == 0:
            self.x_pos = self.x_pos + self.SPEED
        if self.direction == 1:
            self.x_pos = self.x_pos - self.SPEED
        if self.direction == 2:
            self.y_pos = self.y_pos - self.SPEED
        if self.direction == 3:
            self.y_pos = self.y_pos + self.SPEED

        if self.x_pos > 950:
            self.x_pos = 0
        elif self.x_pos < 0:
            self.x_pos = 950
        if self.y_pos > 950:
            self.y_pos = 0
        elif self.y_pos < 0:
            self.y_pos = 950

    def to_right(self):
        self.change_to = 0

    def to_left(self):
        self.change_to = 1

    def to_up(self):
        self.change_to = 2

    def to_down(self):
        self.change_to = 3

    def collision(self, *yums):
        for _ in yums:
            if self.x_pos > _.x_pos + _.width:
                return False
            elif self.x_pos + self.width < _.x_pos:
                return False

            if self.y_pos > _.y_pos + _.height:
                return False
            elif self.y_pos + self.height < _.y_pos:
                return False

            return True


class Segment(GameObject):

    def collision(self, *heads):
        for _ in heads:
            if self.x_pos == _.x_pos and self.y_pos == _.y_pos:
                return True

            return False


class Yum(GameObject):
    pass


pygame.init()

new_game = Game(SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_TITLE)
new_game.run_game()

pygame.quit()
quit()
