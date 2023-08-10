import tkinter as tk

from game import Game

FULLSCREEN = False
MAX_FRAMERATE = 60

# entry point of the program: used by PyCharm to define a run configuration.
if __name__ == "__main__":
    startup_window = tk.Tk()
    startup_window.title("Space Invaders")
    startup_window.attributes('-fullscreen', FULLSCREEN)

    tk.Button(startup_window, text="Start", command=lambda: [
        startup_window.destroy(),
        Game(max_fps=MAX_FRAMERATE, is_fullscreen=FULLSCREEN).start()
    ]).pack()
    tk.Button(startup_window, text="Quit", command=lambda: [startup_window.destroy(), exit(0)]).pack()

    startup_window.mainloop()
