from selenium import webdriver
from time import sleep
import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from selenium.common.exceptions import NoSuchElementException



def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True



driver = webdriver.Chrome()
driver.get("https://www.ozsuper.com/ax_b/b_AAE.php")


df = pd.read_excel("ISIN_ticker.xlsx")
nu_rows = len(df.index)
print("There are ", nu_rows, " rows. ")


df_ISIN = pd.DataFrame(columns = ['ISIN'])




for current_row in range(0, nu_rows): 

    keys_to_enter = df.iloc[current_row]['ticker']
    print("Checking out ", keys_to_enter)
    driver.find_element_by_xpath("""//*[@id="asx_ticker"]""").send_keys(keys_to_enter)
    driver.find_element_by_xpath("""/html/body/table/tbody/tr[6]/td[1]/table/tbody/tr[2]/td/form/input[2]""").click()

    if (check_exists_by_xpath("""/html/body/table/tbody/tr[9]/td/table/tbody/tr[7]/td[2]""")): 
        print("Page for ", keys_to_enter, " exits......................")
        ISIN_code = driver.find_element_by_xpath("""/html/body/table/tbody/tr[9]/td/table/tbody/tr[7]/td[2]""").text
        if (ISIN_code.strip() == ""): 
            print("No ISIN found.........................")
            ISIN_code = "not exist"

    else: 
        print("Page for ", keys_to_enter, " does not exist..........................")
        ISIN_code = "not exist"
        driver.get("https://www.ozsuper.com/ax_b/b_AAE.php")

    df_ISIN = df_ISIN.append({'ISIN': ISIN_code}, ignore_index=True)



print(df_ISIN)
df_ISIN.to_csv('ISIN_final.csv', index = False)
