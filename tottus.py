### final code

import requests
from bs4 import BeautifulSoup
import pandas as pd

urls_ = [
    'https://tottus.falabella.com.pe/tottus-pe/category/cat40556/Videojuegos',
    'https://tottus.falabella.com.pe/tottus-pe/category/cat210477/TV-Televisores',
    'https://tottus.falabella.com.pe/tottus-pe/category/cat50678/Computadoras',
    'https://tottus.falabella.com.pe/tottus-pe/category/cat40488/Audio',
    'https://tottus.falabella.com.pe/tottus-pe/category/cat760702/Telefonia',
    'https://tottus.falabella.com.pe/tottus-pe/category/cat1830468/Smartwatch-y-wearables',
    'https://tottus.falabella.com.pe/tottus-pe/category/cat780530/Refrigerador',
    'https://tottus.falabella.com.pe/tottus-pe/category/cat40538/Cocina',
    'https://tottus.falabella.com.pe/tottus-pe/category/cat40662/Lavado',
    'https://tottus.falabella.com.pe/tottus-pe/category/cat6370558/Electrodomesticos-de-Cocina',
    'https://tottus.falabella.com.pe/tottus-pe/category/cat40487/Aspirado-y-Limpieza',
    'https://tottus.falabella.com.pe/tottus-pe/category/cat4100491/Ropa-interior-y-pijamas'    
]

lista_attrs = []
list_discount = []
list_pricecmr = []
list_priceoffer = []
list_pricenormal = []
list_urls = []
list_name = []
a = 0

#url = "https://www.falabella.com.pe/falabella-pe/category/cat50678/Computadoras"
# Send a request to the URL
#response = requests.get(url)
#soup = BeautifulSoup(response.content, "html.parser")

### get pages per page

def obtainpages(soup):
    pages_ = soup.find('ol',attrs={'class':'jsx-1794558402 jsx-1490357007'}).findAll('li')
    #pages_l = []
    pages_l=[pages_[i].text for i in range(len(pages_))]
    if '...' in pages_l:
        print("si")
        pages_l = list(range(1,int(pages_l[-1])+1))
    return pages_l

def stringtofloat(texto):
    start = texto.find('S/') + 2
    end = len(texto)
    texto = texto[start:end]
    if texto == '':
        texto = '0'
    
    return float(texto.replace(',',''))

for url in urls_:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    number = obtainpages(soup)

    for i in number:
        #print(i)
        if i != '1':
            print(url+"?page={}&store=tottus".format(i))
            if 'falabella-pe' in url:
                response = requests.get(url+"?page={}".format(i))
            else:
                response = requests.get(url+"?page={}&store=tottus".format(i))
            #print(response)
            soup = BeautifulSoup(response.content, "html.parser")
        
        #lista de productos a scrappear
        code_class = soup.find("div", attrs={"id":"testId-searchResults-products"})["class"][0]
        clase = soup.find_all("div",class_="{} search-results--products".format(code_class))[0].findAll("div")[0]["class"]
        clase_ = clase[0]+" "+clase[1]+" "+clase[2]
        lista_ = soup.find_all("div",class_="{} search-results--products".format(code_class))[0].find_all("div",class_=clase_)
        #the old version
        #lista_ = soup.find_all("div",class_="jsx-4099777552 search-results--products")[0].find_all("div",class_="jsx-1327784995 jsx-97019337 pod pod-4_GRID")

        for list_ in lista_:
            a = a+1
            #print(list_.find("ol").find_all("span"))
            lista_n = list_.find("ol").find_all("span")

            #lista_c = lista_[18]
            url_ = list_.find("a")["href"]
            try:
                name = list_.find("img")["alt"].strip()
                #print()
            except:
                name = list_.find_all("b")[1].text

            for x in range(len(lista_n)):
                #print(lista_n[x])
                value = lista_n[x].text.strip()

                if len(lista_n) == 1:
                    #print("es uno")
                    if all(any(m in y for y in lista_n[x]["class"]) for m in ['copy10','medium']):
                        price_o = lista_n[x].text.strip()
                        #print("PO: "+price_o)
                    price_n = ''
                    price_cmr = ''
                    discount = 0
                if len(lista_n) == 2:
                    #print("es dos")
                    if all(any(m in y for y in lista_n[x]["class"]) for m in ['copy10','medium']):
                        price_o = lista_n[x].text.strip()
                        #print("PO: "+price_o)
                    if all(any(m in y for y in lista_n[x]["class"]) for m in ['copy3','medium']):
                        price_n = lista_n[x].text.strip()
                        #print("PN: "+price_n)
                    price_cmr = ''
                    if price_n != '':
                        discount = int(str(round((1-(stringtofloat(price_o)/stringtofloat(price_n)))*100)))
                    else:
                        discount = 0

                if len(lista_n) == 3:
                    #print("es tres")
                    if all(any(m in y for y in lista_n[x]["class"]) for m in ['copy10','medium']):
                        price_o = lista_n[x].text.strip()
                        #print("PO: "+price_o)
                    if all(any(m in y for y in lista_n[x]["class"]) for m in ['copy3','medium']):
                        price_n = lista_n[x].text.strip()
                        #print("PN: "+price_n)
                    price_cmr = ''
                    if all(any(m in y for y in lista_n[x]["class"]) for m in ['copy5','primary']):
                        discount = -1*int(lista_n[x].text.strip().replace('%',''))
                        #print("DS: "+discount)

                if len(lista_n) == 4:
                    #print("es cuatro")
                    if all(any(m in y for y in lista_n[x]["class"]) for m in ['copy10','medium']):
                        price_o = lista_n[x].text.strip()
                        #print("PO: "+price_o)
                    if all(any(m in y for y in lista_n[x]["class"]) for m in ['copy3','medium']):
                        price_n = lista_n[x].text.strip()
                        #print("PN: "+price_n)
                    if all(any(m in y for y in lista_n[x]["class"]) for m in ['copy10','high']):
                        price_cmr = lista_n[x].text.strip()
                        #print("PC: "+price_cmr)
                    if all(any(m in y for y in lista_n[x]["class"]) for m in ['copy5','primary']):
                        discount = -1*int(lista_n[x].text.strip().replace('%',''))
                        #print("DS: "+discount)
            
            list_pricecmr.append(price_cmr)
            list_discount.append(discount)
            list_priceoffer.append(price_o)
            list_pricenormal.append(price_n)
            list_urls.append(url_)
            list_name.append(name)

df = pd.DataFrame({'Product Name':list_name,'Price_cmr':list_pricecmr,'Price_offer':list_priceoffer,'Price_normal':list_pricenormal, 'Discount':list_discount, 'links':list_urls})
df = df.query("`Discount` >= 50").sort_values("Discount", ascending=False)
df = df.drop_duplicates()
df.to_csv('products_tottus.csv', sep=',', index=False, encoding='utf-8')
