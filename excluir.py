from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep


def excluir_anuncios(nav):
    sleep(1)
    tempo = 5
    wait = WebDriverWait(navegador, tempo)
    elemento = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="page-wrapper"]/div[3]/div[2]/div[1]/div[1]/div/div[1]/button')))

    botao = nav.find_element(By.XPATH, '//*[@id="tabelaListagem"]/thead/tr/th[1]/span')
    botao.click()
    sleep(1)

    botao_mais_acoes = nav.find_element(By.XPATH, '//*[@id="page-wrapper"]/div[3]/div[2]/div[4]/div[1]/div[3]/div[2]/button')
    botao_mais_acoes.click()
    sleep(1)

    botao_excluir = nav.find_element(By.XPATH, '//*[@id="page-wrapper"]/div[3]/div[2]/div[4]/div[1]/div[3]/div[2]/div/ul/li[6]/a')
    botao_excluir.click()
    sleep(1)

    botao_confirmar = nav.find_element(By.XPATH, '//*[@id="bs-modal-ui-popup"]/div/div/div/div[3]/button[1]')
    botao_confirmar.click()


########## ADICIONAR OS DADOS DA CONTA #####################
email = ''
senha = ''
id_ecommerce = ''
############################################################

navegador = webdriver.Chrome()
navegador.get('https://accounts.tiny.com.br/realms/tiny/protocol/openid-connect/auth?client_id=tiny-webapp&redirect_uri=https://erp.tiny.com.br/login&scope=openid&response_type=code')

input_email = navegador.find_element(By.XPATH, '//*[@id="kc-content-wrapper"]/react-login/div/div/div[1]/div[1]/div[1]/form/div[1]/div/input')
input_email.send_keys(email)
input_email.send_keys(Keys.TAB)

input_senha = navegador.find_element(By.XPATH, '//*[@id="kc-content-wrapper"]/react-login/div/div/div[1]/div[1]/div[1]/form/div[2]/div/input')
input_senha.send_keys(senha)

entrar = navegador.find_element(By.XPATH, '//*[@id="kc-content-wrapper"]/react-login/div/div/div[1]/div[1]/div[1]/form/div[3]/button')
entrar.click()

sleep(5)
navegador.get(f'https://erp.tiny.com.br/anuncios?idEcommerce={id_ecommerce}')
sleep(5)

botao_filtros = navegador.find_element(By.XPATH, '//*[@id="page-wrapper"]/div[3]/div[2]/div[1]/div[3]/ul/li[1]/a')
botao_filtros.click()
sleep(1)

situacao = navegador.find_element(By.XPATH, '//*[@id="filtroRelacionados"]')
situacao.send_keys('N')
situacao.send_keys(Keys.ENTER)
sleep(1)

botao_aplicar = navegador.find_element(By.XPATH, '//*[@id="page-wrapper"]/div[3]/div[2]/div[1]/div[3]/ul/li[1]/div/div[5]/button[1]')
botao_aplicar.click()
sleep(1)

while True:

    excluir_anuncios(navegador)


    pag = navegador.page_source
    extra = BeautifulSoup(pag, 'html.parser')
    pagination_ul = extra.find('ul', class_='pagination hidden-xs')

    if pagination_ul:
        next_link = pagination_ul.find('li', class_='pnext')
        if next_link:
            excluir_anuncios(navegador)
            print('rodando')
        else:
            excluir_anuncios(navegador)
            navegador.quit()
            break
