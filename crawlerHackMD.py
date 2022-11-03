from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # 讓我們可以按鍵盤上的按鍵
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

def writeResult(result, filePath):
  f = open(filePath, 'w', encoding='utf-8-sig')
  for a in range(len(result)):
      f.write(str(result[a]) + '\n')
  f.close()
  
def crawlerHackMD(url, driverPath, part):
  idList = [] # 第幾行
  editorList = [] # 第幾行是誰編輯

  options = webdriver.ChromeOptions() 
  # to supress the error messages/logs
  options.add_experimental_option('excludeSwitches', ['enable-logging'])
  options.add_argument('--ignore-ssl-errors=yes')
  options.add_argument('--ignore-certificate-errors')
  options.add_argument('--disable-dev-shm-usage')
  options.add_argument('--disable-gpu') #關閉 GPU 避免某些系統或是網頁出錯
  options.add_argument('blink-settings=imagesEnabled=false')  # 不載入圖片, 提升速度
  options.add_argument('--no-sandbox') # 以最高權限執行
  options.add_argument("--disable-javascript") # 禁用 JavaScript
  # 禁用瀏覽器彈出視窗
  prefs = {  
      'profile.default_content_setting_values' :  {  
          'notifications' : 2  
      }  
  }  
  options.add_experimental_option('prefs',prefs)

  driver = webdriver.Chrome(options=options, service=Service(driverPath))
  driver.get(url)
  time.sleep(5)

  for i in range(1, part+1):
    # change to both mode
    WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.CLASS_NAME,'btn.btn-default.ui-both'))
    )
    bothBtn = driver.find_element(By.CLASS_NAME,'btn.btn-default.ui-both')
    bothBtn.click()
    
    WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.CLASS_NAME,'CodeMirror-code'))
    )
    lines = driver.find_element(By.CLASS_NAME,'CodeMirror-code').find_elements(By.CSS_SELECTOR,"div[style='position: relative;']")

    for line in lines:
      try:
          WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CLASS_NAME,'CodeMirror-linenumber'))
          )
          id = line.find_element(By.CLASS_NAME,'CodeMirror-linenumber').text
      except:
          print('catch id error')
          continue
      try:
          WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"pre span span"))
          )
          content = line.find_element(By.CSS_SELECTOR,"pre span span").text
      except:
          print('catch content error')
          continue
      # FIXME
      if(content != ''):
          try:
              WebDriverWait(driver, 50).until(
                EC.presence_of_element_located((By.CLASS_NAME,'authorship-gutter'))
              )
              editor = line.find_element(By.CLASS_NAME,'authorship-gutter').get_attribute("data-original-title")
              if(id not in idList):
                  idList.append(id)
                  editorList.append({'id':id, 'editor':editor})
          except:
              print('no editor')
    
    WebDriverWait(driver, 50).until(
      EC.presence_of_element_located((By.CLASS_NAME,'btn.btn-default.ui-view'))
    )
    # change to view mode
    viewBtn = driver.find_element(By.CLASS_NAME,'btn.btn-default.ui-view')
    viewBtn.click()
    time.sleep(3)
    # scroll down
    driver.execute_script(f'window.scrollTo(0, document.body.scrollHeight/{part}*{i})')
    time.sleep(3)
  driver.quit()
  return editorList



def main():
  # part = 15 
  crawlerResultPath = 'HackMD_Editors.txt' # 爬蟲結果位置
  url = 'https://hackmd.io/x-mWPyvdQ3GrWXNeKpYcIg?view' # HackMD 網址
  chromeDriverPath = 'chromedriver.exe'
  part = 15
  crawlerResult = crawlerHackMD(url, chromeDriverPath, part)
  writeResult(crawlerResult, crawlerResultPath)
main()