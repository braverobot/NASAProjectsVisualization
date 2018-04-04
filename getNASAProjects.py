import sqlite3
import ssl
import sys
import urllib.request, urllib.parse, urllib.error
import json

dbname= "projectdb.sqlite"
baseurl = "https://techport.nasa.gov/api/projects/"

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Create DB
conn = sqlite3.connect(dbname)
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Projects
    (title TEXT, project_id INTEGER UNIQUE, website TEXT, 
    last_updated DATE, lead_organization TEXT)''')

start = None

try:
    row = cur.fetchone()
    if row is None :
        start = 0
    else:
        start = row[0]
except:
    start = 0

many = 0
count = 0
fail = 0

if ( many < 1 ) :
    conn.commit()
    yval = input('Please specify the year for project list beginning:')
    mval = input('Please specify the numerical month for project list beginning:')
    dval = input('Please specify the numerical day for project list beginning:')

    yval = "2018"
    mval = "03"
    dval = "01"

    beginningdate= (yval + '-' + mval + '-' + dval)

    if ( len(yval) is 0 or len(mval) is 0 or len(dval) is 0 ):
        print("Date not specified correctly")
        sys.exit()
    projectsurl = baseurl + '?updatedSince=' + beginningdate
try:
    # Open with a timeout of 5 seconds
    document = urllib.request.urlopen(projectsurl, None, 5, context=ctx)
    text = document.read().decode()
    parsed_json = json.loads(text)
    # Load the project id's into a list called projectlist
    projectlist= ((parsed_json['projects']['projects']))

    for d in projectlist:
        idval=int(d['id'])
        lupdate=(d['lastUpdated'])

        # get project description info
        projecturl = baseurl + str(idval)
        print(projecturl)
        document = urllib.request.urlopen(projecturl, None, 10, context=ctx)

        text1= document.read().decode()
        parsed_json1 = json.loads(text1)
        title= ((parsed_json1['project']['title']))

        try:
            site= ((parsed_json1['project']['website']))
            print(site)
        except:
            print("No Website field located")

        # insert the info into the database, or ignore the info if the unique guid is already in the project_id row

        try:
            count = count+1
            leadorg = ((parsed_json1['project']['leadOrganization']['name']))
            print(leadorg)
            cur.execute("INSERT OR IGNORE INTO Projects (title, project_id, website, last_updated, lead_organization) VALUES" + \
                "('{0}','{1}','{2}','{3}', '{4}')".format(title, idval, site, lupdate, leadorg))
            if count % 5 == 0:
                conn.commit()
                print("Committing to DB")
        except:
            print("No Lead Organization field located")

    if document.getcode() != 200 :
        print("Error code=",document.getcode(), projectsurl)
        sys.exit()

except KeyboardInterrupt:
    print('')
    print('Program interrupted by user...')
    sys.exit()


conn.commit()
cur.close()
print("Data loaded, feel free to open the projectdb.sqlite database")





