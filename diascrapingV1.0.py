from bs4 import BeautifulSoup as soup  # HTML data structure
import random
from datetime import datetime
import time
import pandas as pd
from urllib.request import urlopen as uReq  # Web client
#MInuto en el que empieza el script
start_time = time.time()
#Fecha del dia 
hoy=datetime.now().strftime("%Y-%m-%d")
#Creamos archivo
filename = datetime.now().strftime('PreciosDia-%Y-%m-%d.csv')    
f= open(filename, "w+")
f.close()
#Txt con los links base que vamos a buscar
urlsFile = open("D:\matias\Python scrapping\Scraper Dia\scraper dia\linksdia.txt", "r")
urls = urlsFile.readlines()
#Atributos que nos interesa conseguir
lstmarca = []
lstdescripcion = []
lstprecionormal = []
lstpreciopromo = []
lstfecha=[]

#funcion recurisva que nos va a conseguir los atributos
def links_recursion(x):
        #Html de los links
        page_url= url.strip() + str(x)
        uClient = uReq(page_url)
        page_soup = soup(uClient.read(), "html.parser")
        uClient.close()
        time.sleep(1)
        containers = page_soup.findAll("li", {"layout": "8d6fe5d3-768b-4f53-92b9-71d5c173042f"})
        #obtencion de atributos, 
        if containers !=[]:
            #Nuevas listas temporales para los atributos de los productos en la pagina
            lstmarca1 = []
            lstdescripcion1 = []
            lstprecionormal1 = []
            lstpreciopromo1 = []
            for contain in containers:
                if contain.findAll("div", {"class": "marca"}) !=[] :        
                    try:
                        marca_producto = contain.findAll("div", {"class": "marca"})[0].text.strip().replace(".", "").replace(",", ".")
                    except:
                        marca_producto ="None"
                    try:
                        precio_normal= float(contain.findAll("span", {"class": "old-price"})[0].text.strip().replace("$", "").replace(".", "").replace(",", ".").replace("$", ""))
                        precio_promo= float(contain.findAll("span", {"class": "best-price"})[0].text.strip().replace("$", "").replace(".", "").replace(",", ".").replace("$", ""))

                    except:
                        precio_promo = "None"
                        precio_normal= float(contain.findAll("span", {"class": "best-price"})[0].text.strip().replace("$", "").replace(".", "").replace(",", ".").replace("$", ""))

                    try:
                        descripcion_producto = contain.findAll('a')[1].text.strip().replace(".", "").replace(",", ".")
                    except:
                        descripcion_producto = "None"  
                    #Agrega los atributos a la lista                      
                    lstmarca1.append(marca_producto)
                    lstdescripcion1.append(descripcion_producto)
                    lstprecionormal1.append(precio_normal)
                    lstpreciopromo1.append(precio_promo)
                    lstfecha.append(hoy)
            #Agrega nuestros  en la lista general        
            lstpreciopromo.extend(lstpreciopromo1)
            lstmarca.extend(lstmarca1)
            lstdescripcion.extend(lstdescripcion1)
            lstprecionormal.extend(lstprecionormal1)       
            #Nos permite ir hacia el siguiente link y arrancar nuevamente nuestra funcion
            x+=1
            links_recursion(x)       
                 
                 
   

        return lstmarca, lstdescripcion, lstprecionormal, lstpreciopromo
#Arrancamos nuestra funcion recursiva para cada link
for url in urls:    
    x=1
    links_recursion(x)

#Creamos nuestra dataframe y guardamos la base de datos
df = pd.DataFrame(list(zip(lstmarca, lstdescripcion, lstprecionormal, lstpreciopromo,lstfecha)), 
                columns =['Marca', 'Producto', 'Precio normal', 'PrecioPromocion', "fecha"]) 
df.drop_duplicates(subset=["Producto"], keep="first", inplace=True)
df.to_csv(filename, index=False) 
#Mensaje que nos indica la finalizacion del script y cuanto tiempo tardo
print("--- %s seconds ---" % (time.time() - start_time))