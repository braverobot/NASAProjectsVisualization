import sqlite3
import string

# open the db created by getNasaProjects.py
conn = sqlite3.connect('projectdb.sqlite')
cur = conn.cursor()
counts = dict()

for row in cur.execute('SELECT title FROM Projects'):
    rowsplit= (row[0])

    # Remove punctuation, uppercase, and numbers from each title row
    # This is to help the word-map look smoother without fussing with special characters & case
    text = rowsplit
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.translate(str.maketrans('', '', '1234567890'))
    text = text.strip()
    text = text.lower()
    # Split the text string into a 'list'
    words = text.split()

    # Check lists for common words that are not interesting and skip
    for word in words:
        if word == "for" or word == "and" or word == "and" or word == "from": continue
        if word == "of" or word == "on" or word == "a" or word == "on" or word == "in": continue
        if word =="with" or word == "the" or word == "an": continue
        if word =="by" or word == "to" or word == "i" or word == "or" or word =="d": continue
        print(word)

        # This next line of code takes a word, evaluates if its in the "counts" dict, if not it adds
        # it to the dict. It then adds 1 to the value. If it exists already in the "counts" dict, it
        # just increments the value by 1
        counts[word]= counts.get(word,0) + 1

# Sort the words in the dict by the value
sortedLargeToSmall = sorted(counts, key=counts.get, reverse=True)
highest = None
lowest = None
for keyval in sortedLargeToSmall[:100]:
    if highest is None or highest < counts[keyval] :
        highest = counts[keyval]
    if lowest is None or lowest > counts[keyval] :
        lowest = counts[keyval]
# Assign text size to the highest and lowest word counts
bigsize = 80
smallsize = 20

# Write the nasaWord.js syntax to be used in the htm webpage
fhand = open('nasaWord.js','w')
fhand.write("nasaWord = [")
first = True
for keyval in sortedLargeToSmall[:100]:
    if not first : fhand.write( ",\n")
    first = False
    size = counts[keyval]
    size = (size - lowest) / float(highest - lowest)
    size = int((size * bigsize) + smallsize)
    fhand.write("{text: '"+keyval+"', size: "+str(size)+"}")
fhand.write( "\n];\n")
fhand.close()
