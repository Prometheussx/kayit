from selenium import webdriver
from selenium.webdriver.common.by import By
#make sure you have selenium library if not, type in cmd: pip install selenium
#this will install selenium
# Subscribe to www.youtube.com/HasanImam

driver =  webdriver.Chrome('C:\\Users\\erdem\\OneDrive\\Masaüstü\\Main\\Aşkımınwpbotu\\chromedriver.exe')#webdrivers link will be in video description
driver.get("https://web.whatsapp.com/")

i = 1
while i == 1:
    def dongu(driver):
        print("Login now...\n")

        name = input("Enter name:")
        count = int(input("Count: "))
        msg = input("Message: ")


        user = driver.find_element(By.XPATH,'//span[@title = "{}"]'.format(name))
        user.click()

        msgBox = driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]')

        for i in range(count):
            msgBox.send_keys(msg)
            sendButton = driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')
            sendButton.click()


        print("Mission Successful")
        print(f"{count} messages were sent to {name}")
        return
    
    dongu(driver)