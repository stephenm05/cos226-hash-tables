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
    
    # HF1: just reinterpret the provided stringData as a number and don't bother doing anything else with it, with tableSize set to exactly 15,001 so all spaces are used
    # this results in a fairly random number much larger than tableSize (tableSize=11101010011001, 14 bits, while key has a minimum size of one byte per char in key and all keys are longer than two characters)
    # however, because of the mod operation performed later, only the last several digits of this number, and consequentially the last few chars of stringData, actually effect the final index used
    key = int.from_bytes(stringData.encode(),byteorder='big')
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
            titleIndex+=1
            while hashTitleTable[titleIndex]==None:
                titleIndex+=1
                if titleIndex==tableSize:
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
            quoteIndex+=1
            while hashQuoteTable[quoteIndex]==None:
                quoteIndex+=1
                if quoteIndex==tableSize:
                    quoteIndex=0
            qCollisions+=1
        # when an empty space is found, add the item
        hashQuoteTable[quoteIndex]=movie
                 
        counter += 1
    # hashQuoteTable filled, print stats
    print(f"Quote table stats\nUnused slots: {tableSize-counter}\nCollisions: {qCollisions}\nTime taken: {(time.perf_counter()-startTime):.5f}s\n")
print(f"Items added: {counter}")