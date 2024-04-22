import pandas as pd

from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

import seaborn
import matplotlib.pyplot as plt

from .embedding import emb_train
embedding = emb_train.sentence_embedding

class eval_model:
    # for SVM, kNN and Naive Bayes
    def create_eval_df(dataframe):
        eval_df = dataframe.loc[:, ["Embedding vector", "Domain", "Text"]]
        domain_list = eval_df["Domain"].tolist()

        # domain = 1, misc = 0
        domain_num = []
        for j in range(len(dataframe)):
            d_number = 0
            if domain_list[j] != "Miscellaneous":
                d_number = 1
            else: d_number = 0
            domain_num.append(d_number)
        eval_df["Domain_num"] = domain_num
        return eval_df

    def accuracy_svm(test, train):
        if ("Embedding vector" not in test.columns) and ("Embedding vector" not in train.columns):
            model_path = input("Enter the file path of the model you want to evaluate for accuracy: ")

            test_df = test.copy()
            train_df = train.copy()

            test_df = embedding(test_df, model_path)
            train_df = embedding(train_df, model_path)
            
            test_df = eval_model.create_eval_df(test_df)
            train_df = eval_model.create_eval_df(train_df)
            
        else:
            test_df = test.copy()
            train_df = train.copy()
           
            test_df = eval_model.create_eval_df(test_df)
            train_df = eval_model.create_eval_df(train_df)

        vectors_test = test_df["Embedding vector"].tolist()
        domain_in_test = test_df["Domain_num"].tolist()

        vectors_train = train_df["Embedding vector"].tolist()
        domain_in_train = train_df["Domain_num"].tolist()

        svm_model = svm.SVC()
        svm_model.fit(vectors_train, domain_in_train)
        predict_domain = svm_model.predict(vectors_test)
        accuracy = accuracy_score(domain_in_test, predict_domain)
        
        test_df["Predicted_num_SVM"] = predict_domain

        accuracy_percent = accuracy*100
        print("Accuracy (SVM):", round(accuracy_percent, 5), "%")
        return test_df

    def accuracy_knn(test, train):
        if ("Embedding vector" not in test.columns) and ("Embedding vector" not in train.columns):
            model_path = input("Enter the file path of the model you want to evaluate for accuracy: ")

            test_df = test.copy()
            train_df = train.copy()

            test_df = embedding(test_df, model_path)
            train_df = embedding(train_df, model_path)
            
            test_df = eval_model.create_eval_df(test_df)
            train_df = eval_model.create_eval_df(train_df)
            
        else:
            test_df = test.copy()
            train_df = train.copy()
           
            test_df = eval_model.create_eval_df(test_df)
            train_df = eval_model.create_eval_df(train_df)

        vectors_test = test_df["Embedding vector"].tolist()
        domain_in_test = test_df["Domain_num"].tolist()

        vectors_train = train_df["Embedding vector"].tolist()
        domain_in_train = train_df["Domain_num"].tolist()

        knn_model = KNeighborsClassifier(n_neighbors=5)
        knn_model.fit(vectors_train, domain_in_train)
        predict_domain = knn_model.predict(vectors_test)
        accuracy = accuracy_score(domain_in_test, predict_domain)

        test_df["Predicted_num_kNN"] = predict_domain

        accuracy_percent = accuracy*100
        print("Accuracy (kNN):", round(accuracy_percent, 5), "%")
        return test_df

    def accuracy_naive_bayes(test, train):
        if ("Embedding vector" not in test.columns) and ("Embedding vector" not in train.columns):
            model_path = input("Enter the file path of the model you want to evaluate for accuracy: ")

            test_df = test.copy()
            train_df = train.copy()

            test_df = embedding(test_df, model_path)
            train_df = embedding(train_df, model_path)
            
            test_df = eval_model.create_eval_df(test_df)
            train_df = eval_model.create_eval_df(train_df)
            
        else:
            test_df = test.copy()
            train_df = train.copy()
           
            test_df = eval_model.create_eval_df(test_df)
            train_df = eval_model.create_eval_df(train_df)

        vectors_test = test_df["Embedding vector"].tolist()
        domain_in_test = test_df["Domain_num"].tolist()

        vectors_train = train_df["Embedding vector"].tolist()
        domain_in_train = train_df["Domain_num"].tolist()

        naive_bayes_model = GaussianNB()
        naive_bayes_model.fit(vectors_train, domain_in_train)
        predict_domain = naive_bayes_model.predict(vectors_test)
        accuracy = accuracy_score(domain_in_test, predict_domain)

        test_df["Predicted_num_NB"] = predict_domain

        accuracy_percent = accuracy*100
        print("Accuracy (Naive Bayes):", round(accuracy_percent, 5), "%")
        return test_df

    # SVM, kNN and Naive Bayes
    def evaluate(test, train):
        if ("Embedding vector" not in test.columns) and ("Embedding vector" not in train.columns):
            model_path = input("Enter the file path of the model you want to evaluate for accuracy: ")

            test_df = test.copy()
            train_df = train.copy()

            test_df = embedding(test_df, model_path)
            train_df = embedding(train_df, model_path)
            
            eval_model.accuracy_svm(test_df, train_df)
            eval_model.accuracy_knn(test_df, train_df)
            eval_model.accuracy_naive_bayes(test_df, train_df)
            
        else:
            test_df = test.copy()
            train_df = train.copy()
            
            eval_model.accuracy_svm(test_df, train_df)
            eval_model.accuracy_knn(test_df, train_df)
            eval_model.accuracy_naive_bayes(test_df, train_df)
                        
    # for dimensional reduction techniques (PCA, t-SNE)
    def create_vector_df(dataframe):
        header = []
        pick_a_vector = dataframe.at[0, "Embedding vector"]
        find_range = len(pick_a_vector)

        for i in range(find_range):
            header.append(i)

        test_em_list = dataframe["Embedding vector"].tolist()

        vector_df = pd.DataFrame(test_em_list, columns=header)
        return vector_df
    
    def evaluate_pca(dataframe):
        df = dataframe.copy()
        if "Embedding vector" not in df.columns:
            model_path = input("Enter the file path of the model you want to use: ")
            df = embedding(df, model_path)

        vector_df = eval_model.create_vector_df(df)

        PCA_dimensions = PCA(n_components = 2)
        PCA_fit = PCA_dimensions.fit_transform(vector_df)
        PCA_df = pd.DataFrame(PCA_fit)
        PCA_df["Domain"] = dataframe["Domain"]

        eval_df = eval_model.create_eval_df(df)

        PCA_df["Text"] = eval_df["Text"]
        PCA_df = PCA_df.rename(columns={0: "x_axis", 1: "y_axis"})
        PCA_df["Embedding vector"] = PCA_df.loc[:, ["x_axis", "y_axis"]].values.tolist()

        seaborn.scatterplot(data=PCA_df, x="x_axis", y="y_axis", hue="Domain").set(title="PCA")
        plt.show()
 
    def evaluate_tsne(dataframe):
        df = dataframe.copy()
        if "Embedding vector" not in df.columns:
            model_path = input("Enter the file path of the model you want to use: ")
            df = embedding(df, model_path)

        vector_df = eval_model.create_vector_df(df)

        tsne_dimensions = TSNE(n_components=2)
        TSNE_fit = tsne_dimensions.fit_transform(vector_df)
        TSNE_df = pd.DataFrame(TSNE_fit)
        TSNE_df["Domain"] = dataframe["Domain"]

        eval_df = eval_model.create_eval_df(df)

        TSNE_df["Text"] = eval_df["Text"]
        TSNE_df = TSNE_df.rename(columns={0: "x_axis", 1: "y_axis"})
        TSNE_df["Embedding vector"] = TSNE_df.loc[:, ["x_axis", "y_axis"]].values.tolist()
 
        seaborn.scatterplot(data=TSNE_df, x="x_axis", y="y_axis", hue="Domain").set(title="t-SNE")
        plt.show()