from platforms.desktop.desktop_handler import DesktopHandler
from specializations.dlv2.desktop.dlv2_desktop_service import DLV2DesktopService
from base.option_descriptor import OptionDescriptor
from languages.asp.asp_mapper import ASPMapper
from languages.asp.asp_input_program import ASPInputProgram
from languages.asp.symbolic_constant import SymbolicConstant

import platform
from time import sleep

# Our classes
from player import Player
from timekeeper import Timekeeper
from wall import Wall
from my_callback import MyCallback

class AIManager():
    def __init__(self):
        try:
            # TODO: Gestire per ogni OS, ricordarsi che ogni OS gestisce gli slash in modo diverso
            self.__prepare_handler()

            self.input_fixed_program, self.input_variable_program = ASPInputProgram(), ASPInputProgram()

            # Add the program(s) to the handler
            self.handler.add_program(self.input_fixed_program)
            self.handler.add_program(self.input_variable_program)

            # Register classes
            ASPMapper.get_instance().register_class(Player)
            ASPMapper.get_instance().register_class(Wall)


        except Exception as e:
            self.__raise_exception(e)

    # TODO: Aggiungere nomi files quando saranno creati
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
                self.__raise_exception(e)

    def prepare_programs_for_turn(self, players, asp_path):
        try:
            # Clear all the programs (even the fixed one, because every player has its own)
            self.input_fixed_program.clear_all()
            self.fill_fixed_program(asp_path)                       # Fill the fixed program
            self.input_variable_program.clear_all()                 # Clear the variable program
            self.input_variable_program.add_objects_input(players)  # Add the players objects to the variable program

            # Add the walls to the variable program
            for player in players:
                for wall in player.walls:
                    self.input_variable_program.add_program(self.__generate_full_wall_string_for_program(wall))

            self.__generate

        except Exception as e:
            self.__raise_exception(e)

    def ask_for_a_move(self,player):
        timekeeper = Timekeeper()
        try:
            # Create the callback object, which receives the current player, the current turn start time, and the maximum duration
            my_callback = MyCallback(player,timekeeper.get_start_time(),timekeeper.MAX_TURN_DURATION_SECONDS)
            
            # Start the program asyncronously
            self.handler.start_async(my_callback)
        except Exception as e:
            self.__raise_exception(e)

    def print_programs(self):
        try:
            print("Fixed program:")
            print(self.input_fixed_program.get_programs())
            print("Variable program:")
            print(self.input_variable_program.get_programs())
        except Exception as e:
            self.__raise_exception(e)
        

    def __prepare_handler(self):
        self.os = platform.system()

        if self.os == "Windows":    # Windows
            self.handler = DesktopHandler(DLV2DesktopService("executables\dlv-2.1.1-win64.exe")) 
        elif self.os == "Linux":    # Linux
            self.handler = DesktopHandler(DLV2DesktopService("executables/./dlv-2.1.1-linux-x86_64"))
        elif self.os == "Darwin":    # MacOS
            self.handler = DesktopHandler(DLV2DesktopService("executables/./dlv-2.1.1-macos-12.2"))
        else:
            raise Exception("OS not supported")

    def __raise_exception(self, e):
        raise Exception(str(e))

    def __generate_full_wall_string_for_program(self,wall):
        return(f"wall({wall[0].cell1[0]},{wall[0].cell1[1]},{wall[0].cell2[0]},{wall[0].cell2[1]},{wall[1].cell1[0]},{wall[1].cell1[1]},{wall[1].cell2[0]},{wall[1].cell2[1]}).")
