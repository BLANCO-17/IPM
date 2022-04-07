#AUTHOR - BLANCO
#WEBSCRAPPER FOR EXTRACTING CRYPTO PRICES FROM COINMARKETCAP

#Refer to the getName() function to see default supported coins, feel free to add coins of your choice.
#Make sure to Update the webdriver path in __INIT_

from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller

# from selenium.webdriver.chrome.service import Service
# from time import sleep

class priceExtractor:
    
    def __init__(self):    

        global _PATH
        
        self.option = webdriver.ChromeOptions()
        self.option.add_argument("disable-gpu")
        self.option.add_argument('--headless')
        self.option.add_argument('--no-sandbox')
        self.option.add_argument('--disable-dev-sh-usage') 
        self.option.add_experimental_option('excludeSwitches', ['enable-logging']) #comment this code if you want the webdriver logs in console

        chromedriver_autoinstaller.install()
        # path=Service(_PATH)
        self.driver = webdriver.Chrome(options=self.option)
        
    def getName(self, abv):
        
        # NAME VALUE pairs based on coinmarketcap item's url
        # Add available crypto names and abbreviations of your choice
        # The value of the abbreviation should be one that is being used in the url of coinmarketcap
        #i,e for btc valid url is https://coinmarketcap.com/currencies/bitcoin/ - so we added bitcoin as value for key btc below
        
        name_dict = {}
        name_dict['btc'] = 'bitcoin'
        name_dict['eth'] = 'ethereum'
        name_dict['ada'] = 'cardano'
        name_dict['xrp'] = 'xrp'
        name_dict['xlm'] = 'stellar'
        name_dict['luna'] = 'terra-luna'
        name_dict['bnb'] = 'binance-coin'
        name_dict['sol'] = 'solana'
        name_dict['dot'] = 'polkadot-new'
        name_dict['avax'] = 'avalanche'
        name_dict['matic'] = 'polygon'
        name_dict['link'] = 'chainlink'
        name_dict['mana'] = 'decentraland'
        name_dict['mina'] = 'mina'
        name_dict['vet'] = 'vechain'
        name_dict['atom'] = 'cosmos'
        name_dict['sand'] = 'the-sandbox'
        name_dict['hbar'] = 'hedera'
        name_dict['gala'] = 'gala'
        name_dict['eos'] = 'eos'
        name_dict['reef'] = 'reef'
        name_dict['ltc'] = 'litecoin'
        name_dict['uni'] = 'uniswap'
        name_dict['algo'] = 'algorand'
        name_dict['trx'] = 'tron'
        name_dict['fil'] = 'filecoin'
        name_dict['gala'] = 'gala'
        name_dict['ckb'] = 'nervos-network'

        return name_dict.get(abv)
            
    def getPrice(self, coinname, cur):

        abv = self.getName(coinname)
        price = 0
        price_change = {'percentage': '0.0',
                        'diff': '0',
                        'indic': '-'}
        repPrice = None

        if(cur == 'usd'):
        
            if(abv != None):
                        
                self.driver.get('https://coinmarketcap.com/currencies/'+abv+'/') # Getting page HTML through request
                self.soup = BeautifulSoup(self.driver.page_source, 'html.parser') # Parsing content using beautifulsoup. Notice driver.page_source instead of page.content
                data = self.soup.find("div", {"class": "priceValue"}) # Selecting priceValue Class object
                
                try:
                    repPrice = (data.string).replace("$", "")
                    price = repPrice.replace(",", "")
                    price = float(price)
                    price_change['percentage'] = data.nextSibling.find_next('span').next_sibling
                    # print()
                    # open_price = float(100-float(price_change['percentage']))*100

                    caret = data.nextSibling.find_next('span').get_attribute_list("class")[0]
                    
                    open_price = (price / (100-float(price_change['percentage']) ))*100
                    
                    price_diff = open_price - price
                    price_change['diff'] = round(price_diff, 3)
                    # print(open_price, price, price_change['percentage'])

                    if 'up' in caret:
                        price_change['indic'] = '+'
                    else:
                        price_change['indic'] = '-'
                
                except Exception as e:
                    print("error[getPrice]-", e)
                
                # print(price)                                
            else:
                print("[ERROR] - Item not yet supported. Take a look at the 'getName' function of this class.")
                return 0

        elif(cur == 'inr'):
            coinname = coinname.upper()            
            
            if(abv != None):
                        
                # print(data.tbody.tr.td.text)
                price_change['diff'] = 0
                price_change['indic'] = '+'
                price_change['percentage'] = 0.0
                price = 0
                repPrice = 0
                
                self.driver.get('https://wazirx.com/exchange/'+coinname+'-INR') # Getting page HTML through request                
                self.soup = BeautifulSoup(self.driver.page_source, 'html.parser') # Parsing content using beautifulsoup. Notice driver.page_source instead of page.content
                data = self.soup.find("table", {"class": "trade-history"}) # Selecting priceValue Class object
                i=0
                while(i < 5):
                    try:
                        # data = data.tbody.tr.td.text
                        repPrice = data.tbody.tr.td.text#(data.string).replace(" INR", "")
                        tick = self.soup.find(id="ticker-"+coinname.lower())            
                        obj = tick.findChildren("div", {"class", "market-change"})
                        # print("ticker-"+coinname)
                        ob = obj[0].findChildren("span")
                        
                        perc = (ob[0].text[1:len(ob[0].text)-1]).replace("%", "")
                        if '-' in perc:
                            price_change['indic'] = '-'
                            perc = perc.replace('-', '')
                        else:
                            price_change['indic'] = '+'
                            
                        price_change['percentage'] = perc.replace(" ", '')                                        
                        # for span in ob:
                        #     print(span.text)
                        try:
                            price = repPrice.replace(",", "")                    
                            price = float(price)
                            open_price = (price / (100-float(price_change['percentage']) ))*100
                            price_change['diff'] = round(open_price-price, 2)
                            
                        except Exception as e: print("Calc Error - ", e)
                        
                        break
                    except Exception as e:
                        print("retrieval error :",e)
                        i+=1
                    
            else:
                print("[ERROR] - Item not yet supported. Take a look at the 'getName' function of this class.")
                price = 0                
                
        if price > 1:
            i = repPrice.index('.')
            repPrice = repPrice[:i+3]
            return [round(price, 2), repPrice], price_change
        else: return price, repPrice
                
    def getFNGIndex():
        pass

    def closeDriver(self):
        #always call this function before closing your main script, responsible for flushing the webdriver.exe
        self.driver.quit()
        print("driver closed.")

class Handler:
    
    def __init__(self):
        self.Queue = []
        pass

    def checkQ(self):
        pass
    
    def enQueue(self):
        pass
    


# if __name__ == "__main__":
# pe = priceExtractor()
# print(pe.getPrice('btc', 'usd'))
# pe.closeDriver()
#     sleep(5)
#     del pe
# print(pe.getPrice('ckb')) 

#USAGE
# pe = priceExtractor()
# print(pe.getPrice('ckb', 'usd')) 

# # # # ------------------
# pe.closeDriver() # -> important to call whenever closing application / script.