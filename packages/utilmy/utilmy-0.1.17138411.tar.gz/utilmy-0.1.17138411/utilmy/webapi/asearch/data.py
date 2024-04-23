

from utilmy import pd_to_file, pd_read_file



def converter_text_to_parquet(dirin:str, dirout:str):
    """
    Custom per text data : Yaki job
    https://www.kaggle.com/datasets/kotartemiy/topic-labeled-news-dataset
    title  :   text
    body   :    text
    cat1   :    string   fiction / sport /  politics
    cat2   :    string     important / no-important
    cat3   :    string
    cat4   :    string
    cat5   :    string
    dt_ymd :    int     20240311

    d0="ztmp/news*.zip"
    df = pd_read_file(d0, sep=";")

    df.columns =['cat3', 'cat2', 'title', 'dt_ymd', 'body', 'cat1']

    df = df[ ['title', 'body', 'cat1', 'cat2', 'cat3', 'dt_ymd' ] ]

    pd_to_file(df.sample(1000), d0 + "/df_1k.parquet")


    """


    pd_to_file(df, dirout + "df.parquet")

   
""" 




"""