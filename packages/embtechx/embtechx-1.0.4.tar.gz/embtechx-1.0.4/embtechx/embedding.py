from sentence_transformers import SentenceTransformer, InputExample, losses
from sentence_transformers.evaluation import TripletEvaluator
from torch.utils.data import DataLoader

import time
import pandas as pd
from langdetect import *

from .dataframe import emb_dataframe
concat_df = emb_dataframe.concat_df

model_en = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
model_th = SentenceTransformer("mrp/simcse-model-m-bert-thai-cased")

class emb_train:
    def detect_df_language(dataframe):
        df = dataframe.copy()
        sentences = df["Text"].tolist()
        languages = []
        for i in range(len(sentences)):
            try:
                detected_language = detect(sentences[i])
                languages.append(detected_language)
            except:
                continue

        count = {i: languages.count(i) for i in languages}
        lang_dict = {key:val for key, val in count.items()}
        lang_list = list(lang_dict)
        top_lang = lang_list[0]
        return top_lang

    def sentence_embedding(dataframe, model_path):
        embedding_model = SentenceTransformer(model_path)
        df_with_vectors = dataframe.copy()
        sentence_list = df_with_vectors["Text"].tolist()
        embedding_vectors = embedding_model.encode(sentence_list)
        vectors_list = embedding_vectors.tolist()
        df_with_vectors["Embedding vector"] = vectors_list
        return df_with_vectors

    def create_test_train(dataframe_domain, dataframe_misc):
        domain = dataframe_domain.copy()
        misc = dataframe_misc.copy()
        
        # split dataframe_domain into anchor, positive, and test (domain)
        total_rows = len(domain.index)
        train_rows = int(total_rows*0.4)

        anc = domain[0:train_rows] # 40%
        pos = domain[train_rows:(2*train_rows)] # 40%
        test_domain = domain[(2*train_rows):] # 20%

        # create neg and test (misc) from dataframe_misc
        neg = misc[0:train_rows]
        test_misc = misc[train_rows:(train_rows + len(test_domain))]

        train_list = [anc, pos, neg]
        train = concat_df(train_list)

        test_list = [test_domain, test_misc]
        test = concat_df(test_list)
        return test, train

    # train the model (only)
    def train_model_only(dataframe, file_path):
        # detect the language of the dataframe
        detected_language = emb_train.detect_df_language(dataframe)
        if detected_language == ("th"):
            model = model_th
            print("Model: mrp/simcse-model-m-bert-thai-cased")
        else:
            model = model_en
            print("Model: sentence-transformers/all-MiniLM-L6-v2")

        file_path_before = file_path + "/before"
        file_path_after = file_path + "/after"

        model.save(file_path_before)

        split_at = int(len(dataframe)/3)
        anc = dataframe[0:split_at]
        pos = dataframe[split_at:(2*split_at)]
        neg = dataframe[(2*split_at):]

        anchor = anc["Text"].tolist()
        positive = pos["Text"].tolist()
        negative = neg["Text"].tolist()

        triplet_dict = {"Anchor": anchor,
                        "Positive": positive,
                        "Negative": negative}

        triplet_df = pd.DataFrame(triplet_dict)
        
        train_examples = []
        for i in range(len(triplet_df)):
            train_examples.append(InputExample(texts = triplet_df.iloc[i].tolist()))
        
        train_batch_size = 32
        num_epochs = 30
        eval_steps = 100
        warmup_steps_n = int(len(triplet_df) * num_epochs * 0.1)

        train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=train_batch_size)
        train_loss = losses.TripletLoss(model=model)

        triplet_evaluator = TripletEvaluator.from_input_examples(train_examples)

        start_time = time.time()

        model.fit(train_objectives=[(train_dataloader, train_loss)], evaluator=triplet_evaluator, epochs=num_epochs, \
                evaluation_steps=eval_steps, warmup_steps=warmup_steps_n, \
                callback=lambda score, epoch, steps: print(f"Score: {score}, Epoch: {epoch}, Step: {steps}"))

        model.evaluate(triplet_evaluator, output_path=file_path)
        model.save(file_path_after)
        
        time_taken = time.time()-start_time
        print()
        if (time_taken/3600) >= 1:
            time_taken_hr = time_taken/3600
            print("Time taken:", round(time_taken_hr, 5), "hours")
        else:
            time_taken_min = time_taken/60
            print("Time taken:", round(time_taken_min, 5), "minutes")

    def train_model__only_customize(dataframe, file_path):
        model_id = input("Enter the sentence-transformers model id: ")
        model = SentenceTransformer(model_id)

        file_path_before = file_path + "/before"
        file_path_after = file_path + "/after"

        model.save(file_path_before)

        split_at = int(len(dataframe)/3)
        anc = dataframe[0:split_at]
        pos = dataframe[split_at:(2*split_at)]
        neg = dataframe[(2*split_at):]

        anchor = anc["Text"].tolist()
        positive = pos["Text"].tolist()
        negative = neg["Text"].tolist()
        
        triplet_dict = {"Anchor": anchor,
                        "Positive": positive,
                        "Negative": negative}

        triplet_df = pd.DataFrame(triplet_dict)
        
        train_examples = []
        for i in range(len(triplet_df)):
            train_examples.append(InputExample(texts = triplet_df.iloc[i].tolist()))
        
        train_batch_size = int(input("Enter a batch size: "))
        num_epochs = int(input("Enter an epoch size: "))

        eval_steps = 100
        warmup_steps_n = int(len(dataframe) * num_epochs * 0.1)

        train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=train_batch_size)
        train_loss = losses.TripletLoss(model=model)

        triplet_evaluator = TripletEvaluator.from_input_examples(train_examples)

        start_time = time.time()

        model.fit(train_objectives=[(train_dataloader, train_loss)], evaluator=triplet_evaluator, epochs=num_epochs, \
                evaluation_steps=eval_steps, warmup_steps=warmup_steps_n, \
                callback=lambda score, epoch, steps: print(f"Score: {score}, Epoch: {epoch}, Step: {steps}"))

        model.evaluate(triplet_evaluator, output_path=file_path)
        model.save(file_path_after)
        
        time_taken = time.time()-start_time
        print()
        if (time_taken/3600) >= 1:
            time_taken_hr = time_taken/3600
            print("Time taken:", round(time_taken_hr, 5), "hours")
        else:
            time_taken_min = time_taken/60
            print("Time taken:", round(time_taken_min, 5), "minutes")

    # split dataframes and train the model
    def train_model(dataframe_domain, dataframe_misc):
        test, train = emb_train.create_test_train(dataframe_domain, dataframe_misc)
        file_path = input("Enter a file path to store embedding models: ")
        emb_train.train_model_only(train, file_path)
        return test, train, file_path
    
    def train_model_customize(dataframe_domain, dataframe_misc):
        test, train = emb_train.create_test_train(dataframe_domain, dataframe_misc)
        file_path = input("Enter a file path to store embedding models: ")
        emb_train.train_model__only_customize(train, file_path)
        return test, train, file_path