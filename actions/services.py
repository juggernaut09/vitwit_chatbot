from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
    FollowupAction,
    AllSlotsReset,
    BotUttered,
    SlotSet,
    SessionStarted
)



class ActionServiceAi(Action):
    def name(self) -> Text:
        return "action_service_ai"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Our Applied AI services will help scale your business by building fully autonomous & automated organisations")
        dispatcher.utter_message(text="To see our recent story on AI see the link below:\nhttps://medium.com/vitwit/your-everyday-machine-learning-pipeline-a30e436c786c")
        return [UserUtteranceReverted()]

class ActionServiceBC(Action):
    def name(self) -> Text:
        return "action_service_bc"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Blockchain is the future and it’s already here. Our expert Blockchain developers will help you in adopting the technology of the future.")
        dispatcher.utter_message(text="To see our recent story on Blockchain see the link below:\nhttps://medium.com/vitwit/chain-reaction-1-launching-inter-blockchain-communication-agoric-and-cosmos-5081cf71f3fa")
        return [UserUtteranceReverted()]


class ActionServiceCloud(Action):
    def name(self) -> Text:
        return "action_service_cloud"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="With our expertise in cloud computing & Big data, we deliver diverse range of cloud solutions to help you transform your business.")
        dispatcher.utter_message(text="To see our recent story on Cloud computing and Bigdata see the link below:\nhttps://medium.com/@theakshaygupta/easily-setup-custom-vpc-on-aws-with-terraform-a7240bf7c734?source=---------2------------------")
        return [UserUtteranceReverted()]


class ActionCoreOfferings(Action):
    def name(self) -> Text:
        return "action_core_offerings"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        buttons = []
        buttons.append({
            'title': "Artificial intelligence",
            'payload': 'Artificial Intelligence'
        })
        buttons.append({
            'title': "Block Chain",
            'payload': 'Block Chain'
        })
        buttons.append({
            'title': "Cloud Computing and Big Data",
            'payload': 'Cloud Computing and Big Data'
        })
        dispatcher.utter_message(text="We specialize in providing state of the art technology solutions in AI, Blockchain and Cloud Computing.", buttons=buttons)
        return [UserUtteranceReverted()]
