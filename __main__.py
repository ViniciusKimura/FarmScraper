from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from time import sleep


try: 
    #arr = [["Price", "Total Area", "Location 1", "Location 2", "Link", "Anunciante ID", "Site ID", "Anunciante"]]
    arr = [["Price", "Total Area", "Location 1", "Location 2", "Link"]]
    driver = webdriver.Chrome()

    driver.get("https://www.imovelweb.com.br/rurais-venda-sao-jose-dos-campos-sp.html")
    for i in range(1, 30):
        priceTag = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/div[{i}]/div/div[1]/div[2]/div[1]/div[1]/div[1]/div/div/div/div[1]/h2')))
        totalArea = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/div[{i}]/div/div[1]/div[2]/div[1]/div[1]/div[2]/h3/span[1]')))
        location1 = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/div[{i}]/div/div[1]/div[2]/div[1]/div[1]/div[3]/div/h4[2]')))
        location2 = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/div[{i}]/div/div[1]/div[2]/div[1]/div[1]/div[3]/div/h4[1]')))

        link = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/div[{i}]/div')))
        print(link.get_attribute("data-to-posting"))
        #WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/div[{i}]/div/div[1]/div[2]/div[1]/div[1]/div[3]/div/h4[1]'))).click()

        #link = driver.current_url
        #anuncianteID = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[2]/main/div/div/article/div/section[7]/ul/li[1]')))
        #siteID = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[2]/main/div/div/article/div/section[7]/ul/li[2]')))
        #anunciante = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[2]/main/div/div/aside/div/div/div/div/div[2]/div/div[2]/a')))

        #driver.back()

        #arr.append([priceTag.text, totalArea.text, location1.text, location2.text, link, anuncianteID.text, siteID.text, anunciante.text])
        arr.append([priceTag.text, totalArea.text, location1.text, location2.text, "https://www.imovelweb.com.br" + link.get_attribute("data-to-posting")])
except Exception as e:
    print(f"Error occurred while initializing the driver: {e}")
finally:
    driver.quit()

# Save the data to a CSV file
df = pd.DataFrame(arr[1:], columns=arr[0])
df.to_csv("farm_data.csv", index=False)