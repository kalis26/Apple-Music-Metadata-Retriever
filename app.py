from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://music.apple.com/fr/search?term=influenceurs%20squeezie")

# Use CSS selector for multiple classes
elements_with_class = driver.find_elements(By.CSS_SELECTOR, ".click-action.svelte-c0t0j2")

string = elements_with_class[0].get_attribute("href")

print(string)

driver.quit()