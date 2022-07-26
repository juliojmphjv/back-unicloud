import json
import sys
import urllib.request
from logs.setup_log import logger
class ConsultaReceita:

    def __init__(self, cnpj):
        self.cnpj = cnpj

    def __validation(self):
        'Recebe um CNPJ e retorna True se formato válido ou False se inválido'

        cnpj = self.__parse_input()
        if len(cnpj) != 14 or not cnpj.isnumeric():
            logger.error(f'cnpj not numeric or less than 14 digit')
            return False

        verificadores = cnpj[-2:]
        lista_validacao_um = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        lista_validacao_dois = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

        'Calcular o primeiro digito verificador'
        soma = 0
        for numero, ind in zip(cnpj[:-1], range(len(cnpj[:-2]))):
            soma += int(numero) * int(lista_validacao_um[ind])

        soma = soma % 11
        digito_um = 0 if soma < 2 else 11 - soma

        'Calcular o segundo digito verificador'
        soma = 0
        for numero, ind in zip(cnpj[:-1], range(len(cnpj[:-1]))):
            soma += int(numero) * int(lista_validacao_dois[ind])

        soma = soma % 11
        digito_dois = 0 if soma < 2 else 11 - soma

        logger.info(f'validation result: {verificadores == str(digito_um) + str(digito_dois)}')
        return verificadores == str(digito_um) + str(digito_dois)

    def __parse_input(self):
        'Retira caracteres de separação do CNPJ'
        cnpj = str(self.cnpj)
        cnpj = cnpj.replace('.', '')
        cnpj = cnpj.replace(',', '')
        cnpj = cnpj.replace('/', '')
        cnpj = cnpj.replace('-', '')
        cnpj = cnpj.replace('\\', '')
        logger.info(cnpj)
        return cnpj

    def __consulta_cnpj(self):
        url = 'http://receitaws.com.br/v1/cnpj/{0}'.format(self.__parse_input())
        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('User-agent',
             " Mozilla/5.0 (Windows NT 6.2; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0")]

        with opener.open(url) as fd:
            content = fd.read().decode()

        dic = json.loads(content)
        logger.info(f'dic is: {dic}')
        return dic

    def get_parsed(self):
        return self.__parse_input()

    def cnpj_isvalid(self):
        return (True, self.__consulta_cnpj()['message']) if not self.__consulta_cnpj()['status'] else False

    def get_data(self):
        return self.__consulta_cnpj()

def parse_phone(phone):
    import re
    ddd = re.search('\((\d+)', phone)
    number = phone.split()
    print(ddd[1])
    print(number[1])

if __name__ == '__main__':
    teste = ConsultaReceita('02.334.512/0001-10')
    print(teste.get_data())
    # print(parse_phone('(21) 2772-562'))