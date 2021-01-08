import math
from config import ModelState
import logging


logger = logging.getLogger(__name__)

# gravitational constant
G = 6.67384 * math.pow(10, -11)

# def runge_kutta_4(position_current, velocity_current, force_field, h):
#     velocity_k1 = force_field(position_current)
#     position_k1 = velocity_current
#
#     vk2 = force_field((position_current[0] + (position_k1[0] * h * 0.5), position_current[1] + (position_k1[1] * h * 0.5)))
#
#     rk2 = (velocity_current[0] + (velocity_k1[0] * h * 0.5), velocity_current[1] + (velocity_k1[1] * h * 0.5))
#
#     vk3 = force_field((position_current[0] + (rk2[0] * h * 0.5), position_current[1] + (rk2[1] * h * 0.5)))
#
#     rk3 = (velocity_current[0] + (vk2[0] * h * 0.5), velocity_current[1] + (vk2[1] * h * 0.5))
#
#     vk4 = force_field((position_current[0] + (rk3[0] * h), position_current[1] + (rk3[1] * h)))
#
#     rk4 = (velocity_current[0] + (vk3[0] * h), velocity_current[1] + (vk3[1] * h))
#
#     velocity_next = (velocity_current[0] + (velocity_k1[0] + vk2[0] * 2 + vk3[0] * 2 + vk4[0]) * (float(h) / 6),
#              velocity_current[1] + (velocity_k1[1] + vk2[1] * 2 + vk3[1] * 2 + vk4[1]) * (float(h) / 6))
#
#     position_next = (position_current[0] + (position_k1[0] + rk2[0] * 2 + rk3[0] * 2 + rk4[0]) * (float(h) / 6),
#              position_current[1] + (position_k1[1] + rk2[1] * 2 + rk3[1] * 2 + rk4[1]) * (float(h) / 6))
#
#     return position_next, velocity_next


def runge_kutta_4(position_current, velocity_current, force_field, h):
    # def k_2(k0, k1):
    #     return k0[0] + (k1[0] * h * 0.5), k0[1] + (k1[1] * h * 0.5)
    # def k_3(k0, k2):
    #     return k0[0] + (k2[0] * h * 0.5), k0[1] + (k2[1] * h * 0.5)
    # def k_4(k0, k3):
    #     return k0[0] + (k3[0] * h), k0[1] + (k3[1] * h)
    # def k_next(k0, k1, k2, k3, k4):
    #     return k0[0] + (k1[0] + k2[0] * 2 + k3[0] * 2 + k4[0]) * (float(h) / 6), k0[0] + (
    #                 k1[1] + k2[1] * 2 + k3[1] * 2 + k4[1]) * (float(h) / 6)

    acc_k1 = force_field(position_current)
    vel_k1 = velocity_current

    acc_k2 = force_field(
        (position_current[0] + (vel_k1[0] * h * 0.5), position_current[1] + (vel_k1[1] * h * 0.5)))

    vel_k2 = (velocity_current[0] + (acc_k1[0] * h * 0.5), velocity_current[1] + (acc_k1[1] * h * 0.5))

    acc_k3 = force_field((position_current[0] + (vel_k2[0] * h * 0.5), position_current[1] + (vel_k2[1] * h * 0.5)))

    vel_k3 = (velocity_current[0] + (acc_k2[0] * h * 0.5), velocity_current[1] + (acc_k2[1] * h * 0.5))

    acc_k4 = force_field((position_current[0] + (vel_k3[0] * h), position_current[1] + (vel_k3[1] * h)))

    vel_k4 = (velocity_current[0] + (acc_k3[0] * h), velocity_current[1] + (acc_k3[1] * h))

    velocity_next = (velocity_current[0] + (acc_k1[0] + acc_k2[0] * 2 + acc_k3[0] * 2 + acc_k4[0]) * (float(h) / 6),
                     velocity_current[1] + (acc_k1[1] + acc_k2[1] * 2 + acc_k3[1] * 2 + acc_k4[1]) * (float(h) / 6))

    position_next = (position_current[0] + (vel_k1[0] + vel_k2[0] * 2 + vel_k3[0] * 2 + vel_k4[0]) * (float(h) / 6),
                     position_current[1] + (vel_k1[1] + vel_k2[1] * 2 + vel_k3[1] * 2 + vel_k4[1]) * (float(h) / 6))

    return position_next, velocity_next

# define vector field for gravity
def gravity_force(position_x, position_y, planet_mass, satellite_mass):
    if (position_x, position_y) == (0, 0):
        return (0, 0)
    else:
        unitpx = math.cos(math.atan2(position_y, position_x))
        unitpy = math.sin(math.atan2(position_y, position_x))
        ModF = (-1 * G * planet_mass * satellite_mass) / (((position_x * position_x + position_y * position_y) ** 0.5) ** 2)
        Fgravx = ModF * unitpx
        Fgravy = ModF * unitpy
        return Fgravx, Fgravy

def gravity_field_function(planet_mass, satellite_mass):
    # def gravity_force(position_x, position_y):
    def gravity_force(position):
        position_x, position_y = position
        if (position_x, position_y) == (0, 0):
            return (0, 0)
        else:
            unitpx = math.cos(math.atan2(position_y, position_x))
            unitpy = math.sin(math.atan2(position_y, position_x))
            ModF = (-1 * G * planet_mass * satellite_mass) / (
                        ((position_x * position_x + position_y * position_y) ** 0.5) ** 2)
            Fgravx = ModF * unitpx
            Fgravy = ModF * unitpy
            return Fgravx, Fgravy
    return gravity_force


class Model(object):
    def __init__(self, model_state):
        self.set_state(model_state)

    def step_time_forward(self, position_current, velocity_current):
        # calculate satellite's next position and velocity,
        # based on its current position, velocity and acceleration due to gravity
        # position_current = self.satellite.get_position()
        # velocity_current = self.satellite.get_velocity()
        gravity_field = gravity_field_function(self.planet_mass, self.satellite_mass)

        position_next, velocity_next = runge_kutta_4(position_current,
                                                     velocity_current,
                                                     gravity_field,
                                                     self.time_step)

        # self.position = position_next
        # self.velocity = velocity_next
        return position_next, velocity_next

    # def collision(self):
    #     if ((500 - rnext_canvas[0]) ** 2 + (400 - rnext_canvas[1]) ** 2) ** 0.5 < float(Q) / 75000:


    def get_state(self):
        state_dict = {'position': self.position,
                'position_x': self.position[0],
                'position_y': self.position[1],
                'velocity': self.velocity,
                'velocity_x': self.velocity[0],
                'velocity_y': self.velocity[1],
                'time_step': self.time_step,
                'planet_radius': self.planet_radius,
                'planet_mass': self.planet_mass,
                'satellite_mass': self.satellite_mass}
        return ModelState(**state_dict)

    def set_state(self, model_state):
        self.position = model_state.position
        self.velocity = model_state.velocity
        self.time_step = model_state.time_step
        self.planet_radius = model_state.planet_radius
        self.planet_mass = model_state.planet_mass
        self.satellite_mass = model_state.satellite_mass # doesn't actually affect calcuations!
        self.GRAVITATIONAL_CONSTANT = model_state.GRAVITATIONAL_CONSTANT
