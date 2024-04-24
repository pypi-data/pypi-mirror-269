"""Differential line"""

import taichi as ti

from ..utils import CONSTS

@ti.data_oriented
class DifferentialLine:
    def __init__(self, tolvera, **kwargs) -> None:
        self.tv = tolvera
        self.kwargs = kwargs
        self.CONSTS = CONSTS({"dt": (ti.f32, 0.1)})
        """
        state
            max segments
            tv.s.segments
        init
            starting shape? circle etc.
        step
            for s in segments
                calculate the direction of growth
                apply angle variation and growth rate
                maintain minimum distance between points
        composition
            want to be able to e.g. flock the segments
        """
        self.tv.s.diffline_s = {
            "state": {
                "sigma": (ti.f32, 0.0, 100.0),
            },
            "shape": self.tv.sn,
            "randomise": True,
        }
    @ti.kernel
    def step(self, particles: ti.template(), weight: ti.f32):
        for i in particles:
            pass
    @ti.func
    def proc(self, x, y, z) -> ti.Vector:
        pass
    def randomise(self):
        self.tv.s.diffline_s.randomise()
    def __call__(self, particles: ti.template(), weight: ti.f32=1.0):
        self.step(particles, weight)
