from vpython import *


def vec(x: float, y: float) -> vector:
    return vector(x, y, 0)  # Make everything easier and confine to 2 dimensions


class Phasor:
    def __init__(self, magnitude: float, angle: radians, omega, visible=True):
        self._arrow = arrow(length=magnitude, axis=vec(1, 0).rotate(angle),
                            shaftwidth=0.1, headwidth=0.1)
        self.omega = omega
        self.visible = visible

    @classmethod
    def from_vector(cls, v: vector, visible=True):
        phasor = cls(0, 0, 0)
        phasor.visible = visible
        phasor._arrow.axis = v
        return phasor

    @classmethod
    def from_components(cls, x: float, y: float, visible=True):
        return cls.from_vector(vec(x, y), visible)

    @property
    def axis(self):
        return self._arrow.axis

    @axis.setter
    def axis(self, value):
        self._arrow.axis = value

    @property
    def visible(self):
        return self._arrow.visible

    @visible.setter
    def visible(self, value):
        self._arrow.visible = value

    def add_to_tip(self, other: 'Phasor') -> 'Phasor':
        other._arrow.pos = self.axis + self._arrow.pos
        other.axis = self.axis + other.axis
        return other
        # phasor = Phasor.from_vector(self.axis + other.axis)
        # phasor._arrow.pos = self.axis + self._arrow.pos
        # return phasor

    def __add__(self, other):
        self.add_to_tip(other)

    def rotate(self, angle: radians):
        self._arrow.rotate(angle=angle, axis=vector(0, 0, 1))


class PhasorDiagram:
    dt = 0.01

    def __init__(self):
        self._canvas = canvas()
        self._canvas.autoscale = False
        self._xaxis = box(length=100, width=0.01, height=0.01, canvas=self._canvas)
        self._yaxis = box(length=100, width=0.01, height=0.01, axis=vec(0, 1), canvas=self._canvas)
        self.phasors = list()
        self.result = Phasor(0, 0, 0, False)

    def add(self, phasor: Phasor):
        if self.phasors:  # If there are phasors already, hide additional ones
            phasor.visible = False
        else:  # We must see at least one, however
            phasor.visible = True
        self.result.add_to_tip(phasor)
        self.phasors.append(phasor)

    def cycle(self):
        result = Phasor(0, 0, 0, False)
        for phasor in self.phasors:
            phasor.rotate(phasor.omega * dt)
            self.result.add_to_tip(phasor)


# p1 = Phasor.from_vector(vec(-1, 1))
# p2 = Phasor.from_components(1, 0, False)
# p3 = Phasor.from_components(1, 0, False)
# p4 = Phasor.from_components(1, 0, False)
# p5 = Phasor.from_components(1, 0, False)
PD = PhasorDiagram()

PD.add(Phasor.from_vector(vec(-1, 1)))
PD.add(Phasor.from_components(1, 0))
PD.add(Phasor.from_components(1, 0))
PD.add(Phasor.from_components(1, 0))
PD.add(Phasor.from_components(1, 0))

# print('p1', p1)
# print(p1.axis)
# print(p2.axis)
# p1.axis = vec(-0.5, 0.5)
# print(p1.axis)
#
#
# pf = p1.add_to_tip(p2).add_to_tip(p3).add_to_tip(p4).add_to_tip(p5)
# print(pf.axis)

t = 0
dt = 0.005
while True:
    rate(50)
    PD.cycle()
    # pf.rotate(0.01)

    # t += dt
    # print("Rotating", t)
# print(type(p3))
# print('p3', p3)
# Phasor(0.5, pi/3)
# Phasor(1.5, pi/4)

# PhasorDiagram()
