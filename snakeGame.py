import tkinter as tk
import random

# Game settings
WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20
SPEED = 120

BG_COLOR = "#1e1e1e"
SNAKE_COLOR = "#2ecc71"
FOOD_COLOR = "#e74c3c"
TEXT_COLOR = "white"


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")

        self.score = 0
        self.direction = "Right"
        self.next_direction = "Right"
        self.game_running = True

        self.canvas = tk.Canvas(
            root,
            width=WIDTH,
            height=HEIGHT,
            bg=BG_COLOR,
            highlightthickness=0
        )
        self.canvas.pack()

        self.score_label = tk.Label(
            root,
            text="Score: 0",
            font=("Arial", 16, "bold"),
            fg=TEXT_COLOR,
            bg=BG_COLOR
        )
        self.score_label.pack(fill=tk.X)

        self.root.bind("<Up>", lambda event: self.change_direction("Up"))
        self.root.bind("<Down>", lambda event: self.change_direction("Down"))
        self.root.bind("<Left>", lambda event: self.change_direction("Left"))
        self.root.bind("<Right>", lambda event: self.change_direction("Right"))
        self.root.bind("<space>", lambda event: self.restart_game())

        self.start_game()

    def start_game(self):
        self.score = 0
        self.direction = "Right"
        self.next_direction = "Right"
        self.game_running = True

        start_x = WIDTH // 2
        start_y = HEIGHT // 2

        self.snake = [
            (start_x, start_y),
            (start_x - CELL_SIZE, start_y),
            (start_x - 2 * CELL_SIZE, start_y)
        ]

        self.food = self.generate_food()
        self.update_score()
        self.draw_game()
        self.move_snake()

    def change_direction(self, new_direction):
        opposite = {
            "Up": "Down",
            "Down": "Up",
            "Left": "Right",
            "Right": "Left"
        }

        if new_direction != opposite[self.direction]:
            self.next_direction = new_direction

    def generate_food(self):
        while True:
            x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE

            if (x, y) not in self.snake:
                return (x, y)

    def move_snake(self):
        if not self.game_running:
            return

        self.direction = self.next_direction

        head_x, head_y = self.snake[0]

        if self.direction == "Up":
            head_y -= CELL_SIZE
        elif self.direction == "Down":
            head_y += CELL_SIZE
        elif self.direction == "Left":
            head_x -= CELL_SIZE
        elif self.direction == "Right":
            head_x += CELL_SIZE

        new_head = (head_x, head_y)

        if self.check_collision(new_head):
            self.end_game()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
            self.update_score()
        else:
            self.snake.pop()

        self.draw_game()
        self.root.after(SPEED, self.move_snake)

    def check_collision(self, head):
        x, y = head

        hit_wall = x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT
        hit_self = head in self.snake

        return hit_wall or hit_self

    def draw_game(self):
        self.canvas.delete("all")

        for x, y in self.snake:
            self.canvas.create_rectangle(
                x, y,
                x + CELL_SIZE, y + CELL_SIZE,
                fill=SNAKE_COLOR,
                outline=BG_COLOR
            )

        food_x, food_y = self.food
        self.canvas.create_oval(
            food_x, food_y,
            food_x + CELL_SIZE, food_y + CELL_SIZE,
            fill=FOOD_COLOR,
            outline=FOOD_COLOR
        )

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def end_game(self):
        self.game_running = False

        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 - 20,
            text="GAME OVER",
            fill="white",
            font=("Arial", 28, "bold")
        )

        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 + 25,
            text="Press SPACE to restart",
            fill="white",
            font=("Arial", 16)
        )

    def restart_game(self):
        if not self.game_running:
            self.start_game()


root = tk.Tk()
game = SnakeGame(root)
root.mainloop()