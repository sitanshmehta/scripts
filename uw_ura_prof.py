from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

url = 'https://uwaterloo.ca/engineering/undergraduate-students/degree-enhancement/research-opportunities/ura-supervisor-list-and-usra-placement-list'
keywords = ['machine learning', 'drones', 'neural networks']

options = Options()
options.headless = False  # Keep this False for debugging

driver = webdriver.Chrome(options=options)
driver.get(url)

wait = WebDriverWait(driver, 20)

# Handle the cookies consent dialog
try:
    # Switch to iframe if the consent dialog is in one
    # If not in an iframe, you can comment out or remove these lines
    iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='consent']")))
    driver.switch_to.frame(iframe)

    # Find and click the accept button
    cookies_accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]")))
    cookies_accept_button.click()

    # Switch back to the main content
    driver.switch_to.default_content()
except Exception as e:
    print("Could not find or click the cookies accept button.")
    print(e)

# Scroll down to the "URA supervisor list" element
try:
    supervisor_list_element = wait.until(EC.presence_of_element_located((By.XPATH, "//summary[h2[text()='URA supervisor list']]")))
    driver.execute_script("arguments[0].scrollIntoView(true);", supervisor_list_element)
    time.sleep(2)
    supervisor_list_element.click()
except Exception as e:
    print("Could not find or click the supervisor list button.")
    print(e)
    driver.quit()
    exit()

# Wait for the accordions to load
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'uw-accordion')))

# Update the page source after clicking
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')

# Now extract the supervisors
accordions = soup.find_all('div', class_='uw-accordion')

results = []

for accordion in accordions:
    supervisor_button = accordion.find('button', class_='uw-accordion-trigger')
    if supervisor_button:
        supervisor_name = supervisor_button.get_text(strip=True)
    else:
        supervisor_name = "Unknown Supervisor"

    content_div = accordion.find('div', class_='uw-accordion-content')
    if content_div:
        research_desc = content_div.get_text(separator=' ', strip=True)
        if any(kw.lower() in research_desc.lower() for kw in keywords):
            results.append({'Supervisor': supervisor_name, 'Research': research_desc})

driver.quit()

if results:
    for result in results:
        print(f"Supervisor: {result['Supervisor']}")
        print(f"Research: {result['Research']}")
        print('-' * 80)
else:
    print("No matching supervisors found.")
