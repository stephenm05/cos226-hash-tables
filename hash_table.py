class DataItem:
    def __init__(self, line):
        if len(line)<9:
             print("Initialization Error: Incomplete data")
             return -1
        self.title=line[0]
        self.genre=line[1]
        self.release_date=line[2]
        self.director=line[3]
        self.revenue=float(line[4][1:])
        self.rating=float(line[5])
        self.min_duration=int(line[6])
        self.production_company=line[7]
        self.quote=line[8]
    
    def __str__(self):
         return f"{self.title}, {self.genre}, {self.release_date}, {self.director}, {self.revenue}, {self.rating}/10, {self.min_duration}min, {self.production_company}, {self.quote}"

def hashFunction(stringData):
    # once modded, this function will produce an index in the range 0-{tableSize-1}
    # ideally, each key plugged in will yield a different value in this range, resulting in no collisions during construction
    
    # HF2: previous attempt essentially calculated the index based only off of the last few chars in stringData, and certain combinations of ending chars (ex. "-on", "-er") are more common than others (ex. "-xb", "-tl") because of which characters are generally allowed to end english words
    # to avoid the particularly un-uniform distribution of characters at the end of words, this implementation swaps stringData's first and second halves before interpreting it as a number, thus making the ending bits that play the greatest role in determining the index somewhat more random, because now they could come not just from the end of a word but also from the start or middle
    strBytes = stringData.encode()
    strBytes = strBytes[int(len(strBytes)/2):]+strBytes[:int(len(strBytes)/2)]
    key = int.from_bytes(strBytes,byteorder='big')
    return key

import csv, time

# create empty hash tables
tableSize = 15001 # there are 15,001 items in MOCK_DATA.csv so the table must be at least that big
hashTitleTable = [None] * tableSize
hashQuoteTable = [None] * tableSize

file = "MOCK_DATA.csv"
counter = 0
tCollisions = 0
qCollisions = 0
print(f"Table size: {tableSize}")
with open(file, 'r', newline='',  encoding="utf8") as csvfile:
    reader = csv.reader(csvfile)

    # filling of hashTitleTable begins here, record start time
    print("Filling title table...")
    startTime = time.perf_counter()
    for row in reader:
        if counter == 0: # skip column headers
            counter+=1
            continue

        movie = DataItem(row)

        # first get the key and convert it to an index by making sure it's within the appropriate size using mod
        titleIndex = hashFunction(movie.title) % tableSize
        if hashTitleTable[titleIndex]!=None: # handle collision by changing titleIndex, if necessary
            titleIndex=titleIndex+1 if titleIndex<(tableSize-1) else 0
            while hashTitleTable[titleIndex]==None:
                titleIndex+=1
                if titleIndex>=tableSize:
                    titleIndex=0
            tCollisions+=1
        # when an empty space is found, add the item
        hashTitleTable[titleIndex]=movie
             
        counter += 1
    # hashTitleTable filled, print stats
    print(f"Title table stats\nUnused slots: {tableSize-counter}\nCollisions: {tCollisions}\nTime taken: {(time.perf_counter()-startTime):.5f}s\n")

# repeat above to fill hashQuoteTable
with open(file, 'r', newline='', encoding='utf8') as csvfile:
    print("Filling quote table...")
    reader = csv.reader(csvfile)
    counter = 0
    startTime = time.perf_counter()
    for row in reader:
        if counter == 0: # skip column headers
            counter+=1
            continue

        movie = DataItem(row)

        # first get the key and convert it to an index by making sure it's within the appropriate size using mod
        quoteIndex = hashFunction(movie.quote) % tableSize
        if hashQuoteTable[quoteIndex]!=None: # handle collision by changing quoteIndex, if necessary
            quoteIndex=quoteIndex+1 if quoteIndex<(tableSize-1) else 0
            while hashQuoteTable[quoteIndex]==None:
                quoteIndex+=1
                if quoteIndex>=tableSize:
                    quoteIndex=0
            qCollisions+=1
        # when an empty space is found, add the item
        hashQuoteTable[quoteIndex]=movie
                 
        counter += 1
    # hashQuoteTable filled, print stats
    print(f"Quote table stats\nUnused slots: {tableSize-counter}\nCollisions: {qCollisions}\nTime taken: {(time.perf_counter()-startTime):.5f}s\n")
print(f"Items added: {counter}")