from vpython import *


def vec(x: float, y: float) -> vector:
    return vector(x, y, 0)  # Simplify and confine to 2 dimensions


class Phasor:
    def __init__(self, magnitude: float, angle: radians, omega, color=color.white, visible=True):
        self._arrow = arrow(length=magnitude, axis=vec(1, 0).rotate(angle),
                            shaftwidth=0.1, headwidth=0.1, color=color)
        self.omega = omega
        self.visible = visible

    @classmethod
    def from_vector(cls, v: vector, omega, color=color.white, visible=True) -> 'Phasor':
        phasor = cls(0, 0, omega, color, visible)
        phasor._arrow.axis = v
        return phasor

    @classmethod
    def from_components(cls, x: float, y: float, omega, color=color.white, visible=True) -> 'Phasor':
        return cls.from_vector(vec(x, y), omega, color, visible)

    @property
    def axis(self) -> vector:
        return self._arrow.axis
    @axis.setter
    def axis(self, value):
        self._arrow.axis = value

    @property
    def visible(self) -> bool:
        return self._arrow.visible
    @visible.setter
    def visible(self, value):
        self._arrow.visible = value

    @property
    def color(self) -> vector:
        return self._arrow.color
    @color.setter
    def color(self, value: vector):
        self._arrow.color = value

    @property
    def magnitude(self) -> float:
        return self.axis.mag

    @property
    def pos(self) -> vector:
        return self._arrow.pos

    @property
    def angle(self) -> radians:
        return diff_angle(vec(1, 0), self.axis)

    def rotate(self, angle: radians):
        self._arrow.rotate(angle=angle, axis=vector(0, 0, 1))

    def add_to_tip(self, other: 'Phasor') -> 'Phasor':
        other._arrow.pos = self.axis + self._arrow.pos
        return other

    def __add__(self, other):
        self.add_to_tip(other)

    def __str__(self):
        return str(self.axis)


class PhasorDiagram:
    dt = 0.01

    def __init__(self):
        self.run = False
        self.phasors = list()
        self._canvas = canvas(width=600, height=600, align='left')
        self._canvas.autoscale = False
        self._canvas.userspin = False
        self._canvas.select()
        self._xaxis = box(length=100, width=0.01, height=0.01, canvas=self._canvas)
        self._yaxis = box(length=100, width=0.01, height=0.01, axis=vec(0, 1), canvas=self._canvas)

        self.last_added = Phasor(0, 0, 0)
        self.result = Phasor(0, 0, 0, color.green)
        self.y_proj = Phasor(0, 0, 0, color.yellow)

        self.t = 0
        self.graph = gcurve(color=vector(255, 197, 0), interval=3, graph=graph(background=color.black, align='right'))

    def add(self, phasor: Phasor):
        self.phasors.append(phasor)

    def cycle(self):
        self.last_added = Phasor(0, 0, 0)
        # self.result.axis = vec(0, 0)
        # self.last_added.axis = self.last_added.pos = vec(0, 0)
        for phasor in self.phasors:
            phasor.rotate(phasor.omega * dt)
            self.last_added = self.last_added.add_to_tip(phasor)

        self.t += dt
        self.result.axis = self.last_added.pos + self.last_added.axis
        y_projection = self.result.axis.y
        self.y_proj.axis = vec(0, y_projection)
        self.graph.plot(self.t, y_projection)


PD = PhasorDiagram()

PD.add(Phasor.from_vector(vec(-1, 1), 1))
PD.add(Phasor.from_components(1, 0, 2))
PD.add(Phasor.from_components(1, 1, 3))
PD.add(Phasor.from_components(1, 0.5, -1.5))
# PD.add(Phasor.from_components(0, 0.3, 1))

t = 0
dt = 0.005
while True:
    rate(30)
    PD.cycle()
