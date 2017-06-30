from selenium import webdriver

driver = webdriver.Chrome()
driver.get('http://www.baidu.com')

ele_input_id = driver.find_element_by_id('kw')
ele_btn = driver.find_element_by_id('su')

# 输入搜索内容
ele_input_id.send_keys('肖沪椿')
# 点击搜索按钮
ele_btn.click()
