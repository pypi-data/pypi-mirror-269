import os
import re
import csv
import random
from PIL import Image, ImageDraw, ImageFont


# Odczytanie pliku CSV z przyslowiami
def readCSV(filePath):
    data = []

    with open(filePath, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        for row in reader:
            statement, verbs = row
            verbsList = verbs.split(', ')
            data.append((statement, verbsList))

    return data

# Odczytanie przyslow, wybranie losowego i zwrócenie przysłowia i wektora z rzeczownikami
def randomSentence(filePath):
    data = readCSV(filePath)
    statementNumber = random.randint(0, len(data))
    return data[statementNumber][0], data[statementNumber][1]

# Zamiana wybranego rzeczownika na podany w zdaniu
def replaceWordAtIndex(inputString, index, newWord):
    words = re.findall(r"\w+|[^\w\s]" , inputString)

    if 0 <= index < len(words):
        words[index] = newWord
        return ' '.join(words)
    else:
        return inputString 

# Credits: https://github.com/danieldiekmeier/memegenerator/tree/master
# Robienie mema
def makeMeme(topString, bottomString, inputFilename, pathToFont, outputFilename = "output.jpg"):

    img = Image.open(inputFilename)
    imageSize = img.size

    # find biggest font size that works
    fontSize = int(imageSize[1]/1)
    font = ImageFont.truetype(pathToFont, fontSize)
    topTextSize = font.getsize(topString)
    bottomTextSize = font.getsize(bottomString)
    while topTextSize[0] > imageSize[0]-20 or bottomTextSize[0] > imageSize[0]-20:
        fontSize = fontSize - 1
        font = ImageFont.truetype(pathToFont, fontSize)
        topTextSize = font.getsize(topString)
        bottomTextSize = font.getsize(bottomString)

    # find top centered position for top text
    topTextPositionX = (imageSize[0]/2) - (topTextSize[0]/2)
    topTextPositionY = 0
    topTextPosition = (topTextPositionX, topTextPositionY)

    # find bottom centered position for bottom text
    bottomTextPositionX = (imageSize[0]/2) - (bottomTextSize[0]/2)
    bottomTextPositionY = imageSize[1] - bottomTextSize[1]
    bottomTextPosition = (bottomTextPositionX, bottomTextPositionY) 

    draw = ImageDraw.Draw(img)

    outlineRange = int(fontSize/15)
    for x in range(-outlineRange, outlineRange+1):
        for y in range(-outlineRange, outlineRange+1):
            draw.text((topTextPosition[0]+x, topTextPosition[1]+y), topString, (0,0,0), font=font)
            draw.text((bottomTextPosition[0]+x, bottomTextPosition[1]+y), bottomString, (0,0,0), font=font)

    draw.text(topTextPosition, topString, (255,255,255), font=font)
    draw.text(bottomTextPosition, bottomString, (255,255,255), font=font)

    img.save(outputFilename)

# Podzielenie zdania na dwie części
def splitStringInHalf(inputText):
    words = inputText.split()
    half = len(words) // 2
    return ' '.join(words[:half]), ' '.join(words[half:])

# Wybranie losowego obrazka
def obtainRandomImage(filePath):
    imageFiles = os.listdir(filePath)
    imageFiles = [file for file in imageFiles if file.endswith((".jpg", ".png", ".webp"))]
    randomImage = random.choice(imageFiles)
    return os.path.join(filePath, randomImage)

    