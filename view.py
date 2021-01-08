import tkinter as tk
from tkinter import messagebox
import config as cfg
import logging


logger = logging.getLogger(__name__)

class View(object):
    def __init__(self, root, funcs):

        # self.window = tk.Tk()
        self.window = root
        self.window.geometry("1000x800")
        self.window.title("Planets")

        self.start, self.stop, self.reset, self.settings,self.settings_apply = funcs

        self.canvas = tk.Canvas(self.window, height=700, width=1000, bg="black")
        self.canvas.create_text(200, 40, text="Hit the Reset button to begin get started.", fill="white")
        self.canvas.grid(row=0, column=0, columnspan=6)

        resetbutton = tk.Button(self.window, text="Reset", command=self.reset).grid(row=1, column=0)
        gobutton = tk.Button(self.window, text="Start Simulation", command=self.start).grid(row=1, column=1)
        stopbutton = tk.Button(self.window, text="Stop Simulation", command=self.stop).grid(row=1, column=2)
        settingsbutton = tk.Button(self.window, text="Settings", command=self.settings).grid(row=1, column=3)
        aboutbutton = tk.Button(self.window, text="About", command=self.m_box).grid(row=1, column=4)
        quitbutton = tk.Button(self.window, text="Quit", command=self.window.destroy).grid(row=1, column=5)

    def planet_limits(self, R):
        return (500 - (float(R)), 400 - (float(R)), 500 + (float(R)), 400 + (float(R)))

    def draw_canvas(self, state):
        # logger.debug('Drawing canvas...')
        planet_radius = state.planet_radius

        position = state.position
        rad = int(float(planet_radius) / 75000)

        self.canvas.delete('all')

        planet = self.canvas.create_oval(self.planet_limits(rad), fill="white")
        apple = self.canvas.create_oval(self.planet_limits(5), fill="red")

        r0_canvas = (position[0] / 75000 + 500, (position[1] * 1) / 75000 + 400)
        r0_canvas = (int(r0_canvas[0]), int(r0_canvas[1]))
        self.canvas.move(apple, 500 - r0_canvas[0], 400 - r0_canvas[1])

        velocity = state.velocity
        vx, vy = velocity
        tangential_velocity = (vx**2 + vy**2)**0.5
        self.canvas.create_text(200,40, text='tangential velocity={:.2f} ms-1'.format(tangential_velocity), fill='white')

    def show(self):
        self.window.mainloop()

    def m_box(self):
        messagebox.showinfo(title="About",
                            message="""
                              Trajectory Calculator. 

                              Uses RK4 numerical integration algorithm. 

                                                            """)

class SettingsWindow(object):
    def __init__(self, current_settings, apply_function):

        self.apply_function = apply_function

        # draw the window
        smallie = tk.Tk()
        smallie.geometry("780x280")
        smallie.title("Settings")

        # draw the widgets
        label1 = tk.Label(smallie, text="Planet radius (m):").grid(row=1, column=0)
        self.planetradius = tk.Entry(smallie)
        self.planetradius.grid(row=1, column=1)
        label2 = tk.Label(smallie, text="Planet mass (kg):").grid(row=2, column=0)
        self.planetmass = tk.Entry(smallie)
        self.planetmass.grid(row=2, column=1)
        label3 = tk.Label(smallie, text="initial position x (m):").grid(row=3, column=0)
        self.px = tk.Entry(smallie)
        self.px.grid(row=3, column=1)
        label4 = tk.Label(smallie, text="initial position y (m):").grid(row=4, column=0)
        self.py = tk.Entry(smallie)
        self.py.grid(row=4, column=1)
        label5 = tk.Label(smallie, text="initial velocity x (m/s):").grid(row=5, column=0)
        self.vx = tk.Entry(smallie)
        self.vx.grid(row=5, column=1)
        label6 = tk.Label(smallie, text="initial velocity y (m/s):").grid(row=6, column=0)
        self.vy = tk.Entry(smallie)
        self.vy.grid(row=6, column=1)
        #	label7 = Label(smallie, text = "Apple mass (kg):").grid(row=7, column=0)
        #	applemass = Entry(smallie)
        #	applemass.insert(0, m)
        #	applemass.grid(row=7, column=1)
        label80 = tk.Label(smallie, text="Hint: Earth mass can be written as 5.972e+24").grid(row=2, column=3)

        label0 = tk.Label(smallie, text="                         User inputs:").grid(row=0, column=0, columnspan=4)

        self.entry_box_widgets = {
            'planet_radius': self.planetradius,
            'planet_mass': self.planetmass,
            'position_x': self.px,
            'position_y': self.py,
            'velocity_x': self.vx,
            'velocity_y': self.vy,
        }

        # fill values into the widgets
        self.populate_settings_fields(current_settings)

        applybutton = tk.Button(smallie, text="Apply", command=self.apply_function).grid(row=99, column=4)
        closebutton = tk.Button(smallie, text="Close", command=smallie.destroy)
        closebutton.grid(row=100, column=4)

    def populate_settings_fields(self, settings):
        for field, widget in self.entry_box_widgets.items():
            value = settings.__dict__[field]
            widget.insert(0, value)

    def gather_settings_from_userinput(self):
        settings = {
            'planet_radius': float(self.planetradius.get()),
            'planet_mass': float(self.planetmass.get()),
            'position_x': float(self.px.get()),
            'position_y': float(self.py.get()),
            'velocity_x': float(self.vx.get()),
            'velocity_y': float(self.vy.get()),
            'time_step': cfg.INITIAL_CONFIG['time_step'],
            'satellite_mass': cfg.SATELLITE_MASS,
            'GRAVITATIONAL_CONSTANT': cfg.G
        }
        settings['position'] = (settings['position_x'], settings['position_y'])
        settings['velocity'] = (settings['velocity_x'], settings['velocity_y'])
        return settings
