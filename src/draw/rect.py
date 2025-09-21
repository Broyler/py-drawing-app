from draw.line import draw_line


def draw_rectangle(arr, p1, p2, color, thickness=1):
    x0, y0 = p1
    x1, y1 = p2
    draw_line(arr, (x0, y0), (x1, y0), color, thickness)
    draw_line(arr, (x0, y1), (x1, y1), color, thickness)
    draw_line(arr, (x0, y0), (x0, y1), color, thickness)
    draw_line(arr, (x1, y0), (x1, y1), color, thickness)

