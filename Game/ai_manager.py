from platforms.desktop.desktop_handler import DesktopHandler
from specializations.dlv2.desktop.dlv2_desktop_service import DLV2DesktopService
from base.option_descriptor import OptionDescriptor
from languages.asp.asp_mapper import ASPMapper
from languages.asp.asp_input_program import ASPInputProgram
from languages.asp.symbolic_constant import SymbolicConstant

# Our classes
from player import Player
from wall import Wall
import platform

class AIManager():
    def __init__(self):
        try:
            # TODO: Gestire per ogni OS, ricordarsi che ogni OS gestisce gli slash in modo diverso
            self.__prepare_handler__()

            self.input_fixed_program, self.input_variable_program = ASPInputProgram(), ASPInputProgram()

            # Add the program(s) to the handler
            self.handler.add_program(self.input_fixed_program)
            self.handler.add_program(self.input_variable_program)

            # Register classes
            ASPMapper.get_instance().register_class(Player)
            ASPMapper.get_instance().register_class(Wall)


        except Exception as e:
            print(e)

    # TODO: Aggiungere nomi files quando saranno creati
    def fill_fixed_program(self,asp_path):
        f = open(asp_path, "r")

        for line in f:
            # Doesn't add comments and empty lines to the program
            # TODO: Controllare se il ritorno a capo funzioni con tutti i sistemi operativi
            if line.startswith("%") or line.startswith("\n"):
                continue
            self.input_fixed_program.add_program(line)

    def prepare_programs_for_turn(self, players, asp_path):
        # self.input_fixed_program.clear_all()
        # self.fill_fixed_program(asp_path)
        self.input_variable_program.clear_all()
        self.input_variable_program.add_objects_input(players)

        for player in players:
            for wall in player.walls:
                self.input_variable_program.add_object_input(wall[0])
                self.input_variable_program.add_object_input(wall[1])

    def print_programs(self):
        print("Fixed program:")
        print(self.input_fixed_program.get_programs())
        print("Variable program:")
        print(self.input_variable_program.get_programs())
        

    def __prepare_handler__(self):
        self.os = platform.system()

        if self.os == "Windows":    # Windows
            self.handler = DesktopHandler(DLV2DesktopService("executables\dlv-2.1.1-win64.exe")) 
        elif self.os == "Linux":    # Linux
            self.handler = DesktopHandler(DLV2DesktopService("executables/./dlv-2.1.1-linux-x86_64"))
        elif self.os == "Darwin":    # MacOS
            self.handler = DesktopHandler(DLV2DesktopService("executables/./dlv-2.1.1-macos-12.2"))
        else:
            raise Exception("OS not supported")
