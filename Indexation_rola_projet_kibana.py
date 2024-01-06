# Python script écrit par Rola Monzer pour indexer "rola_projet_kibana" sur le cluster elasticsearch

from elasticsearch import Elasticsearch
import requests

# premiere modification du fichier flights.json
fin = open("flights.json","rt")  # ce fichier est inclus dans le dossier sous le nom "flights_raw.json"
data = fin.read()
data = data.replace("'",'"') # modification des guillemets
data = data.replace('Int"l',"Int'l") # restauration de l'apostrophe du mot "Int'l"
data = data.replace('O"Hare',"O'Hare") # restauration de l'apostrophe du mot "O'Hare"
fin.close()
fout = open("flights.json","wt")
fout.write(data)
fout.close()

# deuxieme modification du fichier flights.json
data = open("flights.json","r")
data_new = open("flights_formater.json","w")

data_ligne = data.readlines()
e = 0
for i in data_ligne:
    data_new.write('{ "index" : { "_index" : "rola_projet_kibana", "_type" : "_doc", "_id": '+ str(e) +'} }\n') # on ajoute un champs "index" pour chaque document
    data_new.write(i) # on écrit le document correspondant 
    e += 1
data.close()
data_new.close()

# initialisation de l'url du cluster elasticsearch avec l'API "_bulk" et du header
url = "http://20.188.37.241:9200/_bulk"
header = {"Content-Type":"application/json"}

# on récupère le contenu du fichier json :
data = open("flights_formater.json", "rb")
data = data.read()

# on crée l'index et on ajoute les documents sur notre cluster elasticsearch :
response = requests.post(url,headers=header,data=data)
print(response.status_code)