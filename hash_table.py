import csv, time, math

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
    
    # HF3: reading stringData's bytes as a number seemed to produce relatively similar results in terms of collisions regardless of how those bytes were mixed up before interpretation
    # since starting and ending in different places doesn't produce uniform-enough results to lower collisions, this attempt tries to introduce an additional level of randomness by first squaring int(stringData) to produce a new number relatively distinct from that produced by other, numerically-close stringDatas
    # from this new number, the five central digits are extracted and used to calculate index
    square = str(int.from_bytes(stringData.encode(),byteorder='big')**2)
    key = int(square[int(len(square)/2)-3:int(len(square)/2)+2])
    return key



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
    endTime = time.perf_counter()
    print(f"Title table stats\nUnused slots: {tableSize-counter}\nCollisions: {tCollisions}\nTime taken: {(endTime-startTime):.5f}s\n")

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
    endTime = time.perf_counter()
    print(f"Quote table stats\nUnused slots: {tableSize-counter}\nCollisions: {qCollisions}\nTime taken: {(endTime-startTime):.5f}s\n")
print(f"Items added: {counter}")