from tkinter import Tk
from tkinter.filedialog import *
from tkinter.simpledialog import *
import re

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
width = askfloat("Dimensions","Width (in)")
height = askfloat("Dimensions","Height (in)")
gridx = askinteger("Grid","# Repeats in X")
gridy = askinteger("Grid","# Repeats in Y")
savefile = asksaveasfilename()

file = open(filename)
lines = file.readlines()

startBlock = []
numberStripped = []
endBlock = []
newFile = []

a = 0
for x in lines:
    start_subprogram = re.match(r'(N)([0-9]+)(\(\*.+)',x)
    end_subprogram = re.match(r'(N)([0-9]+)(G00Z\.1M05M09)',x)
    if start_subprogram:
        start_line = int(start_subprogram.group(2))
    if end_subprogram:
        end_line = int(end_subprogram.group(2))

for i in range(0,start_line):
    matchall = re.match(r'(N)([0-9]+)(.+)',lines[i])
    startBlock.append(matchall.group(3))
    
for i in range(start_line+1,end_line-1):
    matchall = re.match(r'(N)([0-9]+)(.+)',lines[i])
    numberStripped.append(matchall.group(3))

for i in range(end_line, len(lines)):
    matchall = re.match(r'(N)([0-9]+)(.+)',lines[i])
    endBlock.append(matchall.group(3))

for x in startBlock:
    newFile.append(x)

for a in range(0, gridx):
    for b in range(0, gridy):
        if a%2 == 0:
            ymove = -1
        else:
            ymove = 1
            
        for line in numberStripped:
            newFile.append(line)
            
        newFile.append("G0 X0 Y{:f}".format(ymove*height))
        newFile.append("G92 X0 Y0")
    newFile.append("G0 X{:f} Y{:f}".format(width*-1,ymove*height*-1))
    newFile.append("G92 X0 Y0")        

for x in endBlock:
    newFile.append(x)

with open(savefile, 'w') as textfile:
    for line in newFile:
        textfile.write("%s\n" % line)
