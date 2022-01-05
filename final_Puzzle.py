import turtle
import time
import random
class Puzzle ():
    '''
        puzzle is a class for creating the puzzle and dominating
        the puzzle function
    '''

    def __init__(self, puzzle = 'mario.puz'):
        self.turtle = turtle.Turtle()   # create a turtle for puzzle
        self.screen = turtle.Screen()   # opena tutrle screen 
        self.stamp_dictionary = {}  # record the picture stamp
        self.puzzle = puzzle    # record the current puzzle name
        self.pics_info = {} # record the puzzle information
        self.blank_order = 0   #record the current blank order
        self.sequence = []  # record the puzzle sequence
        
    def hide(self):
        '''
        Fucntion: hide
            hide the turtle
        '''
        self.turtle.hideturtle()
        self.turtle.penup()
        
    def show(self):
        '''
        Fucntion: show
            show the turtle
        '''
        self.turtle.showturtle()
        self.turtle.pendown()

    def square(self):
        '''
        Fucntion: square
            darwing the sqaure around the picture
        '''
        # setting the turtle to the right-left of picture
        # and heading to 0 degree
        t = self.turtle
        self.hide()
        size = int(self.pics_info['size'])
        square_x, square_y = t.position()
        t.goto(square_x - size / 2, square_y + size / 2)
        t.setheading(0)
        t.pendown()
        # draw the square
        for i in range(1,5): 
            t.forward(size)
            t.right(90)
        t.penup()
        t.goto(square_x, square_y)

    def load_image(self):
        '''
        Fucntion: load_image
            store the puzzle information from .puz
        '''
        with open(self.puzzle, mode='r') as document:
            pics_info = {}
            for sentence in document:
                sentence = sentence.split()
                length = len(sentence[0]) - 1
                # record the blank tile's title
                if sentence[1][len(sentence[1])- 9:] == 'blank.gif':
                    pics_info['blank_number'] = sentence[0][:length]
                # create a title: path dictionary
                pics_info[sentence[0][:length]] = sentence[1]
                
        # initialize the step
        pics_info['move'] = 0
        # check file data
        self.check_data(pics_info)
        # store data
        self.pics_info = pics_info

    def check_data(self, pics_info):
        '''
            Function: check_data
                check if the data is malformed data
            Parameter:
                pics_info(dictionary): the file data
        '''
        valid_number = ['4', '9', '16']
        ckeck_title = ['name', 'number', 'size', 'thumbnail']
        # check miss titles
        for title in ckeck_title:
            if title not in pics_info:
                print(title, pics_info)
                raise ValueError

        # check bad data
        if not 50< int(pics_info['size']) < 110 or\
           pics_info['number'] not in valid_number:
            raise ValueError
            
            
    def create_sequence(self, suffle):
        '''
        Fucntion: sequence
            create the image sequence and return it
        Parameter:
            number(int): number of pictures
            shuffle(boolean): shuffle the sequence
        '''
        # create a sorted sequence list with a length of puzzle number
        number = int(self.pics_info['number'])
        sequence = []
        for i in range (number):
            sequence.append(i + 1)

        # suffle the sequence
        if suffle:
            for i in range(number):
                change = random.randint(0, number - 1)
                sequence[i], sequence[change] = sequence[change], sequence[i]
        return sequence
    
    def stamp_image(self, x, y, picture_number):
        '''
        Fucntion: stamp_image
            stamp image on the target coordinate
        Parameter:
            x(int): x coordinate
            y(int): y coordinate
            picture_number(int): the image order number
        '''
        # get the image store location
        file_name = self.pics_info[str(picture_number)]
        t = self.turtle
        s = self.screen

        # go to target coordinate and stamp the image
        t.goto(x, y)
        s.addshape(file_name)
        t.shape(file_name)
        self.show()
        stamp_id = t.stamp()

        # store stamp id and coordinate
        self.stamp_dictionary[picture_number] = stamp_id
        self.stamp_dictionary[stamp_id] = (x, y)
        self.hide()
        
    def create_puzzle(self):
        '''
        Fucntion: create_puzzle
            create puzzle and thumbnail
        Parameter:
            shuffle(boolean): shuffled puzzle
        '''
        # set the right-left tile coordinate
        default_x = now_x = -293
        default_y = now_y = 243

        # caculate the space between images and the x limit of puzzle
        pics_number = int(self.pics_info['number'])
        size = int(self.pics_info['size'])
        space = size + 4
        limit = default_x + space * (pics_number**0.5 - 1)

        # stamp the image according to sequence
        # and record the blank tile's order
        blank_order = 0
        for number in self.sequence:
            if number != int(self.pics_info['blank_number']):
                blank_order += 1
            else:
                blank_order += 1
                self.blank_order = blank_order
            # stamp the image and draw the square around it
            self.stamp_image(now_x, now_y, number)
            self.square()
            # change the line if exceed x limit
            if now_x < limit:
                now_x += space
            else:
                now_y -= space
                now_x = default_x
                
        # stamp the thumbnail
        self.stamp_image(330, 310, 'thumbnail')
    
    def near_blank(self, x, y):
        '''
        Fucntion: near_blank
            check if the coordinate(x,y) near the puzzle 
        Parameter:
            x(int): click x coordinate
            y(int): click y coordinate
        '''
        # get the image's space and puzzle's side number
        side_number = int(self.pics_info['number']) ** 0.5
        size = int(self.pics_info['size'])
        space = size + 4
        
        # get left up vertex of puzzle
        x_left_limit = -293 - size / 2
        y_up_limit = 243 + size / 2

        # get column and row of (x,y)
        row = int((x - x_left_limit) / space) + 1
        column = int((y_up_limit - y) / space) + 1

        # if row or column exceed the limit
        # means (x,y) is not in the puzzle area
        if 0 < row <= side_number and 0 < column <= side_number:
            # if (x,y) near blank tile the order different will be
            # 1, -1, -side_number, side_number
            near_different = [1, -1, -side_number, side_number]
            order = int(side_number * (column - 1)+ row)
            return self.blank_order - order in near_different, order
        else:
            return False, 0
        
    def switch(self, x, y):
        '''
        Fucntion: switch
            switch the selected tile with blank tile
        Parameter:
            x(int): click x coordinate
            y(int): click y coordinate
        '''
        # check the click place
        valid_click, order = self.near_blank(x,y)

        # switch the tiles if it is click a adjacent tile
        if valid_click:
            # get image number of tiles
            tile_number = self.sequence[order - 1]
            blank_number = self.sequence[self.blank_order - 1]

            # get stamp id
            id_tile = self.stamp_dictionary[tile_number]
            id_blank = self.stamp_dictionary[blank_number]

            # clear the tiles' stamp from dictionary
            id_tile_x, id_tile_y = self.stamp_dictionary.pop(id_tile)
            id_blank_x, id_blank_y = self.stamp_dictionary.pop(id_blank)

            # clear the stamps from canvas
            self.turtle.clearstamp(self.stamp_dictionary[tile_number])
            self.turtle.clearstamp(self.stamp_dictionary[blank_number])

            # stamp each others' image on each's original coordinate
            self.stamp_image(id_tile_x, id_tile_y, blank_number)
            self.stamp_image(id_blank_x, id_blank_y,tile_number)

            # change the order
            self.sequence[order - 1], self.sequence[self.blank_order - 1] =\
                                      self.sequence[self.blank_order - 1], self.sequence[order - 1]

            # update blank tile's order and count the step
            self.blank_order = order
            self.pics_info['move'] += 1
        return valid_click

    def clear(self):
        '''
        Fucntion: clear
            clear all stamp and drawing
        '''
        for stamp in self.stamp_dictionary.values():
            self.turtle.clearstamp(stamp)
        self.turtle.clear()

    def check_win(self):
        '''
        Fucntion: check_in
            check if the puzzle is finished
        '''
        # if sequenc equal to unshuffle sequence than it is finished
        return self.sequence == self.create_sequence(False)

    def prompt(self, file_name):
        '''
        Fucntion: prompt
            prompt the message
        Parameter:
            file_name(string): the prompt image store location
        '''
        t = self.turtle
        s = self.screen

        #show the prompt in the middle of screen
        t.goto(0, 0)
        s.addshape(file_name)
        t.shape(file_name)
        self.show()
        stamp_id = t.stamp()
        s.update()
        # wait for two second and clear the prompt
        time.sleep(2)
        t.clearstamp(stamp_id)
        self.hide()
        s.update()
        
    def resetbutton(self):
        '''
        Fucntion: resetbutton
            reset the puzzle to sorted version
        '''
        # clear the original puzzle and create a unshuffled one
        self.clear()
        self.sequence = self.create_sequence(False)
        self.create_puzzle()
        
    def quitbutton(self):
        '''
        Fucntion: quitbutton
            end the puzzle game
        '''
        # prompt the quit message and show the credits
        self.prompt('Resources/quitmsg.gif')
        self.prompt('Resources/credits.gif')
        
        # shut down the screen
        self.screen.bye()
        
    def loadbutton(self):
        '''
        Fucntion: loadbutton
            load a new puzzle and show it
        '''
        # create the prompt text
        puzzle = ['luigi.puz','smiley.puz','fifteen.puz','yoshi.puz','mario.puz']
        text = 'Enter the name of the puzzle you wish to load. Choices are:'
        for each in puzzle:
            text = text +'\n' +each
        # ask user to select one
        selected = self.screen.textinput('Load puzzle',text)

        # check if selected puzzle in the list
        if selected in puzzle:
            try:
                # save the original data in case error happended
                temp_puzzle = self.puzzle
                temp_sequence = self.sequence
                temp_pics_info= self.pics_info
                
                # change the puzzle
                self.puzzle = selected
                self.load_image()
                self.clear()
                self.sequence = self.create_sequence(True)
                self.create_puzzle ()
            # if the error happened on data just prompt error
            except ValueError:
                # show the file error message and store it
                self.log_error(ValueError)
            except Exception as error:
                # show the file error message and store it
                self.log_error(error)
                
                # if error happened on the middle of create_puzzle
                # rebuild the original puzzle(ex: image file doesn't exist)
                self.puzzle = temp_puzzle
                self.sequence = temp_sequence
                self.pics_info = temp_pics_info
                self.clear()
                self.create_puzzle () 
        else:
            # show the file error message and store it
            self.log_error(f'{selected} not exist')
            
    def button_press(self, method_name):
        '''
        Fucntion: button_press
            calling different method according to method_name
        Parameter:
            method_name(string): method name
        '''
        # turn method name as a string into method
        method = eval('self.' + method_name + '()')

    def log_error(self, error):
        '''
        Fucntion: log_error
            record the error and show the message
        Parameter:
            error(string): happened error
        '''
        file = open("5001_puzzle.err", "a")
        # write in the file
        file.write(str(error)+'\n')
        # close the file
        file.close()

        # show the file error message
        self.prompt('Resources/file_error.gif')
        
