from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from consultar import consulta
from vincular import vinculo
from bs4 import BeautifulSoup
from time import sleep


def pagina_anuncio(navegador, id_ecommerce, token):
    sleep(5)
    pagina = navegador.page_source
    site = BeautifulSoup(pagina, 'html.parser')
    pesquisa = site.find_all('tr', idproduto='0', attrs={'idanuncio': True})
    lista_anuncios = list()
    for item in pesquisa:
        id_anuncio = item['idanuncio']
        print(id_anuncio)
        lista_anuncios.append(id_anuncio)

    for anuncio in lista_anuncios:
        sleep(5)
        navegador.get(f'https://erp.tiny.com.br/anuncios?idEcommerce={id_ecommerce}#edit/{anuncio}')
        sleep(5)
        pagina_anuncio = navegador.page_source
        informacoes_anuncio = BeautifulSoup(pagina_anuncio, 'html.parser')
        ficha_tecnica = informacoes_anuncio.find('div', class_='atributos-recomendados')

        if ficha_tecnica:
            input_element = ficha_tecnica.find('input', {'value': 'SELLER_SKU'})

            if input_element:
                siblings = input_element.find_next_siblings()
                p_tags = [BeautifulSoup(str(sibling), 'html.parser').find('p', class_='form-control-static viewing-input') for sibling in siblings]

                if p_tags[1]: # try
                    sku = p_tags[1].get_text(strip=True)
                    print(sku)
                    resultado = consulta(sku, token)
                    if resultado:
                        vinculo(navegador, sku)
                    else:
                        print('nao vou vincular')
    sleep(5)
    navegador.find_element(By.XPATH, '//*[@id="page-wrapper"]/div[4]/div/div[1]/ol/li[1]/a').click()


def raspar_dados(email, senha, id_ecommerce, token):
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

    pagina_anuncio(navegador, id_ecommerce, token)

    while True:
        sleep(5)
        pag = navegador.page_source
        extra = BeautifulSoup(pag, 'html.parser')
        pagination_ul = extra.find('ul', class_='pagination hidden-xs')

        if pagination_ul:
            next_link = pagination_ul.find('li', class_='pnext')
            if next_link:
                sleep(1.5)
                botao_avancar = navegador.find_elements(By.CLASS_NAME, 'pnext')
                botao_avancar[1].click()
                pagina_anuncio(navegador, id_ecommerce, token)
            else:
                navegador.quit()
                break
