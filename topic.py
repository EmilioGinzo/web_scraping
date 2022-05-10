
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd


def get_associated_topics(browser, topic):
    link_prefix = "https://github.com/topics/"
    link = link_prefix + topic.lower() + '?o=desc&s=updated&page=' 
    wait = WebDriverWait(browser, 10)
    dict_of_related_topics = {'Topic': 0}
    
    # every article has many repositories topics
    for i in range(1,2):
        browser.get(link + str(i))
        list_articles = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "article")))
        for article in list_articles:
            list_of_related_topics_of_the_article = article.find_elements(by=By.CLASS_NAME, value="topic-tag")
            for topic in list_of_related_topics_of_the_article:
                if topic.text in dict_of_related_topics.keys():
                    dict_of_related_topics[topic.text] += 1
                else:
                    dict_of_related_topics[topic.text] = 1
    print("FUNCIONA")
    dict_sorted = sorted(dict_of_related_topics.items(), key=lambda kv: kv[1], reverse= True)
    for key, val in  dict_sorted:
        print(key + ' : ' + str(val))



def main(browser):
    get_associated_topics(browser, "bot")


browser = webdriver.Chrome("driver\\chromedriver.exe")
main(browser)

