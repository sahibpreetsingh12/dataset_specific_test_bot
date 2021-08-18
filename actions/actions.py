# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import urllib.request, json
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

master_dic_dataset_name = {
        'agricultural data' : 'agcensus_crop',
        'agricluture' : 'agcensus_crop', 
        'agri data' : 'agcensus_crop',
        'agricuture data':'agcensus_crop',
        'agriculture':'agcensus_crop',
        'agriculture census': 'agcensus_crop',
        'agcensus':'agcensus_crop',
        'rainfall':'rainfall',
        'rain data':'rainfall',
        'rainfall data':'rainfall',
        'agricultural census':'agcensus_crop',
        'rain figures':'rainfall',
        'sales of fertiliser':'fertiliser_sales',
        'sales of fertilisers':'fertiliser_sales',
        'fertiliser sales':'fertiliser_sales',
        'fertilizer sales data':'fertiliser_sales',
        'fertilizers sales data':'fertiliser_sales',
         'sales regarding fertlisers':'fertiliser_sales',
         'rbi_deposit':'rbi_deposit',
         'deposits of rbi':'rbi_deposit',
         'rbi-deposit':'rbi_deposit',
         'rbi deposit': 'rbi_deposit',
         'deposits by rbi':'rbi_deposit',
         'investments of rbi':'rbi_deposit',
         'investments by rbi':'rbi_deposit',
         'mnrega employment':'nrga_emp',
         'credit by bank':'rbi_credit',
         'Soil':'soil'
         ,'soil':'soil',
         'pmfby':'pmfby'
         }
class ActionDatasetName(Action):

    def name(self) -> Text:
        return "action_about_data_dataset_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # print(tracker.latest_message['text']) # to get user typed message 

        ls_entity =tracker.latest_message['entities'] # to get entities from user message

        print(ls_entity)

        # initilize the dataset name
        dataset_name = 0

        # spellcheck the user extracted_dataset_name
        extracted_dataset_name = 0

        for i in range(len(ls_entity)):
            if ls_entity[i]['entity'] == 'dataset_name':

                # name of dataset extracted from RASA
                temp_dataset_name = ls_entity[i]['value']

                # name of dataset we get after extraction
                extracted_dataset_name = ls_entity[i]['value']
                print(extracted_dataset_name)
                break
    
        # dictionary  conating all possible name that can be given to a dataset name
    

        global transformed_dataset_name
    
        transformed_dataset_name =0
        global master_dic_dataset_name
        if extracted_dataset_name in master_dic_dataset_name.keys():
            

            transformed_dataset_name = master_dic_dataset_name[extracted_dataset_name]

        
        print(f"after tranformation ---> {transformed_dataset_name}")


        if transformed_dataset_name !=0 :
     
            # by defualt dataset name value will be given to slot if that was extratced from user message
            print("\n","Now slots value is ",tracker.slots['dataset_name'])  

            extracted_ls_entity = []
            for i in range(len(ls_entity)):
                extracted_ls_entity.append(ls_entity[i]['entity'])

            extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
            print(f"Entites we extracted {extracted_ls_entity}")


            dict_of_mapped_data_with_id = {}
            with urllib.request.urlopen("https://indiadataportal.com/meta_data_info") as url:
                data = json.loads(url.read().decode())
                temp_data  = json.dumps(data, indent=4, sort_keys=True)
                temp_data = json.loads(temp_data)

                for i in range(len(temp_data)):
                    data = temp_data[i]
 
                    # print(f"{data['dataset_name']} ---> {data['dataset_id']}")
                    dict_of_mapped_data_with_id[data['dataset_name']] = data['dataset_id']
  

                # if transformed_dataset_name is present in our data we got from json file
                if transformed_dataset_name in dict_of_mapped_data_with_id.keys():
                    
                    # extract id for that dataset name
                    extracted_id = dict_of_mapped_data_with_id[transformed_dataset_name]

                    for i in range(len(temp_data)):
                            data = temp_data[i]
                            if data['dataset_id']==extracted_id:
                                p = json.dumps(data)
                                p = json.loads(p)
                                
                    

                    if len(extracted_ls_entity) >=1:
                        # iterating through all entites other than dataset_name
                        for entity_iter in extracted_ls_entity:

                            # check if entity present in extracted_ls_entity is also present in p ( data in db)
                            # spellcheck the entity
                            if entity_iter in p.keys():
                                # if entity is present in p then print the value of that entity
                                print(f"{entity_iter} ----> {p[entity_iter]}")
                                dispatcher.utter_message(text = f"{entity_iter} is {p[entity_iter]}")
                                
                            
                            else:
                                dispatcher.utter_message(text = 'Sorry but can you pls say it again')
                                # return [SlotSet('dataset_name', dataset_name)]
                    
                    else:
                        dispatcher.utter_message(text = f'Yes you can start with {temp_dataset_name}')
                        

            print(f"Returning value of {transformed_dataset_name}")
            return [SlotSet('dataset_name', transformed_dataset_name)]
        
        # if dataset_name is not present in our data we got from json file
        else:
            dispatcher.utter_message(text = """Can You Please rephrase your question about which dataset
             you want ask """)
        

class ActionGranularityLevel(Action):

    def name(self) -> Text:
        return "action_about_data_granularity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            # intent of user message 
            print(tracker.get_intent_of_latest_message())

            print("\n","Now slots value in granular is ",tracker.slots['dataset_name'])

            ls_entity =tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and  tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_ = tracker.slots['dataset_name']

                # calling global dictionary
                global master_dic_dataset_name

                # if dataset name that is extracted from user message is present in our data we got from json file
                if dataset_name_ in master_dic_dataset_name.keys():
        
                    dataset_name_ = master_dic_dataset_name[dataset_name_]
                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in gran {extracted_ls_entity}")


                dict_of_mapped_data_with_id = {}
                with urllib.request.urlopen("https://indiadataportal.com/meta_data_info") as url:
                    data = json.loads(url.read().decode())
                    temp_data  = json.dumps(data, indent=4, sort_keys=True)
                    temp_data = json.loads(temp_data)
                    for i in range(len(temp_data)):
                        data = temp_data[i]
                        dict_of_mapped_data_with_id[data['dataset_name']] = data['dataset_id']

                    # if extracted dataset name is present in our data we got from json file
                    if dataset_name_ in dict_of_mapped_data_with_id.keys():
                        
                        # extract id for that dataset name
                        extracted_id = dict_of_mapped_data_with_id[dataset_name_]

                        for i in range(len(temp_data)):
                                data = temp_data[i]
                                if data['dataset_id']==extracted_id:
                                    p = json.dumps(data)
                                    p = json.loads(p)
                                    # print(p,'\n')
                        

                        if len(extracted_ls_entity) >=1:
                            # iterating through all entites other than dataset_name
                            for entity_iter in extracted_ls_entity:
                                print("yes i am ")
                                # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                # spellcheck the entity
                                if entity_iter in p.keys():

                                    # if entity is present in p then print the value of that entity
                                    print(f"{entity_iter} ----> {p[entity_iter]}")
                                    dispatcher.utter_message(text = f"{entity_iter} is {p[entity_iter]}")
                                
                                else:
                                    dispatcher.utter_message(text = 'Sorry but can you pls tell again  what feature you are looking for')
                                    dispatcher.utter_message(text = """Ex :Like if you want to know Granularity level of a Dataset
                                                                        say it like :- What is the Granularity level of Rainfall Data""")
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to know Granularity level of a Dataset
                                                                        say it like :- What is the Granularity level of Rainfall Data""")
                                

            else:
                dispatcher.utter_message(text = """Can you specify the Dataset Name completely and
                what's your query reagrding it """)



class ActionSourcedata(Action):

    def name(self) -> Text:
        return "action_about_data_source_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            # intent of user message 
            print(tracker.get_intent_of_latest_message())

            print("\n","Now slots value in source is ",tracker.slots['dataset_name'])

            ls_entity =tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and  tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_ = tracker.slots['dataset_name']

                # calling global dictionary
                global master_dic_dataset_name

                # if dataset name that is extracted from user message is present in our data we got from json file
                if dataset_name_ in master_dic_dataset_name.keys():
        
                    dataset_name_ = master_dic_dataset_name[dataset_name_]

                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in source {extracted_ls_entity}")


                dict_of_mapped_data_with_id = {}
                with urllib.request.urlopen("https://indiadataportal.com/meta_data_info") as url:
                    data = json.loads(url.read().decode())
                    temp_data  = json.dumps(data, indent=4, sort_keys=True)
                    temp_data = json.loads(temp_data)
                    for i in range(len(temp_data)):
                        data = temp_data[i]
                        # print(f"{data['dataset_name']} ---- > {data['dataset_id']} " )
                        dict_of_mapped_data_with_id[data['dataset_name']] = data['dataset_id']

                    # if extracted dataset name is present in our data we got from json file
                    if dataset_name_ in dict_of_mapped_data_with_id.keys():
                        
                        # extract id for that dataset name
                        extracted_id = dict_of_mapped_data_with_id[dataset_name_]

                        for i in range(len(temp_data)):
                                data = temp_data[i]
                                if data['dataset_id']==extracted_id:
                                    p = json.dumps(data)
                                    p = json.loads(p)
                                    # print(p,'\n')
                        

                        if len(extracted_ls_entity) >=1:
                            # iterating through all entites other than dataset_name
                            for entity_iter in extracted_ls_entity:
                                print("yes i am in source")
                                # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                # spellcheck the entity

                                
                                if entity_iter in p.keys():
                                    # if entity is present in p then print the value of that entity
                                    print(f"{entity_iter} ----> {p[entity_iter]}")
                                    dispatcher.utter_message(text = f"{entity_iter} is {p[entity_iter]}")
                                
                                else:
                                    dispatcher.utter_message(text = 'Sorry but can you pls tell again  what feature you are looking for')
                                    dispatcher.utter_message(text = """Ex :Like if you want to know Source of a Dataset
                                                                        say it like :- What is the Source of Rainfall Data""")
                        
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to know Source of a Dataset
                                                                        say it like :- What is the Source of Rainfall Data""")

            else:
                dispatcher.utter_message(text = "Can you tell which dataset it is")



class ActionMethodology(Action):

    def name(self) -> Text:
        return "action_about_data_methodology"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            # intent of user message 
            print("\n",tracker.get_intent_of_latest_message())

            print("\n","Now slots value in Methodology is ",tracker.slots['dataset_name'])

            ls_entity =tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and  tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_ = tracker.slots['dataset_name']
  
                global master_dic_dataset_name
                if dataset_name_ in master_dic_dataset_name.keys():
        
                    dataset_name_ = master_dic_dataset_name[dataset_name_]

                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in Methodology {extracted_ls_entity}")


                dict_of_mapped_data_with_id = {}
                with urllib.request.urlopen("https://indiadataportal.com/meta_data_info") as url:
                    data = json.loads(url.read().decode())
                    temp_data  = json.dumps(data, indent=4, sort_keys=True)
                    temp_data = json.loads(temp_data)
                    for i in range(len(temp_data)):
                        data = temp_data[i]
                        # print(f"{data['dataset_name']} ---- > {data['dataset_id']} " )
                        dict_of_mapped_data_with_id[data['dataset_name']] = data['dataset_id']

                    # if extracted dataset name is present in our data we got from json file
                    if dataset_name_ in dict_of_mapped_data_with_id.keys():
                        
                        # extract id for that dataset name
                        extracted_id = dict_of_mapped_data_with_id[dataset_name_]

                        for i in range(len(temp_data)):
                                data = temp_data[i]
                                if data['dataset_id']==extracted_id:
                                    p = json.dumps(data)
                                    p = json.loads(p)
                                    # print(p,'\n')
                        

                        if len(extracted_ls_entity) >=1:
                            # iterating through all entites other than dataset_name
                            for entity_iter in extracted_ls_entity:
                                print("yes i am in methodology")
                                # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                # spellcheck the entity

                                
                                if entity_iter in p.keys():
                                    # if entity is present in p then print the value of that entity
                                    # print(f"{entity_iter} ----> {p[entity_iter]}")
                                    dispatcher.utter_message(text = f"{entity_iter} is {p[entity_iter]}")
                                
                                else:
                                    dispatcher.utter_message(text = 'Sorry but can you pls tell again  what feature you are looking for')
                                    dispatcher.utter_message(text = """Ex :Like if you want to know Methodology of a Dataset
                                                                        say it like :- What was the methodolgy adopted to make Rainfall Data""")
                        
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to know Methodology of a Dataset
                                                                        say it like :- What was the methodolgy adopted to make Rainfall Data""")

            else:
                dispatcher.utter_message(text = "Can you tell which dataset it is")

class ActionFrequency(Action):

    def name(self) -> Text:
        return "action_about_data_frequency"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            # intent of user message 
            print("\n",tracker.get_intent_of_latest_message())

            print("\n","Now slots value in frequency is ",tracker.slots['dataset_name'])

            ls_entity =tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and  tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_ = tracker.slots['dataset_name']

                 # calling global dictionary
                global master_dic_dataset_name

                # if dataset name that is extracted from user message is present in our data we got from json file
                if dataset_name_ in master_dic_dataset_name.keys():
        
                    dataset_name_ = master_dic_dataset_name[dataset_name_]

                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in frequency {extracted_ls_entity}")


                dict_of_mapped_data_with_id = {}
                with urllib.request.urlopen("https://indiadataportal.com/meta_data_info") as url:
                    data = json.loads(url.read().decode())
                    temp_data  = json.dumps(data, indent=4, sort_keys=True)
                    temp_data = json.loads(temp_data)
                    for i in range(len(temp_data)):
                        data = temp_data[i]
                        # print(f"{data['dataset_name']} ---- > {data['dataset_id']} " )
                        dict_of_mapped_data_with_id[data['dataset_name']] = data['dataset_id']

                    # if extracted dataset name is present in our data we got from json file
                    if dataset_name_ in dict_of_mapped_data_with_id.keys():
                        
                        # extract id for that dataset name
                        extracted_id = dict_of_mapped_data_with_id[dataset_name_]

                        for i in range(len(temp_data)):
                                data = temp_data[i]
                                if data['dataset_id']==extracted_id:
                                    p = json.dumps(data)
                                    p = json.loads(p)
                                    # print(p,'\n')
                        

                        if len(extracted_ls_entity) >=1:
                            # iterating through all entites other than dataset_name
                            for entity_iter in extracted_ls_entity:
                                print("yes i am in frequency")
                                # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                # spellcheck the entity

                                
                                if entity_iter in p.keys():

                                    # if entity is present in p then print the value of that entity
                                    # print(f"{entity_iter} ----> {p[entity_iter]}")
                                    dispatcher.utter_message(text = f"{entity_iter} is {p[entity_iter]}")
                                
                                else:
                                    dispatcher.utter_message(text = 'Sorry but can you pls tell again  what feature you are looking for')
                                    dispatcher.utter_message(text = """Ex :Like if you want to know Frequqncy of about Dataset updation
                                                                        say it like :- How often Rainfall Data is updated""")
                        
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to know Frequqncy of about Dataset updation
                                                                        say it like :- How often Rainfall Data is updated""")
            else:
                dispatcher.utter_message(text = "Can you tell which dataset it is")


class ActionLastDateUpdated(Action):

    def name(self) -> Text:
        return "action_about_data_last_updated_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            # intent of user message 
            # print("\n",tracker.get_intent_of_latest_message())

            print("\n","Now slots value in Last date Updated is ",tracker.slots['dataset_name'])

            ls_entity =tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and  tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_ = tracker.slots['dataset_name']

                # calling global dictionary
                global master_dic_dataset_name

                # if dataset name that is extracted from user message is present in our data we got from json file
                if dataset_name_ in master_dic_dataset_name.keys():
        
                    dataset_name_ = master_dic_dataset_name[dataset_name_]


                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in frequency {extracted_ls_entity}")


                dict_of_mapped_data_with_id = {}
                with urllib.request.urlopen("https://indiadataportal.com/meta_data_info") as url:
                    data = json.loads(url.read().decode())
                    temp_data  = json.dumps(data, indent=4, sort_keys=True)
                    temp_data = json.loads(temp_data)
                    for i in range(len(temp_data)):
                        data = temp_data[i]
                        # print(f"{data['dataset_name']} ---- > {data['dataset_id']} " )
                        dict_of_mapped_data_with_id[data['dataset_name']] = data['dataset_id']

                    # if extracted dataset name is present in our data we got from json file
                    if dataset_name_ in dict_of_mapped_data_with_id.keys():
                        
                        # extract id for that dataset name
                        extracted_id = dict_of_mapped_data_with_id[dataset_name_]

                        for i in range(len(temp_data)):
                                data = temp_data[i]
                                if data['dataset_id']==extracted_id:
                                    p = json.dumps(data)
                                    p = json.loads(p)
                        

                        if len(extracted_ls_entity) >=1:
                            # iterating through all entites other than dataset_name
                            for entity_iter in extracted_ls_entity:
                                print("yes i am in Last Date Updated")
                                # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                # spellcheck the entity

                                
                                if entity_iter in p.keys():

                                    # if entity is present in p then print the value of that entity
                                    # print(f"{entity_iter} ----> {p[entity_iter]}")
                                    dispatcher.utter_message(text = f"{entity_iter} is {p[entity_iter]}")
                                
                                else:
                                    dispatcher.utter_message(text = 'Sorry but can you pls tell again  what feature you are looking for')
                                    dispatcher.utter_message(text = """Ex :Like if you want to know Last Date updated for a Dataset 
                                                                        say it like :- When was this last date updated""")
                        
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to know Last Date updated for a Dataset 
                                                                        say it like :- When was this last date updated""")
            else:
                dispatcher.utter_message(text = "Can you tell which dataset it is")


class ActionSourceLink(Action):

    def name(self) -> Text:
        return "action_about_data_source_link"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            # intent of user message 
            # print("\n",tracker.get_intent_of_latest_message())

            print("\n","Now slots value in Source Link is ",tracker.slots['dataset_name'])

            ls_entity =tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and  tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_ = tracker.slots['dataset_name']

                # calling global dictionary
                global master_dic_dataset_name

                # if dataset name that is extracted from user message is present in our data we got from json file
                if dataset_name_ in master_dic_dataset_name.keys():
        
                    dataset_name_ = master_dic_dataset_name[dataset_name_]


                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in source link {extracted_ls_entity}")


                dict_of_mapped_data_with_id = {}
                with urllib.request.urlopen("https://indiadataportal.com/meta_data_info") as url:
                    data = json.loads(url.read().decode())
                    temp_data  = json.dumps(data, indent=4, sort_keys=True)
                    temp_data = json.loads(temp_data)
                    for i in range(len(temp_data)):
                        data = temp_data[i]
                        # print(f"{data['dataset_name']} ---- > {data['dataset_id']} " )
                        dict_of_mapped_data_with_id[data['dataset_name']] = data['dataset_id']

                    # if extracted dataset name is present in our data we got from json file
                    if dataset_name_ in dict_of_mapped_data_with_id.keys():
                        
                        # extract id for that dataset name
                        extracted_id = dict_of_mapped_data_with_id[dataset_name_]

                        for i in range(len(temp_data)):
                                data = temp_data[i]
                                if data['dataset_id']==extracted_id:
                                    p = json.dumps(data)
                                    p = json.loads(p)
                        

                        if len(extracted_ls_entity) >=1:
                            # iterating through all entites other than dataset_name
                            for entity_iter in extracted_ls_entity:
                                print("yes i am in Source Link")
                                # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                # spellcheck the entity

                                
                                if entity_iter in p.keys():

                                    # if entity is present in p then print the value of that entity
                                    # print(f"{entity_iter} ----> {p[entity_iter]}")
                                    dispatcher.utter_message(text = f"{entity_iter} is {p[entity_iter]}")
                                
                                else:
                                    dispatcher.utter_message(text = 'Sorry but can you pls tell again  what feature you are looking for')
                                    dispatcher.utter_message(text = """Ex :Like if you want to know Source Link for a Dataset 
                                                                        say it like :- What was the source for the dataset""")
                        
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to know Source Link for a Dataset 
                                                                        say it like :- What was the source for the dataset""")
            else:
                dispatcher.utter_message(text = "Can you tell which dataset it is")


class ActionDataExtractionPage(Action):

    def name(self) -> Text:
        return "action_about_data_data_extraction_page"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            # intent of user message 
            # print("\n",tracker.get_intent_of_latest_message())

            print("\n","Now slots value in Source Link is ",tracker.slots['dataset_name'])

            ls_entity =tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and  tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_ = tracker.slots['dataset_name']

                # calling global dictionary
                global master_dic_dataset_name

                # if dataset name that is extracted from user message is present in our data we got from json file
                if dataset_name_ in master_dic_dataset_name.keys():
        
                    dataset_name_ = master_dic_dataset_name[dataset_name_]


                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in source link {extracted_ls_entity}")


                dict_of_mapped_data_with_id = {}
                with urllib.request.urlopen("https://indiadataportal.com/meta_data_info") as url:
                    data = json.loads(url.read().decode())
                    temp_data  = json.dumps(data, indent=4, sort_keys=True)
                    temp_data = json.loads(temp_data)
                    for i in range(len(temp_data)):
                        data = temp_data[i]
                        # print(f"{data['dataset_name']} ---- > {data['dataset_id']} " )
                        dict_of_mapped_data_with_id[data['dataset_name']] = data['dataset_id']

                    # if extracted dataset name is present in our data we got from json file
                    if dataset_name_ in dict_of_mapped_data_with_id.keys():
                        
                        # extract id for that dataset name
                        extracted_id = dict_of_mapped_data_with_id[dataset_name_]

                        for i in range(len(temp_data)):
                                data = temp_data[i]
                                if data['dataset_id']==extracted_id:
                                    p = json.dumps(data)
                                    p = json.loads(p)
                        

                        if len(extracted_ls_entity) >=1:
                            # iterating through all entites other than dataset_name
                            for entity_iter in extracted_ls_entity:
                                print("yes i am in Source Link")
                                # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                # spellcheck the entity

                                
                                if entity_iter in p.keys():

                                    # if entity is present in p then print the value of that entity
                                    # print(f"{entity_iter} ----> {p[entity_iter]}")
                                    dispatcher.utter_message(text = f"{entity_iter} is {p[entity_iter]}")
                                
                                else:
                                    dispatcher.utter_message(text = 'Sorry but can you pls tell again  what feature you are looking for')
                                    dispatcher.utter_message(text = """Ex :Like if you want to know Source Link for a Dataset 
                                                                        say it like :- What was the source for the dataset""")
                        
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to know Source Link for a Dataset 
                                                                        say it like :- What was the source for the dataset""")
            else:
                dispatcher.utter_message(text = "Can you tell which dataset it is")
