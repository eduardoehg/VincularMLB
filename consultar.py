import requests


class Consulta:

    def __init__(self, sku, token):
        self.sku = sku
        self.token = token

        self.pesquisar()

    def pesquisar(self):
        url = 'https://api.tiny.com.br/api2/produtos.pesquisa.php'

        dados = {'token': self.token, 'formato': 'JSON', 'pesquisa': self.sku}
        retorno = requests.get(url, params=dados)

        response_dict = retorno.json()
        status = response_dict.get('retorno', {}).get('status')
        tipo_variacao = response_dict.get('retorno', {}).get('produtos', [{}])[0].get('produto', {}).get('tipoVariacao')
        return status == 'OK' and tipo_variacao == 'N'
