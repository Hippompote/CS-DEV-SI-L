import tkinter as tk

from PIL import ImageTk, Image

from entities.defense import Defense
from entities.immovableentity import ImmovableEntity
from entities.player import Player
from entities.alien import Alien
from world.world import World


class Game:
    """
    The game class of the SpaceInvaders game.
    This class contains almost all the logic of the game and, therefore, should not be inherited.

    Author:
        Aioniostheos
        Fierperle
    """

    def __init__(self, max_fps: int = 60, is_fullscreen: bool = False) -> None:
        """
        Creates a new game.

        Arguments:
            max_fps (int): Optional - the maximum framerate of the game.
            is_fullscreen (bool): Optional - whether the game should be fullscreen or not.
        """

        self.is_fullscreen = is_fullscreen
        self.root = self.__initialize(is_fullscreen)

        frame = tk.Frame(self.root)
        self.__score = tk.StringVar()
        tk.Label(frame, textvariable=self.__score).pack(side="left", padx=15)
        self.__lives_label = tk.Label(frame)
        self.__lives_label.pack(side="right", padx=15)
        frame.pack(side="top", fill="x")

        self.__background = Image.open("./assets/background.png")
        self.__width, self.__height = self.__background.size

        self.__canvas = tk.Canvas(self.root, width=self.__width, height=self.__height)
        self.world = World(canvas=self.__canvas, background=self.__background)

        self.__max_fps = max_fps

        self.is_paused = False
        self.__shoot_cooldown = 0

        # aliens positions properties
        self.__aliens_amount = 23
        self.__max_aliens_per_line = 5
        self.__line_height = 70
        self.__spawn_border = [10, 50]

    def get_max_framerate(self) -> int:
        """
        Returns:
            int: the maximum framerate of the game.
        """

        return self.__max_fps

    def pause(self) -> None:
        """
        Pauses the game. Therefore, this method creates a Toplevel window and creates a pause menu.
        """

        pause_window = tk.Toplevel(self.root)
        PauseMenu(self, pause_window)

    def start(self) -> None:
        """
        Starts the game.
        This method creates a new player and initializes game loops.
        """

        # key bindings
        self.root.bind("<Key>", lambda event: self.__on_key_pressed(event))

        self.root.after(25, lambda: [
            # map borders
            self.world.add_entity(ImmovableEntity(0, int(self.__height / 2), 0, self.__height)),
            self.world.add_entity(ImmovableEntity(int(self.__width / 2), 0, self.__width, 0)),
            self.world.add_entity(ImmovableEntity(self.__width, int(self.__height / 2), 0, self.__height)),
            self.world.add_entity(ImmovableEntity(int(self.__width / 2), self.__height, self.__width, 0)),

            # player
            self.world.add_entity(Player(int(self.__width / 2), self.__height - 50)),

            # defenses
            self.world.add_entity(
                Defense(int(self.__width / 2) - 96, self.__height - 150)),
            self.world.add_entity(
                Defense(int(self.__width / 2) + 96, self.__height - 150)),

            # aliens
            self.__generate_aliens(),

            self.__update_client_loop(),
            self.__update_world_loop()
        ])
        self.root.mainloop()

    def __generate_aliens(self) -> None:
        """
        This method generates the aliens based on the number of aliens and the maximum number of aliens in a line.
        """

        # dynamic parameters
        # increment between aliens in a line
        inline_increment = (self.__width - (2 * self.__spawn_border[0])) / self.__max_aliens_per_line
        # number of lines with maximum number of aliens
        full_line_amount = self.__aliens_amount // self.__max_aliens_per_line

        # full lines generation
        line = 0
        for i in range(full_line_amount * self.__max_aliens_per_line):
            if i % self.__max_aliens_per_line == 0 and i != 0:
                line += 1
            self.world.add_entity(Alien(
                self.__spawn_border[0] + int(inline_increment / 2 + (i % self.__max_aliens_per_line) * inline_increment),
                self.__spawn_border[1] + (line * self.__line_height)
            ))

        # last line generation
        line += 1
        remaining_aliens_amount = self.__aliens_amount % self.__max_aliens_per_line
        inline_increment = self.__width / remaining_aliens_amount
        for i in range(remaining_aliens_amount):
            self.world.add_entity(Alien(
                int(inline_increment / 2 + (i % self.__max_aliens_per_line) * inline_increment),
                self.__spawn_border[1] + (line * self.__line_height)
            ))

    def __initialize(self, is_fullscreen: bool) -> tk.Tk:
        """
        Initialize the game window.

        Arguments:
            is_fullscreen (bool): whether the game should be fullscreen or not.

        Returns:
            the initialized game window.
        """

        root = tk.Tk()
        root.title("Space Invaders")
        root.attributes('-fullscreen', is_fullscreen)
        root.resizable(False, False)

        # the menu bar code is based on: https://pythonspot.com/tk-menubar/
        menu_bar = tk.Menu(root)
        game_menu = tk.Menu(menu_bar, tearoff=0)
        game_menu.add_command(label="Pause", command=self.pause)
        game_menu.add_command(label="New Game", command=lambda: [
            root.destroy(), Game(self.get_max_framerate()).start()
        ])
        game_menu.add_separator()
        game_menu.add_command(label="Quit", command=root.destroy)
        menu_bar.add_cascade(label="Game", menu=game_menu)
        root.config(menu=menu_bar)

        return root

    def __on_key_pressed(self, event) -> None:
        """
        This method is called when a key is pressed.

        Arguments:
            event (tk.Event): the event that is triggered when a key is pressed.
        """

        if not self.is_paused:
            if event.keysym in ["q", "Left"]:
                self.world.client.player.move(-1)
            elif event.keysym in ["d", "Right"]:
                self.world.client.player.move()

            if event.keysym == "Escape":
                self.pause()
            elif event.keysym == "space":
                if self.__shoot_cooldown <= 0:
                    self.world.client.player.shoot()
                    self.__shoot_cooldown = 1000

    def __update_client_loop(self) -> None:
        """
        This method updates the client for each frame (defined by the framerate).
        """

        if not self.is_paused:
            if self.world.client.player is not None:
                image = ImageTk.PhotoImage(
                    Image.open("./assets/life_" + str(self.world.client.player.get_lives()) + ".png"))
                self.__lives_label.configure(image=image)
                self.__lives_label.image = image
                self.__score.set(f"Score: {self.world.client.player.get_score()}")

            self.world.update_client()
            self.root.update()
        self.root.after(int(1000 / self.__max_fps), self.__update_client_loop)

    def __update_world_loop(self) -> None:
        """
        This method updates the world every 100 milliseconds.
        """

        if not self.is_paused:
            self.world.update()

            if self.__shoot_cooldown > 0:
                self.__shoot_cooldown -= 100

            [should_end_game, result] = self.world.should_end_game()
            if should_end_game:
                self.world.update_client()
                if result == "win":
                    end_window = tk.Toplevel(self.root)
                    EndMenu(self, end_window, "All aliens have been destroyed!")
                    return
                elif result == "lose":
                    end_window = tk.Toplevel(self.root)
                    EndMenu(self, end_window, "You have been destroyed!")
                    return
                return

        self.root.after(100, self.__update_world_loop)


class PauseMenu:
    """
    The pause menu of the game. When the game is paused, this menu is displayed.
    The user should not be able to use the game while this menu is displayed.
    This menu contains a new game button, a resume button and a quit button.

    Author:
        Aioniostheos
    """

    def __init__(self, game: Game, window: tk.Toplevel) -> None:
        """
        Creates a new pause menu for the specified game using a pre-initialized window.

        Arguments:
            game (Game): the game to pause.
            window (tk.Tk): the window of the pause menu.
        """

        self.__game = game
        self.__game.is_paused = True
        self.__window = window
        self.__window.title("Game Paused")

        # if the game is fullscreen, the pause menu should also be fullscreen
        self.__window.attributes('-fullscreen', self.__game.is_fullscreen)

        tk.Label(self.__window, text="Pause").pack()
        tk.Button(self.__window, text="New Game", command=self.__new_game).pack()
        tk.Button(self.__window, text="Resume", command=self.__resume).pack()
        tk.Button(self.__window, text="Quit", command=self.__quit).pack()

    def __new_game(self) -> None:
        """
        Starts a new game.
        """

        self.__window.destroy()
        self.__game.root.destroy()
        Game(max_fps=self.__game.get_max_framerate(), is_fullscreen=self.__game.is_fullscreen).start()

    def __resume(self) -> None:
        """
        Resumes the game.
        """

        self.__game.is_paused = False
        self.__window.destroy()

    def __quit(self) -> None:
        """
        Quits the game.
        """

        self.__window.destroy()
        self.__game.root.destroy()
        exit(0)


class EndMenu:
    """
    The end menu of the game. When the game is over, this menu is displayed.
    The user should not be able to use the game while this menu is displayed.
    This menu contains a new game button and a quit button.

    Author:
        Aioniostheos
    """

    def __init__(self, game: Game, window: tk.Toplevel, message: str) -> None:
        """
        Creates a new end menu for the specified game using a pre-initialized window.

        Arguments:
            game (Game): the game to pause.
            window (tk.Tk): the window of the pause menu.
            message (str): the message to display to the user.
        """

        self.__game = game
        self.__game.is_paused = True
        self.__window = window
        self.__window.title("Game Over")

        # if the game is fullscreen, the end menu should also be fullscreen
        self.__window.attributes('-fullscreen', self.__game.is_fullscreen)

        tk.Label(self.__window, text=message).pack()
        tk.Button(self.__window, text="New Game", command=self.__new_game).pack()
        tk.Button(self.__window, text="Quit", command=self.__quit).pack()

    def __new_game(self) -> None:
        """
        Starts a new game.
        """

        self.__window.destroy()
        self.__game.root.destroy()
        Game(max_fps=self.__game.get_max_framerate(), is_fullscreen=self.__game.is_fullscreen).start()

    def __quit(self) -> None:
        """
        Quits the game.
        """

        self.__window.destroy()
        self.__game.root.destroy()
        exit(0)
