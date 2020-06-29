import numpy as np
import csv

ACCEPTED_RELATION = 0.5
linkageDictionary = {}

with open('./model/output/input_master/2019.06.txt') as f:
    lines = f.readlines()
    rawString = lines[0]
    rawString = rawString.replace("[1] \"", "")

    #print("LINE:")
    #print (lines)
    processedString = rawString.replace(" ","").strip().split("\\n")


with open('./model/output/input_master/2019.03.txt') as f:
    lines = f.readlines()
    rawString = lines[0]
    rawString = rawString.replace("[1] \"", "")

    #print("LINE:")
    #print (lines)
    processedStringComp = rawString.replace(" ","").strip().split("\\n")


#mockList = ["pla","plant","cookie","wingle","poo","six","eight","n"]
processedString.pop()
processedStringComp.pop()

lengthString = len(processedStringComp)
wordLength = 0

outputArray = [[0]*lengthString for i in range(lengthString)]

topicCount = 0
for keywords in processedString:
	keywordArray = keywords.split(":")[1].split(",")
	keywordArray.pop()
	for word in keywordArray:
		compTopicCount = 0
		for keywordsComp in processedStringComp:
			keywordCompArray = keywordsComp.split(":")[1].split(",")
			keywordCompArray.pop()
			wordCount = 0
			wordLength = len(keywordCompArray)
			print (wordLength)
			for compWord in keywordCompArray:
				if (word == compWord):
					print (str(topicCount) + ":" + str(compTopicCount) +"=" + word)
					outputArray[topicCount][compTopicCount] = (outputArray[topicCount][compTopicCount] + 1)
					#outputArray[topicCount][compTopicCount] = word
					#print ("Match")
					#print (str(compTopicCount) + ":" + str(topicCount))
					pass
				else:
					#print ("not Match")
					pass
				#outputArray[topicCount][compTopicCount] = wordCount
			compTopicCount = compTopicCount + 1
	topicCount = topicCount + 1

for j in range(lengthString):
	for i in range(lengthString):
		acceptableRange = outputArray[j][i]/wordLength
		if (acceptableRange >= ACCEPTED_RELATION):
			outputArray[j][i] = 1
		else:
			outputArray[j][i] = 0


print(np.matrix(outputArray))
with open("compare(2019.03x2019.06).csv","w+") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(outputArray)
