import requests, re, json
from bs4 import BeautifulSoup

class Answer:

    def __init__(self, url):
        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')

        qContainer = soup.find("div", attrs={"class": "Question__container___2Hui6"})
        self.title = qContainer.find("h1", attrs={"class": "Question__title___1Wgtn"}).text.strip()
        self.author = qContainer.find("span", attrs={"class": "Question__userName___1N1yX"}).text.strip()
        self.questionText = qContainer.find("div", attrs={"class": re.compile("ExpandableContent__content___2Iw4v")}).text.strip()
        if not self.questionText:
            self.questionText = None

        aContainer = soup.find("ul", attrs={"class": "AnswersList__answersList___2ikkB"})
        aList = aContainer.find_all("li")

        self.answers = []
        for ans in aList: 
            aTitle = ans.find(attrs={"class": "UserProfile__userName___1d1RW"})
            aBody = ans.find('p')
            if aTitle != None and aBody != None:
                aTitleText = aTitle.text.strip()
                aBodyText = aBody.text.strip()
                self.answers.append([aTitleText, aBodyText]) 

    def __str__(self):
        return "Title: {}\nAuthor: {}\nQuestion Text: {}".format(self.title, self.author, self.questionText)

    def writeJsonFile(self, fileName, filePath=""):
        data = {}
        data["title"] = self.title
        data["questionText"] = self.questionText
        data["author"] = self.author
        data["answers"] = []
        for ans in self.answers:
            data["answers"].append({"author": ans[0], "text": ans[1]})

        with open(filePath + fileName + ".json", "w") as outfile:
            json.dump(data, outfile)

            
    
        