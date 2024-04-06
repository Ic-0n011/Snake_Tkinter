# FIXME: последний ряд и колонна не такого размера, как остальные

import tkinter

WINDOW_BG = 'black'
CANVAS_BG = 'pink'
LINE_COLOR = 'black'
TILE_SIZE = 32
SNAKE_COLOR = 'green'
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
            width=self.canvas_size,
            height=self.canvas_size,
            bg=CANVAS_BG,
            highlightthickness=0
        )
        self.canvas.pack()
        self.draw_lines()
        self.game = Game(self.canvas, self.tiles_ammount)
        self.window.mainloop()

    def on_key(self, event: tkinter.Event) -> None:
        if event.keysym == 'Escape':
            self.window.destroy()
        else:
            self.game.on_key(event)

    def draw_lines(self) -> None:
        '''Делит поле на клетки вериткальными и горизонтальными линиями'''
        for i in range(1, int(self.tiles_ammount)):
            self.canvas.create_line(
                i * TILE_SIZE,
                0,
                i * TILE_SIZE,
                self.height,
                fill=LINE_COLOR
            )

        for i in range(1, int(self.tiles_ammount)):
            self.canvas.create_line(
                0,
                i * TILE_SIZE,
                self.width,
                i * TILE_SIZE,
                fill=LINE_COLOR
            )


class Game:
    def __init__(self, canvas: tkinter.Canvas, size: int) -> None:
        self.canvas = canvas
        self.size = size
        print(size)
        self.snake = Snake(
            self.size // 2 * TILE_SIZE,
            self.size // 2 * TILE_SIZE,
            TILE_SIZE,
            self.canvas,
            SNAKE_COLOR,
            'up',
            'down',
            'left',
            'right'
        )
        self.update()

    def update(self) -> None:
        self.canvas.delete('snake')
        self.snake.move()
        self.snake.draw()
        self.canvas.after(1000 // FPS, self.update)

    def on_key(self, event: tkinter.Event):
        self.snake.on_key(event)


class Snake:
    def __init__(
            self,
            col: int,
            row: int,
            size: int,
            canvas: tkinter.Canvas,
            color: str,
            key_up: str,
            key_down: str,
            key_left: str,
            key_right: str
    ) -> None:
        self.col = col
        self.row = row
        self.size = size
        self.canvas = canvas
        self.color = color
        self.key_up = key_up
        self.key_down = key_down
        self.key_left = key_left
        self.key_right = key_right
        self.direction = (1, 0)

    def draw(self) -> None:
        self.canvas.create_rectangle(
            self.col,
            self.row,
            self.col + self.size,
            self.row + self.size,
            fill=self.color,
            tags='snake'
        )

    def move(self):
        self.col += self.size * self.direction[0]
        self.row += self.size * self.direction[1]

    def change_direction(self, direction):
        self.direction = direction

    def on_key(self, event: tkinter.Event):
        if event.keysym == self.key_up:
            self.change_direction((0, -1))
        if event.keysym == self.key_down:
            self.change_direction((0, 1))
        if event.keysym == self.key_left:
            self.change_direction((-1, 0))
        if event.keysym == self.key_right:
            self.change_direction((1, 0))


class Food:
    pass


App()
