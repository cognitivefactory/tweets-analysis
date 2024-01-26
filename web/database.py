import pandas as pd
import fcntl
from dotenv import load_dotenv
load_dotenv()
import os
import code

db_labeled_path = os.getenv("PATH_LABELED_TWEETS")
db_unlabeled_path = os.getenv("PATH_UNLABELED_TWEETS")

if os.path.isfile(db_labeled_path):
    df_labeled = pd.read_csv(db_labeled_path)
else:
    df_labeled = pd.DataFrame(columns=["id","sentiment","text","topic","ip"])
    df_labeled.to_csv(db_labeled_path)

if os.path.isfile(db_unlabeled_path):
    df_unlabeled = pd.read_csv(db_unlabeled_path)
else:
    df_unlabeled = pd.read_pickle(os.getenv("PATH_TWEETS"))
    df_unlabeled.to_csv(db_unlabeled_path)

def get_tweet():
    """
    renvois un tuple (id, text, topics)
    """
    # tweet = df_labeled[["id","text","topic"]].pop()
    # return (-1, "text", ["topic"])
    return pop_unlabeled()

def pop_unlabeled():
    """
    renvois le premier tweet non labelisé et le pop
    """
    global df_labeled, df_unlabeled
    tweet = (-1, "Y A EU UN BUG SORRY", ["tristesse"])
    with open(db_unlabeled_path, "w") as file:
        fcntl.flock(file, fcntl.LOCK_EX)
        tweet = tuple(df_unlabeled[["id","text","topic"]].iloc[0])
        df_unlabeled = df_unlabeled.iloc[1:]
        df_unlabeled.to_csv(file)
        fcntl.flock(file, fcntl.LOCK_UN)
    return tweet

def restore_unlabeled(tweet):
    """
    rajoute le tweet dans la bdd non labelisée
    survient lorsqu'un tweet avait été envoyé à un utilisateur et que 
    celui-ci a quitté la page
    """
    global df_labeled, df_unlabeled
    if tweet[0] == -1:
        return
    print(f"restoring tweet : {tweet[0], tweet[2]}")
    with open(db_unlabeled_path, "w") as file:
        fcntl.flock(file, fcntl.LOCK_EX)
        tweet = {
                "id": tweet[0],
                "text": tweet[1],
                "topic": tweet[2]
        }
        df_unlabeled = pd.concat([
            pd.DataFrame(tweet, index=[0]),
            df_unlabeled
        ],
        ignore_index=True)
        df_unlabeled.to_csv(file)
        fcntl.flock(file, fcntl.LOCK_UN)


def add_labeled(id,text,topic,sentiment,ip="0.0.0.0"):
    global df_labeled, df_unlabeled
    with open(db_labeled_path, "w") as file:
        fcntl.flock(file, fcntl.LOCK_EX)
        df_labeled = pd.concat([
            df_labeled,
            pd.DataFrame({
                    "id": id,
                    "sentiment": sentiment,
                    "text": text,
                    "topic": topic,
                    "ip": ip
                },
                index=[0]
            )
        ],
        ignore_index=True)
        df_labeled.to_csv(file)
        fcntl.flock(file, fcntl.LOCK_UN)

