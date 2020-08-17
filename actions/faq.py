from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker, FormAction
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

backend_url = "http://localhost:5000"
class ActionImpactIndustries(Action):
    def name(self) -> Text:
        return "action_impact_industries"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Fintech\nEducation\nHealthcare\nAgritech\nPharmaceuticals\nInternet\nLogistics\nMedia& Entertainment")
        return [UserUtteranceReverted()]


class ActionRecentStories(Action):
    def name(self) -> Text:
        return "action_recent_stories"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="To see our recent story on AI see the link below:\nhttps://medium.com/vitwit/your-everyday-machine-learning-pipeline-a30e436c786c")
        dispatcher.utter_message(text="To see our recent story on Blockchain see the link below:\nhttps://medium.com/vitwit/chain-reaction-1-launching-inter-blockchain-communication-agoric-and-cosmos-5081cf71f3fa")
        dispatcher.utter_message(text="To see our recent story on Cloud computing and Bigdata see the link below:\nhttps://medium.com/@theakshaygupta/easily-setup-custom-vpc-on-aws-with-terraform-a7240bf7c734?source=---------2------------------")
        return [UserUtteranceReverted()]

class ContactForm(FormAction):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "contact_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["name", "mobile", "email"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "name": [self.from_text(intent="inform")],
            "email": [
                self.from_entity(entity="email"),
                self.from_text(intent="inform"),
            ],
            "mobile": [
                self.from_entity(entity="mobile"),
                self.from_text(intent="inform"),
            ]
        }

    def validate_mobile(self,
                    value: Text,
                    dispatcher: CollectingDispatcher,
                    tracker: Tracker,
                    domain: Dict[Text, Any]) -> Optional[Text]:

                    match = re.match("^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$", value)
                    if match:
                        # validation succeeded
                        return {'mobile': value}
                    else:
                        dispatcher.utter_message(text="Please check your mobile number you have typed")
                        # validation failed, set this slot to None, meaning the
                        # user will be asked for the slot again
                        return {'mobile': None}

    def validate_email(self,
                    value: Text,
                    dispatcher: CollectingDispatcher,
                    tracker: Tracker,
                    domain: Dict[Text, Any]) -> Optional[Text]:

                    match = re.match("[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+", value)
                    if match:
                        # validation succeeded
                        return {'email': value.lower()}
                    else:
                        dispatcher.utter_message(text='Please give a valid Email ID')
                        # validation failed, set this slot to None, meaning the
                        # user will be asked for the slot again
                        return {'email': None}

    def submit(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
            ) -> List[Dict]:
            my_obj = {
                "email": tracker.get_slot("email"),
                "mobile": tracker.get_slot("mobile"),
                "name": tracker.get_slot("name")
            }
            response = requests.post("{}/contactus".format(backend_url), json=my_obj)
            body = response.json()
            if response.status_code == 409 or response.status_code == 401 or response.status_code == 500:
                dispatcher.utter_message(text=body['message'])
                return[AllSlotsReset()]
            elif response.status_code == 200:
                dispatcher.utter_message(text="Dear, {} Your details have been successfully submitted, You will be contacted by our HR team shortly".format(tracker.get_slot("name")))
                dispatcher.utter_message(text="If you have general questions about Vitwit,\n
                    please head to our official website(https://vitwit.com/), otherwise contact\n
                    us at [+91 63009 46153](mailto:contact@Vitwit.com) for anything else.")
                return[UserUtteranceReverted()]


class ActionExplainSignupForm(Action):
    """Returns the explanation for the signup form questions"""

    def name(self) -> Text:
        return "action_explain_contact_form"

    def run(self, dispatcher, tracker, domain) -> List[EventType]:
        requested_slot = tracker.get_slot("requested_slot")

        if requested_slot not in SignupForm.required_slots(tracker):
            dispatcher.utter_message(
                text="Sorry, I didn't get that. Please rephrase or answer the question "
                "above."
            )
            return []

        dispatcher.utter_message(template=f"utter_explain_{requested_slot}")
        return []
