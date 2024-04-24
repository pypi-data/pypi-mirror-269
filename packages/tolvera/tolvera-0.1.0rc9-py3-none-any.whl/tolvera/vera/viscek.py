"""Flocking behaviour based on the Viscek model."""

import numpy as np
import taichi as ti

from ..utils import CONSTS

"""
how is theta updated? should i just calculate it from velocity?
add noise * constant
update velocity
update position

vel->theta
theta->vel?

https://docs.taichi-lang.org/api/taichi/math/#taichi.math.tan
https://chat.openai.com/c/81f80436-4270-4d5e-b33f-88babf032717
https://chat.openai.com/c/f9af6e1b-30aa-4079-a19b-d34f30a6cc9d
https://github.com/ajinkya-kulkarni/PyFlocking/blob/main/MainProgram.py
"""


@ti.data_oriented
class Viscek:
    """Viscek flocking model"""
    def __init__(self, tolvera, **kwargs):
        self.tv = tolvera
        self.kwargs = kwargs
        self.CONSTS = CONSTS({"MAX_RADIUS": (ti.f32, 300.0)})
        self.tv.s.viscek_s = {
            "state": {
                "radius": (ti.f32, 0.01, 1.0),
            },
            "shape": (self.tv.sn, self.tv.sn),
            "osc": ("set"),
            "randomise": True,
        }
        self.tv.s.viscek_p = {
            "state": {
                "theta": (ti.f32, -np.pi, np.pi),
            },
            "shape": self.tv.pn,
            "osc": ("get"),
            "randomise": True,
        }
        self.tv.s.viscek_dist = {
            "state": {
                "dist": (ti.f32, 0.0, self.tv.x * 2),
                "dist_wrap": (ti.f32, 0.0, self.tv.x * 2),
            },
            "shape": (self.tv.pn, self.tv.pn),
            "osc": ("get"),
            "randomise": False,
        }

    def randomise(self):
        """Randomise"""
        self.tv.s.viscek_s.randomise()

    @ti.kernel
    def step(self, particles: ti.template(), noise_weight: ti.f32, weight: ti.f32):
        n = particles.shape[0]
        for i in range(n):
            if particles[i].active == 0:
                continue
            p1 = particles[i]
            species = self.tv.s.viscek_s.struct()
            n = 0
            n_dir = ti.Vector([0.0, 0.0])
            for j in range(n):
                if i == j and particles[j].active == 0:
                    continue
                p2 = particles[j]
                dis_wrap = p1.dist_wrap(p2, self.tv.x, self.tv.y)
                dis_wrap_norm = dis_wrap.norm()
                if dis_wrap_norm < species.radius * self.CONSTS.MAX_RADIUS:
                    n_dir += self.tv.s.viscek_p[j].theta
                    n += 1
            avg_dir = n_dir / n
            
                

    def __call__(self, particles, weight: ti.f32 = 1.0):
        """Call the Flock behaviour.

        Args:
            particles (Particles): Particles to step.
            weight (ti.f32, optional): The weight of the Flock behaviour. Defaults to 1.0.
        """
        self.step(particles.field, weight)
