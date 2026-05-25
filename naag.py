import tkinter
import random
import os
import winsound  # works on Windows

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

# -------- HIGH SCORE SYSTEM --------
HIGH_SCORE_FILE = "highscore.txt"

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read())
    return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))

high_score = load_high_score()

# -------- TILE CLASS --------
class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# -------- WINDOW SETUP --------
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg="black",
                        width=WINDOW_WIDTH,
                        height=WINDOW_HEIGHT,
                        borderwidth=0,
                        highlightthickness=0)
canvas.pack()
window.update()

# center window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# -------- GAME VARIABLES --------
snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5)
food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)

velocityX = 0
velocityY = 0

snake_body = []
game_over = False
score = 0

# -------- CONTROLS --------
def change_direction(e):
    global velocityX, velocityY, game_over

    if game_over:
        return

    if (e.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1

    elif (e.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1

    elif (e.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0

    elif (e.keysym == "Right" and velocityX != -1):
        velocityX = 1
        velocityY = 0

# -------- GAME LOGIC --------
def move():
    global snake, food, snake_body, game_over, score, high_score

    if game_over:
        return

    # wall collision
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or
        snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        winsound.Beep(400, 300)
        if score > high_score:
            save_high_score(score)
        return

    # self collision
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            winsound.Beep(400, 300)
            if score > high_score:
                save_high_score(score)
            return

    # food collision
    if (snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        score += 1

        winsound.Beep(1000, 100)  # eat sound

        if score > high_score:
            high_score = score

    # move body
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if i == 0:
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev = snake_body[i-1]
            tile.x = prev.x
            tile.y = prev.y

    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

# -------- DRAW --------
def draw():
    global game_over

    move()
    canvas.delete("all")

    # food
    canvas.create_rectangle(food.x, food.y,
                            food.x + TILE_SIZE,
                            food.y + TILE_SIZE,
                            fill='red')

    # snake head
    canvas.create_rectangle(snake.x, snake.y,
                            snake.x + TILE_SIZE,
                            snake.y + TILE_SIZE,
                            fill='lime green')

    # body
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y,
                                tile.x + TILE_SIZE,
                                tile.y + TILE_SIZE,
                                fill='lime green')

    # score display
    canvas.create_text(40, 20, font="Arial 10",
                       text=f"Score: {score}", fill="white")

    canvas.create_text(100, 20, font="Arial 10",
                       text=f"High: {high_score}", fill="yellow")

    if game_over:
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2,
                           font="Arial 20",
                           text=f"Game Over: {score}",
                           fill="white")

    window.after(100, draw)

# -------- RUN --------
draw()
window.bind("<KeyRelease>", change_direction)
window.mainloop()