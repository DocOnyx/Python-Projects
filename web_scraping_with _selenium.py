from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd



driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


driver.get('https://cryptoevents.global/')
show_more = driver.find_element(By.LINK_TEXT, 'Show more events')
show_more.click()
# text = driver.find_elements(By.CSS_SELECTOR, '.entry-content h1 strong')
# print([t.text for t in text])

conference = driver.find_elements(By.CSS_SELECTOR, '.entry-content p')

events = {}
for item in conference:
    idx = conference.index(item)
    links = item.find_elements(By.TAG_NAME, 'a')
    for x in links:
        if x.get_attribute('target') == '_blank':
            link = x.get_attribute('href')
            title = x.text
            
    details = item.text.splitlines()
    if len(details) > 2: 
        date_loc = details[-1].split('//')
        date = date_loc[0].strip()
        location = date_loc[1].strip()
        events[idx] = {'TITLE': title, 'LINK': link, 'DATE': date, 'LOCATION': location}
   
# print(events)
data_frame = pd.DataFrame(events)
data_frame = data_frame.transpose()
print(data_frame)


driver.quit()
