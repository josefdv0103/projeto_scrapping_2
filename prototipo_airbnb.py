from playwright.sync_api import sync_playwright
import pandas as pd
import numpy as np

def pagina_min_fazenda(cidade, estado, pagina):
    pagina.goto("https://www.airbnb.com.br/")


    #FAZENDO A PESQUISA 
    pagina.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/
    header/div/div[2]/div[1]/div/button[1]''').click()
    pagina.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/
    header/div/div[2]/div[2]/div/div/div/form/div[2]/div/div[1]/div/label/div/input''').fill(cidade + ', ' + estado)
    if cidade in pagina.locator('''/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/header/div/div[2]/div[2]/div/div/div/form/div[2]/div/div[1]/div/div[2]/div''').inner_text():
        pagina.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/header/div/div[2]/div[2]/div/div/div/form/div[2]/div/div[1]/div/div[2]/div''').locator('nth = 0').click()
        pagina.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/header/div/div[2]/div[2]/div/div/div/form/div[2]/div/div[3]/div[2]/div/div/section/div/div/div/div/div[1]/div/div[1]/div/button[2]''').click()
        pagina.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/header/div/div[2]/div[2]/div/div/div/form/div[2]/div/div[3]/div[2]/div/div/section/div/div/div/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/label''').click()
        pagina.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div/header/div/div[2]/div[2]/div/div/div/form/div[2]/div/div[5]/div[1]/div[2]/button/div/div[1]/svg''').click()


    return 
with sync_playwright() as p:
    
    navegador = p.chromium.launch(headless = False)
    pagina = navegador.new_page(viewport = {'width': 1200, 'height': 800})
