import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
options = Options()

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get('https://www.henryschein.es/es-es/DentalClinica/Default.aspx?did=DentalClinica')

categorias = driver.find_element(By.XPATH, "//h1[@class='large bold bg-super-lite pad']")

print(f'texto: {categorias.text}')
