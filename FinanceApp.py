
import streamlit as st  # Streamlit ist das Framework für Web-Apps in Python
import requests         # Damit werden HTTP-Anfragen an APIs gesendet
import pandas as pd     # Die Library Pandas wird importiert für die Datenverarbeitung
import plotly.express as px  # Diese Bibliothek wird verwendet für interaktive Graphen
from streamlit_option_menu import option_menu  # Mit dieser Bibliothek kann ein Menü in der Seitenleiste eingefügt werden
import numpy as np      # Numpy hilft uns mit Zahlen und Arrays zu erstellen
from io import BytesIO # BytesIO ermöglicht uns das Arbeiten mit binären Daten
import yfinance as yf # mit Yahoo können Finanzdaten bezogen bzw. abgerufen werden
from sklearn.preprocessing import PolynomialFeatures # Dient zur Erzeugung von zusätzlichen Merkmalen für polynomielle Regressionen
from sklearn.linear_model import LinearRegression # wird importiert um lineare Regressionsanalysen durchzuführen
from streamlit_autorefresh import st_autorefresh # Wird importiert um die Seite "News" alle 60 Sekunden neu zu laden
from sklearn.model_selection import train_test_split # train_test_split hilft dabei, die Daten in Trainings- und Testdaten zu unterteilen
import matplotlib.pyplot as plt # matplotlib wird für die Visualisierung (Plotten) verwendet
from datetime import datetime # datetime wird benötigt, um mit Datumswerten zu arbeiten


# Persönliche API-Schlüssel für den Zugang zu den Finanzdaten von den Datenanbieter
API_KEY_TWELVEDATA = "fa6409603f0f4d2d9413c1b0a01b68ed"
API_KEY_FMP = "g8o3R38ppGAobko7Iq3TFPCgQy6JjpyZ"
API_KEY_FINNHUB = "cvt9u2pr01qhup0v5oa0cvt9u2pr01qhup0v5oag"

st.set_page_config(page_title="The CapWise App", layout="wide")

with st.sidebar: # Erstellen des Navigationsmenüs in der linken Seitenleiste
    selected = option_menu(
        menu_title="Navigation",  # Titel des Menüs
        options=["Overview", "Risk Profile", "Recommendation", "Obligationen Search", "Stock Search", "News"],  # Menüoptionen
        icons=["house", "bar-chart", "lightbulb", "search", "graph-up", "newspaper"],  # Symbole neben den Optionen
        menu_icon="cast",  # Icon oben links
        default_index=0  # Die erste Seite ("Overview") wird standardmäßig angezeigt
    )
if selected == "Overview": # Erste Seite: Übersicht
    st.title("The CapWise App")
    st.write("Willkommen zur CapWise App! Die App hilft dir dabei dein Risikprofil zu bestimmen und dein Geld richtig anzulegen.")
if selected == "Risk Profile":# Zweite Seite: Hier werden Fragen aufgelistet, um das optimale Risikprofil zu ermitteln
    st.title("Risk Profile")
    st.write("Hier wird dein Risikoprofil anhand einiger Fragen bestimmt.")
    age = st.slider("Wie alt bist du?", min_value=18, max_value=100, step=1)# Frage 1: Alter des Nutzers abfragen, extra erst ab dem Altersjahr von 18 Jahren möglich
    invest_horizon = st.number_input("Wie viele Jahre möchtest du anlegen?", min_value=1, step=1) # Frage 2: Anlagehorizont: Zahlenfeld, in dem die Anzahl Jahre der Investition bestimmt werden
    risk_behavior = st.slider("Wie risikofreudig bist du?", min_value=0, max_value=100, step=1, 
                              help="0 = konservativ, 100 = aggressiv")# Frage 3: Persönliche Risikobereitschaft (zwischen 0 und 100), wird bestimmt mit Slider
    st.write("Wie würdest du reagieren, wenn der Aktienkurs fällt?")   # Frage 4: Reaktion bei Kursverlusten, hier wird nachfolgend ein Graph aufgezeigt
    st.write("Beispiel: der Kurs sinkt um 20 %")

    # Visualisierung eines fallenden Aktienkurses, um dem Nutzer ein Gefühl für Verluste zu geben, der aktualisiert sich jedesmal aufs neue
    dates = pd.date_range(start="2023-01-01", periods=100)
    start_price = 110
    end_price = start_price * 0.8  # 20 % Verlust
    negativ_trend = np.linspace(start_price, end_price, 100)
    random_var = np.random.normal(loc=0, scale=2, size=100)
    stock_prices = negativ_trend + random_var # Preis mit Trend  Schwankungen berechnen
    df = pd.DataFrame({"Date": dates, "Price": stock_prices})
    df.set_index("Date", inplace=True)
    fig = px.line(df, x=df.index, y="Price", title="Fallender Aktienkurs")
    st.plotly_chart(fig)

    #hier dann die Frage 4, wie sich die Person fühlt, bei so einem Kursrückgang
    loss_feeling = st.radio("Wie fühlst du dich bei finanziellen Verlusten?", 
                            options=["Kaum berührt", "Waren mir unangenehm", "Unangenehm und Befürchtung alles zu verlieren", "Keine Aussage trifft zu"])

    # Frage 5: Wie viel Geld möchte man investieren?
    invest_amount = st.selectbox("Wie hoch ist dein Anlagebetrag?", 
                                     options=["0-10 Tausend", "10-50 Tausend", "100-500 Tausend", ">500 Tausend"])

    # Klassifizierung des Nutzers in einen Anlagetyp, abhängig von seinen Antworten, aber nur wenige Kombinationen. Es gäbe natürlich X verschieden Kombinationen, welche man kombinieren könnte um eine exaktes Anlageprofil zu bestimmen
    if invest_horizon <= 5 and risk_behavior <= 30 and loss_feeling == "Unangenehm und Befürchtung alles zu verlieren" and invest_amount == "0-10 Tausend":
        asset_class = "Einkommen"
    elif invest_horizon <= 5 and risk_behavior <= 50 and loss_feeling in ["Unangenehm und Befürchtung alles zu verlieren", "Waren mir unangenehm"]:
        asset_class = "Defensiv"
    elif invest_horizon <= 10 and risk_behavior <= 50 and loss_feeling in ["Waren mir unangenehm", "Kaum berührt"] and invest_amount in ["10-50 Tausend", "100-500 Tausend"]:
        asset_class = "Konservativ"
    elif invest_horizon >= 10 and risk_behavior <= 70 and loss_feeling in ["Kaum berührt", "Waren mir unangenehm"]:
        asset_class = "Ausgewogen"
    elif invest_horizon >= 15 and risk_behavior >= 70 and loss_feeling == "Kaum berührt" and invest_amount == ">500 Tausend":
        asset_class = "Aktien"
    elif invest_horizon >= 10 and risk_behavior >= 60 and loss_feeling in ["Kaum berührt", "Waren mir unangenehm"]:
        asset_class = "Wachstum"
    else:
        asset_class = "Ausgewogen"  # Standardtyp, wenn keine eindeutige Kategorie passt

    # Zeichnen der Risiko-Rendite-Kurve mit Markierung des entsprechenden Nutzerprofils
    x_risiko = np.linspace(0, 100, 6)
    y_return = [1, 2.5, 4, 6.5, 9, 12]
    Vermögens_Klassen = ["Einkommen", "Defensiv", "Konservativ", "Ausgewogen", "Wachstum", "Aktien"]
    Vermögens_Positionen = {x: (x_risiko[i], y_return[i]) for i, x in enumerate(Vermögens_Klassen)}

    figure_risiko_return = px.line(x=x_risiko, y=y_return, labels={"x": "Risiko", "y": "Rendite"}, title="Risikoprofil und Anlagetypen")
    for item in Vermögens_Klassen:
        x_pos, y_pos = Vermögens_Positionen[item]
        figure_risiko_return.add_scatter(x=[x_pos], y=[y_pos], mode="markers+text", text=[item], textposition="top center", marker=dict(size=8, color="blue"))

    selected_x, selected_y = Vermögens_Positionen[asset_class]
    figure_risiko_return.add_scatter(x=[selected_x], y=[selected_y], mode="markers+text", 
                                textposition="top center", marker=dict(size=12, color="red", line=dict(width=2, color="black")))

    st.plotly_chart(figure_risiko_return)
    st.write(f"**Basierend auf deinen Antworten ist dein Anlagetyp:** {asset_class}")
    st.session_state["Anlagetyp"] = asset_class
    
elif selected == "Recommendation":# Dritte Seite: Empfehlungen je nach Profil
    st.title("Investment Recommendation")
    st.write("Empfohlene Portfolio-Zusammensetzung basierend auf deinem Profil.")

    asset_class = st.session_state.get("Anlagetyp", "Unbekannt")
    st.write(f"Dein ermittelter Anlagetyp: **{asset_class}**")
    recommendations = {    # Definition der empfohlenen Verteilung je nach Anlagetyp
        "Einkommen": {"Aktien": 0.0, "Obligationen": 0.9, "Cash": 0.1},
        "Defensiv": {"Aktien": 0.25, "Obligationen": 0.75, "Cash": 0.1},
        "Konservativ": {"Aktien": 0.35, "Obligationen": 0.55, "Cash": 0.1},
        "Ausgewogen": {"Aktien": 0.55, "Obligationen": 0.35, "Cash": 0.1},
        "Wachstum": {"Aktien": 0.75, "Obligationen": 0.15, "Cash": 0.1},
        "Aktien": {"Aktien": 0.9, "Obligationen": 0.0, "Cash": 0.1}
    }

    if Vermögens_Klassen in recommendations:
        dist = recommendations[asset_class]
        df_dist = pd.DataFrame.from_dict(dist, orient='index', columns=['Anteil']).reset_index().rename(columns={"index": "Assetklasse"})
        fig_rec = px.pie(df_dist, names='Assetklasse', values='Anteil', title='Empfohlene Portfolio-Zusammensetzung')
        st.plotly_chart(fig_rec)
    
    st.info("Hinweis: Diese Empfehlung ist generisch und ersetzt keine individuelle Anlageberatung.")

elif selected == "Obligationen Search":  # Vierte Seite: Obligationen anzeigen, eine Datenbank erstellt mittels Excel, aktuelle Obligationen Daten wurden von der Webpage von Six (https://www.six-group.com/de/market-data/bonds/bond-explorer.html) heruntergeladen und als Datenbank in das Projekt implementiert. 
    st.title("Obligationen Search")
    st.write("Aktuelle Obligationen auf dem Markt. Die Daten werden von SIX zur Verfügung gestellt.")


    try:
    
        excel_url = "https://raw.githubusercontent.com/KellyReynard/CS-project/main/Anleihen_Daten.xlsx"
        response = requests.get(excel_url)
        response.raise_for_status()
        df_bonds = pd.read_excel(BytesIO(response.content), engine="openpyxl")
        if df_bonds["MaturityDate"].dtype in [int, float]:
            df_bonds["MaturityDate"] = pd.to_datetime(df_bonds["MaturityDate"].astype(int).astype(str), format="%Y%m%d")
        st.dataframe(df_bonds)

    except Exception as e:
        st.error(f"Fehler beim Laden der Datei: {e}") #wurde von ChatGPT empfohlen, falls der Code nicht funktioniert bzw. die Datei nicht geladen werden kann, dass dies so angegeben wird


    
elif selected == "Stock Search":  # Fünfte Seite: Aktien suchen und Kursverlauf anzeigen
    st.title("Stock Search")

    API_KEY_FINNHUB = "cvt9u2pr01qhup0v5oa0cvt9u2pr01qhup0v5oag"

    ticker = st.text_input("Gib das Aktien-Ticker-Symbol ein (z.B. AAPL, IBM):")
    selected_period = st.selectbox(
        "Wähle den Zeitraum:",
        options=["7 Tage", "1 Monat", "3 Monate", "6 Monate", "1 Jahr"],
        index=1
    )

    period_to_outputsize = {
        "7 Tage": 7,
        "1 Monat": 30,
        "3 Monate": 90,
        "6 Monate": 180,
        "1 Jahr": 365
    }
    outputsize = period_to_outputsize[selected_period]

    if ticker:
        try:
            # Kursdaten von TwelveData
            url_price = (
                f"https://api.twelvedata.com/time_series?"
                f"symbol={ticker}&interval=1day&outputsize={outputsize}&apikey={API_KEY_TWELVEDATA}"
            )
            response_price = requests.get(url_price)
            data_price = response_price.json()

            if "values" in data_price:
                df_price = pd.DataFrame(data_price["values"])
                df_price["datetime"] = pd.to_datetime(df_price["datetime"])
                df_price.set_index("datetime", inplace=True)
                df_price = df_price.astype(float)
                df_price.sort_index(inplace=True)

                fig_price = px.line(
                    df_price,
                    x=df_price.index,
                    y="close",
                    title=f"{ticker} Aktienkurs über {selected_period}"
                )
                st.plotly_chart(fig_price)
            else:
                st.error("Keine Daten für das eingegebene Ticker-Symbol gefunden.") #wurde von ChatGPT empfohlen, falls für den eingegeben Ticker keine Daten abgerufen werden können von der API

            # Analystenempfehlungen
            st.subheader("Analystenempfehlungen")
            url_finnhub = f"https://finnhub.io/api/v1/stock/recommendation?symbol={ticker}&token={API_KEY_FINNHUB}"
            response_finnhub = requests.get(url_finnhub)
            data_finnhub = response_finnhub.json()

            if isinstance(data_finnhub, list) and len(data_finnhub) > 0:
                df_finnhub = pd.DataFrame(data_finnhub)
                df_finnhub["period"] = pd.to_datetime(df_finnhub["period"])
                df_finnhub = df_finnhub.sort_values("period", ascending=False)


                st.write("Die neuesten Empfehlungen respektive Analysteneinschätzungen zu dieser Aktie")
                st.write(f"🟢 Buy: {df_finnhub.iloc[0]['buy']}")
                st.write(f"🟡 Hold: {df_finnhub.iloc[0]['hold']}")
                st.write(f"🔴 Sell: {df_finnhub.iloc[0]['sell']}")

                
            else:
                st.info("Keine Analystendaten gefunden.") #wurde von ChatGPT empfohlen, falls keine Analystenempfehlugen für die eingegeben Aktien von der API abgerufen werden können

                        
            # Der Titel der Web-App wird hier festgelegt
            st.title("Aktienkurs-Vorhersage mit Linearer Regression")
            
            # Benutzer kann hier den Ticker der Aktie eingeben (z.B. UBS für UBS, NESN.SW für Nestle)
            ticker = st.text_input("Gib einen Aktien-Ticker ein (z.B. UBS, NESN.SW, ZURN.SW)", "NESN.SW")
            
            # Daten von Yahoo Finance herunterladen. Wir wählen den Zeitraum von 2015 bis Mai 2025
            start_date = "2015-01-01"  # Beginn des Zeitraums
            end_date = "2025-05-01"    # Ende des Zeitraums
            data = yf.download(ticker, start=start_date, end=end_date)
            
            # Prüfen, ob Daten für den angegebenen Ticker gefunden wurden
            if data.empty:
                # Wenn keine Daten gefunden wurden, wird eine Fehlermeldung angezeigt
                st.error(f"Keine Daten für das Ticker-Symbol '{ticker}' gefunden. Bitte überprüfe den Ticker.")
            else:
                # Um die Daten in ein besser lesbares Format zu bringen, fügen wir eine neue Spalte mit dem Datum hinzu
                data["Date"] = data.index
                # Um das Datum als numerischen Wert zu verwenden, wandeln wir es in eine Ordinalzahl um. (Dies wurde mit Hilfe von ChatPGT herausgefunden)
                data["Date_ordinal"] = pd.to_datetime(data["Date"]).map(pd.Timestamp.toordinal)
            
                # X ist die Eingabe für die Grafik: Das ist die "Date_ordinal"-Spalte, die die Zeit darstellt
                X = data[["Date_ordinal"]]
                # y ist das Ziel, also die "Close"-Preise, also der Schlusskurs der Aktie
                y = data["Close"]
            
                # Wir teilen die Daten in Trainingsdaten (80%) und Testdaten (20%) auf. (Dies wurde mit Hilfe von ChatPGT herausgefunden)
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
                
                # Ein lineares Regressionsmodell wird erstellt, um die Vorhersage durchzuführen
                model = LinearRegression()
                # Das Modell wird mit den Trainingsdaten trainiert
                model.fit(X_train, y_train)
            
                # Wir nutzen das Modell, um Vorhersagen für den gesamten Zeitraum zu treffen  (Dies wurde mit Hilfe von ChatPGT herausgefunden)
                data["Prediction"] = model.predict(X)
            
                # Visualisierung: Erstellen eines Diagramms (Plot)
                fig, ax = plt.subplots(figsize=(10, 6))  # Die Größe des Plots ist 10x6 Zoll
                # Echte Aktienkurse werden im Diagramm angezeigt
                ax.plot(data["Date"], y, label="Echte Kurse")
                # Die Vorhersagen des Modells werden ebenfalls angezeigt (mit gestrichelter Linie)
                ax.plot(data["Date"], data["Prediction"], label="Vorhergesagt", linestyle="--")
                # Achsenbeschriftungen hinzufügen
                ax.set_xlabel("Datum")
                ax.set_ylabel("Kurs")
                # Titel des Diagramms
                ax.set_title(f"Aktienkurs Vorhersage für {ticker} (2020-2025)")
                # Legende anzeigen, um die Linien im Diagramm zu erklären
                ax.legend()
            
                # Setze die Achsenlimits, um den Zeitraum von 2020 bis 2025 anzuzeigen
                ax.set_xlim([data["Date"].iloc[0], data["Date"].iloc[-1]])
            
                # Das Diagramm wird in der Web-App angezeigt
                st.pyplot(fig)
            
                # Prognose für ein zukünftiges Datum, z.B. 31. Dezember 2025
                future_date = datetime(2025, 12, 31)  # Das zukünftige Datum, das wir vorhersagen wollen
                # Um das Datum als numerischen Wert (Ordinalzahl) zu bekommen, konvertieren wir es
                future_ordinal = pd.Timestamp(future_date).toordinal()
            
                # Das Modell wird verwendet, um die Vorhersage für dieses zukünftige Datum zu berechnen (Dies wurde mit Hilfe von ChatPGT herausgefunden)
                future_prediction_array = model.predict([[future_ordinal]])
                # Wir extrahieren die Vorhersage als Fließkommazahl
                future_prediction = float(future_prediction_array[0])
            
                # Die prognostizierten Aktienkurse für das zukünftige Datum werden angezeigt
                st.subheader("Prognose")
                st.write(f"Der vorhergesagte Kurs für {ticker} am {future_date.strftime('%d.%m.%Y')} beträgt **{future_prediction:.2f} USD**.")


elif selected == "News":
    try:
        st.title("Börsennachrichten – Echtzeit")
        st.caption("Die Seite aktualisiert sich automatisch alle 60 Sekunden.")
        st_autorefresh(interval=60 * 1000, key="news_refresh")

        symbol = st.text_input("📈 Gib ein Ticker-Symbol ein (z.B. AAPL, TSLA, IBM):")

        def get_news(ticker_symbol):
            try:
                ticker = yf.Ticker(ticker_symbol)
                news_items = ticker.news
                news_parsed = []

                for item in news_items:
                    if "title" in item and "provider" in item and "link" in item:
                        news_parsed.append({
                            "Titel": item.get("title", "Unbekannt"),
                            "Quelle": item.get("provider", {}).get("displayName", "Unbekannt"),
                            "Veröffentlicht am": item.get("providerPublishTime", "Unbekannt"),
                            "Link": item.get("link", "#")
                        })

                return news_parsed
            except Exception as e:
                st.error(f"Fehler beim Abrufen der Nachrichten: {e}")
                return []

        if symbol:
            news_data = get_news(symbol)

            if not news_data:
                st.warning(f"⚠️ Keine Nachrichten für `{symbol}` gefunden. Zeige allgemeine Marktnachrichten.")
                news_data = get_news("^GSPC")

            if news_data:
                df_news = pd.DataFrame(news_data)
                df_news["Veröffentlicht am"] = pd.to_datetime(df_news["Veröffentlicht am"], unit="s", errors="coerce")
                df_news["Link"] = df_news["Link"].apply(lambda url: f'<a href="{url}" target="_blank">Öffnen</a>')

                st.markdown("### Aktuelle Nachrichten:")
                st.write(df_news.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.info("Keine aktuellen Nachrichten verfügbar.")
        else:
            st.info("Bitte gib ein Ticker-Symbol ein, um Nachrichten zu sehen.")

    except Exception as e:
        st.error(f"Fehler beim Laden der Nachrichten-Seite: {e}")
