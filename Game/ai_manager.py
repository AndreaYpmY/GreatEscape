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
            self.__raise_exception__(e)

    # TODO: Aggiungere nomi files quando saranno creati
    def fill_fixed_program(self,asp_path):
        try:
            f = open(asp_path, "r")
        except Exception as e:
            self.__raise_exception__(e)

        for line in f:
            # Doesn't add comments and empty lines to the program
            if line.startswith("%") or line.startswith("\n"):
                continue
            try:
                self.input_fixed_program.add_program(line)
            except Exception as e:
                self.__raise_exception__(e)

    def prepare_programs_for_turn(self, players, asp_path):
        try:
            # Clear all the programs (even the fixed one, because every player has its own)
            self.input_fixed_program.clear_all()
            #self.fill_fixed_program(asp_path)                       # Fill the fixed program
            self.input_variable_program.clear_all()                 # Clear the variable program
            self.input_variable_program.add_objects_input(players)  # Add the players objects to the variable program

            # Add the walls to the variable program
            for player in players:
                for wall in player.walls:
                    self.input_variable_program.add_program(self.__generate_full_wall_string_for_program__(wall))

        except Exception as e:
            self.__raise_exception__(e)

    def get_answer_sets(self):
        try:
            answer_sets = self.handler.start_sync()
            return answer_sets
        except Exception as e:
            self.__raise_exception__(e)

    # TODO: Controllare il funzionamento di questo metodo, perchè non credo funzioni
    def do_next_move(self,player):
        try:
            answer_sets = self.get_answer_sets()
            for answer_set in answer_sets:
                for predicate in answer_set.get_predicates():
                    if predicate.get_predicate_name() == "newPos":
                        r = predicate.get_predicate_argument(1)
                        c = predicate.get_predicate_argument(2)
                        player.new_position(r,c)
                        break
                    elif predicate.get_predicate_name() == "newWall":
                        # TODO: Gestire i nuovi muri da ASP
                        pass
        except Exception as e:
            self.__raise_exception__(e)

    def print_programs(self):
        try:
            print("Fixed program:")
            print(self.input_fixed_program.get_programs())
            print("Variable program:")
            print(self.input_variable_program.get_programs())
        except Exception as e:
            self.__raise_exception__(e)
        

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

    def __raise_exception__(self, e):
        raise Exception("Error: " + str(e))

    def __generate_full_wall_string_for_program__(self,wall):
        return(f"wall({wall[0].cell1[0]},{wall[0].cell1[1]},{wall[0].cell2[0]},{wall[0].cell2[1]},{wall[1].cell1[0]},{wall[1].cell1[1]},{wall[1].cell2[0]},{wall[1].cell2[1]}).")
