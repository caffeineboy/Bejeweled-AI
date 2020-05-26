######################################################
#   My goal is to make a program that can play bejeweled.
#
#   1) Figure out how to read pixel colors off of the screen
#   2) Figure out how to create a grid of the various pieces of the board
#   3) Figure out how to get all possible moves
#   4) Make a move
#   5) Update screen and repeat
#
#########################################################

"""
Currently I need to synchronize
"""

import pyautogui
from ahk import AHK
import logging
import time
import PIL
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO)

class Bejewled_Grid():
    def __init__(self,grid):
        self.grid = grid
        self.Find_Adjacent_Pieces()

        self.horizontal_consecutives = []
        self.vertical_consecutives = []
        self.match_coordinates = []

    def Find_Adjacent_Pieces(self):
        current_row = 0
        current_col = 0
        while current_row <=7:
            while current_col <= 7:
                #Right now we are iterating through and checking boundary/adjacent conditions
                #Currently checking for top row
                if current_row == 0:
                    self.grid[current_row][current_col].up_adjacent = None
                else:
                    self.grid[current_row][current_col].up_adjacent = self.grid[current_row - 1][current_col]
                #Now we are checking for bottom row
                if current_row == 7:
                    self.grid[current_row][current_col].down_adjacent = None
                else:
                    self.grid[current_row][current_col].down_adjacent = self.grid[current_row + 1][current_col]
                #Now we check for left column
                if current_col == 0:
                    self.grid[current_row][current_col].left_adjacent = None
                else:
                    self.grid[current_row][current_col].left_adjacent = self.grid[current_row][current_col - 1]
                #Now we check for right column
                if current_col == 7:
                    self.grid[current_row][current_col].right_adjacent = None
                else:
                    self.grid[current_row][current_col].right_adjacent = self.grid[current_row][current_col + 1]
                current_col += 1
            current_col = 0
            current_row += 1

    def Find_Consecutive_Pieces(self):
        #Iterate through each piece. If it has an adjacent of same color
        #If there is an adjacent in the left, look at the right piece
        row_counter = 0
        col_counter = 0
        horizontal_consecutives = []
        vertical_consecutives = []
        while row_counter <= 7:
            while col_counter <= 7:
                #Look for horizontal consecutive pieces of same color
                current_piece = self.grid[row_counter][col_counter]
                if col_counter == 7: pass
                elif current_piece.Get_Color() == self.grid[row_counter][col_counter + 1].Get_Color():
                    consecutive_tuple = (current_piece,self.grid[row_counter][col_counter +1])
                    horizontal_consecutives.append(consecutive_tuple)
                #Look for vertical consecutive pieces of same color
                if row_counter == 7: pass
                elif current_piece.Get_Color() == self.grid[row_counter + 1][col_counter].Get_Color():
                    consecutive_tuple = (current_piece,self.grid[row_counter + 1][col_counter])
                    vertical_consecutives.append(consecutive_tuple)



                col_counter += 1
            col_counter = 0
            row_counter += 1
        logging.info("Found %s horizontal consecutives" % str(len(horizontal_consecutives)))
        logging.info("Found %s vertical consecutives" % str(len(vertical_consecutives)))
        self.vertical_consecutives = vertical_consecutives
        self.horizontal_consecutives = horizontal_consecutives

    def Find_Horizontal_Matches(self):
        pass
        #So right now, I have a list of all consecutive pieces horizontally
        #THe tuple is ordered (left_piece, right_piece)
        #Make sure the left piece isn't at the left border, same with the right
        #If there is a piece there, look at it's adjacents and check for color

        #Looking at left side
        match_coordinates = self.match_coordinates
        for piece_pair in self.horizontal_consecutives:
            if piece_pair[0].left_adjacent == None: pass
            else:
                outside_left = piece_pair[0].left_adjacent
                if outside_left.up_adjacent == None: pass
                elif piece_pair[0].Get_Color() == outside_left.up_adjacent.Get_Color():
                    match_coordinates.append((outside_left,outside_left.up_adjacent))
                if outside_left.left_adjacent == None: pass
                elif piece_pair[0].Get_Color() == outside_left.left_adjacent.Get_Color():
                    match_coordinates.append((outside_left,outside_left.left_adjacent))
                if outside_left.down_adjacent == None: pass
                elif piece_pair[0].Get_Color() == outside_left.down_adjacent.Get_Color():
                    match_coordinates.append((outside_left,outside_left.down_adjacent))
            if piece_pair[1].right_adjacent == None: pass
            else:
                outside_right = piece_pair[1].right_adjacent
                if outside_right.up_adjacent == None: pass
                elif piece_pair[1].Get_Color() == outside_right.up_adjacent.Get_Color():
                    match_coordinates.append((outside_right,outside_right.up_adjacent))
                if outside_right.right_adjacent == None: pass
                elif piece_pair[1].Get_Color() == outside_right.right_adjacent.Get_Color():
                    match_coordinates.append((outside_right,outside_right.right_adjacent))
                if outside_right.down_adjacent == None: pass
                elif piece_pair[1].Get_Color() == outside_right.down_adjacent.Get_Color():
                    match_coordinates.append((outside_right,outside_right.down_adjacent))
        print(match_coordinates)
        self.match_coordinates = match_coordinates
        logging.info("Found %s possible horizontal consecutive matches" % (str(len(match_coordinates))))

    def Find_Vertical_Matches(self):
        match_coordinates = self.match_coordinates
        for piece_pair in self.vertical_consecutives:
            if piece_pair[1].down_adjacent == None:
                pass
            else:
                outside_down = piece_pair[1].down_adjacent
                if outside_down.down_adjacent == None:
                    pass
                elif piece_pair[1].Get_Color() == outside_down.down_adjacent.Get_Color():
                    match_coordinates.append((outside_down, outside_down.down_adjacent))
                if outside_down.left_adjacent == None:
                    pass
                elif piece_pair[0].Get_Color() == outside_down.left_adjacent.Get_Color():
                    match_coordinates.append((outside_down, outside_down.left_adjacent))
                if outside_down.right_adjacent == None:
                    pass
                elif piece_pair[0].Get_Color() == outside_down.right_adjacent.Get_Color():
                    match_coordinates.append((outside_down, outside_down.right_adjacent))

            if piece_pair[0].up_adjacent == None:
                pass
            else:
                outside_up = piece_pair[0].up_adjacent
                if outside_up.up_adjacent == None:
                    pass
                elif piece_pair[0].Get_Color() == outside_up.up_adjacent.Get_Color():
                    match_coordinates.append((outside_up, outside_up.up_adjacent))
                if outside_up.left_adjacent == None:
                    pass
                elif piece_pair[0].Get_Color() == outside_up.left_adjacent.Get_Color():
                    match_coordinates.append((outside_up, outside_up.left_adjacent))
                if outside_up.right_adjacent == None:
                    pass
                elif piece_pair[0].Get_Color() == outside_up.right_adjacent.Get_Color():
                    match_coordinates.append((outside_up, outside_up.right_adjacent))
        print(self.match_coordinates)
        print(self.vertical_consecutives)
        self.match_coordinates = match_coordinates

    def Find_Single_Space_Horizontals:

    def Perform_Matches(self):
        for x in self.match_coordinates:
            for y in x:
                Click_Position(y.coordinate)

class Piece():
    def __init__(self,color,position):
        self.color = color
        self.coordinate = position

        self.up_adjacent = None
        self.down_adjacent = None
        self.left_adjacent = None
        self.right_adjacent = None
    def __str__(self):
        return str(self.coordinate)
    def Set_Coordinate(self,new_coord):
        self.coordinate = new_coord
    def Get_Color(self):
        return self.color
    def Set_Up_Adjacent(self,piece):
        self.up_adjacent = piece
    def Set_Down_Adjacent(self,piece):
        self.down_adjacent = piece
    def Set_Left_Adjacent(self,piece):
        self.left_adjacent = piece
    def Set_Right_Adjacent(self,piece):
        self.right_adjacent = piece

def Build_Bejeweled_Grid(color_list):
    """
    So the end goal is to get a grid of 8*8 of piece objects with their color
    From there I can easily make decisions
    """
    temp_grid = []
    piece_counter = 0
    for color in color_list:
        piece_coords = Find_All_Pieces(color)
        for piece in piece_coords:
            logging.info("creating piece %s at %s" %(color,str(piece)))
            new_piece = Piece(color,piece)
            temp_grid.append(new_piece)
            piece_counter += 1
    logging.info("Created %s pieces into bejeweled_grid" % piece_counter)

    #Now we need to sort the grid by y, then x coords
    #Now that I have all the pieces together, I want to stabilize the height
    temp_grid = sorted(temp_grid, key=lambda k: [k.coordinate[1], k.coordinate[0]])
    temp_grid = Stabilize_Coordinates(temp_grid)

    final_grid = [[],[],[],[],[],[],[],[]]
    counter = 0
    sublist_counter = 0
    #Putting 8 pieces in each sublist
    for piece in temp_grid:
        final_grid[sublist_counter].append(piece)
        counter += 1
        if counter == 8:
            counter = 0
            sublist_counter += 1

    return final_grid

def Click_Position(pos_tuple):
    pos_tuple = Click_Position_Helper(pos_tuple)
    pyautogui.click(pos_tuple[0],pos_tuple[1])

def Click_Position_Helper(pos_tuple):
    new_pos_x = pos_tuple[0] + 15
    new_pos_y = pos_tuple[1] + 15
    new_pos_tuple = (new_pos_x,new_pos_y)
    return new_pos_tuple

def Coord_Difference(coord1,coord2):
    #If the difference between the left(s) are different enough:
    if abs(coord1[1] - coord2[1]) > 15 or abs(coord1[0] - coord2[0]) > 15:
        return True
    else:
        return False

def Stabilize_Height(correcting_coord,coord2):
    if abs(correcting_coord[1] - coord2[1]) < 10:
        new_coord = (coord2[0],correcting_coord[1])
    else:
        return coord2
    return new_coord

def Stabilize_Width(correcting_coord,coord2):
    if abs(correcting_coord[0] - coord2[0]) < 10:
        new_coord = (correcting_coord[0],coord2[1])
    else:
        return coord2
    return new_coord

def Stabilize_Coordinates(piece_list):
    #Right now I have all the pieces sorted by their y value
    #I need to go through each piece, and create a new coordinate for them based on stabilize_height
    counter = 0
    while counter < len(piece_list)-1:
        new_coordinate = Stabilize_Height(piece_list[counter].coordinate, piece_list[counter+1].coordinate)
        piece_list[counter+1].Set_Coordinate(new_coordinate)
        counter += 1

    piece_list = sorted(piece_list,key=lambda k: [k.coordinate[0], k.coordinate[1]])

    counter = 0
    while counter < len(piece_list)-1:
        new_coordinate = Stabilize_Width(piece_list[counter].coordinate, piece_list[counter+1].coordinate)
        piece_list[counter+1].Set_Coordinate(new_coordinate)
        counter += 1

    piece_list = sorted(piece_list,key=lambda k: [k.coordinate[1], k.coordinate[0]])
    return piece_list

def Get_Unique_Coords(coord_list):
    """
    The goal of this function is to sort it, and check the next coordinate to see if it is different enough
    Sort, then go through the list and remove the next item if it is similar to the last
    :return:
    """
    unique_list = []
    unique_list.append(coord_list[0])
    counter = 1
    duplicate_counter = 1

    #So I start out with a list of coordinates, and duplicates are grouped
    while counter < len(coord_list)-1:
        #I want to compare coord_list[counter] to each item in unique_list
        unique_flag = True
        #This looks at each item in unique list and compares it to the current coord we are iterating through
        for unique in unique_list:
            if Coord_Difference(unique,coord_list[counter]) == True:
                pass
            else:
                unique_flag = False
        if unique_flag == True:
            unique_list.append(coord_list[counter])
            counter += 1
        else:
            counter +=1


    logging.info("unique length: %s" % len(unique_list))

    #After we get every unique coordinate, we just want to make sure that
    #That coordinates are uniform in height, we dont want 1pixel differneces
    #This matters because of the grid we build later on

    #In order to do this I need to sort the list, default is first value
    unique_list.sort()
    #Now that the list is sorted by (X,y) do stabilizing_width to consecutive
    counter = 0
    while counter <= len(unique_list)-2:
        unique_list[counter+1] = Stabilize_Width(unique_list[counter],unique_list[counter+1])
        counter += 1

    #Now we want to stabilize the height
    sorted(unique_list, key = lambda k: [k[1], k[0]])
    return(unique_list)

def Find_All_Pieces(color):
    color += ".png"
    flame_color = "flame_" + color
    lightning_color = "lightning_" + color
    color_list = pyautogui.locateAllOnScreen(color, confidence=0.73)
    flame_color_list = pyautogui.locateAllOnScreen(flame_color,confidence=0.68)
    lightning_color_list = pyautogui.locateAllOnScreen(lightning_color,confidence=0.63)
    color_list = list(color_list) + list(flame_color_list) + list(lightning_color_list)
    left_list = []
    top_list = []
    coordinate_list = []
    for x in color_list:
        left_list.append(x[0])
        top_list.append(x[1])
        coordinate_list.append((x[0],x[1]))

    final_coords_list = Get_Unique_Coords(coordinate_list)
    return final_coords_list

def main():
    color_list = ["blue","green","orange","purple","red","white","yellow"]
    try:
        counter = 0
        while counter < 3:
            bejeweled_grid = Build_Bejeweled_Grid(color_list)
            bejeweled_object = Bejewled_Grid(bejeweled_grid)
            bejeweled_object.Find_Consecutive_Pieces()
            bejeweled_object.Find_Vertical_Matches()
            bejeweled_object.Find_Horizontal_Matches()
            bejeweled_object.Perform_Matches()
            counter += 1
    except:
        time.sleep(4)
        main()






start_time = time.time()
counter = 0
while counter < 3:
    main()
    time.sleep(2)
    Click_Position((400,400))
    counter += 1
end_time = time.time()

print("Program took %s to run" %(abs(start_time-end_time)) )
