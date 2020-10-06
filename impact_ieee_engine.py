from multiprocessing import Pool as ThreadPool, cpu_count #, Process, Manager
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import bs4 as bs
import time
import json
import requests
import datetime
data = {'journals_magazines':[], 'j_m_pages':[]}
#print("CPU COUNT: {}".format(cpu_count()))
#with open('data22.json') as json_file: data = json.load(json_file)
#try:
#    with open('all.json') as json_file: datanull = json.load(json_file)
#except BaseException as e:
#    print(e)

def get_id_split(s, sep):
    x = s.split(sep)
    for i in x:
        if i.isnumeric():
            return i

def mili_segundos():
    return time.time() * 1000

def thread_pool(size,data,func):
    with ThreadPool(size) as p: 
        pool= p.starmap(func,data)
        p.close()
        p.join()
        return pool

cont_excep = 0
def create_source(url,xpath):
    x=xpath[0]
    y=xpath[1]
    if 'http' in url:
        #print(url)

        firefox_profile = FirefoxProfile()
        ## Disable Flash
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

        driver_options = Options()

        driver_options.add_argument("--disable-extensions")

        driver_options.add_argument("--headless")

        driver_options.headless=True

        driver_options.add_argument("--disable-gpu")

        driver_options.add_argument("--log-level=3")

        firefox_binary = FirefoxBinary('/usr/bin/firefox')
        driver = webdriver.Firefox(firefox_binary=firefox_binary,firefox_profile=firefox_profile,firefox_options=driver_options)
        driver.set_page_load_timeout(186)
        driver.get(url)
        
        try:
            element = WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, "//a[@{x} = '{y}']".format(x=x,y=y))))
        except BaseException as e:
            print('--------------------------------------------------------------------------------')
            cont_excep+=1
            print(cont_excep)
            print(url)
            print("BaseException: {e} {t}".format(e=e,t=type(e)))
            print('--------------------------------------------------------------------------------')
        finally:
            source = driver.page_source
            driver.quit()
            #driver.close()
            return source
    else:
        return None

def create_soup(source):
    if source:
        soup = bs.BeautifulSoup(source,'html.parser')
        return soup
    else:
        return None

def get_journals_magazines_pages():
    source = create_source("https://ieeexplore.ieee.org/browse/periodicals/title?pageNumber=1&rowsPerPage=100",list(("_ngcontent-c36","")))
    soup = create_soup(source)
    journals_magazines_count = 0
    if soup:
        elements = soup.find_all('a')
        for pag in elements:
            if pag.get('_ngcontent-c36') == "" and pag.text.isnumeric():
                journals_magazines_count+=1
        for jm_page in range(1,journals_magazines_count+1):
            data['j_m_pages'].append("https://ieeexplore.ieee.org/browse/periodicals/title?pageNumber={}&rowsPerPage=100".format(jm_page))
    return journals_magazines_count

def get_journals_magazines(soup):
    if soup:
        elements = soup.find_all('a')
        for e in elements:
            if e.get('target') == '_self' and e.get('_ngcontent-c41') =="" and e.text != 'Most Recent Issue':
                jm =  {}
                jm['id']= get_id_split(e.get('href'),"=")
                jm['name']= e.text
                jm['url']= 'https://ieeexplore.ieee.org{}'.format(e.get('href'))
                data['journals_magazines'].append(jm)

def get_journals_magazines_factors(soup, idx):
    if soup:
        elements = soup.find_all('a', class_='stats-jhp-impact-factor')
        if elements:
            data['journals_magazines'][idx]['impact_factor']= (elements[0].text).replace("\n", "").strip()
            
        elements = soup.find_all('a', class_='stats-jhp-eigenfactor')
        if elements:
            data['journals_magazines'][idx]['eigenfactor']= (elements[0].text).replace("\n", "").strip()

        elements = soup.find_all('a', class_='stats-jhp-article-influence-score')
        if elements:
            data['journals_magazines'][idx]['influence_score']= (elements[0].text).replace("\n", "").strip()

        elements = soup.find_all('a', class_='u-mt-02')
        if elements:
            data['journals_magazines'][idx]['all_articles_url']= 'https://ieeexplore.ieee.org{}'.format(elements[0].get('href'))
            data['journals_magazines'][idx]['articles']=[]

def get_articles(soup, idx):
    if soup:
        elements = soup.find_all('a')
        l= open("A_URLS.txt","w+")
        for e in elements:
            if e.get('target') == '_self' and e.get('xplmathjax') =="":# and e.get('_ngcontent-c46') =="" and e.get('xplhighlight') =="" :

                a =  {}
                a['id']= get_id_split(e.get('href'),"/")
                a['name']= e.text
                a['url']= 'https://ieeexplore.ieee.org{}'.format(e.get('href'))
                a['ref_url']='https://ieeexplore.ieee.org/xpl/dwnldReferences?arnumber={}'.format(a['id'])
                data['journals_magazines'][idx]['articles'].append(a)
                l.write('https://ieeexplore.ieee.org{}'.format(e.get('href'))+'\n')
        l.close

def shoot():
    exce_time={'time':[]}
    et={}
    #se obtienen la cantidas de paginaciones para los Journals & Magazines.
    size = get_journals_magazines_pages()

    print('\n\n************** Journals & Magazines **************')
    #Se obtiene el link de cada uno de los jour o maga
    start_time = mili_segundos()
    temp1=[]
    for i in data['j_m_pages']:
        temp1.append(tuple([i,['_ngcontent-c40','']]))

    sources = thread_pool(size, temp1, create_source)
    
    soups = map(create_soup,sources)
    
    for s in soups:
        get_journals_magazines(s)
    end_time = mili_segundos() - start_time
    et['GET_JOURNAL_AND_MAGAZINES_4']=end_time/60000
    print("Tiempo de la operación: {ms}ms = {min}min".format(ms=end_time, min=end_time/60000))
    

    print('\n\n************** Factors y Todos_Articulos_URLs de Journals & Magazines **************')
    #Se obtienen Factors y el link que muestra todos los articulos de ese Journal o Magazine
    start_time = mili_segundos()
    temp2=[]
    for i in data['journals_magazines']:
        temp2.append(tuple([i['url'],['class','u-mt-02']]))
    print("cant jm: {}".format(len(temp2)))

    sources = thread_pool(15, temp2, create_source)

    soups = map(create_soup,sources)#create_soup(sources)

    for idx, val in enumerate(soups):
        get_journals_magazines_factors(val, idx)

    end_time = mili_segundos() - start_time
    et['GET_FACTORS_AND_ALL_ARTICLES_15']=end_time/60000
    print("Tiempo de la operación: {ms}ms = {min}min".format(ms=end_time, min=end_time/60000))
    

    print('\n\n************** Articulos Referencias_URLs **************')
    #Aquí se obtienen las urls de cada articulo como de sus referencias
    start_time = mili_segundos()
    total=[]
    oos=[]
    for jm in data['journals_magazines']:
        if 'all_articles_url' in jm:
            total.append(jm['all_articles_url'])
        else:
            print("Out of scope-> Name: {n} , URL: {u}".format(n=jm['name'],u=jm['url']))
            oos.append([jm['name'],jm['url']])
            total.append('-1')
    print("cant a: {}".format(len(total)))

    sources = []
    for i in total:
        sources.append(create_source(i,['xplmathjax','']))

    soups = map(create_soup,sources)#create_soup(sources)

    for idx, val in enumerate(soups):
        get_articles(val, idx)
    
    oos_dict = {}
    oos_dict['out_of_scope']=oos
    with open('oos.json', 'w') as json_file:
        json.dump(oos_dict, json_file)
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file)
    
    end_time = mili_segundos() - start_time
    et['GET_ARTICLES_AND_REFERENCES']=end_time/60000
    print("Tiempo de la operación: {ms}ms = {min}min".format(ms=end_time, min=end_time/60000))
    exce_time['time'].append(et)
    with open('EXCE_TIME_SHOOT.json', 'w') as json_file:
        json.dump(exce_time, json_file)


db={'dog_tags':[]}
def macros_palin(a):
    ar = a
    dog_tag = requests.get(ar['ref_url'])
    tx=create_soup(dog_tag.text).text
    ar['ref']=tx
    return ar
def kill_confirmed():
    print('\n\n************** Referencias **************')
    #Aquí se obtienen las referencias de cada articulo
    exce_time={'time':[]}
    et={}
    start_time = mili_segundos()
    if data:
        for jm in data['journals_magazines']:
            if 'articles' in jm:
                with ThreadPool(15) as p:
                    pool= p.map(macros_palin,jm['articles'])
                    p.close()
                    p.join()
                for ar in pool:
                    jom={}
                    jom['name']=jm['name']
                    jom['url']=jm['url']
                    if ('impact_factor' and 'eigenfactor' and 'influence_score') in jm:
                        jom['impact_factor']=jm['impact_factor'].replace("\t\t\t", " ")
                        jom['eigenfactor']=jm['eigenfactor'].replace("\t\t\t", " ")
                        jom['influence_score']=jm['influence_score'].replace("\t\t\t", " ")
                    ar['JM']=jom
                    db['dog_tags'].append(ar)
        with open('db3.json', 'w') as json_file:json.dump(db, json_file)
        print('Está hecho')
    end_time = mili_segundos() - start_time
    et['REFERENCES_15']=end_time/60000
    print("Tiempo de la operación: {ms}ms = {min}min".format(ms=end_time, min=end_time/60000))
    exce_time['time'].append(et)
    with open('EXCE_TIME_KILL_CONFIRMED.json', 'w') as json_file:
        json.dump(exce_time, json_file)

if __name__ == '__main__':
    while(True):
        shoot()
        kill_confirmed()
        last={'last_time':''}
        last['last_time']=datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open('last.json', 'w') as json_file:
            json.dump(last, json_file)
    
