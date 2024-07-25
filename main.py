import shutil
import os
import time
import zipfile
import send2trash
import smtplib
from bs4 import BeautifulSoup
import requests
import lxml
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

load_dotenv("D:/Python/AutomationTask/.env")

file_types = {
    "Image": [".jpg", ".jpeg", ".png", ".gif", ".tiff", ".bmp", ".eps"],
    "Code": [".ipynb", ".py", ".js", ".html", ".css", ".php", ".cpp", ".h", ".java"],
    "Document": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Audio": [".mp3", ".wav", ".aac", ".ogg"],
    "Video": [".mp4", ".avi", ".mov", ".flv", ".wmv", ".mpeg"],
    "Application": [".exe"]
}

temp_directories = [
    '/private/var/folders',
    '~/Library/Caches',
    '~/Library/Logs',
    '~/Downloads'
]

temp_extensions = [
    '.log',
    '.cache',
    '.tmp',
    '.dmg',
    '.pkg'
]

#Temp files cleanup

for directory in temp_directories:
    for folderName, subFolder, fileNames in os.walk(os.path.expanduser(directory)):
        for filename in fileNames:
            if os.path.splitext(filename)[1].lower() in temp_extensions:
                filepath = os.path.join(folderName, filename)
                try:
                    if os.path.isdir(filepath):
                        shutil.rmtree(filepath)
                    elif os.path.isfile(filepath):
                        send2trash.send2trash(filepath)
                except Exception as e:
                    print(f"{filename} could not be deleted because of {e}")

#Clean up of downloads folder
os.chdir("C://Users/hp Zbook/Downloads")
for filename in os.listdir():
    extension = os.path.splitext(filename)[1].lower()
    if extension in file_types["Document"]:
        filepath = "C:/Users/hp Zbook/Documents/Downloads"
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        if not os.path.exists(os.path.join(filepath, filename)):
            shutil.move(filename, filepath)
        print(f"Moving {filename} to {filepath}")
    elif extension in file_types["Image"]:
        filepath = "C:/Users/hp Zbook/Pictures/Downloads"
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        if not os.path.exists(os.path.join(filepath, filename)):
            shutil.move(filename, filepath)

        print(f"Moving {filename} to {filepath}")
    elif extension in file_types["Video"]:
        filepath = "C:/Users/hp Zbook/Videos"
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        if not os.path.exists(os.path.join(filepath, filename)):
            shutil.move(filename, filepath)

        print(f"Moving {filename} to {filepath}")
    elif extension in file_types["Application"]:
        filepath = "D:/Softwares"
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        if not os.path.exists(os.path.join(filepath, filename)):
            shutil.move(filename, filepath)

        print(f"Moving {filename} to {filepath}")
    elif extension in file_types["Code"]:
        filepath = "C:/Users/hp Zbook/Documents/Code"
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        if not os.path.exists(os.path.join(filepath, filename)):
            shutil.move(filename, filepath)

        print(f"Moving {filename} to {filepath}")
    elif extension in file_types["Audio"]:
        filepath = "C:/Users/hp Zbook/Music/Downloads"
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        if not os.path.exists(os.path.join(filepath, filename)):
            shutil.move(filename, filepath)

        print(f"Moving {filename} to {filepath}")
    else:
        continue


#Backing up coding work
def backup(backupFile, path):
    exclude = {'.venv', '.idea'}
    for folderName, subFolder, fileNames in os.walk(path, topdown=True):
        subFolder[:] = [directory for directory in subFolder if directory not in exclude]
        backupFile.write(folderName)
        print(f"Backing up {folderName}")
        for file in fileNames:
            backupFile.write(os.path.join(folderName, file))
            print(f"Backing up {file}")


backupFile1 = zipfile.ZipFile("C:/Coding Backup/BackupNew.zip", "a")
backup(backupFile1, "D:/Python")
backup(backupFile1, "D:/Java")
backup(backupFile1, "D:/Web Development")
try:
    os.unlink("C:/Coding Backup/Backup.zip")
except FileNotFoundError:
    print("This is the first Backup")
backupFile1.close()
os.rename("C:/Coding Backup/BackupNew.zip", "C:/Coding Backup/Backup.zip")

#Internet speed check and complain

# driverOptions = webdriver.ChromeOptions()
# driverOptions.add_experimental_option("detach", True)
driver = webdriver.Chrome()
driver.get("https://www.speedtest.net/")

time.sleep(2)

start_button = driver.find_element(By.CSS_SELECTOR, value=".start-button a")
start_button.click()

time.sleep(60)

download_speed = driver.find_element(By.XPATH,
                                     '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span').text
upload_speed = driver.find_element(By.XPATH,
                                   '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text
print(f"Download Speed: {download_speed}\nUpload Speed: {upload_speed}")

driver.close()

if float(download_speed) < 40 or float(upload_speed) < 40:
    with smtplib.SMTP("smtp.gmail.com") as conn:
        conn.starttls()
        conn.login(os.environ.get("MY_EMAIL"), os.environ.get("PASSWORD"))
        conn.sendmail(os.environ.get("MY_EMAIL"), os.environ.get("INTERNET_PROVIDER_EMAIL"),
                      msg=f"Subject: Slow Internet Speed\n\nI have been experiencing slow internet speed today and i would like for you to look into the matter\nDownload Speed: {download_speed}\nUpload Speed: {upload_speed}\nCustomer ID: {os.environ.get("CUSTOMER_ID")}")

#Check if there is a discount on wanted product

MY_EMAIL = os.environ.get("MY_EMAIL")
least_price = 100
amazon_url = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"

https_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,ur-PK;q=0.8,ur;q=0.7",

    "Priority": "u=0, i",
    "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

}

response = requests.get(url=amazon_url, headers=https_headers)
print(response.text)
soup = BeautifulSoup(response.text, "lxml")
price_whole = soup.find(name="span", class_="a-price-whole").getText()
price_fraction = soup.find(name="span", class_="a-price-fraction").getText()
currency_symbol = soup.find(name="span", class_="a-price-symbol").getText()
price_of_product = float(price_whole) + (float(price_fraction) / 100)
product_title = soup.select_one("#productTitle").getText().strip()
print(product_title)
print(price_of_product)

if price_of_product < least_price:
    with smtplib.SMTP("smtp.gmail.com") as Connection:
        Connection.starttls()
        Connection.login(MY_EMAIL, os.environ.get("PASSWORD"))
        Connection.sendmail(MY_EMAIL, MY_EMAIL,
                            f"Subject:Amazon Price Alert!\n\n{product_title} for only {currency_symbol}{price_of_product}\n{amazon_url}".encode(
                                "utf-8"))
