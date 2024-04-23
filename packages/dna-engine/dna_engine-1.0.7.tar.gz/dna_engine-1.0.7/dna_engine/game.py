import pygame
import pygame.freetype
import subprocess
import shutil
import threading
import sys
import os.path

import platform
import ctypes
from time import sleep
from random import randint
from typing import final

from . import audio_manager
from . import input_manager


@final
class Game():
    """
    The class which represents the core of a game project.
	- Handles the updating and rendering of a World object.
	- Responsible for starting and ending Worlds.
    """
    __textures = dict()
    __fonts = dict()
    __audio = dict()

    __build_time = 0
    __build_periods = ""

    __text_entry_toggle = False
    __text_entry_field = ""

    __screen = None
    __game_render = None

    __instance = None

    def __init__(self, game_name = "MyGame", window_width = 800, window_height = 600, build_mode = False) -> None:
        """
        The constructor for the Game class. 

        :param game_name: The name which will be used on the game window's title bar. "MyGame" by default.
        :type game_name: str, optional

        :param window_width: The desired width for the game window. '800' by default.
        :type window_width: int, optional

        :param window_height: The desired height for the game window. '600' by default.
        :type window_height: int, optional

        :param build_mode: Enables 'build mode' for this project. 'False' by default.
        :type build_mode: bool, optional
        """
        
        if Game.__instance == None:
            pygame.init()
            if build_mode and not Game.__is_running_through_bundle():
                self.__build_thread = threading.Thread(target=Game.__build_executable, args=[self]);
            else:
                self.__build_thread = None

            if Game.__is_running_through_bundle() == False:
                self.__build_asset_directory()

            window_width = max(8, window_width)
            window_height = max(8, window_height)

            pygame.key.set_repeat(1000, 50)

            self.__overlay = pygame.Surface((window_width, window_height))
            self.__overlay.fill((32, 32, 32, 128))
            self.__game_running = False;
            self.__clock = pygame.time.Clock();
            self.__audio_manager = audio_manager.AudioManager();
            self.__input_manager = input_manager.InputManager();
            self.__world = None
            self.__fill_colour = (0, 0, 0, 255)
        
            pygame.display.set_caption(game_name)
            if(platform.system() == "Windows"):
                ctypes.windll.shcore.SetProcessDpiAwareness(2)
            
            Game.__screen = pygame.display.set_mode([window_width, window_height], pygame.SCALED | pygame.RESIZABLE | pygame.HWSURFACE)
            Game.__game_render = pygame.Surface((window_width, window_height)).convert_alpha()

            Game.__instance = self
        else:
            raise InitialisationDuplicationException("Game has already been initialised. Only one instance of Game may exist at any given time.")
    
    def __start(self) -> None:
        if self.__build_thread is not None:
            self.__build_thread.start();
        
        self.__game_running = True;
        self.__run__();
    
    def __run__(self) -> None:
        while(self.__game_running == True):
            if self.__build_thread is None:
                    self.__standard_event_handler()
            elif self.__build_thread.is_alive() == False:
                self.__game_running = False

            if self.__build_thread is None: 
                self.__update();
            else:
                Game.__build_time += self.__clock.tick(60) / 1000;
                if Game.__build_time > 1.0:
                    Game.__build_time = 0
                    Game.__build_periods += "."
                    if Game.__build_periods == "....":
                        Game.__build_periods = ""
                self.__world.draw_text("Building " + pygame.display.get_caption()[0]+ ".exe" + Game.__build_periods, 0, 0)
            self.__render();
 
        sleep(0.5)
        pygame.quit();

    def __standard_event_handler(self) -> None:
        for event in pygame.event.get():
            Game.__text_entry_field = ''
            if event.type == pygame.QUIT or (Game.__is_running_through_bundle() == False and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.__game_running = False;
            if event.type == self.__audio_manager.BGM_LOOP_EVENT:
                self.__audio_manager._AudioManager__restart_bgm_loop()
            if event.type == pygame.MOUSEWHEEL:
                self.__input_manager._InputManager__set_mouse_scroll_delta(event.y)


    def __text_entry_event_handler() -> None:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if Game.__text_entry_toggle == True:
                    if event.key == pygame.K_RETURN:
                        Game.__text_entry_toggle = False
                    elif event.key == pygame.K_BACKSPACE:
                        Game.__text_entry_field = Game.__text_entry_field[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        Game.__text_entry_field = ""
                        Game.__text_entry_toggle = False
                    else:
                        Game.__text_entry_field += event.unicode



    def __update(self) -> None:
        delta_time = self.__clock.tick(60) / 1000;
        self.__input_manager._InputManager__update(pygame.key.get_pressed());
        self.__world._update(delta_time);
    
        input_manager.InputManager._InputManager__set_mouse_scroll_delta(0)
    

    def __render(self) -> None:
        Game.__screen.fill(self.__fill_colour)
        Game.__game_render.fill(self.__fill_colour)

        self.__world._render(Game.__game_render);
        Game.__screen.blit(pygame.transform.smoothscale(Game.__game_render, Game.__screen.get_size()).convert_alpha(), (0,0))

        # Flip the display
        pygame.display.update(self.__screen.get_rect())


    def start_world(self, new_screen : 'World') -> None:
        """
        Starts a new World after ending the current one (if it exists).

        :param new_screen: The instance of the desired World sub-class that should be started.
        :type new_screen: World
        """
        if self.__world is not None:
            self.__world._end();

        self.__world = new_screen;
        if self.__build_thread is None:
            self.__world._start()

        if(self.__game_running == False):
            self.__start();


    def end(self):
        """
        Ends the game.
        """
        self.__game_running = False


    def __get_window_width(self) -> int:
        return self.__screen.get_rect().width
    

    def __get_window_height(self) -> int:
        return self.__screen.get_rect().height
    

    def set_background_colour(self, red : int, green : int, blue : int) -> None:
        """
        Sets the background fill of the game window to the desired colour.

        :param red: The red component of the colour. Must be a value between 0 and 255.
        :type red: int
        :param green: The green component of the colour. Must be a value between 0 and 255.
        :type green: int
        :param blue: The blue component of the colour. Must be a value between 0 and 255.
        :type blue: int
        """
        red = max(0, min(red, 255))
        green = max(0, min(green, 255))
        blue = max(0, min(blue, 255))
        self.__fill_colour = (red, green, blue)


    def get_random_number(self, maximum : int) -> int:
        """
        Generates a random integer value.

        :param maximum: The maximum bound of the random number generator.
        :type maximum: int

        :return: An integer value between 0 and the maximum (exclusive).
        :rtype: int
        """
        if maximum > 0:
            return randint(0, maximum - 1)
        else:
            return 0
        

    def ask(prompt : str) -> str:
        """
        Get input from the user. The game will be frozen while text is being entered.

        :param prompt: The prompt string which will be displayed to the player.
        :type prompt: str

        :return: A string value containing the user's entered text.
        :rtype: str
        """
        Game.__text_entry_toggle = True

        #font = Game.__get_font("Arial", 24, True)
        font = pygame.font.SysFont("Consolas", 24)
        overlay = pygame.Surface(Game.__screen.get_rect().size).convert_alpha()
        overlay.fill((64, 64, 64, 128))
        Game.__game_render.blit(overlay, (0,0))

        text_box = pygame.Surface((Game.__game_render.get_size()[0], 72))
        text_box.fill((0, 0, 0))
        ticks = 0
        showEntryBox = True
        while Game.__text_entry_toggle == True:
            Game.__text_entry_event_handler()
            ticks += 1
            if ticks >= 50:
                ticks = 0
                showEntryBox = not showEntryBox

            fresh_render = Game.__game_render.copy()
            prompt_surface = font.render(prompt, True, pygame.Color(255, 255, 32))
            if showEntryBox:
                text_surface = font.render("<< " + Game.__text_entry_field + "\u258C", True, pygame.Color(255, 255, 255))
            else:
                text_surface = font.render("<< "+ Game.__text_entry_field, True, pygame.Color(255, 255, 255))
            
            text_y = 32 + max(0, 32 - text_surface.get_height())
            fresh_render.blit(text_box, (0, 0))
            fresh_render.blit(prompt_surface, (10, 5))
            fresh_render.blit(text_surface, (10, text_y))
            Game.__screen.blit(pygame.transform.smoothscale(fresh_render, Game.__screen.get_size()), (0,0))
            
            # Flip the display
            pygame.display.update(Game.__screen.get_rect())

        return Game.__text_entry_field

        

    def __get_font(filename : str, font_size : int, is_system_font = False) -> pygame.freetype.Font:
        try:
            if filename not in Game.__fonts:
                if is_system_font:
                    Game.__fonts[filename] = pygame.freetype.SysFont(filename, font_size)
                else:
                    filename = "assets/" + filename
                    #Game.__build_asset(filename)
                    Game.__fonts[filename] = pygame.freetype.Font(filename, font_size)
        except FileNotFoundError:
            raise FileNotFoundError("Font file [" + filename + "] not found.")

        return Game.__fonts[filename]


    def __get_texture(filename : str) -> pygame.Surface:
        try:
            filename = "assets/" + filename
            if filename not in Game.__textures:
                #Game.__build_asset(filename)
                Game.__textures[filename] = pygame.image.load(filename).convert_alpha()
        except FileNotFoundError:
            raise FileNotFoundError("Texture file [" + filename + "] not found")

        return Game.__textures[filename]


    def __get_audio(filename : str) -> pygame.mixer.Sound:
        try:
            filename = "assets/" + filename
            if filename not in Game.__audio:
                #Game.__build_asset(filename)
                Game.__audio[filename] = pygame.mixer.Sound(filename)
        except FileNotFoundError:
            raise FileNotFoundError("Audio file [" + filename + "] not found.")
        
        return Game.__audio[filename]
    

    def __build_executable(self) -> None:
        subprocess.run("pyinstaller --onefile -w main.py --name " + pygame.display.get_caption()[0].replace(" ", ""), shell = True)
        self.__world.draw_text("Build complete.", 0, 50)
        self.__game_running = False


    def __build_asset_directory(self) -> None:
        if os.path.exists("assets/") == False:
            os.makedirs("assets/")
            #raise MissingDirectoryException("No \'assets\' folder found in the root directory of this game. Please create one in the same directory as this game\'s \'main.py\' file, then try running again.")
        else:
            asset_directory = "dist/assets/"
            if os.path.exists(asset_directory) == False:
                    os.makedirs(asset_directory)

            shutil.copytree("assets/", asset_directory, dirs_exist_ok=True)


    def __build_asset(filename : str) -> None:
        if __debug__ and not Game.__is_running_through_bundle():
            directory = "dist/" + Game.__get_directory_from_full_path(filename)
            if os.path.exists(directory) == False:
                os.makedirs(directory)
            if os.path.exists("dist/" + filename) == False:
                shutil.copy(filename, "dist/" + filename)


    def __is_running_through_bundle() -> bool:
        return (getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'))


    def __get_directory_from_full_path(full_path : str) -> str:
        return full_path[ : full_path.rfind("/")]
    

class InitialisationDuplicationException(Exception):
    pass

class MissingDirectoryException(Exception):
    pass
