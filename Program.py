import socket
import re
import textwrap

# Socket Programming
s = socket.socket()
host = socket.gethostname()
port = 30120

recievedList = []
s.connect((host, port))
recieved = s.recv(1024)
recievedList = re.split(r' |\r|\n', recieved)
s.close()


# Getting input formatted and put into lists for processing
while "" in recievedList:
	recievedList.remove("")
useList = []
for i in range(7):
	if i % 2 == 0:
		useList.append([format(int(recievedList[i]), '08b'), format(int(recievedList[i+1]), '08b')])
codeList = []
sentList = []
for i in range(4):
	codeList.append(useList[i])
for i in range(len(recievedList)):
	if i % 2 == 0 and i > 6:
		sentList.append([format(int(recievedList[i],base=16),'016b'), format(int(recievedList[i+1],base=16), '064b')])

# Loop the sentList long message, with each extended code word. Have to do it byte by byte, do it based on code word, the move length and advance code word

# Helper function to establish accuracy of codeword, should be in decimal values,but got it from internet, but I believe works just as well
# Address: https://stackoverflow.com/questions/17388213/find-the-similarity-metric-between-two-strings
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
# Would utilize to get diff of anything less than 1. else store likeness and take the most at end.

ValList = []
# Find the least Different so as to find the code word
#Not the most efficient, looping 3 times, but for constant n I'm Ok with it. 
for i in range(len(sentList)):
	placeHold = float(2)
	for j in range(len(codeList)):
		sentByte = textwrap.wrap(sentList[i][1],8)
		minChange = 0
		minValList = []
		justAList = []

		for k in range(len(sentByte)):
			a = similar(sentByte[k],codeList[j][1])
			if a != 1.0 and a > minChange:
				minChange = a
				# Stores multiple values for multiple uses provided I change my mind
				minValList.append([a,k,int(codeList[j][1],2),format(int(sentList[i][0],2),'#06X'),format(int(sentList[i][1],2),'#018X')])
				justAList.append(a)

		# Gets the maximum value from the difference, indicating which values it takes up. 
		if len(minValList) != 0:
			#print(max(minValList))
			#print(max(justAList))
			ValList.append(max(minValList))

# Output
for element in ValList:
	print("Original Message: ")
	print(element[3])
	print("Byte Number to be sent Back: ")
	print(element[1])
	print("\n")
print('')
#print(len(ValList)) # For showing variance between program runs
