import requests


def consulta(sku, token):
    url = 'https://api.tiny.com.br/api2/produtos.pesquisa.php'

    dados = {'token': token, 'formato': 'JSON', 'pesquisa': sku}
    retorno = requests.get(url, params=dados)

    response_dict = retorno.json()
    status = response_dict.get('retorno', {}).get('status')
    tipo_variacao = response_dict.get('retorno', {}).get('produtos', [{}])[0].get('produto', {}).get('tipoVariacao')
    return status == 'OK' and tipo_variacao == 'N'
