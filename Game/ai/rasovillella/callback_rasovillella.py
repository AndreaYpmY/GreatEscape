from base.callback import Callback
from languages.asp.answer_set import AnswerSet

from wall import Wall

import time

class CallbackRasoVillella(Callback):
    def __init__(self,player,start_time,MAX_TURN_DURATION_SECONDS):
        self.player = player
        self.start_time = start_time
        self.MAX_TURN_DURATION_SECONDS = MAX_TURN_DURATION_SECONDS
    

    def callback(self,output):
        print("Elapsed time: " + str(time.time() - self.start_time)) 
        if time.time() - self.start_time > self.MAX_TURN_DURATION_SECONDS:
            print("Callback timeout, random move will be played")
            return
        self._do_next_move(output)

    def _do_next_move(self,output):
        try:
            for answer_set in output.get_optimal_answer_sets():
                print(answer_set.get_answer_set())
                for atom in answer_set.get_answer_set():
                    if atom.startswith("muovi"):
                        new_pos = self.__parse_new_pos(atom)
                        self.player.new_position(new_pos[0],new_pos[1])
                    elif atom.startswith("scegliMuro"):
                        new_wall = self.__parse_new_wall(atom)
                        self.player.place_wall(new_wall)
                    else:
                        self._raise_exception(e)
        except Exception as e:
            self._raise_exception(e)
    
    def __parse_new_pos(self, atom):
        # muovi(ID,R,C)
        return (int(atom[8]), int(atom[10]))
        

    def __parse_new_wall(self, atom):
        # scegliMuro(R1,C1,R2,C2,R3,C3,R4,C4)
        return (Wall((int(atom[11]),int(atom[13])), (int(atom[15]),int(atom[17]))), Wall((int(atom[19]),int(atom[21])), (int(atom[23]),int(atom[25]))))