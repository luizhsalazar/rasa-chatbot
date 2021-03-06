# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from rasa_sdk import Action
import requests
import webbrowser

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset

API_URL = "http://api-cartaweb-hom.intranet.ciasc.gov.br/api/pesquisa-servico?page=1&cdtipo=1&q="
URL_DETALHE_SERVICO = "http://cartaweb-hom.ciasc.sc.gov.br/servicos/detalhe/"

class OpenServicoSCDigital(Action):
    def name(self):
        return 'open_servico_scdigital'

    def run(sel, dispatcher, tracker, domain):
        servico_solicitado = tracker.get_slot('servico_solicitado')
        print(servico_solicitado)

        if servico_solicitado == 'nao_encontrado':
            dispatcher.utter_message('Serviço não encontrado :(')

        webbrowser.open(URL_DETALHE_SERVICO + servico_solicitado)

        return []

class ActionServico(Action):
    def name(self) -> Text:
        return "get_servico_scdigital"

    def run(self, dispatcher, tracker, domain):
        servico = tracker.get_slot('servico')
        print(servico)

        if servico is None:
            dispatcher.utter_message('Não consegui entender o que você quis dizer. Digite novamente, por favor :)')
            return [AllSlotsReset()]

        query_url = API_URL + servico
        res = requests.get(query_url)

        if res.status_code == 200:
            data = res.json()["data"]
            buttons = []

            if (data is None or len(data) == 0):
                dispatcher.utter_message('Serviço não encontrado :(\n Digite um novo serviço, por favor.')
                return [AllSlotsReset()]

            for servico_scdigital in data:
                nome_servico = servico_scdigital['nmtitulo']
                slug_servico = servico_scdigital['nmslug']

                # payload aponta para uma intent diretamente com o valor do slot pré-preenchido
                buttons.append({ "title": nome_servico, "payload": '/acessar_servico{"servico_solicitado": "' + slug_servico + '"}' })

            try:
                dispatcher.utter_message(text="Sim! Clique no serviço que melhor atende você!", buttons=buttons)
            except ValueError:
                dispatcher.utter_message(ValueError)

        return [AllSlotsReset(), SlotSet('servico_solicitado', servico)]
