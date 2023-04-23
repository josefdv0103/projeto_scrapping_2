from playwright.sync_api import sync_playwright
import pandas as pd
import time
from math import ceil

def so_url(string):
    string =  'https://www.airbnb.com.br' + string

    return string

def pagina_pesquisa(cidade, estado, pagina, escolha_tempo):
    pagina.goto("https://www.airbnb.com.br/")

    #FAZENDO A PESQUISA 
    ##ONDE
    pagina.locator('button:has-text("Qualquer lugar")').click()
    pagina.locator('div').locator('input').locator('nth = 1').click()
    pagina.locator('div').locator('input').locator('nth = 1').fill(str(cidade) + ', ' + str(estado))
    pagina.keyboard.press("Enter")

    ###DATAS FLEXIVEIS
    pagina.locator('button:has-text("Datas flexíveis")').click()

    if escolha_tempo[0] == 0:
        ###UM FIM DE SEMANA
        pagina.locator('label:has-text("Um fim de semana")').click()
    if escolha_tempo[0] == 1:
        ###UMA SEMANA
        pagina.locator('label:has-text("Uma semana")').click()
    if escolha_tempo[0] == 2:
        ###UM MÊS
        pagina.locator('label:has-text("Um mês")').click()

    if escolha_tempo[1] == True:
        pagina.locator('button:has-text('+ repr(escolha_tempo[2]) + ')').click()


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
    pagina_2.locator('section').get_by_label("preço mínimoR$").dblclick()
    pagina_2.locator('section').get_by_label("preço mínimoR$").fill(repr(minimo))
    pagina_2.locator('section').get_by_label("preço máximoR$").dblclick()
    pagina_2.locator('section').get_by_label("preço máximoR$").fill(repr(maximo))
    #BOTAO MOSTRAR
    texto_mostrar = pagina_2.locator('footer').get_by_role("link").inner_text()
    print(texto_mostrar)
    ##CASO APAREÇA MAIS DE MIL RESULTADOS, NO CASO, IRA PEGAR UM INTERVALO MENOR
    while "1.000+" in texto_mostrar.split():

        maximo = maximo - int(dif)

        pagina_2.locator('section').get_by_label("preço máximoR$").fill(repr(maximo))

        pagina_2.mouse.click(1500 * 0.6, 1000 * 0.75)

        time.sleep(1)

        texto_mostrar = pagina_2.locator('footer').get_by_role("link").inner_text()

    while int(texto_mostrar.split()[1]) > 270:

        maximo = maximo - int(dif)

        pagina_2.locator('section').get_by_label("preço máximoR$").fill(repr(maximo))

        pagina_2.mouse.click(1500 * 0.6, 1000 * 0.75)

        time.sleep(1)

        texto_mostrar = pagina_2.locator('footer').get_by_role("link").inner_text()

    print(texto_mostrar.split()[1])

    return texto_mostrar

def armazenagem(link, pagina_1, dicionario, tabela_2, cabecalho_1, cabecalho_2):

   #LINK
    dicionario.update({'link' : link})

    #NOTA

    numero = (pagina_1.locator('section').locator('nth = 1').inner_text().strip().find('1,')) + (pagina_1.locator('section').locator('nth = 1').inner_text().strip().find('2,')) + (pagina_1.locator('section').locator('nth = 1').inner_text().strip().find('3,')) + (pagina_1.locator('section').locator('nth = 1').inner_text().strip().find('4,')) + (pagina_1.locator('section').locator('nth = 1').inner_text().strip().find('5,'))
    if numero != -5 and pagina_1.locator('span').locator('h1').inner_text().find('1,') + pagina_1.locator('span').locator('h1').inner_text().find('2,') + pagina_1.locator('span').locator('h1').inner_text().find('3,') + pagina_1.locator('span').locator('h1').inner_text().find('4,') + pagina_1.locator('span').locator('h1').inner_text().find('5,') == -1: 
        dicionario.update({'avaliacao' : float(pagina_1.locator('section').locator('nth = 1').inner_text()[numero + 3: numero + 8].replace(',','.'))})    
    else:
        dicionario.update({'avaliacao' :[None]})

    if 'Superhost' in (cabecalho_1 or cabecalho_2):
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
    if 'Mais' in pagina_1.locator('li').locator('span:has-text("hóspede")').inner_text().split():
        dicionario.update({'hospedes' : int(pagina_1.locator('li').locator('span:has-text("hóspede")').inner_text().split()[2])})
        
    else:    
        dicionario.update({'hospedes' : int(pagina_1.locator('li').locator('span:has-text("hóspede")').inner_text().split()[0])})
    
    #QUARTOS
    if pagina_1.locator('li').locator('nth = 1').inner_text().find('quarto') != -1:
        dicionario.update({'quartos' : int(pagina_1.locator('li').locator('span:has-text("quarto")').inner_text().split()[0])})
    else:
        dicionario.update({'quartos' : 0})

    #BANHEIROS
    dicionario.update({'banheiros' : int(pagina_1.locator('li').locator('span:has-text("banheiro")').inner_text().split()[0])})
    
    #CAMAS
    dicionario.update({'camas' : int(pagina_1.locator('li').locator('span:has-text("cama")').inner_text().split()[0])})

    #QUANT NOITES
    if pagina_1.locator('section').locator('span').locator('div').locator('button').locator("nth = 0").inner_text().find("R$") != -1:
        dicionario.update({'quant_noites' : int(pagina_1.locator('section').locator('span').locator('div').locator('button:has-text("R$")').inner_text().split()[2])})

    else:
        dicionario.update({'reserva_p_noite' : [None]})

    #RESERVAS POR NOITE
    if pagina_1.locator('section').locator('span').locator('div').locator('button').locator("nth = 0").inner_text().find("R$") != -1:
        dicionario.update({'reserva_p_noite' : int(pagina_1.locator('section').locator('span').locator('div').locator('button:has-text("R$")').inner_text().split()[0].replace('.','').replace('R$',''))})

    else:
        dicionario.update({'reserva_p_noite' : [None]})

    #VALOR TOTAL
    if float(pagina_1.locator('section').locator('div').locator('div').locator('span').locator('span:has-text("R$")').locator('nth  = 1').inner_text().split()[-1].replace(',','.').replace('R$','')) <= 10:
        
        dicionario.update({'total_sem_impostos' : float(pagina_1.locator('section').locator('div').locator('div').locator('span').locator('span:has-text("R$")').locator('nth  = 1').inner_text().split()[-1].replace(',','.').replace('R$',''))*1000})   
    else:
        dicionario.update({'total_sem_impostos' : float(pagina_1.locator('section').locator('div').locator('div').locator('span').locator('span:has-text("R$")').locator('nth  = 1').inner_text().split()[-1].replace(',','.').replace('R$',''))})   

    tabela_2 = pd.concat([tabela_2, pd.DataFrame([dicionario])], ignore_index = True)

    return tabela_2

#TABELAS QUE SERAO ARMAZENADAS OS DADOS
tabela_1 = {'link' : [None], 'avaliacao' : [None], 'nº_de_comentarios' : [None], 'superhost' : [None], 'localizacao' : [None], 
            'hospedes' : [None],  'quartos' : [None], 'banheiros' : [None], 'camas': [None], 'reserva_p_noite' : [None], 'quant_noites' : [None], 'total_sem_impostos': [None]}

tabela_2 = pd.DataFrame(tabela_1)

#AREA DE INPUT DE FILTROS--------------------------------------------------------------------------------------------------------------
cidade = str(input('Cidade: '))
estado = str(input('Estado: '))

escolha_tempo = [int(input('Escolha o tempo que estadia em média: \nUm fim de semana(0) | Uma semana(1) | Um mês(2) '))]
if input('Deseja especificar o mes de estadia: s/n? ') == 's' and 'S':
    escolha_tempo.append(True)
    escolha_tempo.append(str(input('Mês(em minusculo): ')))
else:
    escolha_tempo.append(False)
    escolha_tempo.append(False)

preco_minimo = int(input('Preço mínimo: '))
preco_maximo = int(input('Preço máximo: '))

if input('Deseja especificar numero de quartos/camas/banheiros?: s/n ') == ('s' or 'S'):
    n_quartos = str(input('Quantos quartos: '))
    n_camas = str(input('Quantas camas: '))
    n_banheiros = str(input('Quantos banheiros: '))
else:
    n_quartos = 'Qualquer'
    n_camas = 'Qualquer'
    n_banheiros = 'Qualquer'

##---------------------------------------------------------------------------------------------------------------

i = 20
dif = (preco_maximo - preco_minimo)/i

with sync_playwright() as p:


    navegador = p.chromium.launch(headless = False)
    pagina_1 = navegador.new_page(viewport = {'width': 1200, 'height': 800})

    url = pagina_pesquisa(cidade, estado, pagina_1, escolha_tempo)

    pagina_1.close()
    
    pagina_2 = navegador.new_page(viewport = {'width': 1200, 'height': 800})
    
    texto_mostrar = filtro(pagina_2, url, n_quartos, n_camas, n_banheiros, preco_minimo, preco_maximo, dif)

    #SEPARANDO QUANTAS ABAS EXISTEM BASEADO NOS RESULTADOS
    pagina_2.locator('footer').get_by_role("link").click()
    quant_p_abas = 18
    quant_imoveis = int(texto_mostrar.split()[1])
    abas = (quant_imoveis // quant_p_abas) + 1
    print(abas)

    for i in range(abas):

        if i == range(abas)[-1]:
            quant_p_abas = (quant_imoveis % quant_p_abas)

        for j in range(0, 19):
            
            if i == 0:
                j = 1

            texto_link = pagina_2.get_by_role('group').get_by_role('link').locator('nth =' + repr(j)).get_attribute('href')
            
            link_anuncio = so_url(texto_link)

            print(link_anuncio)

            pagina_3 = navegador.new_page(viewport = {'width': 1500, 'height': 1000})

            pagina_3.goto(link_anuncio)

            if pagina_3.locator('main:has-text("Denunciar este anúncio")').inner_text().count("Saiba mais") != 2:

                #CABEÇALHO
                cabecalho_1 = pagina_3.locator('section').locator('nth = 0').inner_text().split()
                cabecalho_2 = pagina_3.locator('section').locator('nth = 1').inner_text().split()


                ## COMENTÁRIOS
                if 'comentários' in (cabecalho_1 or cabecalho_2):
                    tabela_1.update({'nº_de_comentarios' : int(pagina_3.locator('button').locator('span:has-text("comentários")').locator("nth = 1").inner_text().split()[0])})
                else:
                    tabela_1.update({'nº_de_comentarios' : [None]})
                
                tabela_2 = armazenagem(link_anuncio, pagina_3, tabela_1, tabela_2, cabecalho_1, cabecalho_2)

                tabela_2.to_excel('tabela.xlsx')

            pagina_3.close()

            if j == range(1, quant_p_abas)[-1] and i != range(abas)[-1]:
                pagina_2.goto(so_url(pagina_2.get_by_role('navigation').get_by_role('link', name = 'Próximo').get_attribute('href')))
            
            if j == range(1, quant_p_abas)[-1] and i == range(abas)[-1]:
                break

    pagina_2.close()
