# Modulos importados

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime
import os
import time

# Definir la carpeta de trabajo
os.chdir(r'C:\Users\usuario1\Documents\SEA\trafico')

def find_element_by_xpath(url, xpath, zona, data_list):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # Configurar el navegador
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Cargar la página
        driver.get(url)
        driver.implicitly_wait(10)

        # Obtener el elemento y sus propiedades
        element = driver.find_element(By.XPATH, xpath)
        text = element.text
        color = element.value_of_css_property("color")

        print(f"Zona: {zona} | Tiempo: {text} | Color: {color}")

        # Guardar resultado
        new_row = {'Zona': zona, 'Tiempo de demora': text, 
                   'Color de demora': color, 'date': datetime.now()}
        data_list.append(new_row)

    except Exception as e:
        print(f"Error en zona '{zona}': {e}")
    finally:
        driver.quit()

def main():
    data = [
        {"url": "https://www.google.com/maps/dir/-5.1710344,-80.6882293/-5.1936763,-80.6244806/@-5.1870059,-80.6751989,14.04z/data=!4m2!4m1!3e0?entry=ttu&g_ep=EgoyMDI1MDYxNy4wIKXMDSoASAFQAw%3D%3D", 
         "zona": "Avenida Sanchez Cerro"},
        {"url": "https://www.google.com/maps/dir/-5.1988818,-80.6187494/-5.227642,-80.6316605/@-5.2194806,-80.6368398,14.5z/data=!4m2!4m1!3e0?entry=ttu&g_ep=EgoyMDI1MDYyNi4wIKXMDSoASAFQAw%3D%3D", 
         "zona": "Avenida Progreso"},
        {"url": "https://www.google.com/maps/dir/-5.1937747,-80.6228514/-5.1778539,-80.5635536/@-5.1860711,-80.6052518,13.25z/data=!4m2!4m1!3e0?entry=ttu&g_ep=EgoyMDI1MDYyNi4wIKXMDSoASAFQAw%3D%3D", 
         "zona": "Avenida Guardia Civil"},
    ]

    xpath = '//*[@id="section-directions-trip-0"]/div[1]/div/div[1]/div[1]'
    data_list = []

    for item in data:
        find_element_by_xpath(item["url"], xpath, item["zona"], data_list)

    df = pd.DataFrame(data_list)

    try:
        existing_df = pd.read_excel('tiempo_demora.xlsx')
        df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        pass

    df.to_excel('tiempo_demora.xlsx', index=False)
    print(f"Datos guardados a las {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    while True:
        main()
        print("Esperando 1 hora...\n")
        time.sleep(3600)
