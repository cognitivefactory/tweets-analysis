import plotly.express as px
import plotly.figure_factory as ff
import numpy as np
import pandas as pd

# Suppression de l'affichage des messages d'avertissement
import warnings
warnings.filterwarnings('ignore')

import plotly.io as pio
# pio.renderers.default = "png"
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

def load_df():

    df_scrap : pd.DataFrame = pd.read_pickle("data_recap/bdd_scrapped.pickle")
    df_label : pd.DataFrame = pd.read_csv("data_recap/bdd_labeled.csv")
    df_gen   : pd.DataFrame = pd.read_csv("data_recap/tweets_genere.txt", sep="\t", names=["topic","sentiment","text"])

    # suppression des autres sentiments testé lors de la génération
    df_gen = df_gen[df_gen["sentiment"].isin(["positif","neutre","négatif"])]

    mapping_gen_sentiment = {
        "positif": 1, "neutre": 0, "négatif":-1
    }
    df_gen["sentiment"] = df_gen["sentiment"].apply(lambda x: mapping_gen_sentiment[x])

    df_scrap["topic"] = df_scrap["topic"].transform(tuple)
    df_label["topic"] = df_label["topic"].transform(eval) # pour passer de "['theme','theme2']" à la liste

    return df_scrap, df_label, df_gen

def show_info(df : pd.DataFrame, name = ""):
    print(f"- Nombre de tweets : {len(df)}")

    if "topic" in list(df.columns):
        topics = {}
        for topic in df["topic"]:
            if isinstance(topic, str):
                topics[topic] = topics.get(topic,0) +1
                continue
            for subtopic in topic:
                topics[subtopic] = topics.get(subtopic,0) + 1
        topics = {k: v for k,v in sorted(topics.items(), key = lambda item: item[1], reverse=True)}
        print(f"- Nombre de sujets : {len(topics)}")
        
        n_to_display = 20
        fig = px.histogram(
            title = f"Top {n_to_display} des topics ({name})",
            x = list(topics.keys())[:n_to_display],
            y = list(topics.values())[:n_to_display])
        # fig.update_xaxes(categoryorder="total descending")
        fig.show()

    if "sentiment" in list(df.columns):

        fig = px.histogram(
            title = f"Répartition par sentiments ({name})",
            x = ["Négatif","Neutre","Positif"],
            y = [
                len(df[df["sentiment"] == -1]),
                len(df[df["sentiment"] == 0]),
                len(df[df["sentiment"] == 1])
            ],
            color = ["Négatif","Neutre","Positif"],
            color_discrete_map = {
                "Négatif":"#FF0000", 
                "Neutre":"#A0A0A0", 
                "Positif":"#00FF00"
            },
            labels = {"color":"Sentiment"}
        )
        fig.show()

def show_cm(cm, labels, title="Confusion Matrix"):
    z = cm

    # invert z idx values
    z = z[::-1]

    x = labels
    y =  x[::-1].copy() # invert idx values of x

    # change each element of z to type string for annotations
    z_text = [[str(y) for y in x] for x in z]

    # set up figure 
    fig = ff.create_annotated_heatmap(z, x=x, y=y, annotation_text=z_text, colorscale='Viridis')

    # add title
    fig.update_layout(title_text=title)

    fig.add_annotation(dict(font=dict(color="black",size=14),
                            x=0.5,
                            y=-0.10,
                            showarrow=False,
                            text="Prédiction",
                            xref="paper",
                            yref="paper"))

    # add custom yaxis title
    fig.add_annotation(dict(font=dict(color="black",size=14),
                            x=-0.20,
                            y=0.5,
                            showarrow=False,
                            text="Vérité",
                            textangle=-90,
                            xref="paper",
                            yref="paper"))

    # adjust margins to make room for yaxis title
    fig.update_layout(margin=dict(t=50, l=200))

    # fig.update_layout(xaxis_side="bottom")

    # add colorbar
    # fig['data'][0]['showscale'] = True
    fig.show()

def labeled_eval():
    df : pd.DataFrame = pd.read_pickle("data_recap/bdd_labeled_predi_eval.pkl")
    df_polarized = df[df['sentiment_pred'] != 0]

    print("----- Prédiction de Sentiments avec LLM (twitter-xml-roberta)-----")
    print("1. Positif - Neutre - Négatif")
    print(classification_report(df['sentiment'], df['sentiment_pred']))

    cm = confusion_matrix(df['sentiment'], df['sentiment_pred'], labels=[-1,0,1])
    show_cm(cm, labels=["Négatif","Neutre","Positif"],
            title="Matrice de Confusion sur Sentiments (3 classes)")

    print("2. Positif - Négatif (Neutre ignoré)")
    print(classification_report(df_polarized['sentiment'], df_polarized['sentiment_pred']))

    cm = confusion_matrix(df_polarized['sentiment'], df_polarized['sentiment_pred'], labels=[-1,1])
    show_cm(cm, labels=["Négatif","Positif"],
            title="Matrice de Confusion sur Sentiments (2 classes)")

topics = [
    "Politique",
    "Sport",
    "Cinema",
    "Télévision",
    "Jeux vidéo",
    "Littérature",
    "Santé",
    "Alimentation et cuisine",
    "Mode et beauté",
    "Science",
    "Technologie",
    "Musique",
    "Actualités",
    "Économie",
    "Finance",
    "Entreprise",
    "Emploi",
    "Banque",
    "Service client",
    "Sexe",
    "Violence",
    "Discriminations",
    "Histoire et géographie",
    "Écologie",
    "Nature",
    "Culture",
    "Drogues",
    "Media",
    "Insultes",
]

if __name__ == '__main__':

    #scp rasp:/home/rasp/rasp_website/label/data/labeled.csv .

    import os
    os.system(f"scp rasp:/home/rasp/rasp_website/label/data/labeled.csv data/data_recap")

    df_scrap,df_label,df_gen = load_df()

    labeled_eval()
    # show_info(df_label, name="BDD labelisée")
    # show_info(df_scrap, name="BDD scrapped")