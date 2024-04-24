import taichi as ti

from ..particles import Particle

__all__ = ['sin', 'cos']

@ti.kernel
def sin(particles: ti.template(), frequency: ti.f32, magnitude: ti.f32, phase: ti.f32, axis: ti.i32):
    """Apply a sine wave force to particles.

    Args:
        particles (ti.template): Particles.
        frequency (ti.f32): Frequency of the sine wave.
        magnitude (ti.f32): Magnitude of the sine wave.
        phase (ti.f32): Phase of the sine wave.
        axis (ti.i32): Axis to apply the sine wave to.
    """
    for i in range(particles.field.shape[0]):
        p = particles.field[i]
        if p.active == 0:
            continue
        inc = magnitude * ti.sin(1/frequency * p.pos[axis] + phase)
        particles.field[i].vel[axis] += inc

@ti.kernel
def cos(particles: ti.template(), frequency: ti.f32, magnitude: ti.f32, phase: ti.f32, axis: ti.i32):
    """Apply a cosine wave force to particles.

    Args:
        particles (ti.template): Particles.
        frequency (ti.f32): Frequency of the cosine wave.
        magnitude (ti.f32): Magnitude of the cosine wave.
        phase (ti.f32): Phase of the cosine wave.
        axis (ti.i32): Axis to apply the cosine wave to.
    """
    for i in range(particles.field.shape[0]):
        p = particles.field[i]
        if p.active == 0:
            continue
        inc = magnitude * ti.cos(1/frequency * p.pos[axis] + phase)
        particles.field[i].vel[axis] += inc
