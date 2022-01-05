import turtle
import time

class Interface():
    '''
        Interface is a class for creating the interface area, button
        and showing the leader board
    '''
    def __init__(self):
        self.turtle = turtle.Turtle()   # create a turtle for interface
        self.name = ''  # record the user name
        self.move_limit = 0   # record the maximum move limit
        self. button_info = {}  # recordbutton name and location
        
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
        
    def build_interface(self, s):
        '''
        Fucntion: build_interface
            build the interface area
        Parameter:
            s(turtle.screen): the screen of turtle drawing
        '''
        # get user name and move_limit from user input
        self.name = s.textinput('Player name','Your name')
        self.move_limit =  int(s.numinput('Movement', 'Enter the number\
        of chances you want(5-200)',\
                                          default = 50, minval = 5, maxval = 200))
        
        # if user doesn't enter anything
        if self.name == '':
            self.name = 'anonymity'

        # build button name and coordinate
        self.button_info = {'resetbutton.gif':(30, -285), 'loadbutton.gif':\
                            (140, -285), 'quitbutton.gif':(250, -285)}
        
        # create puzzle area
        play_area = [(-350, 350), (80, 350), (80,-180), (-350,-180)]
        self.background(play_area, 'BLACK')
        
        # create rank area and leader board
        rank_area = [(100, 350), (350, 350), (350, -180), (100, -180)]
        self.background(rank_area, 'BLUE')
        self.leader_board(False, 0)
        
        # create reference area
        reference_area = [(-350, -220), (350,-220), (350, -350), (-350, -350)]
        self.background(reference_area, 'BLACK')

        # stamp the bottom
        for button in self.button_info:
            self.build_button(s, button, self.button_info[button])

    def background(self, vertex, color):
        '''
            Function: background
                draw background
            Parameter:
                vertex(list) : four vertex of the background
                color(string) : color of the line
        '''
        #adjust the turtle with selected size, color
        t = self.turtle
        t.color(color)
        t.pensize(10)
        
        # go to start point and draw background
        t.goto(vertex[0][0], vertex[0][1])
        self.show()
        for x, y in vertex[::-1]:
            t.goto(x, y)
        self.hide()

    def build_button(self, s, button, location):
        '''
            Function: build_button
                stamp the button at target coordinate
            Parameter:
                button(string) : name of button
                location(string) : coordinate of button
        '''
        # get the location and file name
        x, y = location
        file_name = 'Resources/' + button
        t = self.turtle

        # go to target place and stamp the button
        t.goto(x, y)
        s.addshape(file_name)
        t.shape(file_name)
        self.show()
        t.stamp()
        
        # hide the turtle for next move
        self.hide()
        
    def leader_board(self, win, move):
        '''
            Function: leader_board
                show and store the leader board
            Parameter:
                win(boolean) : if user win the game
                move(int) : total movement user make
        '''
        # the data path
        path = 'record.txt'

        # save the record if win
        if win:
            # get the old record
            with open(path, mode = 'r') as record:
                # create a competitor list and add the new record into it
                competitor_list =[]
                competitor_list.append((move, self.name))

                # get the old record and put into competitor list
                for competitor in record:
                    competitor = competitor.split()
                    move, name = int(competitor[0]), competitor[2]
                    competitor_list.append((move,name))

                # sort the list 
                competitor_list.sort()

                # get the first 6 competitor
                length = len(competitor_list)
                selected_number = 6 if length > 6 else length

            # save the new record to file
            with open(path, mode = 'w') as record:
                for i in range(selected_number):
                    record.write(f"{competitor_list[i][0]} : {competitor_list[i][1]}\n" )
        else:
            # read document if not exist create one
            with open(path, mode = 'a+') as record:
                #move pointer to beginning
                record.seek(0)
                # write the Leader and record at leader board
                location = [150, 300]
                self.writting('LEADER', 20, location)
                for user in record:
                    location[1] -= 50
                    self.writting(user, 20,location)

    def writting(self, sentence, font_size, location):
        '''
            Function: writting
                show the sentence on canvas
            Parameter:
                sentence(string) : string showing on the canvas
                font_size(int) : font size
                location(list): x and y coordinate
        '''
        # go to target coordinate and write the sentence
        t = self.turtle
        t.goto(location[0], location[1])
        t.pendown()
        t.write(sentence, font =( 'Arial', font_size, 'normal'))
        t.penup()

    def check_button(self, x, y):
        '''
            Function: check_button
                check if click the button
            Parameter:
                x(int): x-coordinate
                y(int): y-coordinate
        '''
        
        for button in self.button_info:
            # get the button coordinate and caculate the distance
            button_x, button_y = self.button_info[button]
            distance = (((button_x - x) **2 + (button_y - y)**2)**0.5)
            
            # return button name if distance < 50
            if distance < 50:
                return button[:len(button)-4]
        return None
