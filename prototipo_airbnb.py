from playwright.sync_api import sync_playwright
import pandas as pd
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

    return pagina.url

def filtro(pagina_2, url, quartos, camas, banheiros, minimo, maximo):

    pagina_2.goto(str(url))

    #FILTRO
    pagina_2.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div/div/div[1]/div[2]/div/div/div/div/div[2]/div/div/button''').click()

    if len(pagina_2.locator('button:has-text("Casa")').all_inner_texts()):
        ##CASA DE HOSPEDES
        pagina_2.locator('button:has-text("Casa")').locator('nth =' + repr(1)).click()
        pagina_2.locator('button:has-text("Casa")').locator('nth =' + repr(2)).click()
        pagina_2.locator('button:has-text("Apartamento")').click()

    else:
        pagina_2.locator('button:has-text("Casa")').locator('nth =' + repr(0)).click()
        pagina_2.locator('button:has-text("Casa")').locator('nth =' + repr(1)).click()
        pagina_2.locator('button:has-text("Apartamento")').click()


    pagina_2.locator('button:has-text(' + repr(quartos) + ')').locator('nth =' + repr(-3)).click()
    pagina_2.locator('button:has-text(' + repr(camas) + ')').locator('nth =' + repr(-2)).click()
    pagina_2.locator('button:has-text(' + repr(banheiros) + ')').locator('nth =' + repr(-1)).click() 

    
    pagina_2.locator('input').locator('nth =' + repr(-19)).fill(repr(minimo))
    pagina_2.locator('input').locator('nth =' + repr(-18)).fill(repr(maximo))

    time.sleep(5)

    texto_mostrar = pagina_2.get_by_role("link").all_inner_texts()[1]

    if texto_mostrar.find('Mostrar') != -1:
        pagina_2.locator('a:has-text("Mostrar")').click()

        pagina_2.locator('article').get_attribute()

    pagina_2.close()


def clicar_anuncios(texto, pagina_2):

    pagina_2.get_by_role("link").all_inner_texts()

preco_minimo = 1000 #int(input('Preço mínimo: '))
preco_maximo = 2000 #int(input('Preço máximo: '))
n_quartos = '1' #str(input('Quantos quartos: '))
n_camas = '1' #str(input('Quantas camas: '))
n_banheiros = '1' #str(input('Quantos banheiros: '))

i = 10
dif = (preco_maximo - preco_minimo)/i

with sync_playwright() as p:
    for j in range(9):

        navegador = p.chromium.launch(headless = False)
        pagina_1 = navegador.new_page(viewport = {'width': 1200, 'height': 800})

        url = pagina_pesquisa('Praia Grande', 'SP', pagina_1)

        pagina_1.close()

        pagina_2 = navegador.new_page(viewport = {'width': 1200, 'height': 800})
        
        preco_minimo += int(dif)

        filtro(pagina_2, url, n_quartos, n_camas, n_banheiros, preco_minimo, preco_maximo)

        clicar_anuncios(texto, pagina_2)



    time.sleep(30)
