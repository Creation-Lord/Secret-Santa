"""
Secret Santa Program
Written by Michael Byrnes
This program will give your list of people a random person they can give a gift to. This is as random as possible and fully automatic.
"""

import random
import os, codecs
from os import listdir
from tkinter import *
#from PIL import ImageTk, Image
from sqlite3 import *

# GUI
gui = Tk()
gui.title('Secrect Santa Selector') #App Title
gui.geometry('1000x600') #App Size

# Image
image = Canvas(gui, width = '800', height = '400') #Image Size
image.grid(row = 1, column = 1, columnspan = 3) #Image Position
img = PhotoImage(file = 'image.png') #Image File
image.create_image(0.01, 0.01, anchor = NW, image = img) #Image Data

# Entry box
entry = Entry(gui, width = '100', bd = 3, relief = 'groove') #Entry Data
entry.insert(0,'Enter names here, keeping each name separated only by a coma.(eg: "Sam,Dean,Jack,Cas,Mary,Bobby,Charlie,Kevin,Crowley")') #Default Text
entry.grid(row = 2, column = 1) #Entry Position

# Charades Toggle
charadesState = True

charadesLabel = Label(gui, text = "Charades Options", fg = "green", font = ("Times New Roman", 16))
charadesLabel.grid(row = 3, column = 2)

# Switch
def switch():
    global charadesState
     
    # Determine is on or off
    if charadesState:
        charadesButton.config(image = off)
        charadesState = False

    else:
        charadesButton.config(image = on)
        charadesState = True

# Define Our Images
on = PhotoImage(file = "on.png")
off = PhotoImage(file = "off.png")
 
# Create A Button
charadesButton = Button(gui, image = on, bd = 0, command = switch)
charadesButton.grid(row = 3, column = 3)

# Functions
def paste(length, order, charades): #The function used in testing to see that all names are there and lined up correctly
	i = 0
	while(i<length-1):
		print(order[i] + ' is giving to ' + order[i+1] + '\nYour charade options are ' + str(charades[i]))
		i += 1
	print(order[i] + ' is giving to ' + order[0])

def text(length, order, charades): #Creates the text files that can be used to allow complete 
        folder_path = os.path.dirname(os.path.abspath('SecretSanta.py')) + '\Txt Files'
        if not os.path.exists(folder_path):
                os.makedirs(folder_path)
        for file_name in listdir(folder_path):
                if file_name.endswith('.txt'):
                        os.remove(folder_path + '\\' + file_name)
        i = 0
        while(i<length-1):
                f = open(folder_path + '\\' + order[i] + '.txt','w')
                if charadesState == True: f.write('You are buying for ' + order[i+1] + '\nYour charade options are ' + str(charades[i]))
                else: f.write('You are buying for ' + order[i+1])
                f.close()
                i += 1
        f = open(folder_path + '\\' + order[i] + '.txt','w')
        if charadesState == True: f.write('You are buying for ' + order[0] + '\nYour charade options are ' + str(charades[i]))
        else: f.write('You are buying for ' + order[0])
        f.close()

def process(): #Main function that runs on button call
        names = entry.get()+ ' '
        people = []
        flag = 0
        for x in range(names.count(',')+1):
                people.append(names[flag:names.find(',',flag,len(names)-1)])
                flag = names.find(',',flag,len(names)-1) + 1
        order = []
        length = len(people) #Cause it's just easier to see
        
        for x in people: #Make order the same size as people
              order.append('')

        for x in range(length+1): #Actual order randomiser, taking a random person from first list then placing them in a random position in the reordered list
                randomnum1 = random.randint(0,len(people)-1)
                while x:
                        randomnum2 = random.randint(0,len(order)-1)
                        if(order[randomnum2] == ''): #Test to make sure an index is not overwritten while not increasing the loop count
                                order[randomnum2] = people.pop(randomnum1)
                                break
        
        # Charades Option
        charades = []
        if charadesState == True:
                connection = connect(database = 'Charades.db')
                database = connection.cursor()
                for x in range(length+1):
                        options = []
                        for y in range(3):
                                randomnum = random.randint(1,80)
                                database.execute("SELECT charade FROM list WHERE number LIKE " + str(randomnum) + ";")
                                for data in database.fetchall():
                                        charade = str(data)
                                        options.append(charade[2:len(charade)-3])
                                print('o is ' + str(options))
                        charades.append(options)
                        print('c is ' + str(charades))

        text(length, order, charades)

def clear():
        folder_path = os.path.dirname(os.path.abspath('SecretSanta.py')) + '\Txt Files'
        for file_name in listdir(folder_path):
                if file_name.endswith('.txt'):
                        os.remove(folder_path + '\\' + file_name)

# Buttons
run = Button(gui, width = '5', height = '1', text = 'Run', command = process)
run.grid(row = 2, column = 2)
clear = Button(gui, width = '8', height = '1', text = 'Clear Files', command = clear)
clear.grid(row = 2, column = 3)

gui.mainloop()