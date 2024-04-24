"""Flock behaviour based on the Boids algorithm."""

import taichi as ti

from ..utils import CONSTS


@ti.data_oriented
class Flock2:
    """Flock behaviour.
    
    The flock operates via a species rule matrix, which is a 2D matrix of species 
    rules, such that every species has a separate relationship with every other 
    species including itself. As in the Boids algorithm, the rules are:
    - `separate`: how much a particle should separate from its neighbours.
    - `align`: how much a particle should align (match velocity) with its neighbours.
    - `cohere`: how much a particle should cohere (move towards) its neighbours.

    Taichi Boids implementation inspired by:
    https://forum.taichi-lang.cn/t/homework0-boids/563
    """
    def __init__(self, tolvera, **kwargs):
        """Initialise the Flock behaviour.

        `flock_s` stores the species rule matrix. 
        `flock_p` stores the rule values per particle, and the number of neighbours.
        `flock_dist` stores the distance between particles.

        Args:
            tolvera (Tolvera): A Tolvera instance.
            **kwargs: Keyword arguments (currently none).
        """
        self.tv = tolvera
        self.kwargs = kwargs
        self.CONSTS = CONSTS({"MAX_RADIUS": (ti.f32, 300.0)})
        self.tv.s.flock2_s = {
            "state": {
                "separate": (ti.f32, 0.01, 1.0),
                "align": (ti.f32, 0.01, 1.0),
                "cohere": (ti.f32, 0.01, 1.0),
                "radius": (ti.f32, 0.01, 1.0),
            },
            "shape": (self.tv.sn, self.tv.sn),
            "osc": ("set"),
            "randomise": True,
        }
        self.tv.s.flock2_p = {
            "state": {
                "separate": (ti.math.vec2, 0.0, 1.0),
                "align": (ti.math.vec2, 0.0, 1.0),
                "cohere": (ti.math.vec2, 0.0, 1.0),
                "nearby": (ti.i32, 0.0, self.tv.p.n - 1),
            },
            "shape": self.tv.pn,
            "osc": ("get"),
            "randomise": False,
        }
        self.tv.s.flock2_dist = {
            "state": {
                "dist": (ti.f32, 0.0, self.tv.x * 2),
                "dist_wrap": (ti.f32, 0.0, self.tv.x * 2),
            },
            "shape": (self.tv.pn, self.tv.pn),
            "osc": ("get"),
            "randomise": False,
        }

    def randomise(self):
        """Randomise the Flock behaviour."""
        self.tv.s.flock2_s.randomise()

    @ti.func
    def set_mag(self, v: ti.template(), mag: ti.f32):
        return (v / v.norm()) * mag
    
    @ti.func
    def set_mag2(self, v: ti.template(), mag: ti.f32):
        return (v / v.norm())# * mag

    @ti.kernel
    def step(self, particles: ti.template(), weight: ti.f32, algotype: ti.i32, single_species: ti.i32):
        """Step the Flock behaviour.

        Pairwise comparison is made and inactive particles are ignored. 
        When the distance between two particles is less than the radius 
        of the species, the particles are considered neighbours. 
        
        The separation, alignment and cohesion are calculated for
        each particle and the velocity is updated accordingly.

        State is updated in `flock_p` and `flock_dist`.

        Args:
            particles (ti.template()): A template for the particles.
            weight (ti.f32): The weight of the Flock behaviour.
        """
        n = particles.shape[0]
        for i in range(n):
            p1 = particles[i]
            if p1.active == 0:
                continue
            if single_species > -1:
                if p1.species != single_species:
                    continue
            separate = ti.Vector([0.0, 0.0])
            align = ti.Vector([0.0, 0.0])
            cohere = ti.Vector([0.0, 0.0])
            nearby = 0
            species = self.tv.s.flock2_s.struct()
            for j in range(n):
                p2 = particles[j]
                if i == j and p2.active == 0:
                    continue
                # if single_species > -1:
                #     if p2.species != single_species:
                #         continue
                species = self.tv.s.flock2_s[p1.species, p2.species]
                dis_wrap = p1.dist_wrap(p2, self.tv.x, self.tv.y)
                dis_wrap_norm = dis_wrap.norm()
                if dis_wrap_norm < species.radius * self.CONSTS.MAX_RADIUS:
                    separate += dis_wrap
                    align += p2.vel
                    cohere += p2.pos
                    nearby += 1
                self.tv.s.flock2_dist[i, j].dist = p1.dist(p2).norm()
                self.tv.s.flock2_dist[i, j].dist_wrap = dis_wrap_norm
            if nearby > 0:
                vel = ti.Vector([0.0, 0.0])
                if algotype == 0:
                    align = (align / nearby) * p1.active * species.align
                    separate = (
                        (separate / nearby) * p1.active * ti.math.max(species.separate, 0.2)
                    )
                    cohere = ((cohere / nearby) - p1.pos) * p1.active * species.cohere
                    vel = (separate + align + cohere).normalized()
                    # vel = separate + align + cohere
                elif algotype == 1:
                    align = self.set_mag((align / nearby), p1.speed) * species.align * p1.active
                    separate = self.set_mag((separate / nearby), p1.speed) * species.separate * p1.active
                    cohere = self.set_mag(((cohere / nearby) - p1.pos), p1.speed) * species.cohere * p1.active
                    vel = separate + align + cohere
                elif algotype == 2:
                    align = self.set_mag2((align / nearby), p1.speed) * species.align * p1.active
                    separate = self.set_mag2((separate / nearby), p1.speed) * species.separate * p1.active
                    cohere = self.set_mag2(((cohere / nearby) - p1.pos), p1.speed) * species.cohere * p1.active
                    vel = separate + align + cohere
                particles[i].vel += vel * weight
                particles[i].pos += particles[i].vel * p1.speed * p1.active * weight
            self.tv.s.flock2_p[i] = self.tv.s.flock2_p.struct(
                separate, align, cohere, nearby
            )

    def __call__(self, particles, weight: ti.f32=1.0, algotype: ti.f32=0, single_species: ti.i32=-1):
        """Call the Flock behaviour.

        Args:
            particles (Particles): Particles to step.
            weight (ti.f32, optional): The weight of the Flock behaviour. Defaults to 1.0.
        """
        self.step(particles.field, weight, algotype, single_species)
