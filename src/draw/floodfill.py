from collections import deque
import numpy as np


def fill_tool(chk_arr, arr, lx, ly, color):
    print(1)
    # BFS flood fill
    # arr = ctx._canvas.to_arr()
    orig_color = tuple(chk_arr[ly,lx])
    target_color = tuple(color)
    visited = np.zeros(chk_arr.shape[:2], dtype=bool)
    queue = deque([(ly, lx)])
    while queue:
        y, x = queue.popleft()
        if visited[y, x]:
            continue

        visited[y, x] = True
        arr[y, x] = target_color

        for dy, dx in ((y-1, x), (y+1, x), (y, x-1), (y, x+1)):
            if 0 <= dy < chk_arr.shape[0] and 0 <= dx < chk_arr.shape[1]:
                if not visited[dy, dx] and tuple(chk_arr[dy, dx]) == orig_color:
                    queue.append((dy, dx))

