from final_Puzzle import Puzzle
from final_Status_board import Status_board
from final_Interface import Interface
import time

def initialize():
    #speed and hide all turtle and set screen size
    puzzle.turtle.speed(0)
    status_board.turtle.speed(0)
    interface.turtle.speed(0)
    puzzle.hide()
    status_board.hide()
    interface.hide()
    puzzle.screen.setup (width=800, height=800)
    
    # show the splash and build the interface
    puzzle.prompt('Resources/splash_screen.gif')
    interface.build_interface(puzzle.screen)
    
    #show th default puzzle
    puzzle.load_image()
    puzzle.sequence = puzzle.create_sequence(True)
    puzzle.create_puzzle()

def game(x, y):
    # stop detect click to proevent multiple click
    puzzle.screen.onclick(None)
    # active function if click the button
    button = interface.check_button(x,y)
    if button:
        puzzle.button_press(button)    
    else:
        # switch the tile if vaild click
        switch = puzzle.switch(x, y)
            
        if switch:
            # update the status board
            status_board.update(puzzle.pics_info['move'])
            # check if the puzzle is finish
            if puzzle.check_win():
                # prompt the win message and show the credits
                puzzle.prompt('Resources/winner.gif')
                puzzle.prompt('Resources/credits.gif')

                #close the window and store the record
                puzzle.screen.bye()
                interface.leader_board(True, puzzle.pics_info['move'])
            # move over the limit
            elif puzzle.pics_info['move'] >= interface.move_limit:
                # prompt the lose message and show the credits
                puzzle.prompt('Resources/Lose.gif')
                puzzle.prompt('Resources/credits.gif')

                 #close the window
                puzzle.screen.bye()
                
    # restart detecting click
    puzzle.screen.onclick(game)

def main():
    try:
        # build the turtle
        global status_board, interface, puzzle
        status_board = Status_board()
        interface =Interface()
        puzzle = Puzzle()
        initialize()
        
        # detect the click
        puzzle.screen.onclick(game)
        puzzle.screen.mainloop()
        
    except Exception as error:
        # show file error message and store it
        puzzle.log_error(error)
        
        #close the window
        puzzle.screen.bye()

if __name__ == '__main__':
    main()
