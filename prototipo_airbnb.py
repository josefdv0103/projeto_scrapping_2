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
    pagina.locator('button').locator('div').locator('nth = 0').click()
    pagina.locator('div').locator('input').locator('nth = 1').click()
    pagina.locator('div').locator('input').locator('nth = 1').fill(str(cidade) + ', ' + str(estado))
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
    pagina_2.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div/div/div[1]
    /div[2]/div/div/div/div/div[2]/div/div/button''').click()

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

    time.sleep(7)

    texto_mostrar = pagina_2.get_by_role("link").all_inner_texts()[1]

    if texto_mostrar.find('Mostrar') != -1:
        time.sleep(5)
        pagina_2.locator('a:has-text("Mostrar")').click()
        quant_p_abas = 18
        quant_imoveis = int(texto_mostrar.split()[1])
        abas = (quant_imoveis // quant_p_abas) + 1

        for i in range(abas):
            if i == range(abas)[-1]:
                quant_p_abas = (quant_imoveis % quant_p_abas)
            for j in range(quant_p_abas):

                texto_link = pagina_2.get_by_role('group').get_by_role('link').locator('nth =' + repr(j)).get_attribute('href')
                
                link_anuncio = so_url(texto_link)

                pagina_3 = navegador.new_page(viewport = {'width': 1200, 'height': 800})

                pagina_3.goto(link_anuncio)

                print(armazenagem(link_anuncio, pagina_3, tabela_1, tabela_2, estado))

                pagina_3.close()

    pagina_2.close()
 
def armazenagem(link, pagina_1, tabela_1, frame, estado):

   #LINK
    tabela_1.update({'Link' : link})

    #NOTA
    tabela_1.update({'Avaliacao' : float(pagina_1.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[1]/div[1]/div/div/div/div/section/div[2]/div[1]/span[1]/span[2]''').inner_text().split()[0].replace(',','.'))})

    #CABEÇALHO
    cabecalho = pagina_1.locator('section').locator('nth = 0').inner_text().split()
    print(cabecalho)
    ## COMENTÁRIOS
    tabela_1.update({'Nº_de_comentarios' : int(cabecalho[len(pagina_1.locator('h1').inner_text().split()) + 2])})
    
    
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
    tabela_1.update({'Hospedes' : int(pagina_1.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/ol/li[1]/span[1]''').inner_text().split()[0])})
    
    #QUARTOS
    tabela_1.update({'Quartos' : int(pagina_1.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/ol/li[2]/span[2]''').inner_text().split()[0])})

    #CAMAS
    tabela_1.update({'Camas' : int(pagina_1.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/ol/li[3]/span[2]''').inner_text().split()[0])})

    #BANHEIROS
    tabela_1.update({'Banheiros' : int(pagina_1.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/ol/li[4]/span[2]''').inner_text().split()[0])})

    #TAXA DE LIMPEZA
    if float(pagina_1.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div/section/div[1]/div[2]/span[2]''').inner_text().split()[0].replace(',','.').replace('R$','')) <= 10:
        
        tabela_1.update({'Taxa_limpeza' : float(pagina_1.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div/section/div[1]/div[2]/span[2]''').inner_text().split()[0].replace(',','.').replace('R$',''))*1000})    

    else:
        tabela_1.update({'Taxa_limpeza' : float(pagina_1.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div/section/div[1]/div[2]/span[2]''').inner_text().split()[0].replace(',','.').replace('R$',''))})    
    
    #HOSPEDAGEM
    if float(pagina_1.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div/section/div[1]/div[1]/span[2]''').inner_text().split()[0].replace(',','.').replace('R$','')) <= 10:
        
        tabela_1.update({'Hospedagem' : float(pagina_1.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div/section/div[1]/div[1]/span[2]''').inner_text().split()[0].replace(',','.').replace('R$',''))*1000})    

    else:
        tabela_1.update({'Hospedagem' : float(pagina_1.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div/section/div[1]/div[1]/span[2]''').inner_text().split()[0].replace(',','.').replace('R$',''))})    

    #TAXA DE SERVIÇO
    if float(pagina_1.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div/section/div[1]/div[3]/span[2]''').inner_text().split()[0].replace(',','.').replace('R$','')) <= 10:
        
        tabela_1.update({'Taxa_servico' : float(pagina_1.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div/section/div[1]/div[3]/span[2]''').inner_text().split()[0].replace(',','.').replace('R$',''))*1000})    

    else:
        tabela_1.update({'Taxa_servico' : float(pagina_1.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div/section/div[1]/div[3]/span[2]''').inner_text().split()[0].replace(',','.').replace('R$',''))})    

    #VALOR TOTAL
    if float(pagina_1.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div/section/div[2]/div/span[2]/span[1]''').inner_text().split()[0].replace(',','.').replace('R$','')) <= 10:
        
        tabela_1.update({'Total_sem_impostos' : float(pagina_1.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div/section/div[2]/div/span[2]/span[1]''').inner_text().split()[0].replace(',','.').replace('R$',''))*1000})   
    else:
        tabela_1.update({'Total_sem_impostos' : float(pagina_1.locator('''xpath = /html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div/section/div[2]/div/span[2]/span[1]''').inner_text().split()[0].replace(',','.').replace('R$',''))})   


    frame = pd.concat([frame, pd.DataFrame([tabela_1])], ignore_index=True)

    return frame


tabela_1 = {'Link' : [None], 'Avaliacao' : [None], 'Nº_de_comentarios' : [None], 'Superhost' : [None], 'Localizacao' : [None], 
            'Hospedes' : [None], 'Hospedagem' : [None], 'Quartos' : [None], 'Banheiros' : [None], 'Camas': [None], 'Taxa_limpeza' : [None], 
            'Taxa_servico': [None], 'Total_sem_impostos': [None]}

tabela_2 = pd.DataFrame([tabela_1])

cidade = 'Praia Grande' #str(input('Cidade: '))
estado = 'São Paulo' #str(input('Estado: '))
preco_minimo = 1000 #int(input('Preço mínimo: '))
preco_maximo = 2000 #int(input('Preço máximo: '))
n_quartos = '1' #str(input('Quantos quartos: '))
n_camas = '1' #str(input('Quantas camas: '))
n_banheiros = '1' #str(input('Quantos banheiros: '))




i = 50
dif = (preco_maximo - preco_minimo)/i

with sync_playwright() as p:
    for j in range(i - 1):

        navegador = p.chromium.launch(headless = False)
        pagina_1 = navegador.new_page(viewport = {'width': 1200, 'height': 800})

        url = pagina_pesquisa(cidade, estado, pagina_1)

        pagina_1.close()
        
        pagina_2 = navegador.new_page(viewport = {'width': 1200, 'height': 800})

        preco_maximo = preco_minimo + int(dif)

        pagina_2.get_by_role("link").all_inner_texts()

        filtro(pagina_2, url, n_quartos, n_camas, n_banheiros, preco_minimo, preco_maximo)

        preco_minimo += int(dif)