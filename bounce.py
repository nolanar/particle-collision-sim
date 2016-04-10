#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tkinter import *
import time
import math

class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dot(self, vec):
        return self.x * vec.x + self.y * vec.y

    def dotRatio(self, vec):
        return self.dot(vec) / self.dot(self)

    def scale(self, a):
        return Vector(self.x * a, self.y * a)

    def norm(self):
        return math.sqrt(self.dot(self))

    def normalise(self):
        return self.scale(self.norm())

    def perpendicular(self):
        return Vector(self.y, -self.x)

    def __add__(self, vec):
        return Vector(self.x + vec.x, self.y + vec.y)

    def __sub__(self, vec):
        return Vector(self.x - vec.x, self.y - vec.y)

class Border:
    def __init__(self, x1, y1, x2, y2):
        self.p = Vector(x1, y1)
        self.q = Vector(x2, y2)
        m = self.p - self.q
        m = m.perpendicular()
        self.n = m.normalise()

    def collide_time(self, ball):
        vel = self.n.dot(ball.vel)
        pos = self.n.dot(ball.pos)
        if vel == 0:
            return None
        t1 = (pos + ball.r) / vel
        t2 = (pos - ball.r) / vel
        t = math.min(t1, t2)
        return None if t < 0 else t

    def collide_event(self, ball):
        vel_n = self.n.scale(self.n.dot(ball.vel))
        ball.pos -= 2 * vel_n

    def draw(self, c):
        c.create_line(self.p.x, self.p.y, self.q.x, self.q.y, width=2)

class Ball:

    def __init__(self, x, y, dx, dy, r, m):
        self.pos = Vector(x, y)
        self.vel = Vector(dx, dy)
        self.r = r
        self.m = m
        self.t = None

    def collide_time(self, ball):
        pos = self.pos - ball.pos
        vel = self.vel - ball.vel
        r = self.r + ball.r

        # return if already intersecting
        if pos.dot(pos) < r*r:
            # print('intersecting')
            return 0 # or None?

        t_min = -vel.dotRatio(pos)

        # return if moving away from eachother
        if t_min < 0:
            # print('moving away', t_min)
            return None

        d_min = pos + vel.scale(t_min)
        len_min = d_min.dot(d_min)

        # return if no collision will occur
        if len_min > r*r:
            # print('no collision')
            return None

        t_del = math.sqrt((r*r - len_min) / vel.dot(vel))
        t_col = t_min - t_del
        return t_col

    def collide_event(self, ball):
        pos = self.pos - ball.pos
        vel = self.vel - ball.vel
        r = self.r + ball.r

        vel_normal = pos.scale(pos.dotRatio(vel))
        self.vel -= vel_normal.scale(2 * ball.m / (self.m + ball.m))
        ball.vel += vel_normal.scale(2 * self.m / (self.m + ball.m))

    def draw(self, c):
        if self.t is None:
            self.t = time.perf_counter()
        t = time.perf_counter() - self.t
        pos = self.pos + self.vel.scale(t)
        r = self.r
        c.create_oval(pos.x - r, pos.y - r, pos.x + r, pos.y + r, fill='black')


WIDTH = 600
HEIGHT = 600

def main():
    root = Tk()
    root.title("Collision Sim")

    canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg= "light grey")
    canvas.pack()

    balls = []
    ball = Ball(100,275, 250, 0, 50, 10)
    balls.append(ball)
    # ball = Ball(500, 325, -250, 0, 50, 10)
    # balls.append(ball)
    
    margin = 5;
    left_border = Border(margin, margin, margin, HEIGHT - margin)
    right_border = Border(WIDTH - margin, margin, WIDTH - margin, HEIGHT - margin)
    top_border = Border(margin, margin, WIDTH - margin, margin)
    bottom_border = Border(margin, HEIGHT - margin, WIDTH - margin, HEIGHT - margin)
    borders = [left_border, right_border, top_border, bottom_border]

    count = 0;
    while True:

        # col_time = balls[0].collide_time(balls[1])
        # if col_time is not None and col_time < 0.01:
        #     Ball.collide_event(balls[0], balls[1])

        canvas.delete(ALL)
        for ball in balls:
            ball.draw(canvas)
        for border in borders:
            border.draw(canvas)

        root.update_idletasks()
        root.update()
        time.sleep(0.01)
        count += 0.01


if __name__ == "__main__":
    main()