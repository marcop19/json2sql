import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
from sqlalchemy import create_engine

db_server = ""
db_username = ""
db_password = ""
db_database = ""

# Connessione a SQL Server tramite SQLAlchemy
engine = create_engine(f'mssql+pyodbc://{db_username}:{db_password}@{db_server}/{db_database}?driver=ODBC+Driver+17+for+SQL+Server')


# URL del web service RESTful
url = "https://tesis-test.konvergence.it/TesisREST/tesisApi/ContractRows/SAP"

# Credenziali per Basic Authentication
username = ""
password = ""

try:
    # Effettua la richiesta GET con Basic Authentication
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    response.raise_for_status()  # Verifica se la richiesta è andata a buon fine (status code 200)

    # Recupera il JSON dalla risposta
    json_data = response.json()

    # Converte il JSON in un DataFrame Pandas
    df = pd.DataFrame(json_data)

    # Inserimento del DataFrame in SQL Server
    df.to_sql('tesis_contract', con=engine, if_exists='replace', index=False)  # 'replace' per sovrascrivere la tabella esistente

except requests.exceptions.RequestException as e:
    print(f"Errore durante la richiesta: {e}")
except ValueError as e:
    print(f"Errore nel parsing del JSON: {e}")