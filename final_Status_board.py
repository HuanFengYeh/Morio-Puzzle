import turtle
import time
class Status_board():
    '''
        Status_board is a class for updatting the move steps
    '''
    def __init__(self):
        # create a turtle
        self.turtle = turtle.Turtle()

    def hide(self):
        '''
        Fucntion: hide
            hide the turtle
        '''
        self.turtle.hideturtle()
        self.turtle.penup()
        
    def update(self, move):
        '''
        Fucntion: update
            update the steps show on canvas
        Parameter:
            move(int): current total movement
        '''
        # set the writting infomation
        sentence = f"Player moves : {move}"
        font_size = 35
        location = [-300, -285]

        #clear the old writting and update a new one
        t = self.turtle
        t.clear()
        t.goto(location[0], location[1])
        t.pendown()
        t.write(sentence, font =( 'Arial', font_size, 'normal'))
        t.penup()


    
