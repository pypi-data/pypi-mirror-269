from nqrduck_spectrometer.base_spectrometer_view import BaseSpectrometerView

class SimulatorView(BaseSpectrometerView):
    def __init__(self, module):
        super().__init__(module)
        # This automatically generates the settings widget based on the settings in the model
        self.widget = self.load_settings_ui()