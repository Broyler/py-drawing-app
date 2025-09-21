def draw_circle(arr, center, radius, color, thickness=1):
    cx, cy = center
    x, y = radius, 0
    err = 0

    while x >= y:
        for dx, dy in [
            (x, y), (y, x), (-y, x), (-x, y),
            (-x, -y), (-y, -x), (y, -x), (x, -y)
        ]:
            px, py = cx + dx, cy + dy
            if 0 <= py < arr.shape[0] and 0 <= px < arr.shape[1]:
                arr[max(0, py-thickness//2):py+thickness//2+1,
                    max(0, px-thickness//2):px+thickness//2+1] = color

        y += 1
        if err <= 0:
            err += 2*y + 1
        if err > 0:
            x -= 1
            err -= 2*x + 1

