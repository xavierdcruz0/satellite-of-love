
# satellite initial position in metres
INITIAL_POSITION = (0, 19000000)

# satellite initial velocity in ms^-1
# v0 = (-7545.686798, 0)
INITIAL_VELOCITY = (-3500, 200)

# time step size in seconds
TIME_STEP = 10

# earth radius in metres
PLANET_RADIUS = 6378000

# earth mass in kg
PLANET_MASS = 5.972 * (10**24)

# apple mass in kg
SATELLITE_MASS = 1

# gravitational constant
G = 6.67384 * (10 ** -11)

INITIAL_CONFIG = {
    'position': INITIAL_POSITION,
    'velocity': INITIAL_VELOCITY,
    'time_step': TIME_STEP,
    'planet_radius': PLANET_RADIUS,
    'planet_mass': PLANET_MASS,
    'satellite_mass': SATELLITE_MASS,
    'GRAVITATIONAL_CONSTANT': G
}

class ModelState(object):
    def __init__(self, **kwargs):
        self.position = kwargs.get('position')
        self.position_x = self.position[0]
        self.position_y = self.position[1]
        self.velocity = kwargs.get('velocity')
        self.velocity_x = self.velocity[0]
        self.velocity_y = self.velocity[1]
        self.time_step = kwargs.get('time_step')
        self.planet_radius = kwargs.get('planet_radius')
        self.planet_mass = kwargs.get('planet_mass')
        self.satellite_mass = kwargs.get('satellite_mass') # doesn't actually affect calcuations!
        self.GRAVITATIONAL_CONSTANT = kwargs.get('GRAVITATIONAL_CONSTANT')