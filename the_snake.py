from random import choice, randint

import pygame as pg


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (160, 160, 160)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (220, 0, 0)
SNAKE_COLOR = (0, 156, 0)
SPEED = 20
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pg.time.Clock()


class GameObject:
    """Родительский класс, от которого наследуются игровые объекты."""

    def __init__(self, body_color=None):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw_cell(self, position, body_color=None, draw_border=None):
        """Метод отрисовки яблока, головы змеи и затирания её хвоста."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        if body_color:
            pg.draw.rect(screen, body_color, rect)
        else:
            pg.draw.rect(screen, self.body_color, rect)
        if draw_border:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Метод, предназначенный для переопределения в дочерних классах."""
        raise NotImplementedError(
            f'Метод draw не определён в классе {self.__class__.__name__}'
        )


class Apple(GameObject):
    """Дочерний класс, описывающий игровой объект - яблоко."""

    def __init__(self, body_color=None, positions=[]):
        super().__init__(body_color)
        self.randomize_position(positions)

    def randomize_position(self, positions):
        """Метод, предназначенный для генерации случайной позиции яблока."""
        while True:
            apple_position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                              randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if apple_position not in positions:
                self.position = apple_position
                break

    def draw(self):
        """Метод отрисовки яблока на игровом поле."""
        self.draw_cell(self.position, APPLE_COLOR, True)


class Snake(GameObject):
    """Дочерний класс, описывающий игровой объект - змейку."""

    def __init__(self, body_color=None):
        super().__init__(body_color)
        self.reset()
        self.direction = RIGHT  # Начальное направление по ТЗ.

    def update_direction(self, new_direction):
        """Метод, предназначенный для обновления направления."""
        if new_direction:
            self.direction = new_direction

    def move(self):
        """Метод, предназначенный для передвижения змейки."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        next_x, next_y = head_x + dx * GRID_SIZE, head_y + dy * GRID_SIZE
        if next_x % SCREEN_WIDTH >= 0 and next_y % SCREEN_HEIGHT >= 0:
            next_position = (next_x % SCREEN_WIDTH, next_y % SCREEN_HEIGHT)
        self.positions.insert(0, next_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Метод, предназначенный для отрисовки тела, головы и затирания
        последнего сегмента змейки на игровом поле.
        """
        self.draw_cell(self.get_head_position(), SNAKE_COLOR, True)
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Метод, возвращающий коордианты первого сегмента змейки"""
        return self.positions[0]

    def reset(self):
        """Метод, предназначенный для сброса змейки в исходное состоятие."""
        self.length = 1
        self.positions = [self.position]
        self.last = None
        self.direction = choice((UP, DOWN, LEFT, RIGHT))
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(snake, apple):
    """Функция обработки действий пользователя."""
    DIRECTIONS = {(UP, pg.K_LEFT): LEFT,
                  (UP, pg.K_RIGHT): RIGHT,
                  (DOWN, pg.K_LEFT): LEFT,
                  (DOWN, pg.K_RIGHT): RIGHT,
                  (LEFT, pg.K_UP): UP,
                  (LEFT, pg.K_DOWN): DOWN,
                  (RIGHT, pg.K_UP): UP,
                  (RIGHT, pg.K_DOWN): DOWN
                  }

    for event in pg.event.get():

        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            new_direction = DIRECTIONS.get((snake.direction, event.key),
                                           snake.direction)
            snake.direction = new_direction
            if event.key == pg.K_r:
                snake.reset()
                apple.randomize_position(snake.positions)
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit


def main():
    """Входная точка в программу. Основной игровой цикл."""
    pg.init()

    snake = Snake(SNAKE_COLOR)
    apple = Apple(APPLE_COLOR, snake.positions)
    record = 1
    pg.display.set_caption(
        f'Exit -> esc. Record = {record}. Current = {snake.length}'
    )

    while True:
        clock.tick(SPEED)
        handle_keys(snake, apple)
        snake.move()
        ate_apple = False
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
            ate_apple = True
            if snake.length > record:
                record = snake.length
        if not ate_apple and snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            apple.randomize_position(snake.positions)
        try:
            snake.draw()
        except NotImplementedError as e:
            print(e)
            break
        try:
            apple.draw()
        except NotImplementedError as e:
            print(e)
            break
        pg.display.update()


if __name__ == '__main__':
    main()
