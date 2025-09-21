def draw_line(arr, p1, p2, color, thickness=1):
    x0, y0 = p1
    x1, y1 = p2

    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy

    while True:
        if 0 <= y0 < arr.shape[0] and 0 <= x0 < arr.shape[1]:
            arr[max(0, y0-thickness//2):y0+thickness//2+1,
                max(0, x0-thickness//2):x0+thickness//2+1] = color

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy

