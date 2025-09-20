import pytest
from src.main import Snake, Food, COLS, ROWS, WallCollision, SelfCollision

def test_snake_initial_length():
    snake = Snake(init_length=3)
    assert len(snake.body) == 3

def test_snake_head_starts_in_middle():
    snake = Snake(init_length=3)
    mid_x, mid_y = COLS // 2, ROWS // 2
    assert snake.head == (mid_x, mid_y)

def test_snake_moves_right():
    snake = Snake(init_length=3)
    old_head = snake.head
    new_head = snake.compute_next_head()
    snake.move_head(new_head)
    assert snake.head[0] == old_head[0] + 1
    assert snake.head[1] == old_head[1]

def test_snake_grows_when_grow_called():
    snake = Snake(init_length=3)
    snake.grow(2)
    snake.move_head((snake.head[0] + 1, snake.head[1]))  # move once
    assert len(snake.body) == 4
    snake.move_head((snake.head[0] + 1, snake.head[1]))  # move twice
    assert len(snake.body) == 5

def test_food_not_spawn_on_snake():
    snake = Snake(init_length=5)
    food = Food(snake.body)
    assert food.position not in snake.body
    x, y = food.position
    assert 0 <= x < COLS
    assert 0 <= y < ROWS

def test_snake_reset():
    snake = Snake(init_length=3)
    snake.grow(2)
    snake.move_head((snake.head[0] + 1, snake.head[1]))
    snake.reset()
    assert len(snake.body) == 3
    assert snake.head == (COLS // 2, ROWS // 2)


def test_snake_prevent_reverse():
    snake = Snake(init_length=3)
    old_dir = snake.direction
    snake.set_direction(-1, 0)  # opposite of right
    assert snake.direction == old_dir  # should not update


def test_food_respawn():
    snake = Snake(init_length=3)
    food = Food(snake.body)
    old_position = food.position
    food.respawn(snake.body)
    assert food.position != old_position
    assert food.position not in snake.body
