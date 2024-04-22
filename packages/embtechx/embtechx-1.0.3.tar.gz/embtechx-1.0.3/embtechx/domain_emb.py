from .dataframe import emb_dataframe
create_df = emb_dataframe.create_df
create_misc = emb_dataframe.create_misc

from .embedding import emb_train
embedding = emb_train.sentence_embedding
train_model = emb_train.train_model
train_model_customize = emb_train.train_model_customize

from .evaluate import eval_model
evaluate = eval_model.evaluate
evaluate_svm = eval_model.accuracy_svm
evaluate_knn = eval_model.accuracy_knn
evaluate_naive_bayes = eval_model.accuracy_naive_bayes
evaluate_pca = eval_model.evaluate_pca
evaluate_tsne = eval_model.evaluate_tsne

def domain_emb():
    domain_path = input("Enter the file path for a domain dataframe: ")
    domain_name = input("Enter a name of the domain: ")
    domain_dataframe = create_df(domain_name, domain_path)
    misc_path = input("Enter the file path for a miscellaneous dataframe: ")
    domain_misc = create_misc(misc_path)

    test, train, file_path = train_model(domain_dataframe, domain_misc)
    file_path_before = file_path + "/before"
    file_path_after = file_path + "/after"

    train_df = embedding(train, file_path_before)
    test_df_before = embedding(test, file_path_before)
    test_df_after = embedding(test, file_path_after)

    print("Before the training")
    evaluate(test_df_before, train_df)
    evaluate_pca(test_df_before)
    evaluate_tsne(test_df_before)

    print()
    print("After the training")
    evaluate(test_df_after, train_df)
    evaluate_pca(test_df_after)
    evaluate_tsne(test_df_after)

def domain_emb_customize():
    domain_path = input("Enter the file path for a domain dataframe: ")
    domain_name = input("Enter a name of the domain: ")
    domain_dataframe = create_df(domain_name, domain_path)
    misc_path = input("Enter the file path for a miscellaneous dataframe: ")
    domain_misc = create_misc(misc_path)

    test, train, file_path = train_model_customize(domain_dataframe, domain_misc)
    file_path_before = file_path + "/before"
    file_path_after = file_path + "/after"

    train_df = embedding(train, file_path_before)
    test_df_before = embedding(test, file_path_before)
    test_df_after = embedding(test, file_path_after)

    print("Before the training")
    evaluate(test_df_before, train_df)
    evaluate_pca(test_df_before)
    evaluate_tsne(test_df_before)

    print()
    print("After the training")
    evaluate(test_df_after, train_df)
    evaluate_pca(test_df_after)
    evaluate_tsne(test_df_after)