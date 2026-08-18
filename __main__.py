from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from time import sleep
from seleniumbase import sb_cdp
from playwright.sync_api import sync_playwright
  
#arr = [["Price", "Total Area", "Location 1", "Location 2", "Link", "Anunciante ID", "Site ID", "Anunciante"]]
arr = [["Price", "Total Area", "Location", "Link", "ID Link"]]

sb = sb_cdp.Chrome()
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    page = browser.contexts[0].pages[0]

    for i in range(1, 10):
        page.goto(f"https://www.imovelweb.com.br/rurais-venda-sao-jose-dos-campos-sp-pagina-{i}.html")
        sb.solve_captcha()
        count_card = sb.select_all("xpath=/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/div")
        total_cards = len(count_card)
        print(f"Total cards found: {total_cards}")
        
#driver = uc.Chrome(options=options)


for i in range(1, 5):
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



# Save the data to a CSV file
df = pd.DataFrame(arr[1:], columns=arr[0])
df.to_csv("farm_data.csv", index=False)