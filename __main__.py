from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from time import sleep
import undetected_chromedriver as uc



try: 
    #arr = [["Price", "Total Area", "Location 1", "Location 2", "Link", "Anunciante ID", "Site ID", "Anunciante"]]
    arr = [["Price", "Total Area", "Location", "Link", "ID Link"]]

    options = webdriver.ChromeOptions() 
    options.headless = True
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    #driver = uc.Chrome(options=options)
    driver = uc.Chrome()

    
    for i in range(1, 5):
        driver.get(f"https://www.imovelweb.com.br/rurais-venda-sao-jose-dos-campos-sp-pagina-{i}.html")
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/div')
            )
        )
        count_card = driver.find_elements(By.XPATH, '/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/div')
        print(f"Total cards found: {len(count_card)}")
        for j in range(1, len(count_card) + 1):
            priceTag = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/div[{j}]/div/div[1]/div[2]/div[1]/div[1]/div[1]/div/div/div/div[1]/h2')))
            totalArea = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/div[{j}]/div/div[1]/div[2]/div[1]/div[1]/div[2]/h3/span[1]')))
            location1 = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/div[{j}]/div/div[1]/div[2]/div[1]/div[1]/div[3]/div/h4[2]')))
            location2 = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/div[{j}]/div/div[1]/div[2]/div[1]/div[1]/div[3]/div/h4[1]')))
            link = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/div[{j}]/div')))
            link = link.get_attribute("data-to-posting")
            id_link = link.split(".html")[0].split("-")[-1]

            arr.append([priceTag.text,totalArea.text,location1.text + ", " + location2.text,"https://www.imovelweb.com.br" + link,id_link])
except Exception as e:
    print(f"Error occurred while initializing the driver: {e}")


# Save the data to a CSV file
df = pd.DataFrame(arr[1:], columns=arr[0])
df.to_csv("farm_data.csv", index=False)