import os
import json
import numpy as np
import pandas as pd
import itertools
from random import sample


# configure dataset folder
dir_path = os.path.dirname(os.path.realpath(__file__))
relationship_folder = os.path.join(dir_path, '../dataset/relationship/')
new_dataset_folder = os.path.join(dir_path, '../dataset/posts_new/')

# load relationship data
itag = 0

def get_support_pairs(arrs):
    pairs = []
    for arrid, arr in enumerate(arrs):
        if len(arrs) >= 2:
            claims = arr[0]
            supports = arr[1:len(arr)]
            for claim in claims:
                for support in supports:
                    pairs.append(set([claim-1, support-1]))
    # pairs
    return pairs

def get_pos_traing_data(pos_pairs, contents):
    training_data = []
    training_labels = []
    for arrid, arr in enumerate(pos_pairs):
        if len(pos_pairs) >= 2:
            claims = arr[0]
            supports = arr[1:len(arr)]
            claim_text = ". ".join([contents[claim-1]["content"] for claim in claims])
            for support in supports:
                try:
                    training_data.append([claim_text, contents[support-1]["content"]])
                    training_labels.append(1)
                except Exception:
                    print(support)
                
    return training_data, training_labels

def get_neg_traing_data(neg_pairs, contents):
    training_data = []
    training_labels = []
    for neg_pair in neg_pairs:
        training_data.append([contents[neg_pair[0]-1]["content"], contents[neg_pair[1]-1]["content"]])
        training_labels.append(0)
    return training_data, training_labels

def generate_training_samples(postdata, relations):
    training_data = []
    training_labels = []
    for k in postdata.keys():
        reply_data = postdata[k][0]["reply-info"]
        # print("data length:",len(reply_data))
        for rid, r in enumerate(reply_data):
            contents = r["reply_contents"]
            contents_len = len(contents)
            sen_ids = list(range(contents_len))
            # --- permutations
            com2 = [set(l) for l in list(itertools.permutations(sen_ids, 2))]
            relation_ids = relations[rid]
            pos_pairs_full = get_support_pairs(relation_ids)
            pos_pairs_num = np.sum([len(p) for p in relation_ids])
            # --- negative pairs
            neg_pairs = [list(pair) for pair in com2 if pair not in pos_pairs_full]
            neg_pairs = sample(neg_pairs, len(neg_pairs))
            if len(neg_pairs) > pos_pairs_num:
                neg_pairs = neg_pairs[:pos_pairs_num]
            # print(neg_pairs)
            # --- generate positive-paired training data
            pos_data, pos_labels = get_pos_traing_data(relation_ids, contents)
            # --- generate negative-paired training data
            neg_data, neg_labels = get_neg_traing_data(neg_pairs, contents)
            # --- organize data
            curr_data = pos_data + neg_data
            curr_labels = pos_labels + neg_labels
            training_data.extend(curr_data)
            training_labels.extend(curr_labels)    

    return training_data, training_labels



def load_relationship_data(inputpath, file_list, dir_list):
    dir_or_files = os.listdir(inputpath)
    for dir_file in dir_or_files:
        dir_file_path = os.path.join(inputpath,dir_file)
        if os.path.isdir(dir_file_path):
            dir_list.append(dir_file_path)
            load_relationship_data(dir_file_path,file_list,dir_list)
        else:
            file_list.append(dir_file_path)
            # print(dir_file_path)
            # filename = dir_file_path.split("/")[-1]
            # if filename.endswith(".json"):
            #     with open(dir_file_path, "r") as f:
            #         relationships = json.load(f)["support_relationship"]
            #     posts_path = os.path.join(new_dataset_folder, filename.split(".")[0]+"_new.json")
            #     print(filename)
            #     with open(posts_path, "r") as f:
            #         posts = json.load(f)
            #     training_data, training_labels = generate_training_samples(posts, relationships)
            #     print(training_data, training_labels)
            #     exit()
    return
file_list = []
dir_list = []
load_relationship_data(relationship_folder, file_list, dir_list)
print(file_list)
print(dir_list)