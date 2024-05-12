from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from consultar import Consulta
from vincular import Vinculo
from bs4 import BeautifulSoup
from time import sleep


def esperar(navegador, elemento):
    WebDriverWait(navegador, 30).until(EC.element_to_be_clickable((By.XPATH, elemento)))
    sleep(1)


class RasparDados:

    def __init__(self, email, senha, id_ecommerce, token):
        self.email = email
        self.senha = senha
        self.id_ecommerce = id_ecommerce
        self.token = token
        self.navegador = None

        self.iniciar()

    def iniciar(self):
        self.navegador = webdriver.Chrome()
        self.navegador.get('https://accounts.tiny.com.br/realms/tiny/protocol/openid-connect/auth?client_id=tiny-webapp&redirect_uri=https://erp.tiny.com.br/login&scope=openid&response_type=code')

        input_email = self.navegador.find_element(By.XPATH, '//*[@id="kc-content-wrapper"]/react-login/div/div/div[1]/div[1]/div[1]/form/div[1]/div/input')
        input_email.send_keys(self.email)
        input_email.send_keys(Keys.TAB)

        input_senha = self.navegador.find_element(By.XPATH, '//*[@id="kc-content-wrapper"]/react-login/div/div/div[1]/div[1]/div[1]/form/div[2]/div/input')
        input_senha.send_keys(self.senha)

        entrar = self.navegador.find_element(By.XPATH, '//*[@id="kc-content-wrapper"]/react-login/div/div/div[1]/div[1]/div[1]/form/div[3]/button')
        entrar.click()

        esperar(self.navegador, elemento='//*[@id="main-menu"]/div[2]/div[1]/div[1]/div[1]')
        self.navegador.get(f'https://erp.tiny.com.br/anuncios?idEcommerce={self.id_ecommerce}')

        self._pagina_anuncio()

    def _pagina_anuncio(self):
        esperar(self.navegador, elemento='//*[@id="tabelaListagem"]/thead/tr/th[1]/span')
        sleep(5)
        pagina = self.navegador.page_source
        site = BeautifulSoup(pagina, 'html.parser')
        pesquisa = site.find_all('tr', idproduto='0', attrs={'idanuncio': True})
        lista_anuncios = list()
        for item in pesquisa:
            id_anuncio = item['idanuncio']
            print(id_anuncio)
            lista_anuncios.append(id_anuncio)

        if lista_anuncios:
            self._anuncio_individual(lista_anuncios)
        else:
            self._proxima_pagina()

    def _anuncio_individual(self, lista_anuncios):
        for anuncio in lista_anuncios:
            sleep(1.5)
            self.navegador.get(f'https://erp.tiny.com.br/anuncios?idEcommerce={self.id_ecommerce}#edit/{anuncio}')
            esperar(self.navegador, elemento='//*[@id="section-dados-imagens"]')
            sleep(5)
            cadastro_anuncio = self.navegador.page_source
            informacoes_anuncio = BeautifulSoup(cadastro_anuncio, 'html.parser')
            ficha_tecnica = informacoes_anuncio.find('div', class_='atributos-recomendados')

            if ficha_tecnica:
                input_element = ficha_tecnica.find('input', {'value': 'SELLER_SKU'})
                if input_element:
                    siblings = input_element.find_next_siblings()
                    p_tags = [BeautifulSoup(str(sibling), 'html.parser').find('p', class_='form-control-static viewing-input') for sibling in siblings]
                    if p_tags[1]:
                        sku = p_tags[1].get_text(strip=True)
                        print(sku)
                        pesquisa = Consulta(sku, self.token)
                        resultado = pesquisa.pesquisar()
                        if resultado:
                            Vinculo(self.navegador, sku)
                        else:
                            print('nao vou vincular')
        esperar(self.navegador, elemento='//*[@id="page-wrapper"]/div[4]/div/div[1]/ol/li[1]/a')
        sleep(5)
        self.navegador.find_element(By.XPATH, '//*[@id="page-wrapper"]/div[4]/div/div[1]/ol/li[1]/a').click()
        self._proxima_pagina()

    def _proxima_pagina(self):
        esperar(self.navegador, elemento='//*[@id="tabelaListagem"]/thead/tr/th[1]/span')
        pag = self.navegador.page_source
        extra = BeautifulSoup(pag, 'html.parser')
        pagination_ul = extra.find('ul', class_='pagination hidden-xs')
        try:
            pagination_ul.find('li', class_='pnext')
            sleep(1.5)
            botao_avancar = self.navegador.find_elements(By.CLASS_NAME, 'pnext')
            botao_avancar[1].click()
            esperar(self.navegador, elemento='//*[@id="tabelaListagem"]/thead/tr/th[1]/span')
            sleep(2)
            self._pagina_anuncio()
        except AttributeError:
            self.navegador.quit()
