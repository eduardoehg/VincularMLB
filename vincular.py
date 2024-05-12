from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Vinculo:

    def __init__(self, navegador, sku):
        self.navegador = navegador
        self.sku = sku

        self.relacionar()

    def relacionar(self):
        sleep(1)
        botao_acoes = self.navegador.find_element(By.XPATH, '//*[@id="page-wrapper"]/div[4]/div/div[1]/div/div[2]/button')
        botao_acoes.click()

        sleep(1)
        botao_relacionar_anuncios = self.navegador.find_element(By.XPATH, '//*[@id="im_12"]/a')
        botao_relacionar_anuncios.click()

        sleep(1)
        barra_pesquisa = self.navegador.find_element(By.XPATH, '//*[@id="bs-modal"]/div/div/div/div[2]/div[2]/div[1]/div/div/input')
        barra_pesquisa.send_keys(self.sku)
        barra_pesquisa.send_keys(Keys.ENTER)

        sleep(1)
        produto = self.navegador.find_element(By.XPATH, '//*[@id="bs-modal"]/div/div/div/div[2]/div[2]/div[2]/table/tbody/tr/td[4]')
        produto.click()

        sleep(1)
        botao_continuar = self.navegador.find_element(By.XPATH, '//*[@id="bs-modal"]/div/div/div/div[3]/button[1]')
        botao_continuar.click()

        sleep(1)
        botao_relacionar = self.navegador.find_element(By.XPATH, '//*[@id="bs-modal"]/div/div/div/div[3]/button[2]')
        botao_relacionar.click()
