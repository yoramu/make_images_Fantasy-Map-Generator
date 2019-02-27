from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep
from tqdm import trange
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import os
import json


def driver_setting():
	d = datetime.now()
	download_directory  = "setting_{0:%Y%m%d_%H%M%S}".format(d)
	os.mkdir(download_directory)

	chop = webdriver.ChromeOptions()
	prefs = {"download.default_directory" : download_directory}
	chop.add_experimental_option("prefs",prefs)
	chop.add_argument('--ignore-certificate-errors')

	driver = webdriver.Chrome("./chromedriver",chrome_options = chop)
	driver.get("https://azgaar.github.io/Fantasy-Map-Generator/")
	return driver, download_directory


def map_style_setting(driver, template):
	move = ActionChains(driver)
	driver.find_element_by_xpath('//*[@id="styleTab"]').click()
	#海を真っ黒にする スライダーを0にする
	ele = driver.find_element_by_xpath('//*[@id="styleOpacityInput"]')
	move.click_and_hold(ele).move_by_offset(-60, 0).release().perform()
	#style選択のelement
	map_element = driver.find_element_by_xpath('//*[@id="styleElementSelect"]')
	#coastlineを選択 ２つのスライダーを0にする
	Select(map_element).select_by_value('coastline')
	ele = driver.find_element_by_xpath('//*[@id="styleStrokeWidth"]')
	move.click_and_hold(ele).move_by_offset(-70, 0).release().perform()
	ele = driver.find_element_by_xpath('//*[@id="styleOpacity"]')
	move.click_and_hold(ele).move_by_offset(-90, 0).release().perform()
	#landmassを選択 スライダを0にする
	Select(map_element).select_by_value('landmass')
	ele = driver.find_element_by_xpath('//*[@id="styleOpacity"]')
	move.click_and_hold(ele).move_by_offset(-90, 0).release().perform()
	#coastlineを選択 ２つのスライダーを0にする
	Select(map_element).select_by_value('lakes')
	ele = driver.find_element_by_xpath('//*[@id="styleStrokeWidth"]')
	move.click_and_hold(ele).move_by_offset(-70, 0).release().perform()
	ele = driver.find_element_by_xpath('//*[@id="styleOpacity"]')
	move.click_and_hold(ele).move_by_offset(-90, 0).release().perform()

def map_setting(driver, width, height, template):
	#menuボタンを押す
	driver.find_element_by_xpath('//*[@id="optionsTrigger"]').click()
	#heatmapに設定する
	map_element = driver.find_element_by_xpath('//*[@id="layoutPreset"]')
	Select(map_element).select_by_value('layoutHeightmap')
	#Riversをボタンをoffにする
	driver.find_element_by_xpath('//*[@id="toggleRivers"]').click()
	#style変更
	map_style_setting(driver, template)
	#optionを押す
	driver.find_element_by_xpath('//*[@id="optionsTab"]').click()
	#画像の大きさを入力する
	width_ele = driver.find_element_by_xpath('//*[@id="mapWidthInput"]')
	width_ele.clear()
	width_ele.send_keys(width)
	height_ele = driver.find_element_by_xpath('//*[@id="mapHeightInput"]')
	height_ele.clear()
	height_ele.send_keys(height)
	#属性を設定する
	map_element = driver.find_element_by_xpath('//*[@id="templateInput"]')
	Select(map_element).select_by_value(template)
	#メジャーを消す
	driver.find_element_by_xpath('//*[@id="customizeTab"]').click()
	driver.find_element_by_xpath('//*[@id="editScale"]').click()
	driver.find_element_by_xpath('//*[@id="toggleScaleBar"]').click()
	driver.find_element_by_xpath('//*[@id="scaleBottom"]/button[2]').click()
	#Scale Editorを閉じる
	driver.find_element_by_xpath('//*[@id="dialogs"]/div[19]/div[1]/button').click()
	#optionsを押す
	driver.find_element_by_xpath('//*[@id="optionsTab"]').click()
	#設定画面の透明度を上げてマップを見れるようにする
	move = ActionChains(driver)
	ele = driver.find_element_by_xpath('//*[@id="transparencyInput"]')
	move.click_and_hold(ele).move_by_offset(90, 0).release().perform()
	#png resolutionを等倍にする
	ele = driver.find_element_by_xpath('//*[@id="pngResolutionInput"]')
	move.click_and_hold(ele).move_by_offset(-90, 0).release().perform()


        

def save_map_images(driver,download_directory,template, width, height, flag):
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "randomMap")))
	driver.find_element_by_xpath('//*[@id="randomMap"]').click()
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "saveButton")))
	driver.find_element_by_xpath('//*[@id="saveButton"]').click()
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "savePNG")))
	driver.find_element_by_xpath('//*[@id="savePNG"]').click()
	#don't show again
	if not flag:
		driver.find_element_by_xpath('//*[@id="dialogs"]/div[18]/div[3]/div/button[1]').click()
	#jsonにする
	settingDict = {
		"width" : width,
		"height" : height,
		"map_cells_density" : int(driver.find_element_by_xpath('//*[@id="sizeOutput"]').text),
		"heightmap_template" : template,
		"burgs_count" : int(driver.find_element_by_xpath('//*[@id="manorsOutput"]').text),
		"states_count" : int( driver.find_element_by_xpath('//*[@id="regionsOutput"]').text),
		"states_disbalance" : int(driver.find_element_by_xpath('//*[@id="powerOutput"]').text),
		"neutral_distance" : int(driver.find_element_by_xpath('//*[@id="neutralOutput"]').text),
		"cultures_count" : int(driver.find_element_by_xpath('//*[@id="culturesOutput"]').text),
		"precipitation" : int(driver.find_element_by_xpath('//*[@id="precOutput"]').text),
		"relief_icons_size" : int(driver.find_element_by_xpath('//*[@id="reliefSizeOutput"]').text),
		"relief_density" : int(driver.find_element_by_xpath('//*[@id="reliefDensityOutput"]').text[:-1]),
		"swampiness" : int(driver.find_element_by_xpath('//*[@id="swampinessOutput"]').text),
		"transparency" : int(driver.find_element_by_xpath('//*[@id="transparencyOutput"]').text),
		"png_resolution" : int(driver.find_element_by_xpath('//*[@id="pngResolutionOutput"]').text[:-1]),
	}
	#Layoutを押す(map seedを取得)
	driver.find_element_by_xpath('//*[@id="layoutTab"]').click()
	settingDict["map_seed"] = driver.find_element_by_xpath('//*[@id="optionsSeed"]').get_attribute("value")
	d = datetime.now()
	with open(os.path.join(download_directory, "{0:%Y%m%d_%H%M%S}.txt".format(d)), 'w', encoding='utf-8') as f:
		f.write(json.dumps(settingDict))
	# optionsを押す
	driver.find_element_by_xpath('//*[@id="optionsTab"]').click()


def main():
	flag = False
	number_of_times = 3000
	template_list = ["Volcano", "High Island", "Low Island", "Continents", "Archipelago", "Atoll", "Mainland", "Peninsulas"]
	template = "Archipelago"
	width = "320"
	height = "180"
	driver, download_directory = driver_setting()
	map_setting(driver, width, height, template)
	for i in trange(number_of_times):
		save_map_images(driver, download_directory, template, width, height, flag)
		flag = True



if __name__ == '__main__':
	main()