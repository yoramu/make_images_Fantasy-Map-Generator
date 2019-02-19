from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep
from tqdm import trange
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


driver = webdriver.Chrome("./chromedriver")
driver.get("https://azgaar.github.io/Fantasy-Map-Generator/")


template_list = ["Volcano", "High Island", "Low Island", "Continents", "Archipelago", "Atoll", "Mainland", "Peninsulas"]
width = "320"
height = "180"

#フォルダーをつくりそこに入れていく

#menuボタンを押す
driver.find_element_by_xpath('//*[@id="optionsTrigger"]').click()
#sleep(3)
#heatmapに設定する
map_element = driver.find_element_by_xpath('//*[@id="layoutPreset"]')
Select(map_element).select_by_value('layoutHeightmap')
#sleep(5)
#optionを押す
driver.find_element_by_xpath('//*[@id="optionsTab"]').click()
#sleep(3)
#画像の大きさを入力する
width_ele = driver.find_element_by_xpath('//*[@id="mapWidthInput"]')
width_ele.clear()
width_ele.send_keys(width)
height_ele = driver.find_element_by_xpath('//*[@id="mapHeightInput"]')
height_ele.clear()
height_ele.send_keys(height)
#属性を設定する
map_element = driver.find_element_by_xpath('//*[@id="templateInput"]')
Select(map_element).select_by_value(template_list[0])
#メジャーを消す
driver.find_element_by_xpath('//*[@id="customizeTab"]').click()
driver.find_element_by_xpath('//*[@id="editScale"]').click()
driver.find_element_by_xpath('//*[@id="toggleScaleBar"]').click()
driver.find_element_by_xpath('//*[@id="scaleBottom"]/button[2]').click()
#Scale Editorを閉じる
driver.find_element_by_xpath('//*[@id="dialogs"]/div[19]/div[1]/button').click()
#optionを押す(設定取得のため)
driver.find_element_by_xpath('//*[@id="optionsTab"]').click()

for i in trange(3000):
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "randomMap")))
        driver.find_element_by_xpath('//*[@id="randomMap"]').click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "saveButton")))
        driver.find_element_by_xpath('//*[@id="saveButton"]').click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "savePNG")))
        driver.find_element_by_xpath('//*[@id="savePNG"]').click()
        #html保存
        # html = driver.page_source
        html = driver.find_element_by_xpath('//*[@id="options"]').text
        d = datetime.now()
        with open("{0:%Y%m%d_%H%M%S}.txt".format(d), 'w', encoding='utf-8') as f:
                f.write(html)