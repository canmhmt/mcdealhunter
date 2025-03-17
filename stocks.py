from bs4 import BeautifulSoup
import time
from app.models import PsqlQuery
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import yagmail
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

yag = yagmail.SMTP(user='canmhmtgt@gmail.com', password='password')

def create_app():
    while True:
        zara_urls = PsqlQuery.get_urls_query("zara")
        hm_urls = PsqlQuery.get_urls_query("hm")
        if zara_urls or hm_urls:
            print("The urls copied from Database")
        else:
            print("There is no url in database.")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        while True:
            try:
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service)
                break
            
            except Exception as e:
                print("The Chrome could not start. Trying again in 5 sec..")
                time.sleep(5)

        if zara_urls:
            zara_stocks(zara_urls, driver)
        if hm_urls:
            hm_stocks(hm_urls, driver)
        driver.close()

        time.sleep(250)

def zara_stocks(zara_urls, driver):
    for url in zara_urls:
        stock_link = url[0]
        username = url[1]
        stock_source = url[2]
        mail = url[3]
        link_id = url[4]
        price = 0
        while True:
            try:       
                driver.get(stock_link)
                try:
                    button = driver.find_element(By.CSS_SELECTOR, "button.zds-button.store-selector__button.worldwide__submit-button.zds-button--secondary")
                    if button:
                        button.click()
                except:
                    pass

                soup = BeautifulSoup(driver.page_source, "html.parser")
                item_picture_div = soup.find("picture", class_ = "media-image")
                try:
                    item_picture = item_picture_div.find_all("img", class_ = "media-image__image media__wrapper--media")
                except:
                    item_picture = None
                if item_picture is not None:
                    for img in item_picture:
                        if img["src"] == "https://static.zara.net/stdstatic/6.40.0/images/transparent-background.png":
                            img.decompose()
                if item_picture:
                    item_picture_url = item_picture[0]["src"]
                else:
                    item_picture_url = "https://brandlogos.net/wp-content/uploads/2022/04/zara-logo-brandlogos.net_-512x512.png"

                outher_stock_status = soup.find("span", class_ = "product-detail-show-similar-products__action-tip")
                break
            except Exception as e:
                print("Connection problem, trying again..", e)
                time.sleep(5)

        try:
            inner_stock_status = outher_stock_status.find("span")
            if inner_stock_status and inner_stock_status.text.strip() == "TÜKENDİ":
                try:
                    PsqlQuery.delete_stock_info(stock_link)
                    sizes = None
                    send_mail(2, mail, stock_link, sizes, stock_source)
                except:
                    pass
        except:
            which_stock = soup.find_all("div", class_ = "size-selector-sizes-size__info")
            for stock in which_stock:
                span = stock.find("span") 
                if span and span.text.strip() == "Az sayıda ürün":
                    span.decompose()
                
                viewsimilars = stock.find_all("div", class_ = "size-selector-sizes-size__view-similars")
                if viewsimilars:
                    size_label = stock.find("div", class_ = "size-selector-sizes-size__label")
                    if size_label:
                        sizes = size_label.text.strip()
                        try:
                            sizes = sizes.split("(", 1)[0]
                        except:
                            pass
                        stock_status = "Stokta yok"
                        try:
                            PsqlQuery.delete_specific_stock(stock_link, sizes)
                        except:
                            print(f"Inserting new data.. {stock_link} -- {sizes}, {stock_status}")
                        try:
                            PsqlQuery.insert_stock_info(stock_status, sizes, item_picture_url, price, link_id)
                        except:
                            print("Same value in database.")
                else:
                    sizes = stock.text.strip()
                    sizes = sizes.split("(", 1)[0]
                    stock_status = "Stokta"
                    try:
                        PsqlQuery.delete_specific_stock(stock_link, sizes)
                    except:
                        print(f"Inserting new data.. {stock_link} -- {sizes}, {stock_status}")
                    try:
                        PsqlQuery.insert_stock_info(stock_status, sizes, item_picture_url, price, link_id)
                    except:
                        print("Same value in database.")
                    send_mail(1, mail, stock_link, sizes, stock_source)
    print(f"The Zara process has been completed.")

def hm_stocks(hm_urls, driver):
    for url in hm_urls:
        stock_link = url[0]
        username = url[1]
        stock_source = url[2]
        mail = url[3]
        link_id = url[4]
        price = 0
        while True:
            try:       
                driver.get(stock_link)
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sizeButton-0")))
                except Exception as e:
                    print("The page could not be loaded.", e)
                    continue

                soup = BeautifulSoup(driver.page_source, "html.parser")
                item_picture_button = soup.find("button", class_ = "ecc322")
                item_picture_div = item_picture_button.find("div", class_ = "def5f0 fcc68c a33b36 f6e252")
                item_picture = item_picture_div.find_all("img")

                if item_picture:
                    item_picture_url = item_picture[0]["src"]
                else:
                    item_picture_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/H%26M-Logo.svg/2560px-H%26M-Logo.svg.png"
                break
            except Exception as e:
                print("Connection problem, trying again..", e)
                time.sleep(5)
        
        which_stock = soup.find_all("div", attrs={"id": re.compile(r"^sizeButton-")}) 
        if which_stock == []:
            target_input = soup.find("input", attrs={"id": re.compile(r"^00-")})
            if target_input:
                which_stock = target_input.find_previous_siblings("label").text.strip()

        for stock in which_stock:    
            inner_stock_status = stock.find("label")
            size_label = inner_stock_status.text.strip()
            if inner_stock_status.has_attr("class"):
                stock_status = "Stokta yok"
                try:
                    PsqlQuery.delete_specific_stock(stock_link, size_label)
                except:
                    print(f"Inserting new data.. {stock_link} -- {size_label}, {stock_status}")
                try:
                    PsqlQuery.insert_stock_info(stock_status, size_label, item_picture_url, price, link_id)
                except:
                    print("Same value in database.")
            else:
                if size_label:
                    stock_status = "Stokta"
                    try:
                        PsqlQuery.delete_specific_stock(stock_link, size_label)
                    except:
                        print(f"Inserting new data.. {stock_link} -- {size_label}, {stock_status}")
                    try:
                        PsqlQuery.insert_stock_info(stock_status, size_label, item_picture_url, price, link_id)
                    except:
                        print("Same value in database.")
    print(f"The HM process has been completed.")


def send_mail(mail_id, mail, stock_link, stock_size, stock_source):
    if mail_id == 1:
        subject = f"{stock_source}, yeni stok geldi."
        body = f"Merhaba. {stock_source}'ya bu url'ye ait {stock_link}, {stock_size} beden/numara ürün gelmiştir."
    if mail_id == 2:
        subject = f"{stock_source}, Stok Tükendi."
        body = f"Merhaba. {stock_source}'da bu url'ye ait {stock_link} stok tamamen tükemiştir."
    try:
        yag.send(to=mail, subject=subject, contents=body)
    except Exception as e:
        print("Could not send mail", e)

if __name__ == "__main__":
    create_app()