import re
import urllib.request, json
import urllib.parse
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import time
import random

inputFile = 'words.txt'
outputFile = 'output.txt'
urlPrefix = 'https://sozluk.gov.tr/gts?ara='
delimiter = '\t'
threadCount = 16

def cleanWord(word):
    word = re.split(',|/|\(', word)[0] # get the word itself by removing stuff after a , a / or in brackets. This is just extra metadata we don't want
    # replace some special Turkish capital letters (don't lower all, as some have special meanings when capitalized)
    word = word.replace('Ç', 'ç')
    word = word.replace('İ', 'i')
    word = word.replace('Ş', 'ş')
    word = word.strip() # remove whitespace
    return word

def processWord(word):
    processed = word.strip() # each line starts with the word itself

    cleanedWord = cleanWord(word)
    url = urlPrefix + urllib.parse.quote(cleanedWord)

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        for info in data:
            if 'telaffuz' not in info:
                processed += delimiter + 'error'
            else:
                pronunciation = info['telaffuz']
                if not pronunciation: processed += delimiter + '0'
                else: processed += delimiter + pronunciation
    
    processed += '\n'
    return processed

def tryProcessWord(word):
    for _ in range(5):
        try:
            return processWord(word)
        except:
            time.sleep(random.uniform(0.5, 1.5))
            pass
    return "failed\n"

with Pool(threadCount) as pool:
    with open(inputFile, 'r') as wordsFile:
        words = wordsFile.readlines()
        processedWords = tqdm(pool.imap(tryProcessWord, words), total=len(words))
        # processedWords = tqdm(pool.map(tryProcessWord, words))

    with open(outputFile, 'w') as output:
        output.writelines(processedWords)
