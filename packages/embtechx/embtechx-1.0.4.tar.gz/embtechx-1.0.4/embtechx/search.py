from sentence_transformers import SentenceTransformer
from IPython.display import display

from sklearn.neighbors import NearestNeighbors

from .embedding import emb_train
sentence_embedding = emb_train.sentence_embedding

def find_related_sentences(dataframe, model_path):
    model = SentenceTransformer(model_path)

    sentence = input("Enter a keyword: ")
    vector = model.encode(sentence)
    
    if "Embedding vector" not in dataframe.columns:           
        dataframe_v = dataframe.copy()
        dataframe_v = sentence_embedding(dataframe_v, model_path)
        embedding_vector = dataframe_v["Embedding vector"].tolist()
    else:
        dataframe_v = dataframe.copy()
        embedding_vector = dataframe_v["Embedding vector"].tolist()
    
    knn_model = NearestNeighbors(n_neighbors=len(dataframe_v))
    knn_model.fit(embedding_vector)

    distances, indices = knn_model.kneighbors([vector])

    result = dataframe_v.iloc[indices[0]].copy()
    result["Distance"] = distances[0]

    result_df = result.loc[:, ["Text", "Domain", "Embedding vector", "Distance"]]
    result_df = result_df[result_df["Distance"] <= 1]

    display(result_df)

    if len(result_df) == 0:
        exit()
    else: 
        print()
        cont_or_no = input("Would you like to add more keywords? (yes/no): ")
        if cont_or_no == "y" or cont_or_no == "Y" or cont_or_no == "yes" or cont_or_no == "Yes" or cont_or_no == "YES":
            find_related_sentences(result_df)
        elif cont_or_no == "n" or cont_or_no == "N" or cont_or_no == "no" or cont_or_no == "No" or cont_or_no == "NO":
            return result_df
        else:
            exit()