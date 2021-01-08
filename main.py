import tkinter as tk
from controller import Controller
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def main():
    root = tk.Tk()
    app = Controller(root)
    app.render_app()

if __name__ == '__main__':
    main()