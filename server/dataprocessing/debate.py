import json
import pandas as pd
with open("/home/meng/dataset/debate/meng/users.json") as user_file:
    user_data_json = json.load(user_file)
with open("/home/meng/dataset/debate/meng/debates.json") as debate_file:
    debate_data_json = json.load(debate_file)

user_data = pd.DataFrame.from_dict(user_data_json)
debates_data = pd.DataFrame.from_dict(debates_data_json)
print(user_data.head())