from random import choice
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

ALL_CELLS = {(x * GRID_SIZE, y * GRID_SIZE) for x in range(GRID_WIDTH - 1)
             for y in (range(GRID_HEIGHT - 1))}

TURNS = {(UP, pg.K_LEFT): LEFT,
         (UP, pg.K_RIGHT): RIGHT,
         (DOWN, pg.K_LEFT): LEFT,
         (DOWN, pg.K_RIGHT): RIGHT,
         (LEFT, pg.K_UP): UP,
         (LEFT, pg.K_DOWN): DOWN,
         (RIGHT, pg.K_UP): UP,
         (RIGHT, pg.K_DOWN): DOWN
         }


class GameObject:
    """Родительский класс, от которого наследуются игровые объекты."""

    def __init__(self, body_color=None):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw_cell(self, position, body_color=None):
        """Метод отрисовки яблока, головы змеи и затирания её хвоста."""
        if body_color is None:
            body_color = self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        if body_color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Метод, предназначенный для переопределения в дочерних классах."""
        raise NotImplementedError(
            f'Метод draw не определён в классе {type(self).__name__}'
        )


class Apple(GameObject):
    """Дочерний класс, описывающий игровой объект - яблоко."""

    def __init__(self, body_color=APPLE_COLOR, positions=[]):
        super().__init__(body_color)
        self.randomize_position(positions)

    def randomize_position(self, positions):
        """Метод, предназначенный для генерации случайной позиции яблока."""
        if ALL_CELLS - set(positions):
            self.position = choice(tuple(ALL_CELLS - set(positions)))
        else:
            # Объявил бы в глобальной области видимости,
            # но тесты не разрешают переносить pg.init().
            font = pg.font.Font('freesansbold.ttf', 32)
            text_surface = font.render('Победа!', True, (0, 0, 0))
            screen.blit(text_surface, dest=(200, 208))

    def draw(self):
        """Метод отрисовки яблока на игровом поле."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Дочерний класс, описывающий игровой объект - змейку."""

    def __init__(self, body_color=SNAKE_COLOR):
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
        self.positions.insert(0, ((head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
                                  (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT))
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Метод, предназначенный для отрисовки тела, головы и затирания
        последнего сегмента змейки на игровом поле.
        """
        self.draw_cell(self.get_head_position())
        if self.last and self.last != self.get_head_position():
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


def handle_keys(snake, apple):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():

        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            snake.direction = TURNS.get((snake.direction, event.key),
                                        snake.direction)
            if event.key == pg.K_r:
                screen.fill(BOARD_BACKGROUND_COLOR)
                snake.reset()
                apple.randomize_position(snake.positions)
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit


def main():
    """Входная точка в программу. Основной игровой цикл."""
    pg.init()

    snake = Snake()
    apple = Apple(positions=snake.positions)
    record = 1
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake, apple)
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
            record = max(record, snake.length)
        elif snake.get_head_position() in snake.positions[4:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(snake.positions)
        pg.display.set_caption(
            f'Exit -> esc. Record = {record}. Current = {snake.length}'
        )
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
