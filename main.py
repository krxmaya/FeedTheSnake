import sys, pygame, random, time
from pygame.math import Vector2


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_topright.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_topleft.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_bottomright.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bottomleft.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('Audio/apple_crunch.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        grass_color = color_dark_green

        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self, score=None):
        old = len(self.snake.body) - 3
        if score is None:
            score = 0
            old = old + score
            score_text = str(old)
        else:
            old = old + score
            score_text = str(old)

        score_surface = small_font.render(score_text, True, color_white)
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6,
                              apple_rect.height)

        pygame.draw.rect(screen, color_dark_green, bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, color_white, bg_rect, 2)

    def pause(self):
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()

            screen.fill(color_dark_green)
            text_medium("Paused", color_white, whole - 470, whole - 80)
            text_medium("Press c to continue", color_white, whole - 570, whole - 45)
            text_medium("Press q to quit", color_white, whole - 530, whole - 10)
            pygame.display.update()
            clock.tick(5)

    def mission(self):
        if len(self.snake.body) - 3 < 50:
            text_small("Task: Feed the snake correct information about", color_white, whole - 790, whole - 790)
            text_small("Password Security.", color_white, whole - 790, whole - 760)
        elif len(self.snake.body) - 3 == 50:
            text_small('Congratulations! You successfully completed the task.', color_white, whole - 790, whole - 790)

    def notif(self):
        if (len(self.snake.body) - 3) % 3 == 0 and (len(self.snake.body) - 3) != 0:
            text_medium('Press SPACE to complete task.', (220, 20, 60), whole - 700, whole - 90)

    def pass_one(self):
        a = True
        while a:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        a = False
                    elif event.key == pygame.K_t:
                        self.game_over()
                        a = False

            pop_up_box(whole - 650, whole - 600, 500, 400, 'Is this a strong password?')
            button_one(whole - 720, whole - 400)
            button_two(whole - 480, whole - 400)
            task_one_key(re_pass_a, whole - 650, whole - 500)
            pygame.display.update()
            clock.tick(15)

    def pass_two(self):
        b = True
        while b:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.game_over()
                        b = False
                    elif event.key == pygame.K_t:
                        b = False

            pop_up_box(whole - 650, whole - 600, 500, 400, 'Is this a strong password?')
            button_one(whole - 720, whole - 400)
            button_two(whole - 480, whole - 400)
            task_one_key(pass_b, whole - 700, whole - 500)
            pygame.display.update()
            clock.tick(15)

    def pass_three(self):
        c = True
        while c:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.game_over()
                        c = False
                    elif event.key == pygame.K_t:
                        c = False

            pop_up_box(whole - 650, whole - 600, 500, 400, 'Is this a strong password?')
            button_one(whole - 720, whole - 400)
            button_two(whole - 480, whole - 400)
            task_one_key(pass_c, whole - 700, whole - 500)
            pygame.display.update()
            clock.tick(15)

    def pass_four(self):
        d = True
        while d:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.game_over()
                        d = False
                    elif event.key == pygame.K_t:
                        d = False

            pop_up_box(whole - 650, whole - 600, 500, 400, 'Is this a strong password?')
            button_one(whole - 720, whole - 400)
            button_two(whole - 480, whole - 400)
            task_one_key(pass_d, whole - 700, whole - 500)
            pygame.display.update()
            clock.tick(15)

    def pass_five(self):
        e = True
        while e:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        e = False
                    elif event.key == pygame.K_t:
                        self.game_over()
                        e = False

            pop_up_box(whole - 650, whole - 600, 500, 400, 'Is this a strong password?')
            button_one(whole - 720, whole - 400)
            button_two(whole - 480, whole - 400)
            task_one_key(pass_e, whole - 700, whole - 500)
            pygame.display.update()
            clock.tick(15)

    def pass_six(self):
        f = True
        while f:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        f = False
                    elif event.key == pygame.K_t:
                        self.game_over()
                        f = False

            pop_up_box(whole - 650, whole - 600, 500, 400, 'Is this a strong password?')
            button_one(whole - 720, whole - 400)
            button_two(whole - 480, whole - 400)
            task_one_key(re_pass_f, whole - 650, whole - 480)
            pygame.display.update()
            clock.tick(15)

    def tf_one(self):
        g = True
        while g:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        g = False
                    elif event.key == pygame.K_t:
                        self.game_over()
                        g = False

            pop_up_box(whole - 650, whole - 600, 500, 400, 'TRUE or FALSE')
            button_three(whole - 720, whole - 400)
            button_four(whole - 480, whole - 400)
            task_one_key(tf_a, whole - 650, whole - 550)
            pygame.display.update()
            clock.tick(15)

    def tf_two(self):
        h = True
        while h:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.game_over()
                        h = False
                    elif event.key == pygame.K_t:
                        h = False

            pop_up_box(whole - 650, whole - 600, 500, 400, 'TRUE or FALSE')
            button_three(whole - 720, whole - 400)
            button_four(whole - 480, whole - 400)
            task_one_key(tf_b, whole - 650, whole - 550)
            pygame.display.update()
            clock.tick(15)

    def tf_three(self):
        i = True
        while i:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.game_over()
                        i = False
                    elif event.key == pygame.K_t:
                        i = False

            pop_up_box(whole - 650, whole - 600, 500, 400, 'TRUE or FALSE')
            button_three(whole - 720, whole - 400)
            button_four(whole - 480, whole - 400)
            task_one_key(tf_c, whole - 650, whole - 550)
            pygame.display.update()
            clock.tick(15)

    def tf_four(self):
        j = True
        while j:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        j = False
                    elif event.key == pygame.K_t:
                        self.game_over()
                        j = False

            pop_up_box(whole - 650, whole - 600, 500, 400, 'TRUE or FALSE')
            button_three(whole - 720, whole - 400)
            button_four(whole - 480, whole - 400)
            task_one_key(tf_d, whole - 650, whole - 550)
            pygame.display.update()
            clock.tick(15)

    def tf_five(self):
        k = True
        while k:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        k = False
                    elif event.key == pygame.K_t:
                        self.game_over()
                        k = False

            pop_up_box(whole - 650, whole - 600, 500, 400, 'TRUE or FALSE')
            button_three(whole - 720, whole - 400)
            button_four(whole - 480, whole - 400)
            task_one_key(tf_e, whole - 650, whole - 550)
            pygame.display.update()
            clock.tick(15)

    def sc_one(self):
        l = True
        while l:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.game_over()
                        l = False
                    elif event.key == pygame.K_t:
                        l = False
            pop_up_box(whole - 650, whole - 600, 500, 400, '')
            task_one_key(sc_a, whole - 655, whole - 700)
            pygame.display.update()
            clock.tick(15)

    def sc_two(self):
        m = True
        while m:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        m = False
                    elif event.key == pygame.K_t:
                        m = False
                        self.game_over()
            pop_up_box(whole - 650, whole - 600, 500, 400, '')
            task_one_key(sc_b, whole - 655, whole - 700)
            pygame.display.update()
            clock.tick(15)

    def sc_three(self):
        n = True
        while n:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        n = False
                    elif event.key == pygame.K_t:
                        n = False
                        self.game_over()
            pop_up_box(whole - 650, whole - 600, 500, 400, '')
            task_one_key(re_sc_c, whole - 650, whole - 680)
            pygame.display.update()
            clock.tick(15)

    def sc_four(self):
        o = True
        while o:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.game_over()
                        o = False
                    elif event.key == pygame.K_t:
                        o = False
            pop_up_box(whole - 650, whole - 600, 500, 400, '')
            task_one_key(sc_d, whole - 650, whole - 750)
            pygame.display.update()
            clock.tick(15)

    def sc_five(self):
        p = True
        while p:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        p = False
                    elif event.key == pygame.K_t:
                        p = False
                        self.game_over()
            pop_up_box(whole - 650, whole - 600, 500, 400, '')
            task_one_key(sc_e, whole - 650, whole - 720)
            pygame.display.update()
            clock.tick(15)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 20
whole = cell_size * cell_number
screen = pygame.display.set_mode((whole, whole))
clock = pygame.time.Clock()

# game image elements
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
small_font = pygame.font.Font('milk_nice.ttf', 25)
medium_font = pygame.font.Font('milk_nice.ttf', 35)
large_font = pygame.font.Font('milk_nice.ttf', 55)
color_white = (255, 255, 255)
color_light_green = (154, 225, 123)
color_dark_green = (107, 186, 98)
color_blue = (66, 71, 109)

# buttons
button_one = pygame.image.load('Graphics/btn_one.png').convert_alpha()
button_throw = pygame.transform.scale(button_one, (400, 200))
button_two = pygame.image.load('Graphics/btn_two.png').convert_alpha()
button_feed = pygame.transform.scale(button_two, (400, 200))

button_three = pygame.image.load('Graphics/btn_three.png').convert_alpha()
button_true = pygame.transform.scale(button_three, (400, 200))
button_four = pygame.image.load('Graphics/btn_four.png').convert_alpha()
button_false = pygame.transform.scale(button_four, (400, 200))

# texts
pass_a = pygame.image.load('Graphics/pass_a.png').convert_alpha()
re_pass_a = pygame.transform.scale(pass_a, (500, 100))
pass_b = pygame.image.load('Graphics/pass_b.png').convert_alpha()
pass_c = pygame.image.load('Graphics/pass_c.png').convert_alpha()
pass_d = pygame.image.load('Graphics/pass_d.png').convert_alpha()
pass_e = pygame.image.load('Graphics/pass_e.png').convert_alpha()
pass_f = pygame.image.load('Graphics/pass_f.png').convert_alpha()
re_pass_f = pygame.transform.scale(pass_f, (500, 80))

tf_a = pygame.image.load('Graphics/tf_a.png').convert_alpha()
tf_b = pygame.image.load('Graphics/tf_b.png').convert_alpha()
tf_c = pygame.image.load('Graphics/tf_c.png').convert_alpha()
tf_d = pygame.image.load('Graphics/tf_d.png').convert_alpha()
tf_e = pygame.image.load('Graphics/tf_e.png').convert_alpha()

sc_a = pygame.image.load('Graphics/sc_a.png').convert_alpha()
sc_b = pygame.image.load('Graphics/sc_b.png').convert_alpha()
sc_c = pygame.image.load('Graphics/sc_c.png').convert_alpha()
re_sc_c = pygame.transform.scale(sc_c, (480, 580))
sc_d = pygame.image.load('Graphics/sc_d.png').convert_alpha()
sc_e = pygame.image.load('Graphics/sc_e.png').convert_alpha()

# help
help_a = pygame.image.load('Graphics/help_a.png').convert_alpha()
help_b = pygame.image.load('Graphics/help_b.png').convert_alpha()

pygame.display.set_caption('Feed The Snake')
icon = pygame.image.load('Graphics/snake_icon.png')
pygame.display.set_icon(icon)
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)


def text_small(msg, color, x, y):
    screen_text = small_font.render(msg, True, color)
    screen.blit(screen_text, (x, y))

def text_medium(msg, color, x, y):
    screen_text = medium_font.render(msg, True, color)
    screen.blit(screen_text, (x, y))

def text_large(msg, color, x, y):
    screen_text = large_font.render(msg, True, color)
    screen.blit(screen_text, (x, y))


def pop_up_box(x_pos, y_pos, w, h, text):
    popup = pygame.Rect(x_pos, y_pos, w, h)
    popup_text = small_font.render(text, True, color_white)

    pygame.draw.rect(screen, color_dark_green, popup)
    text_rect = popup_text.get_rect(center=(whole - 450, whole - 550))
    screen.blit(popup_text, text_rect)

def task_one_key(image, x, y):
    pass_rect = pygame.Rect(x, y, 400, 200)
    screen.blit(image, pass_rect)


def button_one(x, y):
    btn_one_rect = pygame.Rect(x, y, 400, 200)
    screen.blit(button_throw, btn_one_rect)

def button_two(x, y):
    btn_one_rect = pygame.Rect(x, y, 400, 200)
    screen.blit(button_feed, btn_one_rect)

def button_three(x, y):
    btn_one_rect = pygame.Rect(x, y, 400, 200)
    screen.blit(button_true, btn_one_rect)

def button_four(x, y):
    btn_one_rect = pygame.Rect(x, y, 400, 200)
    screen.blit(button_false, btn_one_rect)


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
                if event.key == pygame.K_h:
                    help_one()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        screen.fill(color_dark_green)
        text_large("Feed the Snake", color_white, whole - 600, whole - 700)
        text_medium("1. Use arrow keys to control the snake.", color_white, whole - 750, whole - 550)
        text_medium("2. Feed red apples to the snake.", color_white, whole - 750, whole - 450)
        text_medium("3. If answer in question is wrong, the ", color_white, whole - 750, whole - 350)
        text_medium("   game restarts. ", color_white, whole - 750, whole - 310)
        text_medium("4. Reach 50 points to win game.", color_white, whole - 750, whole - 250)
        text_small("Press SPACE to start", color_white, whole - 550, whole - 80)
        text_small("Press H for info about password security", color_white, whole - 650, whole - 50)

        pygame.display.update()
        clock.tick(15)

def help_one():
    h_a = True
    while h_a:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    help_two()
                if event.key == pygame.K_BACKSPACE:
                    h_a = False
        screen.fill(color_dark_green)
        task_one_key(help_a, whole - 800, whole - 800)
        pygame.display.update()
        clock.tick(15)

def help_two():
    h_o = True
    while h_o:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    h_o = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        screen.fill(color_dark_green)
        task_one_key(help_b, whole - 800, whole - 800)
        pygame.display.update()
        clock.tick(15)


main_game = MAIN()


def game_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                elif event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                elif event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
                elif event.key == pygame.K_SPACE and len(main_game.snake.body)-3 == 3:
                    main_game.pass_one()
                elif event.key == pygame.K_SPACE and len(main_game.snake.body)-3 == 6:
                    main_game.pass_two()
                elif event.key == pygame.K_SPACE and len(main_game.snake.body)-3 == 9:
                    main_game.pass_three()
                elif event.key == pygame.K_SPACE and len(main_game.snake.body)-3 == 12:
                    main_game.pass_four()
                elif event.key == pygame.K_SPACE and len(main_game.snake.body)-3 == 15:
                    main_game.pass_five()
                elif event.key == pygame.K_SPACE and len(main_game.snake.body)-3 == 18:
                    main_game.pass_six()
                elif event.key == pygame.K_SPACE and len(main_game.snake.body)-3 == 21:
                    main_game.tf_one()
                elif event.key == pygame.K_SPACE and len(main_game.snake.body)-3 == 24:
                    main_game.tf_two()
                elif event.key == pygame.K_SPACE and len(main_game.snake.body)-3 == 27:
                    main_game.tf_three()
                elif event.key == pygame.K_SPACE and len(main_game.snake.body)-3 == 30:
                    main_game.tf_four()
                elif event.key == pygame.K_SPACE and len(main_game.snake.body)-3 == 33:
                    main_game.tf_five()
                elif event.key == pygame.K_SPACE and len(main_game.snake.body)-3 == 36:
                    main_game.sc_one()
                elif event.key == pygame.K_SPACE and len(main_game.snake.body)-3 == 39:
                    main_game.sc_two()
                elif event.key == pygame.K_SPACE and len(main_game.snake.body) - 3 == 42:
                    main_game.sc_three()
                elif event.key == pygame.K_SPACE and len(main_game.snake.body) - 3 == 45:
                    main_game.sc_four()
                elif event.key == pygame.K_SPACE and len(main_game.snake.body) - 3 == 48:
                    main_game.sc_five()
                elif event.key == pygame.K_p:
                    main_game.pause()
                #elif event.key == pygame.K_SPACE:


        screen.fill((116, 201, 107))
        main_game.draw_elements()
        main_game.mission()
        main_game.notif()
        pygame.display.update()
        clock.tick(60)


game_intro()
game_loop()
