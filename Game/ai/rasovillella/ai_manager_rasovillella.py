from base.option_descriptor import OptionDescriptor
from languages.asp.asp_mapper import ASPMapper
from languages.asp.asp_input_program import ASPInputProgram
from specializations.clingo.desktop.clingo_desktop_service import ClingoDesktopService
from platforms.desktop.desktop_handler import DesktopHandler
from ..ai_manager import AIManager        # 
from timekeeper import Timekeeper
from .callback_rasovillella import CallbackRasoVillella
from .path_resolver import PathResolver
from .path import Path

import sys
sys.path.append("..\\..")
from player import Player
from wall import Wall


class AIManagerRasoVillella(AIManager):

    def __init__(self,asp_path):
        super().__init__()
        self.my_path_resolver : PathResolver
        self.enemy_path_resolver : PathResolver
        self.init_path_resolver = 1
        self.asp_path = asp_path
        ASPMapper.get_instance().register_class(Player)
        ASPMapper.get_instance().register_class(Wall)
        ASPMapper.get_instance().register_class(Path)
        

    def prepare_programs_for_turn(self, players):
        try:
            self.input_fixed_program.clear_all()
            self.fill_fixed_program(self.asp_path)
            self.input_variable_program.clear_all()
            self.input_variable_program.add_objects_input(players)  # Add the players objects to the variable program
            self.input_variable_program.add_program(f"myId({self.myId}).")
            self.findPath()
            self.addPath()
            for player in players:
                for wall in player.walls:
                    self.input_variable_program.add_program(self._generate_full_wall_string_for_program(wall))

            # self.print_programs()
            # print("##############FIXED##############\n")
            print("Variable program:")
            print(self.input_variable_program.get_programs())
            print("##############FIXED##############\n")

        except Exception as e:
            self._raise_exception(e)
        
        
    def ask_for_a_move(self, myId, players):

        self.myId = myId

        for player in players:
            if(player.id == myId):
                self.my_path_resolver = PathResolver(players,myId)
            else:
                self.enemy_path_resolver = PathResolver(players,player.id)

        self.prepare_programs_for_turn(players)


        my_player = players[self.myId-1]

        try:
            start_time = self.timekeeper.get_start_time()
            MAX_TURN_DURATION_SECONDS = self.timekeeper.MAX_TURN_DURATION_SECONDS
            my_callback = CallbackRasoVillella(my_player,start_time,MAX_TURN_DURATION_SECONDS)

            self.handler.start_async(my_callback)
        except Exception as e:
            self._raise_exception(e)

    def findPath(self):
        self.my_path_resolver.findMinPath()
        self.enemy_path_resolver.findMinPath()

    def addPath(self):
        self.input_variable_program.add_objects_input(self.my_path_resolver.path)
        self.input_variable_program.add_objects_input(self.enemy_path_resolver.path)
