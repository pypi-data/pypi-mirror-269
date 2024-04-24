"""The Vera module provides a wrapper for all available forces and behaviours."""

from . import forces
from . import geom
from .flock import Flock
from .flock2 import Flock2
from .reaction_diffusion import ReactionDiffusion
from .slime import Slime
from .particle_life import ParticleLife
from .swarmalators import Swarmalators

class Vera:
    """The Vera class provides a wrapper for all available forces and behaviours,
    that can be applied to a Tolvera entities such as the Particle system."""
    def __init__(self, tolvera, **kwargs) -> None:
        """Initialise the Vera class.
        
        Args:
            tolvera (Tolvera): A Tolvera instance.
            **kwargs: Keyword arguments passed to the Vera.
        """
        self.tv = tolvera
        self.add_forces_to_self()
        # self.add_geom_to_self()
        self.flock = Flock(tolvera, **kwargs)
        self.flock2 = Flock2(tolvera, **kwargs)
        self.slime = Slime(tolvera, **kwargs)
        self.rd = ReactionDiffusion(tolvera, **kwargs)
        self.plife = ParticleLife(tolvera, **kwargs)
        self.swarm = Swarmalators(tolvera, **kwargs)

    def add_forces_to_self(self):
        """Add all forces to the Vera instance."""
        for f in forces.__all__:
            setattr(self, f, getattr(forces, f))
    
    def add_geom_to_self(self):
        """Add all geom functions to the Vera instance."""
        for g in geom.__all__:
            setattr(self, g, getattr(geom, g))

    def randomise(self):
        """Randomise all forces and behaviours."""
        self.flock.randomise()
        self.slime.randomise()
        self.rd.randomise()
