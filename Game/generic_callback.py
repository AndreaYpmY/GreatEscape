from base.callback import Callback
from languages.asp.answer_set import AnswerSet

import time

class GenericCallback(Callback):
    def __init__(self,player,start_time,MAX_TURN_DURATION_SECONDS):
        self.player = player
        self.start_time = start_time
        self.MAX_TURN_DURATION_SECONDS = MAX_TURN_DURATION_SECONDS
    
    '''
    TO BE OVERRIDDEN IN !!!YOUR!!! CHILD CLASS

    This method is called when the callback is triggered.
    output: AnswerSets object.
    '''
    def callback(self,output):
        raise NotImplementedError("This method must be implemented in the child class")

    '''
    You can call this method in your callback to handle your next move.
    output: AnswerSets object.
    '''
    def _do_next_move(self,output):
        raise NotImplementedError("This method must be implemented in the child class")

    def _raise_exception(self, e):
        raise Exception(str(e))
        