from base.callback import Callback
from threading import Lock

import time

class MyCallback(Callback):
    def __init__(self,player,start_time,MAX_TURN_DURATION_SECONDS):
        self.player = player
        self.start_time = start_time
        self.MAX_TURN_DURATION_SECONDS = MAX_TURN_DURATION_SECONDS
    
    def callback(self,output):
        # TODO: Gestire il timeout
        print("Elapsed time: " + str(time.time() - self.start_time)) 
        if time.time() - self.start_time > self.MAX_TURN_DURATION_SECONDS:
            print("Callback timeout, random move will be played")
            return
        self.do_next_move(self.player,output)

    # TODO: Controllare il funzionamento di questo metodo, perchè non credo funzioni
    def do_next_move(self,player,answer_sets):
        try:
            for answer_set in answer_sets.get_optimal_answer_sets():
                for predicate in answer_set.get_predicates():
                    if predicate.get_predicate_name() == "newPos":
                        r = predicate.get_predicate_argument(1)
                        c = predicate.get_predicate_argument(2)
                        self.player.new_position(r,c)
                        break
                    elif predicate.get_predicate_name() == "newWall":
                        # TODO: Gestire i nuovi muri da ASP
                        pass
        except Exception as e:
            self.__raise_exception(e)
    
    def __raise_exception(self, e):
        raise Exception(str(e))
        