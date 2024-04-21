# VREPLACER-MEME-GENERATOR
This tool allows you to create text for memes with the help of locally hosted AI and automatically generate images

## Usage
The `Generator` class provides a convenient way to interact with the meme generation functionality. Below is an example of how to use it:
```
from Generator import Generator

def main():
    params = {
            "dataFile": "./przyslowia.csv",
            "imageFolder": "./IMAGES",
            "fontFile": "./FONTS/impact.ttf",
            "aiModel": "bielik4",
            "aiURL": "http://127.0.0.1:11434/api/generate",
            "aiPrompt": 'Popraw zdanie w nawiasach tylko przez odmianę słów [{text}]. Twoja odpowiedź musi zawierać tylko poprawione zdanie po polsku i nic więcej.'
            }
    generator = Generator(params)               # Create object of Generator class and initialize it with params
    generator.loadRandomSentence()              # Load random sentence from dataFile
    generator.changeRandomWord("pipi")          # Change one allowed word to pipi
    generator.checkSpelling()                   # Send request to LLM model to check spelling
    generator.generateImage("outputfile.jpg")   # Generate image and save it to outputfile.jpg

if __name__ == "__main__":
    main()
```

## Generator fields
By default all fields are initiated as None

| Field | Context | Type |
|----------|----------|----------|
| `dataFile` | Path to `.csv` file containing preprocessed data | String |
| `imageFolder` | Path to folder with images from which generator selects random one that will be used for meme generation | String |
| `fontFile` | Path to `.ttf` file with font that will be used for meme generation| String |
| `aiModel` | Name of specific Ollama LLM model | String |
| `aiURL` | Address to send request | String |
| `aiPrompt` | Prompt used in request. Should contain '{text}' for buffered text insertion | String |
| `currentBuffer` | Dict holding the loaded sentence and substitution positions | Dict |

### Regarding data
The .csv file contains two columns: the original sentence and a list of indexes representing positions allowed to change. Preprocessing example can be found [here](.\SRC\DataProcessing.py). It takes Polish sentences from `.txt` file and extracts noun positions.

## Generator methods
| Field | Context | 
|----------|----------|
| `setParams(params)` | Updates all Generator fields that are specified in `params` except `currentBuffer` | 
| `setDataFilePath(pathToFile)` | Sets the `dataFile` field |
| `setImageFolderPath(pathToFolder)` | Sets the `imageFolder` field |
| `setFontFilePath(pathToFile)` | Sets the `fontFile` field |
| `setAiModel(aiModel)` | Sets the `aiModel` field |
| `setAiURL(URL)` | Sets the `aiURL` field |
| `setAiPrompt(prompt)` | Sets the `aiPrompt` field to the specified prompt. Raises an exception if the prompt does not contain '{text}'. |
| `getCurrentText()` | Returns the text stored in `currentBuffer` | 
| `loadRandomSentence()` | Loads a random sentence from `dataFile` into `currentBuffer` | 
| `changeRandomWord(wordToChange)` | Replaces a random word from list in `currentBuffer` with `wordToChange` | 
| `checkSpelling()` | Sends request to `aiURL` with `aiPrompt` and overrides `currentBuffer` with response. Clears `currentBuffer` `substitutionIndex` field | 
| `generateImage(outputFile)` | Create meme with random image from `imageFolder` and `currentBuffer` | 

