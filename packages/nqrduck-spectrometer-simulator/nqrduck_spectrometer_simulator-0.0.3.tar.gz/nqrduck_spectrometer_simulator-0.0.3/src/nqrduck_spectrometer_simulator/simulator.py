from nqrduck_spectrometer.base_spectrometer import BaseSpectrometer
from .model import SimulatorModel
from .view import SimulatorView
from .controller import SimulatorController

Simulator = BaseSpectrometer(SimulatorModel, SimulatorView, SimulatorController)