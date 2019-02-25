import random

class RollDice:
    def __init__(self):
        pass
            
    #generate a number with a base of one to six
    #if d increases the base by a multiple of one and six
    def roll_d6(self, d=1):
        start = 1 * d
        end   = 6 * d
        return(random.randint(start,end))
