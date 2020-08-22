import os
import json 
import numpy as np
import pandas as pd
import language_check
tool = language_check.LanguageTool('en-US')



#### data folder configuration
dataset_folder = "/data2/xingbo/chi2021/meng/PersuasiveSpeech/server/dataset/posts/"
new_dataset_folder = "/data2/xingbo/chi2021/meng/PersuasiveSpeech/server/dataset/posts_new/"
concreteness_labeling_path = "/data2/xingbo/chi2021/meng/PersuasiveSpeech/server/dataset/AoA_ratings_Kuperman_et_al_BRM.xlsx"
concreteness_db = pd.read_excel(concreteness_labeling_path)
print(concreteness_db.head())
# print(np.max(concreteness_db["Rating.Mean"]))

concreteness_dict = {}
for index, row in concreteness_db.iterrows():
    concreteness_dict[row["Word"]] = row["Rating.Mean"]/25.0
# print(concreteness_dict)
# exit()

#### sentence eloquence calculation
def find_sentence_errors(texts):
    matches = tool.check(texts)
    # errors
    errors_num = len(matches)
    # correct errors
    correct_texts = language_check.correct(texts, matches)
    
    # print(matches)
    detailed = []
    for m in matches:
        detailed.append({
            "category": m.category,
            "contextoffset": m.contextoffset,
            "errorlength": m.errorlength,
            "message": m.msg,
            "replacements":m.replacements,
        })
        # print(m.contextoffset, m.errorlength, m.category ,m.msg, m.replacements, m.locqualityissuetype)
    
    return [errors_num, correct_texts, detailed]


#### sentence concreteness calculation

def cal_sentence_concreteness(texts):
    words = texts.strip().split()
    concreteness_score = []
    for word in words:
        try:
            concreteness_score.append(concreteness_dict[word])
        except Exception:
            continue
    # print(concreteness_score)
    return round(float(np.mean(concreteness_score)), 4)

def get_data(input_dir, outputdir):
    data_lists = os.listdir(input_dir)
    print(data_lists)
    for data_list in data_lists:
        data_path = os.path.join(input_dir, data_list)
        with open(data_path, "r") as f:
            data = json.load(f)
        data_keys = list(data.keys())
        for data_key in data_keys:
            # title: Dating-16
            reply_infos = data[data_key][0]["reply-info"]

            for rinfoidx, rinfo in enumerate(reply_infos):
                # print(rinfo.keys())
                reply_contents = rinfo["reply_contents"]
                # print(reply_contents)
                for rcontentidx, rcontent in enumerate(reply_contents):
                    ##########################################################
                    # step1: eloquence score calculation
                    cContent = rcontent["content"]
                    errors = find_sentence_errors(cContent)
                    rcontent["elo_info"] = errors
                    rcontent["eloquence"] = errors[0]
                    # if errors[0] > 0:
                    #     rcontent["eloquence"] = errors[0]
                        # print(data[data_key][0]["reply-info"][rinfoidx]["reply_contents"][rcontentidx]["elo_info"])
                    
                    ##########################################################
                    # step2: concreteness score calculation
                    rcontent["concreteness"] = cal_sentence_concreteness(cContent)
                    # print(rcontent["concreteness"] )
        
        # store
        with open(os.path.join(new_dataset_folder, data_list.split(".")[0]+"_new.json"), "w") as f:
            json.dump(data, f, indent = 2)
                    



if __name__ == '__main__':
    get_data(dataset_folder, new_dataset_folder)
