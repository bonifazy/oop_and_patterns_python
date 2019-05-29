import pygame
import random
import math  # to Vec2d csl
from abc import ABC  # to Polyline csl


SCREEN_DIM = (1200, 800)  # Default resolution


class Vec2d:
    """
    Point.  Description.  Math and present operations.
    """
    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]

    def __add__(self, other):  # return with Vec2d type to math and slice operations
        dote = (self.x + other.x, self.y + other.y)
        return Vec2d(dote)

    def __mul__(self, k: float):
        return self.x * k, self.y * k

    def __sub__(self, other):
        return self.x - other.x, self.y - other.y

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str((self.x, self.y))

    def __len__(self):
        return math.ceil(math.sqrt(self.x ** 2 + self.y ** 2))

    def __getitem__(self, item):  # slice point[x][0|1]
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError

    def int_pair(self):
        return int(self.x), int(self.y)


class Polyline(ABC):
    """
    All modifications with ready points array (self.points, self.speeds)
        of your points and creation inner poly from Knot.
    create: draw_points(points=None, your polyline; points=*, inner polyline from Knot class)
    update: set_points
    modify: other methods
    """

    def __init__(self):
        self.points = []
        self.speeds = []
        self.speed = 1
        self.steps = 1
        self.style = "points"
        self.width = 1
        self.color = (255, 255, 255)
        self.res = (640, 480)

    # Update coordinates of points
    def set_points(self):
        _points = self.points
        _speeds = self.speeds
        for p in range(len(_points)):
            point = Vec2d(_points[p])
            speed_p = Vec2d(_speeds[p])
            self.points[p] = point + speed_p
            if _points[p][0] > self.res[0] or _points[p][0] < 0:  # reflex point if > width
                self.speeds[p] = (- _speeds[p][0], _speeds[p][1])
            if _points[p][1] > self.res[1] or _points[p][1] < 0:  # if > height
                self.speeds[p] = (_speeds[p][0], - _speeds[p][1])

    # main draw
    def draw_points(self, points=None, style=None, _color=(255, 255, 255)):
        _points = points if points else self.points  # first prediction if get from 'get_knot'
        if style:  # lines
            for p_n in range(-1, len(_points) - 1):
                pygame.draw.line(game_display, _color, (int(_points[p_n][0]), int(_points[p_n][1])),
                                 (int(_points[p_n + 1][0]), int(_points[p_n + 1][1])), self.width)
        else:  # points
            for p in _points:
                pygame.draw.circle(game_display, _color,
                                   (int(p[0]), int(p[1])), self.width)

    # if press 'R'
    def clear(self):
        self.points = list()
        self.speeds = list()

    # if press '< left'
    def del_last(self):
        self.points.pop()
        self.speeds.pop()

    # if press 'W'
    def speed_more(self):
        for i in range(len(self.speeds)):
            if abs(self.speeds[i][0]) < 30:
                self.speeds[i] = (self.speeds[i][0] * 1.5, self.speeds[i][1] * 1.5)

    # if press 'S'
    def speed_less(self):
        for i in range(len(self.speeds)):
            if abs(self.speeds[i][0]) > 1.5:
                self.speeds[i] = (self.speeds[i][0] * 0.7, self.speeds[i][1] * 0.7)

    # if mouse button on the point
    def del_point(self):
        for i in range(len(self.points)):
            precision = 10
            if abs(self.points[i][0] - event.pos[0]) <= precision and \
                    abs(self.points[i][1] - event.pos[1]) <= precision:
                if len(self.points) >= 2:  # keep one point, '>= 1' del all
                    self.points.remove(self.points[i])
                    self.speeds.remove(self.speeds[i])
                    break

    # if press '> right' or mouse button on default mode without pause
    def add_point(self, pos):
        point_pos = pos if pos else (random.randint(0, res_mode[0]), random.randint(0, res_mode[1]))
        speed_pos = ((random.random() - 0.5) * self.speed, (random.random() - 0.5) * self.speed) if pos \
            else (random.random() * self.speed * 3, random.random() * self.speed * 3)
        self.points.append(point_pos)
        # fixed Sursera bugs. True random points addiction: random(0, 1) + 0.5
        # Bugs direction: to bottom, to right
        self.speeds.append(speed_pos)


class Knot(Polyline):
    """
    Search inner polyline
    """

    # recursion finder of points
    def get_point(self, pnt, alpha, deg=None):
        if deg is None:
            deg = len(pnt) - 1
        if deg == 0:
            return pnt[0]
        point = Vec2d(pnt[deg])
        point = Vec2d(point * alpha)
        dote = Vec2d(self.get_point(pnt, alpha, deg - 1)) * (1 - alpha)
        another_point = Vec2d(dote)
        answer = point + another_point
        return answer

    # split poly on 'count' parts
    def get_points(self, pnt):
        alpha = 1 / self.steps
        res = []
        for a in range(self.steps):
            res.append(self.get_point(pnt, a * alpha))
        return res

    # find the points with 'count' alpha
    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for d in range(-2, len(self.points) - 2):
            ptn = list()
            x = Vec2d(self.points[d])
            y = Vec2d(self.points[d + 1])
            z = Vec2d(self.points[d + 2])
            ptn.append((x + y) * 0.5)
            ptn.append(y)
            ptn.append((y + z) * 0.5)
            res.extend(self.get_points(ptn))
        return res


def draw_help():
    res = res_mode
    game_display.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = list()
    data.append(["\'F1\'", "Show Help"])
    data.append(["\'R\'", "Restart"])
    data.append(["\'P\'", "Pause/Play"])
    data.append(["\'W\'", "Faster"])
    data.append(["\'S\'", "Slowly"])
    data.append(["Mouse button above point", "only in Pause mode. Delete point"])
    data.append(["\'Up\' key or \'Num+\'", "More alpha inner polyline"])
    data.append(["\'Down\' key or \'Num-\'", "Less alpha"])
    data.append(["\'Left\' key", "Delete last vector"])
    data.append(["\'Right\' key", "Random speedy point"])
    data.append(["", ""])
    data.append([str(knot.steps), "Alpha"])
    data.append([str(len(knot.points)), 'Current points'])
    # set with screen resolution
    pygame.draw.lines(game_display, (255, 50, 50, 2), True, [
        (0, 0), (res[0], 0), (res[0], res[1]), (0, res[1])], 3)
    for num, text in enumerate(data):
        game_display.blit(font1.render(
            text[0], True, (128, 128, 144)), (res[0] // 4, res[1] // 4 + 30 * num))
        game_display.blit(font2.render(
            text[1], True, (128, 128, 255)), (res[0] // 2, res[1] // 4 + 30 * num))


if __name__ == "__main__":
    pygame.init()
    infoObject = pygame.display.Info()
    display_max_resolution = True  # add new feature
    res_mode = (infoObject.current_w, infoObject.current_h) if display_max_resolution else SCREEN_DIM
    game_display = pygame.display.set_mode(res_mode)
    pygame.display.set_caption("MyScreenSaver")
    color = pygame.Color(0)
    working = True
    show_help = False
    pause = False
    hue = 0

    # settings
    knot = Knot()  # main container
    knot.res = res_mode
    knot.speed = 17
    knot.steps = 17
    knot.style = 'line'
    knot.width = 2
    knot.color = color
    # after no takes global vars, else color updater (line #261)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:  # if press 'R'
                    knot.clear()  # del all points
                if event.key == pygame.K_p:  # if press 'P'
                    pause = not pause
                if event.key == pygame.K_KP_PLUS or event.key == pygame.K_UP:  # update: add new function - arrow (Up)
                    knot.steps += 1
                if event.key == pygame.K_F1:  # if press 'F1'
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS or event.key == pygame.K_DOWN:  # arrow (Down)
                    knot.steps -= 1 if knot.steps > 1 else 0
                if event.key == pygame.K_LEFT:  # arrow (Left)
                    if len(knot.points) >= 2:  # keep one point, '>= 1' del all points
                        knot.del_last()
                if event.key == pygame.K_RIGHT:  # arrow (Right), add faster point in random position
                        knot.add_point(None)
                if event.key == pygame.K_w:  # 'W' to more speed
                    knot.speed_more()
                if event.key == pygame.K_s:  # 'S' to less speed
                    knot.speed_less()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause:  # in pause del point under cursor with precision in px
                    knot.del_point()
                else:  # add new point
                    knot.add_point(event.pos)

        game_display.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)

        knot.draw_points()
        knot.draw_points(knot.get_knot(), style=False, _color=color)  # True|False to change inner poly lines|points
        if not pause:
            knot.set_points()
        if show_help:
            draw_help()
        pygame.display.flip()
    pygame.display.quit()
    pygame.quit()
    exit(0)
