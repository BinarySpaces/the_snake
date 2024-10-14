from random import choice, randint
import pygame


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 15

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Родительский класс, от которого наследуются игровые объекты."""

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Метод, предназначенный для переопределения в дочерних классах."""
        pass


class Apple(GameObject):
    """Дочерний класс, описывающий игровой объект - яблоко."""

    def __init__(self, snake_positions=[]):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.snake_positions = snake_positions
        self.position = self.randomize_position()

    def randomize_position(self):
        """Метод."""
        while True:
            apple_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            apple_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            apple_position = (apple_x, apple_y)
            if apple_position not in self.snake_positions:
                return apple_position

    def draw(self):
        """Метод отрисовки яблока на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Дочерний класс, описывающий игровой объект - змейку."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод, предназначенный для обновления направления."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, предназначенный для передвижения змейки."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        next_x, next_y = head_x + dx * GRID_SIZE, head_y + dy * GRID_SIZE
        next_position = (next_x, next_y)
        if next_x == SCREEN_WIDTH or next_x < 0:
            next_position = (next_x % SCREEN_WIDTH, next_y)
        elif next_y == SCREEN_HEIGHT or next_y < 0:
            next_position = (next_x, next_y % SCREEN_HEIGHT)
        self.last = self.positions[-1]
        if len(self.positions) > self.length:
            self.positions.pop()
        self.positions.insert(0, next_position)

    def draw(self):
        """Метод, предназначенный для отрисовки тела, головы и затирания
        последнего сегмента змейки на игровом поле.
        """
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод, возвращающий коордианты первого сегмента змейки"""
        return self.positions[0]

    def reset(self):
        """Метод, возвращающий змейку в исходное состоятие."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None


def handle_keys(game_object, resetted_apple):
    """Функция обработки действий пользователя.
    Добавил полезный функционал - при нажатии клавиши 'r' происходит сброс и
    задаётся новое положение для яблока как и при стандартном сбросе.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pygame.K_r:
                game_object.reset()
                resetted_apple.position = resetted_apple.randomize_position()


def main():
    """Входная точка в программу."""
    pygame.init()

    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake, apple)
        snake.update_direction()
        snake.move()
        snake.draw()
        apple.draw()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
        if apple.position in snake.positions:
            apple.position = apple.randomize_position()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.position = apple.randomize_position()
        pygame.display.update()
        screen.fill(BOARD_BACKGROUND_COLOR)


if __name__ == '__main__':
    main()
