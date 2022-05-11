from asyncio.windows_events import NULL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import matplotlib.pyplot as plt

def get_Top20_languages(browser):
    try:
        browser.get("https://www.tiobe.com/tiobe-index/")
        tiobe_file = open('Tiobe Top 20 lenguajes.txt', 'w', encoding = 'utf-8')
        table_top = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "top20"))
        )
        
        languages = table_top.find_element(by=By.TAG_NAME, value="tbody").find_elements(by=By.TAG_NAME, value="tr")
        dict_top20_name_rating = {'Nombre':[], 'Tiobe Rating': []}

        for language in languages:
            td = language.find_elements(by=By.TAG_NAME, value="td")
            tiobe_file.write(td[4].text + "\t" + td[5].text + '\n')
            dict_top20_name_rating['Nombre'].append(td[4].text)
            dict_top20_name_rating['Tiobe Rating'].append(td[5].text)
        return dict_top20_name_rating
    except:
        return NULL
    finally:
        tiobe_file.close()

def github_topics_top20(browser, topic):
    try:
        link_prefix = "https://github.com/topics/"
        list_of_wrong_names = ['C#','C++','Delphi/Object Pascal','Classic Visual Basic','Visual Basic']
        list_of_right_names = ['csharp','cpp','pascal','visual basic','vbnet']
        
        if topic in list_of_wrong_names:
            link = link_prefix + list_of_right_names[list_of_wrong_names.index(topic)]
        else:
            link = link_prefix + topic.lower()

        browser.get(link)
        
        repositories_with_text = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/main/div[2]/div[2]/div/div[1]/h2"))
        )

        for s in repositories_with_text.text.split():
            if s[:1].isdigit():
                repositories = s
                break


        return int(repositories.replace(",", ""))
    except:
        return NULL


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
    df = df.sort_values(by=['Github Rating'], ascending=False)
    print(df)
    df.to_csv('Top 20 lenguajes - Repositorios.txt', sep='\t',mode='w',index=False)
    bar_chart(df)

def bar_chart(df):
    df = df.sort_values(by = ['Github Rating'], ascending = False)
    fig, ax = plt.subplots(figsize =(16, 8))
    ax.bar(df['Nombre'], df['Github Rating'])
    plt.xlabel('Github Rating')
    plt.ylabel('Nombre')
    plt.title('Grafico de Github Rating del Top 20 Lenguajes', loc ='left')
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    plt.xticks(rotation=90)
    ax.grid(b = True, color ='grey',
        linestyle ='solid', linewidth = 0.5,
        alpha = 0.2)
    plt.subplots_adjust(bottom=0.23, right=0.95, top=0.94, left=0.05)
    plt.show()

# dictionary_top20_languages = {'Nombre': [], 'Tiobe Rating': [], 'Github Rating': []}
def main(browser):
    dictionary_top20_languages = get_Top20_languages(browser)
    list_top20_repositories = []
    file_top20_repositories = open('Resultados.txt', 'w', encoding = 'utf-8')
    for language in dictionary_top20_languages['Nombre']:
        repository = github_topics_top20(browser, language)
        list_top20_repositories.append(repository)
        file_top20_repositories.write(language + "\t" + str(repository) + '\n')
    
    file_top20_repositories.close()
    list_github_rating = github_rating(list_top20_repositories)
    dictionary_top20_languages['Github Rating'] = list_github_rating
    github_rating_dataframe(dictionary_top20_languages) #bar_chart is called inside this function

if __name__ == "__main__":
    try:
        browser = webdriver.Chrome("driver\\chromedriver.exe")
        main(browser)
    finally:
        browser.quit()
