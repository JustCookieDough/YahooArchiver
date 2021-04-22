import requests, re, json
from bs4 import BeautifulSoup

class Answer:

    def __init__(self, url):
        page = requests.get(url)
        self.url = url

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

    def scroll(self, start, end):
        qid = self.url.split("=")[1]

        headers = {
            'authority': 'answers.yahoo.com',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'accept': 'application/json',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
            'content-type': 'application/json',
            'origin': 'https://answers.yahoo.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': self.url,
            'accept-language': 'en-US,en;q=0.9,es-CO;q=0.8,es;q=0.7',
        }

        data = '{"type":"CALL_RESERVICE","payload":{"qid":"' + qid + '","count":' + str(end) + ',"start":' + str(start) + ',"lang":"en-US","sortType":"RELEVANCE"},"reservice":{"name":"FETCH_QUESTION_ANSWERS_END","start":"FETCH_QUESTION_ANSWERS_START","state":"CREATED"},"kvPayload":{"key":"' + qid + '","kvActionPrefix":"KV/questionAnswers/"}}'

        response = requests.put('https://answers.yahoo.com/_reservice_/', headers=headers, data=data)
        
        decodeJson = json.loads(response.content.decode('utf-8'))
        for answer in decodeJson["payload"]["answers"]:
            self.answers.append([answer["answerer"]["nickname"], answer["text"]])
        return decodeJson
        
        