import extruct
import requests
import pprint
import pandas as pd
import csv
from w3lib.html import get_base_url
from extruct.jsonld import JsonLdExtractor

#Lista de paginas en wong

urls_page = ['https://www.wong.pe/tecnologia/camaras/accesorios-de-camaras',
            #'https://www.wong.pe/tecnologia/camaras/camaras-de-accion',
            #'https://www.wong.pe/tecnologia/camaras/camaras-digitales',
            #'https://www.wong.pe/tecnologia/camaras/drones',
            'https://www.wong.pe/tecnologia/computo/all-in-one',
            'https://www.wong.pe/tecnologia/computo/laptops',
             'https://www.wong.pe/tecnologia/televisores?page=1',
             'https://www.wong.pe/tecnologia/televisores?page=2',
             'https://www.wong.pe/tecnologia/televisores?page=3',
             'https://www.wong.pe/tecnologia/televisores?page=4',
             'https://www.wong.pe/tecnologia/televisores?page=5',
             'https://www.wong.pe/tecnologia/televisores?page=6']


##set parameters
pp = pprint.PrettyPrinter(indent=2)
#r = requests.get('https://www.wong.pe/tecnologia/televisores?page=3')
#base_url = get_base_url(r.text, r.url)
####data = extruct.extract(r.text, base_url, syntaxes=['microdata', 'opengraph', 'rdfa'], uniform=True)
#data = extruct.extract(r.text, base_url=base_url)

products=[] #List to store name of the product
prices_fp=[] #List to store final price of the product
prices_op=[] #List to store old price of the product
discounts=[] #List to store discounts of the product
urls_name=[] #List to store discounts of the product
## conf extraction




## process
for urls__ in urls_page:
    r = requests.get(urls__)##'https://www.wong.pe/tecnologia/televisores?page=3')
    base_url = get_base_url(r.text, r.url)
    data = extruct.extract(r.text, base_url=base_url)
    jslde = JsonLdExtractor()
    data = jslde.extract(r.text)
    try:
        json_list = data[1]["itemListElement"]
        if len(json_list)!=0:
            for i in json_list:
                #print(i['position'])
                url_ = i["item"]['@id']
                name_ = i["item"]['name']
                price_fp = i["item"]['offers']['lowPrice']
                price_op = i["item"]['offers']['highPrice']
                discount = round((1-float(price_fp/price_op))*100)

                urls_name.append(url_)
                products.append(name_)
                prices_fp.append(price_fp)
                prices_op.append(price_op)
                discounts.append(discount)
    except:
        pass
    
        #break
    
df = pd.DataFrame({'Product Name':products,'Price_finalPrice':prices_fp,'Price_OldPrice':prices_op, 'Discount':discounts, 'Url_product':urls_name})
df.to_csv('products_wong_all.csv', sep=';' ,index=False, encoding='utf-8')
df = df.query("`Price_OldPrice` <= 1000").sort_values(by='Price_OldPrice', ascending=True)
df.to_csv('products_wong.csv', sep=';' ,index=False, encoding='utf-8') #,quotechar='"',quoting=csv.QUOTE_NONNUMERIC)
print('finish')
