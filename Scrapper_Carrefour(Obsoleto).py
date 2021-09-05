import pyautogui
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time
import pandas as pd 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import select
from bs4 import BeautifulSoup # HTML data structure

#Fecha del dia
fecha = datetime.today().strftime('%Y/%m/%d')
#abre driver google chrome
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH) #Busca y abre chrome 
driver.maximize_window()
#archivo txt con los links de la pagina carrefour
urlsFile = open("D:\matias\Python scrapping\BOT CARREFOUR\links.txt", "r")
urls = urlsFile.readlines()

for url in urls:

    #listas con los atributos q vamos a obtener de cada producto
    lstmarca = []
    lstdescripcion = []
    lstprecio = []
    lstpromocion = []
    lstfecha = []
    lstid = []


    driver.get(url)

    time.sleep(3)
    #intenta reconocer una imagen que esta al final de la pagina de carrfour para saber si ya no hay mas elementos que cargar o una pagina siguiente
    while 2:
        if pyautogui.locateOnScreen('D:\matias\Python scrapping\BOT CARREFOUR\mailcarrefour.png', grayscale=True, confidence=0.8) == None:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            #Si hay para ver mas productos clickea el boton
            while 1:
                if pyautogui.locateOnScreen('D:\matias\Python scrapping\BOT CARREFOUR\Vermas.png', grayscale=True, confidence=0.8) != None: #Imagen de ver mas productos
                    pyautogui.click(x=1827, y=830, clicks=2, interval=0, button='left') #Para saber las coordenadas x e y usar el comando pyautogui.displayMousePosition()
                    time.sleep(4)
                else:
                    time.sleep(4)
                    break      
        else:
            break
    #HTML que nos interesa
    html = driver.page_source
    page_soup = BeautifulSoup(html)
    
    seccion = page_soup.select("body > div.ui-page.ui-page-theme-a.ui-page-active > div.wrapper > div.page > div.breadcrumbs > div > ul > li")[1].text.strip()
    #Creamos archivo csv con la fecha de hoy donde se guardara nuestra base de datos
    filename = datetime.now().strftime( seccion + "-" + 'PreciosCarrefour-%Y-%m-%d.csv')    
    f= open(filename, "w+")
    f.close()
    #Seccion html que nos interesa donde se encuentra informacion
    containers = page_soup.findAll("div", {"class": "product-container"}) # agarra cada producto
    
    #obtencion de cada atributo mediante parseo del codigo html
    for contain in containers :
        
        idproducto = contain.div.a['data-id']

        
        marca_producto = contain.find_all("p", {"class": "brand truncate"})[0].text.strip().replace(".", "").replace(",", ".") 

        descripcion_producto = contain.find_all("p", {"class": "title title-food truncate"})[0].text.strip().replace(".", "").replace(",", ".")   

        try:
            precio_producto = contain.find_all("p", {"class": "price 207 precio-regular-productos-destacados"})[0].text.strip().replace("$", "").replace(".", "").replace(",", ".")
  
        except:
            precio_producto = contain.find_all("p", {"class": "regular-price"})[0].text.strip().replace("$", "").replace("Precio", "").replace("regular","").replace(":","").replace(".", "").replace(",", ".")
    
        try:
            promocion_disponible = contain.find_all("p", {"class": "offer"})[0].text.strip().replace("$", "").replace(".", "").replace(",", ".")
            promocion = True
        except:
            promocion = False
           
        #Se agrega los atributos a las listas generadas anteriormente
        lstmarca.append(marca_producto)
        lstdescripcion.append(descripcion_producto)
        lstprecio.append(precio_producto)
        lstpromocion.append(promocion)
        lstfecha.append(fecha)
        lstid.append(idproducto)

    
    #creamos nuestro df y guardamos el archivo
    df = pd.DataFrame(list(zip(lstmarca, lstdescripcion, lstprecio, lstpromocion, lstfecha, lstid)), 
                   columns =['Marca', 'Producto', 'Precio', 'Promocion', 'Fecha', "ID"]) 

    df.drop_duplicates(subset=["ID"], keep="first", inplace=True)
    df.to_csv(filename, index=False)


