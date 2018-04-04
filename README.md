**NASA Project Name keyword visualization**

The **getNasaProjects.py** script pulls all of the projects from a specific date and loads them into a local sqlite3 db.

The **wordMapCreate.py** script then reaches into that sqlite3 db and takes the title of each project, removes uninteresting words (and, or, to, the, etc) and adds them to a dictionary with the number of times they appear. It then creates a htm page that you can open locally to view a word cloud of the most common used words in the titles.

My scripts make use of the d3.layout.cloud.js and the d3.v2.js javascripts that are readily available at  http://www.jasondavies.com/word-cloud/ but provided in my repo for ease

- To use: clone repo and build the database by running the following:
```
python3 getNasaProjects.py
```
- Then run the wordmap htm builder:
```
python3 wordMapCreate.py
```
- You can then locally open the nassaWord.htm file
```
open nasaWord.htm
```
