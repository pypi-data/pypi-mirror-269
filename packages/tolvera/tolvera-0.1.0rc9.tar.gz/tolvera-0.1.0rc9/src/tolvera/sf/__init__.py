import numpy as np
import signalflow as sf
from ..osc.update import Updater

class Osc(sf.Patch):
    def __init__(self, 
                 osc_type='sine',
                 freq=440, 
                 gain=1.0,
                 pan=0.0,
                 channels=2):
        super().__init__()
        freq = self.add_input("freq", freq)
        gain = self.add_input("gain", gain)
        pan = self.add_input("pan", pan)
        match osc_type.lower():
            case 'sine':
                osc = sf.SineOscillator(freq)
            case 'saw':
                osc = sf.SawOscillator(freq)
            case 'square':
                osc = sf.SquareOscillator(freq)
            case 'triangle':
                osc = sf.TriangleOscillator(freq)
            case 'impulse':
                osc = sf.Impulse(freq)
            case 'sinelfo':
                osc = sf.SineLFO(freq)
            case 'sawlfo':
                osc = sf.SawLFO(freq)
            case 'squarelfo':
                osc = sf.SquareLFO(freq)
            case 'trianglelfo':
                osc = sf.TriangleLFO(freq)
            case _:
                osc = sf.SineOscillator(freq)
        panner = sf.AzimuthPanner(channels, osc, pan)
        output = panner * gain
        self.set_output(output)
        self.set_auto_free(True)
    def __setattr__(self, name, value):
        self.set_input(name, value)

class OscBank:
    """
    Example
    """
    def __init__(self,
                 osc_type='sine',
                 number = 16, 
                 freq = (100, 1000),
                 pan = (-1, 1),
                 channels = 2,
                 update_rate = 10):
        self.osc_type = osc_type
        self.number = number
        self.freq = freq
        self.pan = pan
        self.channels = channels
        self.gain = (0, 1/self.number)
        self.update_rate = update_rate
        self.freqs = [int(np.random.uniform(*self.freq)) for _ in range(self.number)]
        self.pans = [np.random.uniform(*self.pan) for _ in range(self.number)]
        self.gains = [np.random.uniform(*self.gain) for _ in range(self.number)]
        self.oscs = [Osc(self.osc_type, f,g,p, self.channels) for f,g,p in zip(self.freqs, self.gains, self.pans)]
        self.updater = Updater(self.update, self.update_rate)
    def update(self, freqs, pans, gains):
        for i, s in enumerate(self.oscs):
            s.freq = freqs[i]
            s.pan = pans[i]
            s.gain = gains[i]
    def play(self):
        [s.play() for s in self.oscs]
    def stop(self):
        [s.stop() for s in self.oscs]
    def __call__(self, freqs, pans, gains):
        self.updater(freqs, pans, gains)

class Flt(sf.Patch):
    def __init__(self,
                 input: sf.Node,
                 filter_type="low_pass", 
                 cutoff=1000, 
                 resonance=0.6):
        super().__init__()
        # self.input = input
        # self.filter_type = filter_type
        cutoff = self.add_input("cutoff", cutoff)
        resonance = self.add_input("resonance", resonance)
        flt = sf.SVFilter(input, filter_type, cutoff, resonance)
        self.set_output(flt)
        self.set_auto_free(True)
    def __setattr__(self, name, value):
        self.set_input(name, value)

class FltBank:
    """
    Example:
        audio_in = sf.AudioIn()
        flts = FltBank(audio_in, tv.pn//128)
        def update():
            nonlocal flts
            p_np = tv.p.field.to_numpy()
            pos = p_np['pos']
            cutoffs = map_range(pos.T[0], 0, tv.x, *flts.cutoff)
            resonances  = map_range(pos.T[0], 0, tv.x, *flts.resonance)
            flts(cutoffs, resonances)
        flts.play()
    """
    def __init__(self,
                 input: sf.Node,
                 number = 16, 
                 filter_type = "bandpass",
                 cutoff = (100, 10000),
                 resonance = (0.6, 0.99),
                 update_rate = 10):
        self.number = number
        self.filter_type = filter_type
        self.cutoff = cutoff
        self.resonance = resonance
        self.update_rate = update_rate
        self.cutoffs = [int(np.random.uniform(*self.cutoff)) for _ in range(self.number)]
        self.resonances = [np.random.uniform(*self.resonance) for _ in range(self.number)]
        self.filters = [Flt(input, filter_type, c, r) for c,r in zip(self.cutoffs, self.resonances)]
        self.updater = Updater(self.update, self.update_rate)
    def update(self, cutoffs, resonances):
        for i, f in enumerate(self.filters):
            f.cutoff = cutoffs[i]
            f.resonance = resonances[i]
    def play(self):
        [f.play() for f in self.filters]
    def stop(self):
        [f.stop() for f in self.filters]
    def __call__(self, cutoffs, resonances):
        self.updater(cutoffs, resonances)

    
class EuclideanPatch (sf.Patch):
    """
    Example:
        clock = Impulse(8)
        a = EuclideanPatch(clock, 2, 23, 7, 80, 0.99, 0.0, 10.0)
        b = EuclideanPatch(clock, 3, 13, 9, 800, 0.98, 0.7, 0.2)
        c = EuclideanPatch(clock, 4, 16, 11, 8000, 0.97, -0.7, 0.05)
        d = EuclideanPatch(clock, 2, 19, 12, 480, 0.99, 0.0, 0.2)
    """
    def __init__(self, clock, divider=1, sequence_length=24, num_events=8, cutoff=8000, resonance=0.99, pan=0.0, amp=0.5):
        super().__init__()
        self.clock = clock
        self.cutoff = self.add_input("cutoff", cutoff)
        self.resonance = self.add_input("resonance", resonance)
        self.divider = self.add_input("divider", divider)
        self.sequence_length = self.add_input("sequence_length", sequence_length)
        self.num_events = self.add_input("num_events", num_events)
        self.amp = self.add_input("amp", amp)
        self.pan = self.add_input("pan", pan)
        self.eu = sf.Euclidean(sf.ClockDivider(self.clock, self.divider), self.sequence_length, self.num_events)
        self.flt = sf.SVFilter(self.eu, "low_pass", cutoff=self.cutoff, resonance=self.resonance)
        self.panned = sf.StereoPanner(self.flt * self.amp, self.pan)
        self.set_output(self.panned)

class PingPongDelayPatch (sf.Patch):
    """
    Example:
        pingpong = PingPongDelayPatch(mix)
        pingpong.play()
    """
    def __init__(self, input=0, delay_time=1/8, feedback=0.7, wet=0.3):
        super().__init__()
        mono_input = sf.ChannelMixer(1, input)
        delay_l = sf.AllpassDelay(mono_input, delay_time=delay_time, feedback=feedback)
        delay_r = sf.OneTapDelay(delay_l, delay_time=(delay_time/2))
        wetdry = sf.WetDry(input, [ delay_l, delay_r ], wet)
        self.set_output(wetdry)

class GranulatorPatch (sf.Patch):
    """
    Example:
        clock = sf.Impulse(8)
        audio_path = os.path.join(os.path.dirname(__file__), "audio", "gliss.aif")
        granulator = GranulatorPatch(clock, audio_path)
        granulator.play()
    """
    def __init__(self,
                 clock, 
                 audio_path,
                 pan_min=-1,
                 pan_max=1,
                 pos_min=0,
                 pos_max=1,
                 rate_min=0.5,
                 rate_max=2.0,
                 duration=0.5,
                 envelope_shape="triangle"):
        super().__init__()
        buf = sf.Buffer(audio_path)
        self.pan_min = self.add_input("pan_min", pan_min)
        self.pan_max = self.add_input("pan_max", pan_max)
        self.pos_min = self.add_input("pos_min", pos_min)
        self.pos_max = self.add_input("pos_max", pos_max)
        self.rate_min = self.add_input("rate_min", rate_min)
        self.rate_max = self.add_input("rate_max", rate_max)
        self.duration = self.add_input("duration", duration)
        self.envelope_shape = self.add_input("envelope_shape", envelope_shape)
        granulator = sf.Granulator(
            buffer=buf,
            clock=clock,
            pan=sf.RandomUniform(self.pan_min, self.pan_max, clock=clock),
            pos=sf.RandomUniform(self.pos_min, int(self.pos_max * buf.duration), clock=clock),
            rate=sf.RandomExponential(self.rate_min, self.rate_max, clock=clock),
            duration=self.duration)
        envelope = sf.EnvelopeBuffer(self.envelope_shape)
        granulator.set_buffer("envelope", envelope)
        self.set_output(granulator)
