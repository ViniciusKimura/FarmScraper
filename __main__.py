from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from time import sleep
import undetected_chromedriver as uc

city = "São José dos Campos, SP"
property_type = "Rural"
property_type_op = ["Apartamento", "Casa", "Rural"]
payment_type = "Venda"
payment_type_op = ["Venda", "Aluguel"]

def wait_find_element(parent, by, value, timeout=15):
    return WebDriverWait(parent, timeout).until(
        EC.presence_of_element_located((by, value))
    )

driver = None
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
        wait_find_element(driver, By.CSS_SELECTOR, '[data-tracking="Alquilar"]').click()
    elif(payment_type == "Venda"):
        wait_find_element(driver, By.CSS_SELECTOR, '[data-tracking="Comprar"]').click()

    wait_find_element(driver, By.CSS_SELECTOR, '[data-qa="search-property-selector"]').click()
    if(property_type == "Apartamento"):
        wait_find_element(driver, By.CSS_SELECTOR, '[data-qa="search-property-selector-item-Apartamento (Todos)"]').click()
    elif(property_type == "Casa"):
        wait_find_element(driver, By.CSS_SELECTOR, '[data-qa="search-property-selector-item-Casa (Todos)"]').click()
    elif(property_type == "Rural"):
        wait_find_element(driver, By.CSS_SELECTOR, '[data-qa="search-property-selector-item-Rurais (Todos)"]').click()

    wait_find_element(driver, By.CSS_SELECTOR, '[data-qa="search-input"] input').send_keys(city)

    wait_find_element(driver, By.CSS_SELECTOR, 'button[data-qa="search-button"]').click()

    page_limit = 4
    for i in range(1, page_limit + 1):
        #driver.get(f"https://www.imovelweb.com.br/rurais-venda-sao-jose-dos-campos-sp-pagina-{i}.html")
        wait_find_element(driver, By.CLASS_NAME, 'postingsList-module__card-container')
        sleep(3)
        cards = driver.find_elements(By.CLASS_NAME, 'postingsList-module__card-container')
        print(f"Page {i}/{page_limit} - Total cards found: {len(cards)}")
        for card in cards:
            priceTag = card.find_element(By.CSS_SELECTOR,'[data-qa="POSTING_CARD_PRICE"]').text
            area_elements = card.find_elements(By.CSS_SELECTOR,'span.postingMainFeatures-module__posting-main-features-span')
            if area_elements:
                totalArea = area_elements[0].text
            else:
                totalArea = "N/A"
            location1 = card.find_element(By.CSS_SELECTOR,'h4.postingLocations-module__location-address').text
            location2 = card.find_element(By.CSS_SELECTOR,'h4.postingLocations-module__location-text').text
            link = card.find_element(By.CSS_SELECTOR,'[data-qa="posting PROPERTY"]')
            link = link.get_attribute("data-to-posting")
            id_link = link.split(".html")[0].split("-")[-1]

            arr.append([priceTag,totalArea,location1 + ", " + location2,"https://www.imovelweb.com.br" + link,id_link])

        if i < page_limit:
            next_page = wait_find_element(driver, By.CSS_SELECTOR, 'a[data-qa="PAGING_NEXT"]')
            driver.execute_script("arguments[0].click();",next_page)

            WebDriverWait(driver, 15).until(
                EC.staleness_of(cards[0])
            )
except Exception as e:
    print(f"Error occurred during scraping: {e}")
finally:
    sleep(2)
    if driver is not None:
        try:
            driver.quit()
        except Exception as e:
            print(f"Error closing driver: {e}")

# Save the data to a CSV file
sleep(2)
df = pd.DataFrame(arr[1:], columns=arr[0])
df.to_csv("farm_data.csv", index=False)