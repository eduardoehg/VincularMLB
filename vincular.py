from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def esperar(navegador, elemento):
    WebDriverWait(navegador, 30).until(EC.element_to_be_clickable((By.XPATH, elemento)))
    sleep(1)


class Vinculo:

    def __init__(self, navegador, sku):
        self.navegador = navegador
        self.sku = sku

        self.relacionar()

    def relacionar(self):
        sleep(1)
        esperar(self.navegador, elemento='//*[@id="page-wrapper"]/div[4]/div/div[1]/div/div[2]/button')
        botao_acoes = self.navegador.find_element(By.XPATH, '//*[@id="page-wrapper"]/div[4]/div/div[1]/div/div[2]/button')
        botao_acoes.click()

        sleep(1)
        esperar(self.navegador, elemento='//*[@id="im_12"]/a')
        botao_relacionar_anuncios = self.navegador.find_element(By.XPATH, '//*[@id="im_12"]/a')
        botao_relacionar_anuncios.click()

        sleep(1)
        esperar(self.navegador, elemento='//*[@id="bs-modal"]/div/div/div/div[2]/div[2]/div[1]/div/div/input')
        barra_pesquisa = self.navegador.find_element(By.XPATH, '//*[@id="bs-modal"]/div/div/div/div[2]/div[2]/div[1]/div/div/input')
        barra_pesquisa.send_keys(self.sku)
        barra_pesquisa.send_keys(Keys.ENTER)

        sleep(1)
        esperar(self.navegador, elemento='//*[@id="bs-modal"]/div/div/div/div[2]/div[2]/div[2]/table/tbody/tr/td[4]')
        produto = self.navegador.find_element(By.XPATH, '//*[@id="bs-modal"]/div/div/div/div[2]/div[2]/div[2]/table/tbody/tr/td[4]')
        produto.click()

        sleep(1)
        esperar(self.navegador, elemento='//*[@id="bs-modal"]/div/div/div/div[3]/button[1]')
        botao_continuar = self.navegador.find_element(By.XPATH, '//*[@id="bs-modal"]/div/div/div/div[3]/button[1]')
        botao_continuar.click()

        sleep(1)
        esperar(self.navegador, elemento='//*[@id="bs-modal"]/div/div/div/div[3]/button[2]')
        botao_relacionar = self.navegador.find_element(By.XPATH, '//*[@id="bs-modal"]/div/div/div/div[3]/button[2]')
        botao_relacionar.click()
