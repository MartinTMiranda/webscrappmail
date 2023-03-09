from bs4 import BeautifulSoup as soup
import requests
import pandas as pd
#url = "https://www.tailoy.com.pe/"
#url = 'https://www.tailoy.com.pe/tecnologia/tv-y-video.html'

urls = ['https://www.tailoy.com.pe/tecnologia/tv-y-video.html',
       'https://www.tailoy.com.pe/tecnologia/electrohogar/linea-blanca.html',
        'https://www.tailoy.com.pe/tecnologia/art-technology.html',
        'https://www.tailoy.com.pe/tecnologia/mundo-gamer.html',
        'https://www.tailoy.com.pe/tecnologia/audio.html',
        'https://www.tailoy.com.pe/tecnologia/fotografia.html',
        'https://www.tailoy.com.pe/tecnologia/celulares.html',
        'https://www.tailoy.com.pe/tecnologia/computo.html'
       ]

products=[] #List to store name of the product
prices_fp=[] #List to store final price of the product
prices_op=[] #List to store old price of the product
discounts=[] #List to store discounts of the product
urls_name=[] #List to store discounts of the product
## conf extraction

#function
def stringtofloat(texto):
    start = texto.find('S/') + 2
    end = len(texto)
    texto = texto[start:end]
    
    return float(texto.replace(',',''))


def make_soup(url):    
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
    page = requests.get(url,headers=header)
    page_soup = soup(page.content, 'lxml')
    return page_soup 

def obtain_pages(html_text):
    try:
        pagins = html_text.find(attrs={'class':'items pages-items'}).text.split()
        pagins = [s for s in pagins if s not in ['Página','página','Estás','leyendo','la','Siguiente']]
    except:
        pagins = ['1']
    return pagins

#print(make_soup(url))
for url in urls:
    
    html_text = make_soup(url)
    list_pagins = obtain_pages(html_text)
    
    for number in list_pagins:
        print(number)
        if number != '1':
            html_text = make_soup(url+'?p='+number)  
            print(url+'?p='+number)
    
        pages = html_text.findAll(attrs={'class':'product details product-item-details'})

        for page in pages:
            #print(page)
            link_ = page.find('a',attrs={'class':'product-item-link'})["href"]
            price_fp= page.find('div',attrs={'class':"price-box price-final_price"}).find(attrs={'data-price-type':'finalPrice'}).text

            try:
                price_op= page.find('span',attrs={'class':'old-price'}).find('span',attrs={'data-price-type':'oldPrice'}).text
                discount=round((1-stringtofloat(price_fp)/stringtofloat(price_op))*100)
            except:
                price_op = ''
                discount = 0
            #price_fp = page.find('span',attrs={'class':'special-price'}).find('span',attrs={'class':'price'}).text
            #price_op = page.find('span',attrs={'class':'old-price'}).find('span',attrs={'class':'price'}).text
            name_ = page.find('a',attrs={'class':'product-item-link'}).text.strip()
            #discount = round((1-stringtofloat(price_fp)/stringtofloat(price_op))*100)

            urls_name.append(link_)
            products.append(name_)
            prices_fp.append(price_fp)
            prices_op.append(price_op)
            discounts.append(discount)
        
df = pd.DataFrame({'Product Name':products,'Price_finalPrice':prices_fp,'Price_OldPrice':prices_op, 'Discount':discounts, 'Url_product':urls_name})
df = df.query("`Discount` >= 50").sort_values("Discount", ascending=False)
df.to_csv('products_tailoy.csv', sep=';',index=False, encoding='utf-8')
print('finish')
