from config import ModelState, INITIAL_CONFIG
from model import Model
from view import View, SettingsWindow
import logging


logger = logging.getLogger(__name__)

class Controller(object):
    def __init__(self, root):
        self.root = root
        initial_config = ModelState(**INITIAL_CONFIG)
        self.model = Model(initial_config)
        self.view = View(self.root, [self.start, self.stop, self.reset, self.settings_window, self.settings_apply])
        self.settings_view = None

        # set up the initial conditions
        initial_conditions = self.model.get_state()
        self.view.draw_canvas(initial_conditions)

        self.running = False

    def render_app(self):
        self.view.show()

    def settings_window(self):
        state = self.model.get_state()
        sw = SettingsWindow(state, self.settings_apply)
        self.settings_view = sw

    def settings_apply(self):
        settings = self.settings_view.gather_settings_from_userinput()
        new_config = ModelState(**settings)
        self.model.set_state(new_config)
        self.view.draw_canvas(new_config)

    def reset(self):
        '''
        Stops any running simulation, reset satellite to initial position + velocity
        '''
        logger.debug('Resetting simulation...')
        # set up the initial conditions
        initial_conditions = self.model.get_state()
        self.view.draw_canvas(initial_conditions)
        self.running = False

    def start(self):
        '''
        Begin the simulation
        '''
        if not self.running:
            logger.debug('Starting simulation...')
            self.running = True
            self._update_loop()
        else:
            logger.debug('Simulation is already running, stop pressing start!')

    def _update_loop(self):
        if self.running:
            state = self.model.get_state()
            position_current = state.position
            velocity_current = state.velocity

            position_next, velocity_next = self.model.step_time_forward(position_current, velocity_current)

            self.model.position = position_next
            self.model.velocity = velocity_next

            state_updated = self.model.get_state()

            self.view.draw_canvas(state_updated)
            self.root.after(10, self._update_loop)

    def stop(self):
        '''
        Stop running the simulation
        '''
        self.running = False
        logger.debug('Simulation stopped!')
