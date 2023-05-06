from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv

# make a request to a webpage
urls = ['https://hiraoka.com.pe/televisores/televisores',
       'https://hiraoka.com.pe/televisores/cine-en-casa',
       'https://hiraoka.com.pe/electrohogar/refrigeracion/refrigeradoras',
       'https://hiraoka.com.pe/electrohogar/cocina-y-empotrables',
       'https://hiraoka.com.pe/electrohogar/lavado-y-limpieza',
       'https://hiraoka.com.pe/computo-y-tecnologia/computadoras',
       'https://hiraoka.com.pe/computo-y-tecnologia/accesorios-computo',
       'https://hiraoka.com.pe/computo-y-tecnologia/fotografia',
       'https://hiraoka.com.pe/apple-peru/macbook',
       'https://hiraoka.com.pe/apple-peru/iphone',
       'https://hiraoka.com.pe/apple-peru/ipad',
       'https://hiraoka.com.pe/apple-peru/audio',
       'https://hiraoka.com.pe/celulares/celulares',
       'https://hiraoka.com.pe/celulares/smartwatch',
       'https://hiraoka.com.pe/gaming/consolas',
       'https://hiraoka.com.pe/gaming/accesorios-gaming',
       'https://hiraoka.com.pe/audio-y-musica/audifonos',
       'https://hiraoka.com.pe/audio-y-musica/audio']

# creating params
products=[] #List to store name of the product
prices_fp=[] #List to store final price of the product
prices_op=[] #List to store old price of the product
discounts=[] #List to store discounts of the product
list_urls=[] #List to store urls of the product

#url = "https://hiraoka.com.pe/computo-y-tecnologia/computadoras"
#response = requests.get(url)

# create a BeautifulSoup object from the webpage's HTML
#soup = BeautifulSoup(response.content, "html.parser")

# extract the HTML from the BeautifulSoup object
#html = soup.prettify()

#function
def string_to_float(texto):
    start = texto.find('S/') + 3
    end = len(texto)
    texto = texto[start:end]
    
    return float(texto.replace(',',''))

def obtain_pages(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    try:
        pagins = soup.find(attrs={'class':'items pages-items'}).text.split()
        pagins = [s for s in pagins if s not in ['Página','página','Estás','leyendo','la','Siguiente','Actualmente','estás','Anterior']]
        value2_ = []
        if '5' in pagins:
            print('si')
            value_ = pagins
            response = requests.get(url+"?p={}".format('5'))
            soup = BeautifulSoup(response.content, "html.parser")
            pagins = soup.find(attrs={'class':'items pages-items'}).text.split()
            pagins = [s for s in pagins if s not in ['Página','página','Estás','leyendo','la','Siguiente','Actualmente','estás','Anterior']]
            [value_.append(i) for i in pagins]
            #value_ = list(set(value_))
            [value2_.append(item) for item in value_ if item not in value2_]
            return value2_
        else:
            return pagins
    except:
        pagins = ['1']
        return pagins

def obtain_pages2(html_text):
    try:
        pagins = html_text.find(attrs={'class':'items pages-items'}).text.split()
        pagins = [s for s in pagins if s not in ['Página','página','Estás','leyendo','la','Siguiente','Actualmente','estás']]
    except:
        pagins = ['1']
    return pagins

for url_ in urls:
    print(url_)
    response = requests.get(url_)
    soup = BeautifulSoup(response.content, "html.parser")
    
    pages_f = obtain_pages(url_)

    for i in pages_f:
    #while(True):
        if i!='1':
            #driver.get(url_+"?p={}".format(i))
            response = requests.get(url_+"?p={}".format(i))
            soup = BeautifulSoup(response.content, "html.parser")
            print(url_+"?p={}".format(i))
        #content = driver.page_source
        #soup = BeautifulSoup(content)
        for a in soup.findAll(attrs={'class':'product details product-item-details'}):
            name=a.find('strong',attrs={'class':'product name product-item-name'}).find(attrs={'class':'product-item-link'})['title']
            price_fp=a.find('div',attrs={'class':"price-box price-final_price"}).find(attrs={'data-price-type':'finalPrice'}).text
            link = a.find('a',attrs={'class':'product-item-link'})['href']
            try:
                price_op=a.find('span',attrs={'class':'old-price'}).find('span',attrs={'data-price-type':'oldPrice'}).text
                discount=round((1-string_to_float(price_fp)/string_to_float(price_op))*100)
            except:
                price_op = ''
                discount = 0
            products.append(name)
            prices_fp.append(price_fp)
            prices_op.append(price_op)
            discounts.append(discount)
            list_urls.append(link)

df = pd.DataFrame({'Product Name':products,'Price_finalPrice':prices_fp,'Price_OldPrice':prices_op, 'Discount':discounts, 'Url_product':list_urls})
df = df.query("`Discount` >= 50").sort_values("Discount", ascending=False)
df.to_csv('products_hk.csv', sep=';', index=False, encoding='utf-8') #,quotechar='"',quoting=csv.QUOTE_NONNUMERIC)