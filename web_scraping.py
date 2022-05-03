from asyncio.windows_events import NULL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def get_Top20_languages(browser):
    try:
        browser.get("https://www.tiobe.com/tiobe-index/")
        tiobe_file = open('tiobe_top_20.txt', 'w', encoding = 'utf-8')
        table_top = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "top20"))
        )
        
        languages = table_top.find_element(by=By.TAG_NAME, value="tbody").find_elements(by=By.TAG_NAME, value="tr")
        dict_top20_name_rating = {'Nombre':[], 'Rating': []}

        for language in languages:
            td = language.find_elements(by=By.TAG_NAME, value="td")
            tiobe_file.write(td[4].text + "\t" + td[5].text + '\n')
            dict_top20_name_rating['Nombre'].append(td[4].text)
            dict_top20_name_rating['Rating'].append(td[5].text)
        return dict_top20_name_rating
    except:
        return NULL
    finally:
        tiobe_file.close()

def github_topics_top20(browser, topic):
    try:
        link_prefix = "https://github.com/topics/"
        list_of_wrong_names = ['C#','C++','Delphi/Object Pascal','Classic Visual Basic','Visual Basic']
        list_of_right_names = ['c-sharp','cpp','pascal','visual basic','vbnet']
        
        if topic in list_of_wrong_names:
            link = link_prefix + list_of_right_names[list_of_wrong_names.index(topic)]
        else:
            link = link_prefix + topic.lower()

        browser.get(link)
        resultados = open('Resultados.txt', 'a', encoding = 'utf-8')
        repositories_with_text = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/main/div[2]/div[2]/div/div[1]/h2"))
        )

        for s in repositories_with_text.text.split():
            if s[:1].isdigit():
                repositories = s
                break

        resultados.write(topic + "\t" + repositories + '\n')
        return int(repositories.replace(",", ""))
    except:
        return NULL
    finally:
        resultados.close()

def github_rating(list_top20_repositories):
    list_github_rating = []
    max_repositories = max(list_top20_repositories)
    min_repositories = min(list_top20_repositories)
    difference_max_min = max_repositories - min_repositories
    for repository in list_top20_repositories:
        list_github_rating.append(((repository - min_repositories)/difference_max_min)*100)
    return list_github_rating

def github_rating_dataframe(dictionary_top20_languages):
    df = pd.DataFrame.from_dict(dictionary_top20_languages)
    df = df.sort_values(by=['Rating'], ascending=False)
    print(df)
    df.to_csv('Top 20 lenguajes.txt', sep='\t',mode='w',index=False)

def main(browser):
    dictionary_top20_languages = get_Top20_languages(browser)
    list_top20_repositories = []
    for language in dictionary_top20_languages['Nombre']:
        list_top20_repositories.append(github_topics_top20(browser, language))
    list_github_rating = github_rating(list_top20_repositories)
    dictionary_top20_languages['Rating'] = list_github_rating
    github_rating_dataframe(dictionary_top20_languages)

browser = webdriver.Chrome("driver\\chromedriver.exe")
main(browser)
browser.quit()
