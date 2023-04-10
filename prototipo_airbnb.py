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

def filtro(pagina_2, url, quartos, camas, banheiros, minimo, maximo, dif):

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
    pagina_2.locator('section').locator('label').locator('div').locator('div').locator('input').locator('nth = 0').fill(repr(minimo))
    pagina_2.locator('section').locator('label').locator('div').locator('div').locator('input').locator('nth = 1').fill(repr(maximo))   

    #BOTAO MOSTRAR
    texto_mostrar = pagina_2.locator('footer').get_by_role("link").inner_text()

    ##CASO APAREÇA MAIS DE MIL RESULTADOS, NO CASO, IRA PEGAR UM INTERVALO MENOR
    while "mil" in texto_mostrar.split():

        maximo = maximo - int(dif)

        pagina_2.locator('section').locator('label').locator('div').locator('div').locator('input').locator('nth = 1').fill(repr(maximo))

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

    return texto_mostrar

def armazenagem(link, pagina_1, dicionario, tabela_2, cabecalho):

   #LINK
    dicionario.update({'link' : link})

    #NOTA
    
    if 'estrelas' in pagina_1.locator('h2').locator('span').locator('nth = 1').inner_text().split():
        dicionario.update({'avaliacao' : float(pagina_1.locator('h2').locator('span').locator('nth = 1').inner_text().split()[0].replace(',','.'))})    
    else:
        dicionario.update({'avaliacao' :[None]})

    if 'Superhost' in cabecalho:
        ##SUPERHOST
        dicionario.update({'superhost' : 'Sim'})
        ##CIDADE/BAIRRO
        dicionario.update({'localizacao' : pagina_1.locator('div').locator('span').locator('button').locator('span:has-text("Brasil")').inner_text()})
    else:
        ##SUPERHOST
        dicionario.update({'superhost' : 'Nao'})
        ##CIDADE/BAIRRO
        dicionario.update({'localizacao' : pagina_1.locator('div').locator('span').locator('button').locator('span:has-text("Brasil")').inner_text()})

    #HOSPEDES
    if 'Mais' in pagina_1.locator('li').locator('span:has-text("hóspedes")').inner_text().split():
        dicionario.update({'hospedes' : int(pagina_1.locator('li').locator('span:has-text("hóspedes")').inner_text().split()[2])})
        
    else:    
        dicionario.update({'hospedes' : int(pagina_1.locator('li').locator('span:has-text("hóspedes")').inner_text().split()[0])})
    
    #QUARTOS
    dicionario.update({'quartos' : int(pagina_1.locator('li').locator('span:has-text("quarto")').inner_text().split()[0])})
    
    #BANHEIROS
    dicionario.update({'banheiros' : int(pagina_1.locator('li').locator('span:has-text("banheiro")').inner_text().split()[0])})
    
    #CAMAS
    dicionario.update({'camas' : int(pagina_1.locator('li').locator('span:has-text("cama")').inner_text().split()[0])})

    #QUANT NOITES
    dicionario.update({'quant_noites' : int(pagina_1.locator('section').locator('span').locator('div').locator('button').locator('div:has-text("noite")').inner_text().split()[-2])})

    #RESERVAS POR NOITE
    #if float(pagina_1.locator('section').locator('span').locator('div').locator('button').locator('div:has-text("noite")').inner_text().split()[0].replace(',','.').replace('R$','')) < 10:
    dicionario.update({'reserva_p_noite' : int(pagina_1.locator('section').locator('span').locator('div').locator('button').locator('div:has-text("noite")').inner_text().split()[0].replace('.','').replace('R$',''))})
    #else:   
    #    dicionario.update({'reserva_p_noite' : int(pagina_1.locator('section').locator('span').locator('div').locator('button').locator('div:has-text("noite")').inner_text().split()[0].replace(',','.').replace('R$',''))})

    #VALOR TOTAL
    if float(pagina_1.locator('section').locator('div').locator('div').locator('span').locator('span:has-text("R$")').locator('nth  = 1').inner_text().split()[-1].replace(',','.').replace('R$','')) <= 10:
        
        dicionario.update({'total_sem_impostos' : float(pagina_1.locator('section').locator('div').locator('div').locator('span').locator('span:has-text("R$")').locator('nth  = 1').inner_text().split()[-1].replace(',','.').replace('R$',''))*1000})   
    else:
        dicionario.update({'total_sem_impostos' : float(pagina_1.locator('section').locator('div').locator('div').locator('span').locator('span:has-text("R$")').locator('nth  = 1').inner_text().split()[-1].replace(',','.').replace('R$',''))})   

    tabela_2 = pd.concat([tabela_2, pd.DataFrame([dicionario])], ignore_index = True)

    return tabela_2

tabela_1 = {'link' : [None], 'avaliacao' : [None], 'nº_de_comentarios' : [None], 'superhost' : [None], 'localizacao' : [None], 
            'hospedes' : [None],  'quartos' : [None], 'banheiros' : [None], 'camas': [None], 'reserva_p_noite' : [None], 'quant_noites' : [None], 
            'taxa_limpeza' : [None], 'taxa_servico': [None], 'total_sem_impostos': [None]}

tabela_2 = pd.DataFrame(tabela_1)

cidade = 'Praia Grande' #str(input('Cidade: '))
estado = 'São Paulo' #str(input('Estado: '))
preco_minimo = 1000 #int(input('Preço mínimo: '))
preco_maximo = 1500 #int(input('Preço máximo: '))
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
    
    texto_mostrar = filtro(pagina_2, url, n_quartos, n_camas, n_banheiros, preco_minimo, preco_maximo, dif)

    #SEPARANDO QUANTAS ABAS EXISTEM BASEADO NOS RESULTADOS
    pagina_2.locator('footer').get_by_role("link").click()
    quant_p_abas = 18
    quant_imoveis = int(texto_mostrar.split()[1])
    abas = (quant_imoveis // quant_p_abas) + 1
    print(abas)
    print(quant_p_abas)

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

            ## COMENTÁRIOS
            if 'comentários' in cabecalho:
                tabela_1.update({'nº_de_comentarios' : int(pagina_3.locator('button').locator('span:has-text("comentários")').locator("nth = 1").inner_text().split()[0])})
            else:
                tabela_1.update({'nº_de_comentarios' : [None]})
            
            tabela_2 = armazenagem(link_anuncio, pagina_3, tabela_1, tabela_2, cabecalho)

            tabela_2.to_excel('tabela.xlsx')

            pagina_3.close()

            if j == range(1, quant_p_abas)[-1]:
                pagina_2.goto(so_url(pagina_2.get_by_role('navigation').get_by_role('link', name = 'Próximo').get_attribute('href')))

            

    pagina_2.close()
