import requests, re, json, time, configparser, pprint
from answer import Answer
from bs4 import BeautifulSoup

def main(): 
    print("loading config")
    try:
        config = configparser.RawConfigParser()
        configFilePath = "main.config"
        config.read(configFilePath)
        
        startingIndex = int(config.get("main-config", "starting-index"))
        date = config.get("main-config", "start-date").replace("/", "")
        fileLocation = config.get("main-config", "file-location")
        errorsLocation = config.get("main-config", "error-location")
        numQuestionsPerDay = int(config.get("main-config", "num-questions-per-day"))
        numToIncrement = int(config.get("main-config", "num-to-increment-date"))
    except:
        print("config load failed. halting")
        return

    print("config loaded. beginning scraping")
    
    numSinceHit = 0
    i = 0

    while True:
        index = i + startingIndex
        url = "https://answers.yahoo.com/question/index?qid=10" + date + str(index).zfill(5) # the structure of a question id:
        print("testing " + url)                                                              # 10YYMMDDIIIII i is a 5 digit index
        if isValidPage(url):                                                                 # that seems to be sequential
            numSinceHit = 0                                                                  # thats the old qid system the new one
            print("valid page found at " + url)                                              # is a little different but its the same vibe
            try:                                                                             
                ans = Answer(url)
                print("object generated, writing file")
                ans.writeJsonFile("10" + date + str(index).zfill(5), fileLocation)
                print("file written")
            except:
                print("error while generating object. logging")
                logErrors("10" + date + str(index).zfill(5), errorsLocation)
        else:
            numSinceHit += 1
            print("too many misses. incrementing date")
            if (numSinceHit == numToIncrement):
                numSinceHit = 0
                i = 0
                date = incrementDate(date)
        if i > numQuestionsPerDay:
            print("reached end of scope. incrementing date")
            numSinceHit = 0
            i = 0
            date = incrementDate(date)
        i += 1



def isValidPage(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    if "Too Many Requests" in str(soup):
        print("lmao we're being rate limited pog")
        print("welp we gotta wait for like 10 minutes?")
        time.sleep(600)
        return False
    return not bool(soup.find("div", attrs={"class": "ErrorState__hintTitle___2_v9E"}))

def logErrors(index, filePath):
    file = open(filePath, "a")
    file.write(str(index) + "\n")

def incrementDate(date): # this is gonna fucking suck to write
    year = int(str(date)[:2])
    month = int(str(date)[2:4])
    day = int(str(date)[4:])
    if (month == 12 and day >= 31):
        year += 1
        month = 1
        day = 1
    elif (month == 2 and day >= 28):
        month += 1
        day = 1
    elif ((month == 4 or month == 6 or month == 9 or month == 11) and day >= 30):
        month += 1
        day = 1
    elif (day == 31):
        month += 1
        day = 1
    else:
        day += 1
    return str(year).zfill(2) + str(month).zfill(2) + str(day).zfill(2) # call me chef boyardee cause this is some fucking spaghetti code holy shit

main()