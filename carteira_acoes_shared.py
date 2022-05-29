# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time
import telebot

# configs do Telelgram (TeleBot)
tg_id = [1,2,3] # ids Telegram de quem irá receber a mensagem no final (obter ids no bot https://t.me/RawDataBot)
CHAVE_API="CHAVE_API_DO_BOT_AQUI" # Criar um bot no Telegram através do Bot Father e preencha aqui a chave a chave. Ex: 5642342523:bATgMpYf-YGBD_8DEj4dXboZmvWkAY_A0jM
bot = telebot.TeleBot(CHAVE_API)

# Preencha a lista com as ações que deseja acompanhar / *** NÃO É RECOMENDAÇÃO DE COMPRA ***
fii = ['MXRF11','HCTR11','IRDM11','PETR4','MGLU3']

# Caminhos que o navegador deverá seguir, site e XPATH, necessário modificar caso haja alguma manutenção na página
xp_valor = '/html/body/div[2]/div[6]/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[3]/span[1]/span[1]'
url_base = 'https://br.tradingview.com/chart/?symbol='

# função que aguarda o elemento ser carregado
def esperar_title(driver):
    ele = driver.title
    return bool(ele)

# inserir argumentos para o navegador
options = webdriver.ChromeOptions()
options.add_argument('headless') # navegador invisível, comente essa linha para ver o site

# iniciar o navegador baixando e atualizando o webdriver de acordo com sua versão do Chrome instalada
d = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)

ret = ''
for f in fii:
    f.upper()
    d.get(url_base + f)

    wdw = WebDriverWait(d,30,poll_frequency=1) # aguardar o elemento por 30 segundos, verificando com frequencia de 1 segundo
    wdw.until(esperar_title)

    if wdw:
        time.sleep(5) # time fixo pois o site carrega com o código da ação, após alguns segundos ele atualiza para a mensagem que queremos
        c = str(d.title)
        c = c.replace('.',',')
        c = c.replace(f + ' ','')
        ret += f'[{f}]\n{c}\n\n'
    else:
        ret += f'[{f}]\nERRO!\n\n'
    
    print(f'[{f}] - OK!')

ret = 'Atualização dos valores das ações\n\n' + ret
ret += '-------------------\n'
ret += 'Fonte: br.tradingview.com\n'
ret += 'Desenvolvido por @walisilva2' # Favor não retirar os créditos.
print(ret)
print('-------------------')

for t in tg_id:
    bot.send_message(t, ret)
    print('Enviado para: ' + str(t))

print('Finalizado.')
d.quit()
