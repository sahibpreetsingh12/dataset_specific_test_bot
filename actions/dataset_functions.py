# from typing import Any, Text, Dict, List
# import urllib.request, json
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.events import SlotSet

# def dataset_name_fun(dispatcher,tracker,ls_entity ,dataset_name,
#                 temp_dataset_name):
#     print("\n","Now slots value is ",tracker.slots['dataset_name'])  
#     extracted_ls_entity = []
#     for i in range(len(ls_entity)):
#         extracted_ls_entity.append(ls_entity[i]['entity'])
#     extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
#     print(f"Entites we extracted {extracted_ls_entity}")




#     # if dataset_name in master_dic_dataset_name.keys():
#     #     dataset_name = master_dic_dataset_name[dataset_name]

#     dictionary_data_name_in_db = {}
#     with urllib.request.urlopen("https://indiadataportal.com/meta_data_info") as url:
#         data = json.loads(url.read().decode())
#         temp_data  = json.dumps(data, indent=4, sort_keys=True)
#         temp_data = json.loads(temp_data)
#         for i in range(len(temp_data)):
#             data = temp_data[i]
#             # print(f"{data['dataset_name']} ---- > {data['id']} " )
#             dictionary_data_name_in_db[data['dataset_name']] = data['id']

#         # if extracted dataset name is present in our data we got from json file
#         if dataset_name in dictionary_data_name_in_db.keys():
            
#             # extract id for that dataset name
#             extracted_id = dictionary_data_name_in_db[dataset_name]

#             for i in range(len(temp_data)):
#                     data = temp_data[i]
#                     if data['id']==extracted_id:
#                         p = json.dumps(data)
#                         p = json.loads(p)
#                         # print(p,'\n')
            

#             if len(extracted_ls_entity) >=1:
#                 # iterating through all entites other than dataset_name
#                 for entity_iter in extracted_ls_entity:

#                     # check if entity present in extracted_ls_entity is also present in p ( data in db)
#                     # spellcheck the entity
#                     if entity_iter in p.keys():
#                         # if entity is present in p then print the value of that entity
#                         print(f"{entity_iter} ----> {p[entity_iter]}")
#                         dispatcher.utter_message(text = f"{entity_iter} is {p[entity_iter]}")
                    
#                     else:
#                         dispatcher.utter_message(text = 'Sorry but can you pls say it again')
            
#             else:
#                 dispatcher.utter_message(text = f'Yes you can start with {temp_dataset_name}')

# Configuration for Rasa NLU.
# https://rasa.com/docs/rasa/nlu/components/

