import requests, re, json, time, configparser
from answer import Answer
from bs4 import BeautifulSoup

def main(): 
    print("loading config")
    try:
        config = configparser.RawConfigParser()
        configFilePath = "main.config"
        config.read(configFilePath)
        
        startingIndex = int(config.get("main-config", "starting-index"))
        date = config.get("main-config", "date").replace("/", "")
        fileLocation = config.get("main-config", "file-location")
        errorsLocation = config.get("main-config", "error-location")
        runLength = int(config.get("main-config", "run-length"))
    except:
        print("config load failed. halting")
        return

    print("config loaded. beginning scraping")
    
    for i in range(runLength):
        index = i + startingIndex
        url = "https://answers.yahoo.com/question/index?qid=10" + date + str(index).zfill(5) # the structure of a question id:
        print("testing " + url)                                                              # 10YYMMDDIIIII i is a 5 digit index
        if isValidPage(url):                                                                 # that seems to be sequential
            print("valid page found at " + url)
            try:
                ans = Answer(url)
                print("object generated, writing file")
                ans.writeJsonFile("10" + date + str(index).zfill(5), fileLocation)
                print("file written")
            except:
                print("error while generating object. logging")
                logErrors("10" + date + str(index).zfill(5), errorsLocation)


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
    pass

ans = Answer("https://answers.yahoo.com/question/index?qid=20210418200035AAAKmv6")
ans.scroll(11, 20)