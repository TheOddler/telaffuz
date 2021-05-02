import re
import urllib.request, json
import urllib.parse
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

words = open('words.txt', 'r')
output = open('output.txt', 'w')
urlPrefix = 'https://sozluk.gov.tr/gts?ara='

def writeColumn(data):
    output.write(data)
    output.write('\t')

def nextLine():
    output.write('\n')

for word in tqdm(words.readlines()):
    word = re.split(',|/', word)[0].strip()
    if not word: continue
    url = urlPrefix + urllib.parse.quote(word)
    # print(url)

    writeColumn(word)

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())

        # print(data)

        for info in data:
            if 'telaffuz' not in info:
                writeColumn('error')
            else:
                pronunciation = info['telaffuz']
                if not pronunciation: writeColumn('0')
                else: writeColumn(pronunciation)
    
    nextLine()



words.close()
output.close()
