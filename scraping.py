from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import json
import argparse


N = 10

class Scraping:
    def __init__(self):
        s=Service(ChromeDriverManager().install())
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(service=s, chrome_options=options)

    def findInputs(self, inp):
        with open(inp, 'r') as f:
            inputs = json.load(f)
        return inputs

    def findTitreAuteurId(self):
        #Titre
        titre = self.soup.find("meta", {"name": "title"})
        #Auteur
        auteur = self.soup.find("link", {"itemprop": "name"})
        #ID
        idVideo = self.soup.find("meta", {"itemprop": "videoId"})
        return titre['content'], auteur['content'], idVideo['content']

    def findJaime(self):
        jaimebutton = self.soup.find("button", {"class": "yt-spec-button-shape-next yt-spec-button-shape-next--tonal yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m yt-spec-button-shape-next--icon-leading yt-spec-button-shape-next--segmented-start"})
        while jaimebutton == None:
            time.sleep(2)
            self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            jaimebutton = self.soup.find("button", {"class": "yt-spec-button-shape-next yt-spec-button-shape-next--tonal yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m yt-spec-button-shape-next--icon-leading yt-spec-button-shape-next--segmented-start"})
        if jaimebutton['aria-label'][0] == 'C':
            #Français
            jaime = jaimebutton['aria-label'].split("Cliquez sur \"J'aime\" pour cette vidéo comme ")[1].split(" autres internautes.")[0]
        else:
            #Anglais
            jaime = jaimebutton['aria-label'].split("like this video along with ")[1].split(" other people")[0]
        return jaime

    def findDescription(self):
        try:
            element = self.driver.find_element(By.XPATH, "//*[@id=\"content\"]/div[2]/div[6]/div[1]/ytd-button-renderer[1]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]")
            element.click()
        except NoSuchElementException:
            pass
        element = self.driver.find_element(By.XPATH, "//*[@id=\"expand\"]")
        element.click()
        time.sleep(1)
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        descDiv = self.soup.find("yt-formatted-string", {"class": "style-scope ytd-text-inline-expander"})
        return descDiv

    def findLiens(self, descDiv):
        listLiens = []
        liens = descDiv.find_all("a")
        for lien in liens:
            if lien["href"][0] == '/':
                listLiens.append("https://www.youtube.com"+lien["href"])
            else:
                listLiens.append(lien["href"])
        return listLiens

    def findCommentaires(self):
        commentaires = []
        element = self.driver.find_element(By.XPATH, "//*[@id=\"comments\"]")
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        commentsList = self.soup.find_all("ytd-comment-thread-renderer", {"class": "style-scope ytd-item-section-renderer"}, limit = N)
        while commentsList == []:
            time.sleep(1)
            self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            commentsList = self.soup.find_all("ytd-comment-thread-renderer", {"class": "style-scope ytd-item-section-renderer"}, limit = N)
        for comment in commentsList:
            commentaires.append(comment.find("yt-formatted-string", {"id": "content-text"}).text)
        return commentaires


    def focusId(self, id):
        self.driver.get("https://www.youtube.com/watch?v="+id)
        time.sleep(3)
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--input', action="store")
    parser.add_argument('--output', action="store")

    s = Scraping()

    args = parser.parse_args()
    inp = args.input
    outp = args.output
    inputs = s.findInputs(inp)
    dataList = {"videos_list": []}
    for input in inputs['videos_id']:
        s.focusId(input)
        titre, auteur, idVideo = s.findTitreAuteurId()
        jaime = s.findJaime()
        descDiv = s.findDescription()
        listLiens = s.findLiens(descDiv)
        commentaires = s.findCommentaires()

        data = {}
        data['Titre'] = titre
        data['Auteur'] = auteur
        data['PouceBleu'] = jaime
        data['Description'] = descDiv.text
        data['Liens'] = listLiens
        data['Id'] = idVideo
        data['Commentaires'] = commentaires
        dataList["videos_list"].append(data)

    with open(outp, 'w') as f:
        f.write(json.dumps(dataList, indent=4))

    s.driver.quit()

if __name__ == '__main__':
    main()