from platforms.desktop.desktop_handler import DesktopHandler
from specializations.dlv2.desktop.dlv2_desktop_service import DLV2DesktopService
from languages.asp.asp_mapper import ASPMapper
from languages.asp.asp_input_program import ASPInputProgram

import platform
from time import sleep

# Our classes
from player import Player
from timekeeper import Timekeeper
from wall import Wall
from generic_callback import GenericCallback

class AIManager():
    def __init__(self):
        try:
            self._prepare_handler()
            self.timekeeper = Timekeeper()
            self.input_fixed_program, self.input_variable_program = ASPInputProgram(), ASPInputProgram()

            # Add the program(s) to the handler
            self.handler.add_program(self.input_fixed_program)
            self.handler.add_program(self.input_variable_program)

            # Register classes (if needed)
            # ASPMapper.get_instance().register_class(Player)
            # ASPMapper.get_instance().register_class(Wall)


        except Exception as e:
            self._raise_exception(e)

    def fill_fixed_program(self,asp_path):
        try:
            f = open(asp_path, "r")
        except Exception as e:
            self.__raise_exception(e)

        for line in f:
            # Doesn't add comments and empty lines to the program
            if line.startswith("%") or line.startswith("\n"):
                continue
            try:
                self.input_fixed_program.add_program(line)
            except Exception as e:
                self._raise_exception(e)

    
    ''' 
    TO BE OVERRIDDEN IN !!!YOUR!!! CHILD CLASS

    players: list of Player objects, each one representing a player, with its own walls
    asp_path: path to the ASP file
    '''
    def prepare_programs_for_turn(self, players, asp_path):
        raise NotImplementedError("This method must be implemented in the child class")
    

    ''' 
    TO BE OVERRIDDEN IN !!!YOUR!!! CHILD CLASS
    
    player: the current player

    you can also choose to pass more parameters, if you need them
    '''
    def ask_for_a_move(self,player):
        raise NotImplementedError("This method must be implemented in the child class")

    def print_programs(self):
        try:
            print("Fixed program:")
            print(self.input_fixed_program.get_programs())
            print("Variable program:")
            print(self.input_variable_program.get_programs())
        except Exception as e:
            self._raise_exception(e)
        

    def _prepare_handler(self):
        self.os = platform.system()

        if self.os == "Windows":    # Windows
            self.handler = DesktopHandler(DLV2DesktopService("executables\dlv-2.1.1-win64.exe")) 
        elif self.os == "Linux":    # Linux
            self.handler = DesktopHandler(DLV2DesktopService("executables/./dlv-2.1.1-linux-x86_64"))
        elif self.os == "Darwin":    # MacOS
            self.handler = DesktopHandler(DLV2DesktopService("executables/./dlv-2.1.1-macos-12.2"))
        else:
            raise Exception("OS not supported")

    def _raise_exception(self, e):
        raise Exception(str(e))

    def _generate_full_wall_string_for_program(self,wall):
        return(f"wall({wall[0].cell1[0]},{wall[0].cell1[1]},{wall[0].cell2[0]},{wall[0].cell2[1]},{wall[1].cell1[0]},{wall[1].cell1[1]},{wall[1].cell2[0]},{wall[1].cell2[1]}).")
