import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

url = '' #Inserir link do site desejavel para pesquisa 

class Teste:
    def __init__(self):
        self._driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self._wait = WebDriverWait(self._driver, 50)
        self._wait_quickly = WebDriverWait(self._driver, 2)

    def get(self):
        self._driver.get(url)

    def num_pedido(self, documento):
        try:
            pedido = self._wait.until(EC.presence_of_element_located((By.ID, 'orderNumber')))
        except Exception as e:
            print(e)
        else:
            try:
                pedido.clear()
            except Exception as e:
                print(e)
            pedido.send_keys(str(documento))
            time.sleep(1)

    def clicar_pesquisar(self):
        try:
            pesquisar = self._wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[2]/div/div/form/button")))
            pesquisar.click()
        except Exception as e:
            print(e)

    def status(self):
        try:
            table_info = self._wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div/div[3]/div/table/tbody/tr[1]')))
            data_estimada = self._wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div/div[2]/div/div[2]/div[1]')))
            previsao_estimada = self._wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div/div[2]/div/div[2]/div')))    
            
            
            list_table_info = table_info.text.split(' ')
            list_table_estimada = data_estimada.text.split(' ')

            list_previsao = previsao_estimada.text.split(' ')
            data_previsao = list_previsao[3].split('\n')

            if "Entrega" in list_table_info:
                print(list_table_info[0])
            
            else:
                print(list_table_estimada[3])

            return list_table_info[0], list_table_info[2], data_previsao[1]
        
        except Exception as e:
            print(e)
            

    def voltar_pagina(self):
        self._driver.back()
        time.sleep(2)

    def get_error(self):
        try:
            error = self._wait_quickly.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div/h1')))
            print(error.text)
            return True
        except:
            print("No error")
            return False

def main():
    teste = Teste()
    teste.get()
    time.sleep(2)

    df = pd.read_csv('base.csv', sep=";", on_bad_lines='skip')
    documentos = df["DOCUMENTOS"]

    data_list = []
    evento_list = []
    previsao_list = []
    documento_list = []
    

    for documento in documentos:
        teste. num_pedido(documento)
        teste.clicar_pesquisar()
        time.sleep(2)

        error = teste.get_error()
        if error:
            print("ERROR MAIN")
            documento_list.append(documento)
            data_list.append('0')
            evento_list.append('0')
            previsao_list.append('0')
            teste.voltar_pagina()
           
            continue
        else:
            print("NO ERROR MAIN")
            data, evento, previsao = teste.status()

            time.sleep(2)

            documento_list.append(documento)
            data_list.append(data)
            evento_list.append(evento)
            previsao_list.append(previsao)
            teste.voltar_pagina()


        result_df = pd.DataFrame({
            'Documento' : documento_list,
            'Data': data_list,
            'Evento': evento_list,
            'Previsão de entrega': previsao_list,
        })

        result_df.to_csv('resultado.csv', sep= ';',encoding='utf-8-sig', index=False)

    teste._driver.quit()

main()