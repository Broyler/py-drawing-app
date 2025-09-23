from enum import Enum


class Tool(Enum):
    PENCIL = "pencil"
    ERASER = "eraser"
    FILL = "fill"
    LINE = "line"
    RECT = "rect"
    CIRCLE = "circle"


colors = {
    "black": "#000000",
    "white": "#ffffff",
    "red": "#ff0000",
    "orange": "#ffa500",
    "yellow": "#ffff00",
    "green": "#00ff00",
    "lightblue": "#add8e6",
    "blue": "#0000ff",
    "purple": "#800080",
    "pink": "#ff69b4",
    "gray": "#808080",
    "brown": "#964b00",
    "customcolor": "#ffffff",
}

tools = [
    "pencil",
    "eraser",
    "fill",
    "line",
    "rect",
    "circle",
]

canvas_width = 32
canvas_height = 32
canvas_channels = 4
scale_factor = 10
canvas_pad = 10
undo_buffer = 35

