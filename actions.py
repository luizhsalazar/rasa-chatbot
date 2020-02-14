# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from rasa_sdk import Action
import requests

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

class FetchNameAction(Action):
    def name(self):
        return "action_fetch_profile"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message('Hey there, {name}!', tracker)
