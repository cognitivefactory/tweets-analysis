import flet as ft
import database
import pandas as pd

def main(page: ft.Page):
    print(f"client {page.client_ip} connected")
    page.title = "FORDISME"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = "#054547"
    txt_tweet = ft.Text(
        value="Tweet : ",
        size=30,
        color="#FFFFFF"
    )
    txt_id = ft.Text(
        value = "id : , topics : []",
        size = 20,
        italic=True,
        color="#A0A0A0"
    )
    current_tweet = (-1, "CLIQUE SUR CHARGER UN AUTRE TWEET OMG", ["violence","énervement"])
    def load_tweet(tweet=None):
        nonlocal current_tweet
        if tweet is None:
            print(f"fetching for {page.client_ip}...")
            id,text,topic = database.get_tweet()
            print(f"  fetched : {id=}, {topic=}")
        else:
            id,text,topic = tweet
        txt_tweet.value = f"{text}"
        txt_id.value = f"id : {id}\ntopic : {topic}"
        current_tweet = [id, text, topic]
        page.update()
    load_tweet(tweet=current_tweet)

    def change_tweet(evt):
        tmp = current_tweet
        load_tweet()
        database.restore_unlabeled(tmp)
    but_charger = ft.ElevatedButton(
        content=ft.Text("Charger un\nautre tweet",size=30),
        on_click=change_tweet
    )

    def send(value):
        if current_tweet[0] != -1:
            database.add_labeled(*current_tweet, value, ip=page.client_ip)
            load_tweet()

    but_positif = ft.ElevatedButton(
        content=ft.Text("\nPositif !\n",size=30),
        bgcolor="#00FF00",
        on_click=lambda evt: send(1)
    )
    but_negatif = ft.ElevatedButton(
        content=ft.Text("\nNegatif !\n",size=30),
        bgcolor="#FF0000",
        on_click=lambda evt: send(-1)
    )
    but_neutre = ft.ElevatedButton(
        content=ft.Text("On sait pas\n(tweet cassé, ...)",size=30),
        bgcolor="#A0A0A0",
        on_click=lambda evt: send(0)
    )

    page.add(
        txt_tweet,
        txt_id,
        ft.Row([
            but_positif,
            but_negatif
        ]),
        but_neutre,
        but_charger
    )

    def handle_disconnect(evt):
        print(f"client {page.client_ip} disconnected")
        if current_tweet[0] != -1:
            database.restore_unlabeled(current_tweet)

        # current_tweet = [-1, "text", ["topic"]]
    def handle_connect(evt):
        print(f"client {page.client_ip} re-connected")
        load_tweet((-1, "CLIQUE SUR CHARGER UN AUTRE TWEET OMG", ["violence","énervement"]))
    page.on_disconnect = handle_disconnect
    page.on_connect = handle_connect

ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8000)