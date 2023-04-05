from playwright.sync_api import sync_playwright
import pandas as pd
import time
from math import ceil

def so_url(string):
    string =  'https://www.airbnb.com.br' + string

    return string

def pagina_pesquisa(cidade, estado, pagina):
    pagina.goto("https://www.airbnb.com.br/")

    #FAZENDO A PESQUISA 
    ##ONDE
    pagina.locator('button:has-text("Qualquer lugar")').click()
    pagina.locator('div').locator('input').locator('nth = 1').click()
    pagina.locator('div').locator('input').locator('nth = 1').fill(str(cidade) + ', ' + str(estado))
    pagina.keyboard.press("Enter")
    ###DATAS FLEXIVEIS
    pagina.locator('button:has-text("Datas flexíveis")').click()
    ###UM FIM DE SEMANA
    pagina.locator('label:has-text("Um fim de semana")').click()
    ##BOTAO DE BUSCA
    pagina.locator('button:has-text("Buscar")').click()
    return pagina.url

def filtro(pagina_2, url, quartos, camas, banheiros, minimo, maximo, dif, dicionario, frame):

    pagina_2.goto(str(url))

    #FILTRO
    pagina_2.locator('button:has-text("Filtro")').click()

    if len(pagina_2.locator('button:has-text("Casa")').all_inner_texts()):
        ##CASA DE HOSPEDES
        pagina_2.locator('button:has-text("Casa")').locator('nth =' + repr(1)).click()
        pagina_2.locator('button:has-text("Casa")').locator('nth =' + repr(2)).click()
        pagina_2.locator('button:has-text("Apartamento")').click()

    else:
        pagina_2.locator('button:has-text("Casa")').locator('nth =' + repr(0)).click()
        pagina_2.locator('button:has-text("Casa")').locator('nth =' + repr(1)).click()
        pagina_2.locator('button:has-text("Apartamento")').click()

    #QUANT QUARTOS, CAMAS E BANHEIROS
    pagina_2.locator('button:has-text(' + repr(quartos) + ')').locator('nth =' + repr(-3)).click()
    pagina_2.locator('button:has-text(' + repr(camas) + ')').locator('nth =' + repr(-2)).click()
    pagina_2.locator('button:has-text(' + repr(banheiros) + ')').locator('nth =' + repr(-1)).click() 

    #LIMITES DE PREÇO
    pagina_2.locator('input').locator('nth =' + repr(-19)).fill(repr(minimo))
    pagina_2.locator('input').locator('nth =' + repr(-18)).fill(repr(maximo))   

    #BOTAO MOSTRAR
    texto_mostrar = pagina_2.locator('footer').get_by_role("link").inner_text()

    ##CASO APAREÇA MAIS DE MIL RESULTADOS, NO CASO, IRA PEGAR UM INTERVALO MENOR
    while "mil" in texto_mostrar.split():

        maximo = maximo - int(dif)

        pagina_2.locator('input').locator('nth =' + repr(-18)).fill(repr(maximo))

        pagina_2.mouse.click(1500 * 0.6, 1000 * 0.75)

        time.sleep(1)

        texto_mostrar = pagina_2.locator('footer').get_by_role("link").inner_text()

        print(texto_mostrar)

    while int(texto_mostrar.split()[1]) > 270:

        maximo = maximo - int(dif)

        pagina_2.locator('input').locator('nth =' + repr(-18)).fill(repr(maximo))

        pagina_2.mouse.click(1500 * 0.6, 1000 * 0.75)

        time.sleep(1)

        texto_mostrar = pagina_2.locator('footer').get_by_role("link").inner_text()


    #SEPARANDO QUANTAS ABAS EXISTEM BASEADO NOS RESULTADOS
    pagina_2.locator('footer').get_by_role("link").click()
    quant_p_abas = 18
    quant_imoveis = int(texto_mostrar.split()[1])
    abas = (quant_imoveis // quant_p_abas) + 1

        
    for i in range(abas):

        if i == range(abas)[-1]:
            quant_p_abas = (quant_imoveis % quant_p_abas)

        for j in range(1, quant_p_abas):

            texto_link = pagina_2.get_by_role('group').get_by_role('link').locator('nth =' + repr(j)).get_attribute('href')
            
            link_anuncio = so_url(texto_link)

            pagina_3 = navegador.new_page(viewport = {'width': 1500, 'height': 1000})

            pagina_3.goto(link_anuncio)

            #CABEÇALHO
            cabecalho = pagina_3.locator('section').locator('nth = 0').inner_text().split()
            print(cabecalho)

            ## COMENTÁRIOS
            dicionario.update({'Nº_de_comentarios' : int(cabecalho[len(pagina_3.locator('h1').inner_text().split()) + 2])})
            
            armazenagem(link_anuncio, pagina_3, dicionario, frame, estado, cabecalho)

            pagina_3.close()

    pagina_2.close()
 
def armazenagem(link, pagina_1, dicionario, frame, estado, cabecalho):

   #LINK
    tabela_1.update({'Link' : link})

    #NOTA
    tabela_1.update({'Avaliacao' : float(pagina_1.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[1]/div[1]/div/div/div/div/section/div[2]/div[1]/span[1]/span[2]''').inner_text().split()[0].replace(',','.'))})    
    
    if 'Superhost' in cabecalho:
        ##SUPERHOST
        tabela_1.update({'Superhost' : 'Sim'})
        ##CIDADE/BAIRRO
        tabela_1.update({'Localizacao' : ' '.join(cabecalho[(len(pagina_1.locator('h1').inner_text().split()) + 8) : -(3 + len(estado))])})
    else:
        ##SUPERHOST
        tabela_1.update({'Superhost' : 'Nao'})
        ##CIDADE/BAIRRO
        tabela_1.update({'Localizacao' : ' '.join(cabecalho[(len(pagina_1.locator('h1').inner_text().split()) + 5) : -(3 + len(estado))])})

    #HOSPEDES
    tabela_1.update({'Hospedes' : int(pagina_1.locator('li').locator('span:has-text("hóspedes")').inner_text().split()[0])})
    
    #QUARTOS
    tabela_1.update({'Quartos' : int(pagina_1.locator('li').locator('span:has-text("quarto")').inner_text().split()[0])})

    #CAMAS
    tabela_1.update({'Camas' : int(pagina_1.locator('li').locator('span:has-text("cama")').inner_text().split()[0])})

    #BANHEIROS
    tabela_1.update({'Banheiros' : int(pagina_1.locator('li').locator('span:has-text("banheiro")').inner_text().split()[0])})
    
    #VALOR TOTAL
    if float(pagina_1.locator('span:has-text("R$")').locator('nth = 1').inner_text().split()[-1].replace(',','.').replace('R$','')) <= 10:
        
        tabela_1.update({'Total_sem_impostos' : float(pagina_1.locator('span:has-text("R$")').locator('nth = 1').inner_text().split()[-1].replace(',','.').replace('R$',''))*1000})   
    else:
        tabela_1.update({'Total_sem_impostos' : float(pagina_1.locator('span:has-text("R$")').locator('nth = 1').inner_text().split()[-1].replace(',','.').replace('R$',''))})   

    frame = pd.concat([frame, pd.DataFrame([dicionario])], ignore_index = True)

    return frame.to_excel('tabela.xlsx')

tabela_1 = {'Link' : [None], 'Avaliacao' : [None], 'Nº_de_comentarios' : [None], 'Superhost' : [None], 'Localizacao' : [None], 
            'Hospedes' : [None], 'Hospedagem' : [None], 'Quartos' : [None], 'Banheiros' : [None], 'Camas': [None], 'Taxa_limpeza' : [None], 
            'Taxa_servico': [None], 'Total_sem_impostos': [None]}

tabela_2 = pd.DataFrame(tabela_1)

cidade = 'Praia Grande' #str(input('Cidade: '))
estado = 'São Paulo' #str(input('Estado: '))
preco_minimo = 1000 #int(input('Preço mínimo: '))
preco_maximo = 2000 #int(input('Preço máximo: '))
n_quartos = '1' #str(input('Quantos quartos: '))
n_camas = '1' #str(input('Quantas camas: '))
n_banheiros = '1' #str(input('Quantos banheiros: '))


i = 30
dif = (preco_maximo - preco_minimo)/i

with sync_playwright() as p:


    navegador = p.chromium.launch(headless = False)
    pagina_1 = navegador.new_page(viewport = {'width': 1200, 'height': 800})

    url = pagina_pesquisa(cidade, estado, pagina_1)

    pagina_1.close()
    
    pagina_2 = navegador.new_page(viewport = {'width': 1200, 'height': 800})

    filtro(pagina_2, url, n_quartos, n_camas, n_banheiros, preco_minimo, preco_maximo, dif, tabela_1, tabela_2)

