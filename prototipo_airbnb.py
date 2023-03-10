from playwright.sync_api import sync_playwright
import pandas as pd
import numpy as np
import time


def pagina_pesquisa(cidade, estado, pagina):
    pagina.goto("https://www.airbnb.com.br/")

    #FAZENDO A PESQUISA 
    ##ONDE
    pagina.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/
    header/div/div[2]/div[1]/div/button[1]''').click()
    pagina.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/
    header/div/div[2]/div[2]/div/div/div/form/div[2]/div/div[1]/div/label/div/input''').click()
    pagina.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/
    header/div/div[2]/div[2]/div/div/div/form/div[2]/div/div[1]/div/label/div/input''').fill(str(cidade) + ', ' + str(estado))
    ##QUANDO
    pagina.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/
    header/div/div[2]/div[2]/div/div/div/form/div[2]/div/div[1]/div/div[2]/div''').locator('nth = 0').click()
    ###DATAS FLEXIVEIS
    pagina.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/
    header/div/div[2]/div[2]/div/div/div/form/div[2]/div/div[3]/div[2]/div/div/section/div/div/div/div/div[1]/div/div[1]/div/button[2]''').click()
    ###UM FIM DE SEMANA
    pagina.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/
    header/div/div[2]/div[2]/div/div/div/form/div[2]/div/div[3]/div[2]/div/div/section/div/div/div/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/label''').click()
    ##BOTAO DE BUSCA
    pagina.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/
    header/div/div[2]/div[2]/div/div/div/form/div[2]/div/div[5]/div[1]/div[2]/button''').click()

    #url = pagina.url 

    return pagina.url 

def filtro(pagina, url):

    pagina.goto(str(url))

    #FILTRO
    pagina.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div/div/div[1]/div[2]/div/div/div/div/div[2]/div/div/button''').click()

    ##CASA DE HOSPEDES
    print(pagina.get_by_role("group").get_by_role("button").get_attribute("class"))

    #pagina.locator('''xpath = /html/body/div[15]/section/div/div/div[2]/div/div[2]/div/div/main/div[4]/div/div/div/div/section
    #/div[2]/div/div/div/div/div[2]/div[1]/button''').click()
    #pagina.locator('''xpath = /html/body/div[15]/section/div/div/div[2]/div/div[2]/div/div/main/div[4]/div/div/div/div/
    #section/div[2]/div/div/div/div/div[2]/div[2]/button/div/div''').click()
    #pagina.locator('''xpath = /html/body/div[15]/section/div/div/div[2]/div/div[2]/div/div/main/div[4]/div/div/div/div/
    #section/div[2]/div/div/div/div/div[2]/div[3]/button/div/div''').click()




with sync_playwright() as p:
    
    navegador = p.chromium.launch(headless = False)
    pagina_1 = navegador.new_page(viewport = {'width': 1200, 'height': 800})

    url = pagina_pesquisa('Praia Grande', 'SP', pagina_1)
    pagina_1.close()

    pagina_2 = navegador.new_page(viewport = {'width': 1200, 'height': 800})

    filtro(pagina_2, url)

    time.sleep(30)
