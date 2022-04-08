import csv
#import regex
import re
from bcb import get_json_response

textToFinalCSV = 'CPF ou CNPJ;Aniversario;Solicitar;Repescagem;\n'

# Read in the CSV file 'lista.csv' with the following columns: 'cpfOuCnpj' and 'date'
with open('lista.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    # for each row, get the cpf or cnpj and the date
    for row in reader:
        cpfOrCnpj = row[0]
        date = row[1]

        # if the date has '/' convert date dd/mm/yyyy to yyyy-mm-dd
        if '/' in date:
            date = date.split('/')
            date = date[2] + '-' + date[1] + '-' + date[0]

        # with regex remove all non-numeric characters from cpf or cnpj
        cpfOrCnpj = re.sub('[^0-9]', '', cpfOrCnpj)

        # get the dates from the json response
        dates = get_json_response(cpfOrCnpj, date)

        # if dates is False, add on final csv file the cpf or cnpj and the date and '' on the other columns
        if dates == False:
            textToFinalCSV += cpfOrCnpj + ';' + date + ';' + ';' + ';' + '\n'
        # if dates is not False
        else:
            #solicitar = dates['solicitar']['inicio'] + ' até ' + dates['solicitar']['fim']
            solicitar = dates['solicitar']['inicio'] + ' até ' + dates['solicitar']['fim']
            #repescagem = dates['repescagem']['inicio'] + ' até ' + dates['repescagem']['fim']
            repescagem = dates['repescagem']['inicio'] + ' até ' + dates['repescagem']['fim']
            textToFinalCSV += cpfOrCnpj + ';' + date + ';' + solicitar + ';' + repescagem + '\n'
    
# write the final csv file with utf-8 encoding
with open('final.csv', 'w', encoding='utf-8') as csvfile:
    csvfile.write(textToFinalCSV)
