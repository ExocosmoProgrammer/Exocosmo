import math
from functions import defs
for i in defs:
    exec(f'from functions import {i}')
IMPORTING = 1


class rectangle:
    def __init__(self, rect, rotation):
        try:
            self.points = [[math.cos(getRadAngle(rect.left - rect.centerx, rect.top - rect.centery) + rotation) * dis((rect.left, rect.top), (rect.centerx, rect.centery)) + rect.centerx, math.sin(getRadAngle(rect.left - rect.centerx, rect.top - rect.centery) + rotation) * dis((rect.left, rect.top), (rect.centerx, rect.centery)) + rect.centery],
                           [math.cos(getRadAngle(rect.right - rect.centerx, rect.top - rect.centery) + rotation) * dis((rect.right, rect.top), (rect.centerx, rect.centery)) + rect.centerx, math.sin(getRadAngle(rect.right - rect.centerx, rect.top - rect.centery) + rotation) * dis((rect.right, rect.top), (rect.centerx, rect.centery)) + rect.centery],
                           [math.cos(getRadAngle(rect.right - rect.centerx, rect.bottom - rect.centery) + rotation) * dis((rect.right, rect.bottom), (rect.centerx, rect.centery)) + rect.centerx, math.sin(getRadAngle(rect.right - rect.centerx, rect.bottom - rect.centery) + rotation) * dis((rect.right, rect.bottom), (rect.centerx, rect.centery)) + rect.centery],
                           [math.cos(getRadAngle(rect.left - rect.centerx, rect.bottom - rect.centery) + rotation) * dis((rect.left, rect.bottom), (rect.centerx, rect.centery)) + rect.centerx, math.sin(getRadAngle(rect.left - rect.centerx, rect.bottom - rect.centery) + rotation) * dis((rect.left, rect.bottom), (rect.centerx, rect.centery)) + rect.centery]]
            self.initialPoints = self.points.copy()
            xpoints = [point[0] for point in self.points]
            ypoints = [point[1] for point in self.points]
            self.left = min(xpoints)
            self.right = max(xpoints)
            self.bottom = max(ypoints)
            self.top = min(ypoints)
            self.diagonal = 0
            self.center = [(self.left + self.right) / 2, (self.top + self.bottom) / 2]
            self.centerx = self.center[0]
            self.centery = self.center[1]
            self.rect = rect.copy()
            self.angle = rotation
        except NameError:
            assert IMPORTING

    def updatePoints(self):
            xpoints = [point[0] for point in self.points]
            ypoints = [point[1] for point in self.points]
            self.left = min(xpoints)
            self.right = max(xpoints)
            self.bottom = max(ypoints)
            self.top = min(ypoints)
            self.center = [(self.left + self.right) / 2, (self.top + self.bottom) / 2]
            self.centerx = self.center[0]
            self.centery = self.center[1]

    def scale(self, x, y):
        self.points = self.initialPoints.copy()
        for point in self.points:
            if point[0] == self.rect.left:
                point[0] = self.rect.centerx - x / 2
            else:
                point[0] = self.rect.centerx + x / 2
            if point[1] == self.rect.top:
                point[1] = self.rect.centery - y / 2
            else:
                point[1] = self.rect.centery + y / 2
        self.updatePoints()
        self.rotate(self.angle)
        self.updatePoints()

    def rotate(self, angle):
        try:
            self.center = [(self.left + self.right) / 2, (self.top + self.bottom) / 2]
            self.angle += angle
            for point in self.points:
                point[0] = self.center[0] + math.cos(getRadAngle(self.center[0] - point[0], self.center[1] - point[1]) + math.pi + angle) * dis(point, self.center)
                point[1] = self.center[1] + math.sin(getRadAngle(self.center[0] - point[0], self.center[1] - point[1]) + math.pi + angle) * dis(point, self.center)
            self.updatePoints()
        except NameError:
            assert IMPORTING

    def move(self, x, y):
        for point in self.points:
            point[0] += x
            point[1] += y
        self.left += x
        self.top += y
        self.right += x
        self.bottom += y
        for point in self.initialPoints:
            point[0] += x
            point[1] += y

    def getQRJKLM(self):
        self.diagonal = 1
        try:
            self.q = (self.points[1][1] - self.points[0][1]) / (self.points[1][0] - self.points[0][0])
        except ZeroDivisionError:
            self.diagonal = 0
            self.q = 999999999999999
        try:
            self.r = (self.points[3][1] - self.points[0][1]) / (self.points[3][0] - self.points[0][0])
        except ZeroDivisionError:
            self.diagonal = 0
            self.r = 9999999999999999999
        try:
            self.j = self.points[0][1] - self.q * self.points[0][0]
            self.k = self.points[2][1] - self.q * self.points[2][0]
            self.l = self.points[0][1] - self.r * self.points[0][0]
            self.m = self.points[2][1] - self.r * self.points[2][0]
        except AttributeError:
            pass

    def checkCollisionWithRect(self, rect):
        try:
            self.getQRJKLM()
            rect.getQRJKLM()
            if self.diagonal:
                if self.j > self.k and self.l > self.m:
                    option = 1
                elif self.j > self.k and self.l < self.m:
                    option = 2
                elif self.j < self.k and self.l < self.m:
                    option = 3
                else:
                    option = 4
                for i in rect.points:
                    if option == 1 and self.q * i[0] + self.k < i[1] < self.q * i[0] + self.j and self.r * i[0] + self.m < i[1] < self.r * i[0] + self.l:
                        print(f'point {i} touched the rect {self.points}')
                        return 1
                    elif option == 2 and self.q * i[0] + self.k < i[1] < self.q * i[0] + self.j and self.r * i[0] + self.l < i[1] < self.r * i[0] + self.m:
                        print(f'point {i} touched the rect {self.points}')
                        return 1
                    elif option == 3 and self.q * i[0] + self.j < i[1] < self.q * i[0] + self.k and self.r * i[0] + self.l < i[1] < self.r * i[0] + self.m:
                        print(f'point {i} touched the rect {self.points}')
                        return 1
                    elif option == 4 and self.q * i[0] + self.j < i[1] < self.q * i[0] + self.k and self.r * i[0] + self.m < i[1] < self.r * i[0] + self.l:
                        print(f'point {i} touched the rect {self.points}')
                        return 1
            else:
                for i in rect.points:
                    if self.top <= i[1] <= self.bottom and self.left <= i[0] <= self.right:
                        return 1
            if rect.diagonal:
                if rect.j > rect.k and rect.l > rect.m:
                    option2 = 1
                elif rect.j > rect.k and rect.l < rect.m:
                    option2 = 2
                elif rect.j < rect.k and rect.l < rect.m:
                    option2 = 3
                else:
                    option2 = 4
                for i in self.points:
                    if option2 == 1 and rect.q * i[0] + rect.k < i[1] < rect.q * i[0] + rect.j and rect.r * i[0] + rect.m < i[1] < rect.r * i[0] + rect.l:
                        return 1
                    elif option2 == 2 and rect.q * i[0] + rect.k < i[1] < rect.q * i[0] + rect.j and rect.r * i[0] + rect.l < i[1] < rect.r * i[0] + rect.m:
                        return 1
                    elif option2 == 3 and rect.q * i[0] + rect.j < i[1] < rect.q * i[0] + rect.k and rect.r * i[0] + rect.l < i[1] < rect.r * i[0] + rect.m:
                        return 1
                    elif option2 == 4 and rect.q * i[0] + rect.j < i[1] < rect.q * i[0] + rect.k and rect.r * i[0] + rect.m < i[1] < rect.r * i[0] + rect.l:
                        return 1
            else:
                for i in self.points:
                    if rect.top <= i[1] <= rect.bottom and rect.left <= i[0] <= rect.right:
                        return 1
            self.lines = {(tuple(self.points[0]), tuple(self.points[1]),): (self.q, self.j,),
                          (tuple(self.points[2]), tuple(self.points[3]),): (self.q, self.k,),
                          (tuple(self.points[0]), tuple(self.points[3]),): (self.r, self.l,),
                          (tuple(self.points[1]), tuple(self.points[2]),): (self.r, self.m,)}
            rect.lines = {(tuple(rect.points[0]), tuple(rect.points[1]),): (rect.q, rect.j,),
                          (tuple(rect.points[2]), tuple(rect.points[3]),): (rect.q, rect.k,),
                          (tuple(rect.points[0]), tuple(rect.points[3]),): (rect.r, rect.l,),
                          (tuple(rect.points[1]), tuple(rect.points[2]),): (rect.r, rect.m,)}
            for line in [key for key in self.lines.keys()]:
                for line2 in [key for key in rect.lines.keys()]:
                    try:
                        collisionPoint = [(self.lines[line][1] - rect.lines[line2][1]) / (self.lines[line][0] - rect.lines[line2][0])]
                        collisionPoint.append(collisionPoint[0] * self.lines[line][0] + self.lines[line][1])
                        if getLesser(line[0][0], line[1][0]) < collisionPoint[0] < getGreater(line[0][0], line[1][0]) and getLesser(line[0][1], line[1][1]) < collisionPoint[1] < getGreater(line[0][1], line[1][1]) and getLesser(line[0][0], line[1][0]) < collisionPoint[0] < getGreater(line[0][0], line[1][0]) and getLesser(line2[0][1], line2[1][1]) < collisionPoint[1] < getGreater(line2[0][1], line2[1][1]):
                            return 1
                    except ZeroDivisionError:
                       pass

            return 0
        except NameError:
            assert IMPORTING