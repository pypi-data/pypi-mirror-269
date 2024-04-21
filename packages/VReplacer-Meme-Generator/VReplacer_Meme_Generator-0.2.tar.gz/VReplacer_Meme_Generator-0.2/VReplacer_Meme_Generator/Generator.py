import random
import requests
from . import _Helpers

class Generator():
    def __init__(self, params = {}) -> None:
        self.dataFile = None
        self.imageFolder = None
        self.fontFile = None
        self.aiModel = None
        self.aiURL = None
        self.aiPrompt = None
        self.currentBuffer = {"text": None,
                              "substitutionIndex": []}
        self.setParams(params)

    def setParams(self, params = {}):
        if 'dataFile' in params.keys(): self.setDataFilePath(params['dataFile'])
        if 'imageFolder' in params.keys(): self.setImageFolderPath(params['imageFolder'])
        if 'fontFile' in params.keys(): self.setFontFilePath(params['fontFile'])
        if 'aiModel' in params.keys(): self.setAiModel(params['aiModel'])
        if 'aiURL' in params.keys(): self.setAiURL(params['aiURL'])
        if 'aiPrompt' in params.keys(): self.setAiPrompt(params['aiPrompt'])

    def getCurrentText(self): return self.currentBuffer["text"]
    
    def setDataFilePath(self, pathToFile : str): self.dataFile = pathToFile
    
    def setImageFolderPath(self, pathToFolder : str): self.imageFolder = pathToFolder

    def setFontFilePath(self, pathToFile : str): self.fontFile = pathToFile

    def setAiModel(self, aiModel : str): self.aiModel = aiModel

    def setAiURL(self, URL : str): self.aiURL = URL

    def setAiPrompt(self, prompt : str):
        if "{text}" not in prompt:
            raise Exception("Prompt should contain '{text}'")
        self.aiPrompt = prompt

    def loadRandomSentence(self):
        if self.dataFile is None:
            raise Exception("Data path not specified!")
        self.currentBuffer["text"], self.currentBuffer["substitutionIndex"] = _Helpers.randomSentence(self.dataFile)
    
    def changeRandomWord(self, wordToChange):
        if self.currentBuffer["substitutionIndex"]:
            wordNumber = int(random.choice(self.currentBuffer["substitutionIndex"].pop()))
            self.currentBuffer["text"] = _Helpers.replaceWordAtIndex(self.currentBuffer["text"], wordNumber, wordToChange)
        else:
            raise Exception("Sentence not loaded or no more nouns to change!")

    def checkSpelling(self):
        if self.aiModel is None:
            raise Exception("Model not set!")
        if self.aiURL is None:
            raise Exception("URL not set!")
        if self.aiPrompt is None:
            raise Exception("Prompt not set!")
        
        data = {
            "model": self.aiModel,
            "prompt": self.aiPrompt.format(text = self.currentBuffer["text"]),
            "stream": False
        }

        response = requests.post(self.aiURL, json=data)
        self.currentBuffer["substitutionIndex"] = None
        self.currentBuffer["text"] = response.json()['response']

    def generateImage(self, outputFile = "output.jpg"):
        if self.imageFolder is None:
            raise Exception("Image folder path not set!")
        if self.fontFile is None:
            raise Exception("Font file path not set!")
        if self.currentBuffer["text"] is None:
            raise Exception("Text not set!")
        
        firstHalfOfSentence, secondHalfOfSentence = _Helpers.splitStringInHalf(self.currentBuffer["text"])
        _Helpers.makeMeme(firstHalfOfSentence, secondHalfOfSentence, _Helpers.obtainRandomImage(self.imageFolder), self.fontFile, outputFile)  