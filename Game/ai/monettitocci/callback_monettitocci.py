from base.callback import Callback
from languages.asp.answer_set import AnswerSet

from wall import Wall

import time

class CallbackMonettiTocci(Callback):
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
                    if atom.startswith("newPos"):
                        new_pos = self.__parse_new_pos(atom)
                        self.player.new_position(new_pos[0],new_pos[1])
                    elif atom.startswith("newWall"):
                        new_wall = self.__parse_new_wall(atom)
                        self.player.place_wall(new_wall)
                    else:
                        self._raise_exception(e)
        except Exception as e:
            self._raise_exception(e)
    
    def __parse_new_pos(self, atom):
        # newPos(cell(R,C))
        return (int(atom[12]), int(atom[14]))

    def __parse_new_wall(self, atom):
        # newWall(cell(R1,C1),cell(R2,C2),cell(R3,C3),cell(R4,C4))
        return (Wall((int(atom[13]),int(atom[15])), (int(atom[23]),int(atom[25]))), Wall((int(atom[33]),int(atom[35])), (int(atom[43]),int(atom[45]))))

        