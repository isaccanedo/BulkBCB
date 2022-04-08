#import httplib2 to make http requests
from wsgiref import headers
import httplib2
#import json to parse the json response
import json
import time


'''
    This function get from https://valoresareceber.bcb.gov.br/publico/rest/valoresAReceber/#cpfOrCnpj/#date the json response if the cpf or cnpj has values to be received

    @param cpfOrCnpj: cpf or cnpj to be searched
    @param date: date to be searched

    @return: if 'temValorAReceber' is true, return the json response, else return FALSE
'''
def get_json_response(cpfOrCnpj, date):
    #sleep 2 seconds between each request
    time.sleep(2)

    #create the url to be searched
    url = 'https://valoresareceber.bcb.gov.br/publico/rest/valoresAReceber/' + cpfOrCnpj + '/' + date
    #create the http object
    http = httplib2.Http()
    #get the response
    response, content = http.request(url, 'GET', headers={'Accept': 'application/json', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/83.0.4254.46'})

    #if the response is 200, the request was successful
    if response.status == 200:
        #parse the json response
        json_response = json.loads(content)
        #if 'temValorAReceber' is true, return the json response
        if json_response['temValorAReceber']:

            dates = {
                'solicitar': {
                    'inicio': '',
                    'fim': ''
                },
                'repescagem': {
                    'inicio': '',
                    'fim': ''
                },
                'resgate': {
                    'inicio': '',
                    'fim': ''
                }
            }

            #the dates['solicitar']['inicio'] is the date in json_response['datasLiberacao'][0]['dataInicioEpochSeconds'] converted of Epoch time i to date dd/mm/yyyy
            dates['solicitar']['inicio'] = time.strftime('%d/%m/%Y', time.localtime(json_response['datasLiberacao'][0]['dataInicioEpochSeconds']))
            #the dates['solicitar']['fim'] is the date in json_response['datasLiberacao'][0]['dataFimEpochSeconds'] converted of Epoch time i to date dd/mm/yyyy
            dates['solicitar']['fim'] = time.strftime('%d/%m/%Y', time.localtime(json_response['datasLiberacao'][0]['dataFimEpochSeconds']))
            #the dates['resgate']['inicio'] is the date in json_response['datasLiberacao'][1]['dataInicioEpochSeconds'] converted of Epoch time i to date dd/mm/yyyy
            dates['resgate']['inicio'] = time.strftime('%d/%m/%Y', time.localtime(json_response['datasLiberacao'][1]['dataInicioEpochSeconds']))
            #the dates['resgate']['fim'] is the date in json_response['datasLiberacao'][1]['dataFimEpochSeconds'] converted of Epoch time i to date dd/mm/yyyy
            dates['resgate']['fim'] = time.strftime('%d/%m/%Y', time.localtime(json_response['datasLiberacao'][1]['dataFimEpochSeconds']))
            #the dates['repescagem']['inicio'] is the date in json_response['datasLiberacao'][2]['dataInicioEpochSeconds'] converted of Epoch time i to date dd/mm/yyyy
            dates['repescagem']['inicio'] = time.strftime('%d/%m/%Y', time.localtime(json_response['datasLiberacao'][2]['dataInicioEpochSeconds']))
            #the dates['repescagem']['fim'] is the date in json_response['datasLiberacao'][2]['dataFimEpochSeconds'] converted of Epoch time i to date dd/mm/yyyy
            dates['repescagem']['fim'] = time.strftime('%d/%m/%Y', time.localtime(json_response['datasLiberacao'][2]['dataFimEpochSeconds']))

            return dates
        #else return FALSE
        else:
            return False
    #else, the request was not successful return false
    else:
        return False