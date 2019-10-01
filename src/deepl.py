import requests
from bs4 import BeautifulSoup as soup
from selenium import webdriver
import time


class DeepL:
    def __init__(self):
        self.settings = {'req_url':  'https://www.deepl.com/translator',
                         'direction': '#de/en/'}

    def translate(self, input_text):
        # browser settings
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        # start browser
        driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)
        # navigate to deepl.com
        driver.get(self.settings['req_url'] + self.settings['direction'] + input_text)

        # wait until translation is done
        translation = []
        start_time = time.time()
        while translation == []:
            time.sleep(0.2)
            # get source
            page_source = driver.page_source
            # parse source using bs4
            suppe = soup(page_source, 'lxml')
            # extract translation
            translations = suppe.find_all("button", class_="lmt__translations_as_text__text_btn")
            translation = translations[0].contents
            print("Wating for deepl.com to finish translation...")
        end_time = time.time()
        print("It took deepl.com {} seconds to process.".format(end_time - start_time))

        # retrun it
        return translation[0]

### DEBUG CALL
if __name__ == "__main__":
    translator = DeepL()
    result = translator.translate("Man muss sich immer wieder vergegenwärtigen, wieviele Anwendungen Machine Learning in welch kurzer Zeit substanziell verbessert oder komplett neu ermöglicht hat, denn beim Einsatz der Technik üben sich viele Unternehmen in Understatement. Siri erkennt gesprochene Sprache und Facebook erkennt Gesichter, ohne dass Apple und Co. groß auf die dahinterliegende Technik hinweisen würden.")
    print(result)