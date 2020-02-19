# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from rasa_sdk import Action
import requests

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

API_URL = "http://api-cartaweb-hom.intranet.ciasc.gov.br/api/pesquisa-servico?page=1&cdtipo=1&q=teatro"

class ApiAction(Action):
	def name(self):
		return "action_servicos_sc_digital"

	def run(self, dispatcher, tracker, domain):
		res = requests.get(API_URL)
		if res.status_code == 200:
			data = res.json()["data"]
			servico = data[0]

			out_message = "Serviço encontrado {}.".format(servico["nmdescricao"])
			dispatcher.utter_message(out_message)

		return []

class ActionServico(Action):
    def name(self) -> Text:
        return "action_servico"

    def run(self, dispatcher, tracker, domain):
        cpf = tracker.get_slot('cpf')
        print(cpf)

        try:
            dispatcher.utter_message("O seu serviço é {}?".format(cpf))
        except ValueError:
            dispatcher.utter_message(ValueError)
        return [SlotSet("cpf", cpf)]
