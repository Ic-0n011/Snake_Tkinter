import tkinter
import random

WINDOW_BG = 'black'
CANVAS_BG = 'pink'
LINE_COLOR = 'black'
TILE_SIZE = 30
SNAKE_COLOR = 'green'
TAIL_COLOR = '#7FFF00'
FOOD_COLOR = 'red'
FPS = 15


class App:
    def __init__(self) -> None:
        self.window = tkinter.Tk()
        self.window.attributes('-fullscreen', True)
        self.window['bg'] = WINDOW_BG
        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()
        self.canvas_size = min((self.width, self.height))
        self.tiles_ammount = self.canvas_size // TILE_SIZE
        self.window.bind('<Key>', self.on_key)
        self.canvas = tkinter.Canvas(
            self.window,
            width=self.width // TILE_SIZE * TILE_SIZE,
            height=self.height // TILE_SIZE * TILE_SIZE,
            bg=CANVAS_BG,
            highlightthickness=0
        )
        self.canvas.pack()
        self.draw_lines()
        self.max_col = self.width // TILE_SIZE * TILE_SIZE
        self.max_row = self.height // TILE_SIZE * TILE_SIZE
        self.game = Game(self.canvas, self.tiles_ammount, self.max_col, self.max_row)
        self.window.mainloop()

    def on_key(self, event: tkinter.Event) -> None:
        if event.keysym == 'Escape':
            self.window.destroy()
        else:
            self.game.on_key(event)

    def draw_lines(self) -> None:
        '''Делит поле на клетки вериткальными и горизонтальными линиями'''
        for i in range(1, self.width // TILE_SIZE):
            self.canvas.create_line(
                i * TILE_SIZE,
                0,
                i * TILE_SIZE,
                self.height,
                fill=LINE_COLOR
            )

        for i in range(1, self.height // TILE_SIZE):
            self.canvas.create_line(
                0,
                i * TILE_SIZE,
                self.width,
                i * TILE_SIZE,
                fill=LINE_COLOR
            )

    def end_game(self):
        print("конец")
        self.window.destroy()


class Game:
    def __init__(self, canvas: tkinter.Canvas, size: int, max_col, max_row) -> None:
        self.canvas = canvas
        self.size = size
        self.col = max_col // TILE_SIZE
        self.row = max_row // TILE_SIZE
        self.max_col = max_col
        self.max_row = max_row
        self.snake = Snake(
            self.size // 2 * TILE_SIZE,
            self.size // 2 * TILE_SIZE,
            self.max_col,
            self.max_row,
            self.canvas,
            SNAKE_COLOR,
            key_up='Up',
            key_down='Down',
            key_left='Left',
            key_right='Right'
        )
        self.food = None
        self.update()

    def update(self) -> None:
        self.snake.collide_border()
        self.snake.collide_tail()
        if not self.food:
            clean_cell = []
            for col in range(self.max_col//TILE_SIZE):
                col = col * TILE_SIZE
                for row in range(self.max_row//TILE_SIZE):
                    row = row * TILE_SIZE
                    if col != self.snake.col and row != self.snake.row:
                        for i in self.snake.segments:
                            if col != self.snake.segments[i].col and row != self.snake.segments[i].row:
                                clean_cell.append[(col, row)]
            food_cord = random.choice(clean_cell)
            self.food = Food(
                self.canvas,
                food_cord[0],
                food_cord[1]
            )
        self.canvas.delete('snake')
        self.canvas.delete('food')
        self.food.draw()
        self.snake.draw()
        if self.snake.is_move:
            self.snake.move()
            self.food = self.snake.eating(self.food)
        self.canvas.after(132, self.update)

    def on_key(self, event: tkinter.Event):
        self.snake.on_key(event)


class Snake:
    def __init__(
            self,
            col: int,
            row: int,
            max_col: int,
            max_row: int,
            canvas: tkinter.Canvas,
            color: str,
            key_up: str,
            key_down: str,
            key_left: str,
            key_right: str
    ) -> None:
        self.is_move = True
        self.col = col
        self.row = row
        self.max_col = max_col
        self.max_row = max_row
        self.canvas = canvas
        self.color = color
        self.key_up = key_up
        self.key_down = key_down
        self.key_left = key_left
        self.key_right = key_right
        self.direction = (1, 0)
        self.segments = dict()

    def create_new_segment(self):
        self.segments[len(self.segments)+1] = Tail(
            self,
            self.col,
            self.row,
            self.canvas,
            TAIL_COLOR,
            len(self.segments)+1
            )

    def draw(self) -> None:
        self.canvas.create_rectangle(
            self.col,
            self.row,
            self.col + TILE_SIZE,
            self.row + TILE_SIZE,
            fill=self.color,
            tags='snake'
        )

    def move(self):
        if len(self.segments) > 0:
            self.segments[1].draw()
            self.segments[1].next_col = self.col
            self.segments[1].next_row = self.row
            self.segments[1].move()
        self.col += TILE_SIZE * self.direction[0]
        self.row += TILE_SIZE * self.direction[1]

    def change_direction(self, direction):
        if self.direction[0] == -direction[0]:
            return
        if self.direction[1] == -direction[1]:
            return
        self.direction = direction

    def on_key(self, event: tkinter.Event):
        if event.keysym == self.key_up:
            direction = (0, -1)
        elif event.keysym == self.key_down:
            direction = (0, 1)
        elif event.keysym == self.key_left:
            direction = (-1, 0)
        elif event.keysym == self.key_right:
            direction = (1, 0)
        self.change_direction(direction)

    def eating(self, food):
        if self.col == food.col and self.row == food.row:
            self.create_new_segment()
            food = None
        return food

    def collide_border(self):
        if self.col < 0 or self.col > self.max_col:
            self.canvas['bg'] = 'red'
            self.is_move = False
        if self.row < 0 or self.row > self.max_row:
            self.canvas['bg'] = 'red'
            self.is_move = False

    def collide_tail(self):
        return
        # FIXME: если есть хвост, то змея с нми сразу сталкивается
        for i in self.segments:
            if self.col == self.segments[i].col:
                if self.row == self.segments[i].row:
                    self.canvas['bg'] = 'red'
                    self.is_move = False


class Tail():
    def __init__(
            self,
            snake: Snake,
            col: int,
            row: int,
            canvas: tkinter.Canvas,
            color: str,
            number_segment: int
    ) -> None:
        self.snake = snake
        self.col = col
        self.row = row
        self.canvas = canvas
        self.color = color
        self.number_segmen = number_segment
        self.next_col = col
        self.next_row = row

    def draw(self) -> None:
        self.canvas.create_rectangle(
            self.col,
            self.row,
            self.col + TILE_SIZE,
            self.row + TILE_SIZE,
            fill=self.color,
            tags='snake'
        )

    def move(self):
        if len(self.snake.segments) > self.number_segmen:
            self.snake.segments[self.number_segmen+1].next_col = self.col
            self.snake.segments[self.number_segmen+1].next_row = self.row
            self.snake.segments[self.number_segmen+1].move()
            self.snake.segments[self.number_segmen+1].draw()
        self.col = self.next_col
        self.row = self.next_row


class Food:
    def __init__(self, canvas: tkinter.Canvas, col: int, row: int) -> None:
        self.canvas = canvas
        self.col = col
        self.row = row
        self.color = FOOD_COLOR

    def draw(self) -> None:
        self.canvas.create_rectangle(
            self.col,
            self.row,
            self.col + TILE_SIZE,
            self.row + TILE_SIZE,
            fill='red',
            tags='food'
        )


App()
