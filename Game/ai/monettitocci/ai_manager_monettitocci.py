from base.option_descriptor import OptionDescriptor
from languages.asp.asp_mapper import ASPMapper
from languages.asp.asp_input_program import ASPInputProgram
from specializations.clingo.desktop.clingo_desktop_service import ClingoDesktopService
from platforms.desktop.desktop_handler import DesktopHandler


# Our classes
from ..ai_manager import AIManager        # Superclass
from player import Player
from timekeeper import Timekeeper
from wall import Wall
from .path_resolver import PathResolver
from .callback_monettitocci import CallbackMonettiTocci

import platform
import time

class AIManagerMonettiTocci(AIManager):
    def __init__(self,asp_path):
        super().__init__()

        # Register classes
        #ASPMapper.get_instance().register_class(Player)
        
        self.asp_path = asp_path
        self.my_id = None

    def prepare_programs_for_turn(self, players, asp_path):
        try:
            # Clear all the programs (even the fixed one, because every player has its own)
            self.input_fixed_program.clear_all()
            self.fill_fixed_program(asp_path)                       # Fill the fixed program
            self.input_variable_program.clear_all()                 # Clear the variable program
            #self.input_variable_program.add_objects_input(players)  # Add the players objects to the variable program

            if self.my_id is not None:
                self.input_variable_program.add_program("myId(" + str(self.my_id) + ").") # Add the current player id to the variable program

                self.path_resolver = PathResolver(players, self.my_id)
                self.path_resolver.generate_min_paths_cost()
                # Add the cost limits to the variable program
                ## Put the cost limits in the following format: [(player_id, cost_limit), ...] in a list
                cost_limits = self.path_resolver.get_cost_limits()
                
                for cost_limit in cost_limits:
                    self.input_variable_program.add_program(f"costLimit({cost_limit[0]},{cost_limit[1]}).")

                # Add the min paths cost to the variable program
                min_paths_cost = self.path_resolver.get_min_paths_cost()

                for cost in min_paths_cost:
                    self.input_variable_program.add_program(f"minDistance({cost[0]},cell({cost[1][0]},{cost[1][1]}),cell({cost[2][0]},{cost[2][1]}),{cost[3]}).")
            else:
                raise Exception("my_id is None")

            # Add the players to the variable program
            for player in players:
                self.input_variable_program.add_program(self.__generate_player_string_for_program(player))

            # Add the walls to the variable program
            for player in players:
                for wall in player.walls:
                    self.input_variable_program.add_program(self._generate_full_wall_string_for_program(wall))
            
            #self.print_programs()
        except Exception as e:
            self._raise_exception(e)

    def ask_for_a_move(self, current_player_id, players):
        self.my_id = current_player_id
        self.prepare_programs_for_turn(players, self.asp_path)

        my_player = players[current_player_id-1]

        try:
            start_time = self.timekeeper.get_start_time()
            MAX_TURN_DURATION_SECONDS = self.timekeeper.MAX_TURN_DURATION_SECONDS
            
            # Create the callback object, which receives the current player, the current turn start time, and the turn's maximum duration
            my_callback = CallbackMonettiTocci(my_player,start_time,MAX_TURN_DURATION_SECONDS)
            
            # Start the program asyncronously
            self.handler.start_async(my_callback)
        except Exception as e:
            self._raise_exception(e)
    
    def _prepare_handler(self):
        self.os = platform.system()

        if self.os == "Windows":    # Windows
            self.handler = DesktopHandler(ClingoDesktopService("executables\clingo.exe")) 
        elif self.os == "Linux":    # Linux
            self.handler = DesktopHandler(ClingoDesktopService("executables/./clingo"))
        else:
            raise Exception("OS not supported")

    def __generate_player_string_for_program(self, player):
        return f'player({player.id},cell({player.r},{player.c}),{player.remaining_walls},"{player.goal}").'

    def _generate_full_wall_string_for_program(self,wall):
        return(f"wall(cell({wall[0].cell1[0]},{wall[0].cell1[1]}),cell({wall[0].cell2[0]},{wall[0].cell2[1]}),cell({wall[1].cell1[0]},{wall[1].cell1[1]}),cell({wall[1].cell2[0]},{wall[1].cell2[1]})).")
        