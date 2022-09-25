# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionSolicitarEdadUsuario(Action):
  
    def name(self) -> Text:
         return "action_edad"
    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
              anios = tracker.latest_message['entities'][0]['value']
              if int(anios)>=18:
                 message="De acuerdo! Hora necesito que me brindes tu nombre completo y DNI para proceder con la solicitud"
              else: 
                 message="Lo siento pero debera presentarse una de nuestras sucursales. Debera venir con un tutor o adulto responsable, para adquirir una extension de su tarjeta de DEBITO/CREDITO ."
              dispatcher.utter_message(text=str(message)) #template="utter_desea_continuar_tramites,..,..,"
              return []

class ActionCiudad(Action):
   def name(self) -> Text:
         return "action_ciudad_residencia"
   def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
              ciudad = tracker.latest_message['entities'][0]['value'] # busco/guardo la ultima entidad "ciudad"
              intent = tracker.lastest_message['intent'].get['name']  # verifico q halla consultado donde retirar la tarjeta
              dispatcher.utter_message(text="bien") # contesta el bot
              if str(intent)=="ciudad_banco":
               return[SlotSet("slot_ciudad",ciudad)] # guardo la ciudad del usuario
               #return[SlotSet("slot_ciudad",str(ciudad))]
              return []
              

class ActionBanco(Action):
  
    def name(self) -> Text:
         return "action_banco_afiliado"
    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
              banco = tracker.latest_message['entities'][0]['value'] # busco la ultima entidad bancaria 
              intent = tracker.lastest_message['intent'].get['name'] # busca la ultima action del usuario ("banco_afiliado")
              ciudad=tracker.get_slot("slot_ciudad") # recupero el slot de la ciudad
              message="Las sucursales disponibles en "+ str(ciudad) + "para el banco "+ (banco) +"son:"
              if str(intent)=="banco_afiliado":
                  if str(banco)=="Banco Provincia":
                      message= message+ "Av.Colon 1333 ; Pinto 699 ;Quintana 450"
                      return [SlotSet("slot_bank",banco)]
                  else: 
                     message="No hay sucursales disponibles en "+ ciudad + "o falta anidar mas IF"
              dispatcher.utter_message(text=str(message))  
              return []             
#x=5
#def get_name():
#    dsdsds

class Action_horarios_Banco(Action):

   def name(self) -> Text:
         return "action_horarios_tarde"
   def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

              intent = tracker.lastest_message['intent'].get['name'] #busco el ultimo intento
              if str(intent)=="horario_tarde":
                  ciudad=tracker.get_slot("slot_ciudad") # recupero el slot de la ciudad
                  bank=tracker.get_slot("slot_bank") # recupero el slot de la ciudad
                  if str(bank)=="Banco Provincia":
                     if str(ciudad)=="Tandil":
                        dispatcher.utter_message(text="Los horarios del "+bank+" en "+ciudad+" son de 12 a 15 hs")  
                     else:    # si no esta en las sentencias , no hay horarios de tarde "para x sucursal si lo complejizamos"
                        dispatcher.utter_message(text="Lo siento mucho, no contamos con horarios para la tarde. Puedes visitarnos siempre de 8:00 a 12:00 hs")
                        dispatcher.utter_message(text="Hay algo mas en lo que pueda ayudarte ?") # remplazar text=... por :: template="utter_X"
              return []

              #ES NECESARIO SEMEJANTE IF ?????? O reune esa info a partir del tracker????? 


              #FALTA HACER EL SLOT TIME TARDE PARA Q QUEDE COMPLETO