"""Inspired by https://github.com/williamgilpin/dysts"""

import taichi as ti

from ..utils import CONSTS

@ti.data_oriented
class Lorentz:
    def __init__(self, tolvera, **kwargs) -> None:
        self.tv = tolvera
        self.kwargs = kwargs
        self.CONSTS = CONSTS({"dt": (ti.f32, 0.1)})
        self.lorentz_s = {
            "state": {
                "sigma": (ti.f32, 0.0, 100.0),
                "rho":   (ti.f32, 0.0, 100.0),
                "beta":  (ti.f32, 0.0, 100.0),
            },
            "shape": self.tv.sn,
            "randomise": True,
        }
    @ti.kernel
    def step(self, particles: ti.template(), weight: ti.f32):
        for i in particles:
            self.tv.p[i].pos = self.proc(self.tv.p[i].pos[0], self.tv.p[i].pos[1], self.tv.p[i].pos[2])
            self.tv.p[i].pos = self.tv.p[i].pos % self.tv.x
    @ti.func
    def proc(self, x, y, z) -> ti.Vector:
        dt = self.CONSTS.dt
        s = self.tv.s.lorentz_s["sigma"] # index
        r = self.tv.s.lorentz_s["rho"]
        b = self.tv.s.lorentz_s["beta"]
        dx = s * (y - x)
        dy = x * (r - z) - y
        dz = x * y - b * z
        x += dx * dt
        y += dy * dt
        z += dz * dt
        return ti.Vector([x, y, z])
    def randomise(self):
        self.tv.s.lorentz_s.randomise()
    def __call__(self, particles: ti.template(), weight: ti.f32=1.0):
        self.step(particles, weight)
