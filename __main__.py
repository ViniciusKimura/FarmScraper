from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
#from time import sleep
import undetected_chromedriver as uc

city = "São José dos Campos, SP"
property_type = "Rural"
property_type_op = ["Apartamento", "Casa", "Rural"]
payment_type = "Venda"
payment_type_op = ["Venda", "Aluguel"]

try: 
    #arr = [["Price", "Total Area", "Location 1", "Location 2", "Link", "Anunciante ID", "Site ID", "Anunciante"]]
    arr = [["Price", "Total Area", "Location", "Link", "ID Link"]]

    options = webdriver.ChromeOptions() 
    options.headless = True
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    #driver = uc.Chrome(options=options)
    driver = uc.Chrome(version_main=154)
    


    driver.get("https://www.imovelweb.com.br")
    if(payment_type == "Aluguel"):
        driver.find_element(By.XPATH, '/html/body/div[2]/main/div[4]/div/form/div/div[1]/div/ul/li[1]/button/div').click()
    elif(payment_type == "Venda"):
        driver.find_element(By.XPATH, '/html/body/div[2]/main/div[4]/div/form/div/div[1]/div/ul/li[2]/button/div').click()

    driver.find_element(By.XPATH, '/html/body/div[2]/main/div[4]/div/form/div/div[2]/div/label/div/div').click()
    if(property_type == "Apartamento"):
        driver.find_element(By.XPATH, '/html/body/div[2]/main/div[4]/div/form/div/div[2]/div/label/div/div[2]/div/div[1]/div[2]/div[1]').click()
    elif(property_type == "Casa"):
        driver.find_element(By.XPATH, '/html/body/div[2]/main/div[4]/div/form/div/div[2]/div/label/div/div[2]/div/div[2]/div[2]/div[1]').click()
    elif(property_type == "Rural"):
        driver.find_element(By.XPATH, '/html/body/div[2]/main/div[4]/div/form/div/div[2]/div/label/div/div[2]/div/div[3]/div[2]/div[1]').click()

    driver.find_element(By.XPATH, '/html/body/div[2]/main/div[4]/div/form/div/div[3]/div/div/ul/div/input').send_keys(city)

    driver.find_element(By.XPATH, '/html/body/div[2]/main/div[4]/div/form/div/div[4]/button').click()

    for i in range(1, 5):
        #driver.get(f"https://www.imovelweb.com.br/rurais-venda-sao-jose-dos-campos-sp-pagina-{i}.html")
        cards = driver.find_elements(By.CLASS_NAME, 'postingsList-module__card-container')
        print(f"Total cards found: {len(cards)}")
        for card in cards:
            priceTag = card.find_element(By.CSS_SELECTOR,'[data-qa="POSTING_CARD_PRICE"]').text
            totalArea = card.find_element(By.CSS_SELECTOR,'span.postingMainFeatures-module__posting-main-features-span').text
            location1 = card.find_element(By.CSS_SELECTOR,'h4.postingLocations-module__location-address').text
            location2 = card.find_element(By.CSS_SELECTOR,'h4.postingLocations-module__location-text').text
            link = card.find_element(By.CSS_SELECTOR,'[data-qa="POSTING_CARD_LINK"]')
            link = link.get_attribute("data-to-posting")
            id_link = link.split(".html")[0].split("-")[-1]

            arr.append([priceTag.text,totalArea.text,location1.text + ", " + location2.text,"https://www.imovelweb.com.br" + link,id_link])
except Exception as e:
    print(f"Error occurred while initializing the driver: {e}")


# Save the data to a CSV file
df = pd.DataFrame(arr[1:], columns=arr[0])
df.to_csv("farm_data.csv", index=False)