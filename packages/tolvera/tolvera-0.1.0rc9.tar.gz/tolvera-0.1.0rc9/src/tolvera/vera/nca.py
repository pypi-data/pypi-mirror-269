"""
https://github.com/google/swissgl/blob/main/demo/NeuralCA.js
"""

import taichi as ti
import numpy as np

from ..pixels import Pixels
from ..utils import CONSTS

@ti.data_oriented
class NCA:
    def __init__(self, tolvera, **kwargs):
        self.tv = tolvera
        self.kwargs = kwargs
        self.CONSTS = CONSTS({"MAX_RADIUS": (ti.f32, 300.0)})
        self.px = Pixels(self.tv, **kwargs)
        self.tv.s.nca_s = {
            "state": {
                "uv": (ti.f32, 0., 1.),
                "percept": (ti.f32, 0., 1.),
            },
            "shape": (self.tv.x, self.tv.y),
            "randomise": True,
        }
        self.tv.s.nca_w = {
            "state": { "r": (ti.math.vec4, 0., 1.) },
            "shape": (4, 4), "randomise": False,
        }
        self.tv.s.nca_b = {
            "state": { "b": (ti.math.vec4, 0., 1.) },
            "shape": 1, "randomise": False,
        }
        self.init_wb()

    def init_wb(self):
        self.tv.s.nca_w.from_vec([
            -67,1,2,44,-13,-59,4,30,-1,16,-57,9,-10,-4,-2,-41,
            19,-18,-1,8,-4,35,8,0,-4,-4,-1,0,34,31,21,-25,
            4,13,18,-57,-79,-22,-25,71,-12,-11,24,27,-17,-8,-7,6,
            11,10,4,0,4,1,2,7,-26,-33,-15,-3,22,27,20,-34,
        ])
        self.tv.s.nca_b.from_vec([2,-5,-14,9])

    @ti.kernel
    def step(self, weight: ti.f32):
        for i, j in ti.ndrange(self.tv.x, self.tv.y):
            s = ...
            dp = ...
            p = self.perceive()
            ds = self.rule(s-0.5, p-0.5)

    @ti.func
    def perceive():
        pass

    @ti.func
    def rule(self, s: ti.math.vec4, p: ti.math.vec4)->ti.math.vec4:
        W0 = s * ti.Matrix([
            self.tv.s.nca_w[0,0].r,
            self.tv.s.nca_w[0,1].r,
            self.tv.s.nca_w[0,2].r,
            self.tv.s.nca_w[0,3].r
        ])
        W1 = s * ti.Matrix([
            self.tv.s.nca_w[1,0].r,
            self.tv.s.nca_w[1,1].r,
            self.tv.s.nca_w[1,2].r,
            self.tv.s.nca_w[1,3].r
        ])
        W2 = ti.abs(s) * ti.Matrix([
            self.tv.s.nca_w[2,0].r,
            self.tv.s.nca_w[2,1].r,
            self.tv.s.nca_w[2,2].r,
            self.tv.s.nca_w[2,3].r
        ])
        W3 = ti.abs(p) * ti.Matrix([
            self.tv.s.nca_w[3,0].r,
            self.tv.s.nca_w[3,1].r,
            self.tv.s.nca_w[3,2].r,
            self.tv.s.nca_w[3,3].r
        ])
        return 1e-3 * (W0 + W1 + W2 + W3 + self.tv.s.nca_b[0].b)

    def __call__(self, weight: ti.f32 = 1.0):
        self.step(weight)
        return self.px
