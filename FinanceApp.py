
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
from datetime import datetime, timedelta # datetime wird benötigt, um mit Datumswerten zu arbeiten
import openpyxl # openpyxl wird benötigt, um Excel-Dateien zu lesen
import feedparser # feedparser wird verwendet, um RSS-Feeds zu parsen

# Persönliche API-Schlüssel für den Zugang zu den Finanzdaten von den Datenanbieter
API_KEY_TWELVEDATA = "fa6409603f0f4d2d9413c1b0a01b68ed"
API_KEY_FMP = "g8o3R38ppGAobko7Iq3TFPCgQy6JjpyZ"
API_KEY_FINNHUB = "cvt9u2pr01qhup0v5oa0cvt9u2pr01qhup0v5oag"

st.set_page_config(page_title="The CapWise App", layout="wide")

with st.sidebar: # Erstellen des Navigationsmenüs in der linken Seitenleiste
    selected = option_menu(
        menu_title="Navigation",  # Titel des Menüs
        options=["Übersicht", "Risikoprofil", "Investitionsempfehlung", "Obligationen Suche", "Aktien Suche", "News"],  # Menüoptionen
        icons=["house", "bar-chart", "lightbulb", "search", "graph-up", "newspaper"],  # Symbole neben den Optionen
        menu_icon="cast",  # Icon oben links
        default_index=0  # Die erste Seite ("Overview") wird standardmäßig angezeigt
    )
if selected == "Übersicht": # Erste Seite: Übersicht
    st.title("The CapWise App")
    st.write("Willkommen zur CapWise App! Die App hilft dir dabei dein Risikprofil zu bestimmen und dein Geld richtig anzulegen.")
    st.video("https://www.youtube.com/watch?v=K9SiRyumlzw") # Hier kannst du den Link zu deinem Video einfügen


    st.markdown("""
    ### 💬 Wer sind wir?

    Wir sind ein Team von Studierenden, das eine moderne, benutzerfreundliche Investment-App entwickelt hat.

    ---

    ### 🎯 Unser Ziel

    Wir wollen es einfacher machen, in die Welt der Investitionen einzusteigen.  
    *Du gibst dein Risikoprofil an, wir geben dir klare Empfehlungen.*

    ---

    ### Was findest du in unserer App?

    - 📊 *Risikoprofilanalyse* – Wir analysieren deine Risikobereitschaft
    - 💡 *Empfohlene Portfolio-Zusammensetzung* – angepasst an dich
    - 🔍 *Obligationenübersicht* – mit Laufzeiten, Zinssätzen und Risiken
    - 📈 *Aktienrecherche mit Prognose* – inklusive Kursverlauf und Machine-Learning-Forecast
    - 📰 *Live-Finanznachrichten* – für jedes Unternehmen, z. B. Apple, Tesla oder UBS

    ---

    Diese Anwendung richtet sich an:
    - Einsteiger
    - Studierende
    - Finanzinteressierte

    """)

if selected == "Risikoprofil":# Zweite Seite: Hier werden Fragen aufgelistet, um das optimale Risikprofil zu ermitteln
    st.title("Risikoprofil")
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

    # Klassifizierung des Nutzers in einen Anlagetyp, abhängig von seinen Antworten, aber nur wenige Kombinationen. Es gäbe natürlich extrem viele verschieden Kombinationen, welche man kombinieren könnte um eine exaktes Anlageprofil zu bestimmen. Wir haben uns aus Komplexitätsgründen dagegen entschieden.
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
    Asset_Klassen = ["Einkommen", "Defensiv", "Konservativ", "Ausgewogen", "Wachstum", "Aktien"]
    Vermögens_Positionen = {x: (x_risiko[i], y_return[i]) for i, x in enumerate(Asset_Klassen)}

    figure_risiko_return = px.line(x=x_risiko, y=y_return, labels={"x": "Risiko", "y": "Rendite"}, title="Risikoprofil und Anlagetypen")
    for item in Asset_Klassen:
        x_pos, y_pos = Vermögens_Positionen[item]
        figure_risiko_return.add_scatter(x=[x_pos], y=[y_pos], mode="markers+text", text=[item], textposition="top center", marker=dict(size=8, color="blue"))

    selected_x, selected_y = Vermögens_Positionen[asset_class]
    figure_risiko_return.add_scatter(x=[selected_x], y=[selected_y], mode="markers+text", 
                                textposition="top center", marker=dict(size=12, color="red", line=dict(width=2, color="black")))

    st.plotly_chart(figure_risiko_return)
    st.write(f"**Basierend auf deinen Antworten ist dein Anlagetyp:** {asset_class}")
    st.session_state["Anlagetyp"] = asset_class
    
elif selected == "Investitionsempfehlung":  # Third page: recommendations by profile
    st.title("Investitionsempfehlung")
    st.write("Empfohlene Portfolio-Zusammensetzung basierend auf deinem Profil.")
    
    Asset_Klassen = ["Einkommen", "Defensiv", "Konservativ", "Ausgewogen", "Wachstum", "Aktien"]
    
    # get the determined profile from session state
    asset_class = st.session_state.get("Anlagetyp", "Unbekannt")
    st.write(f"Die von dir bestimmte Anlageklasse: **{asset_class}**")
    
    # mapping of recommended allocations
    recommendations = {
        "Einkommen":   {"Aktien": 0.0,  "Obligationen": 0.9,  "Cash": 0.1},
        "Defensiv":    {"Aktien": 0.25, "Obligationen": 0.75, "Cash": 0.1},
        "Konservativ": {"Aktien": 0.35, "Obligationen": 0.55, "Cash": 0.1},
        "Ausgewogen":  {"Aktien": 0.55, "Obligationen": 0.35, "Cash": 0.1},
        "Wachstum":    {"Aktien": 0.75, "Obligationen": 0.15, "Cash": 0.1},
        "Aktien":      {"Aktien": 0.9,  "Obligationen": 0.0,  "Cash": 0.1}
    }

    # check the string key, not the list
    if asset_class in recommendations:
        dist = recommendations[asset_class]
        df_dist = (
            pd.DataFrame.from_dict(dist, orient="index", columns=["Anteil"])
              .reset_index()
              .rename(columns={"index": "Assetklasse"})
        )
        fig_rec = px.pie(
            df_dist,
            names="Assetklasse",
            values="Anteil",
            title="Empfohlene Portfolio-Zusammensetzung"
        )
        st.plotly_chart(fig_rec)
    else:
        st.warning("Asset class not found in recommendations. Bitte überprüfe deinen Anlagetyp.")

    st.info("Hinweis: Diese Empfehlung ist generisch und ersetzt keine individuelle Anlageberatung.")

elif selected == "Obligationen Suche":  # Vierte Seite: Obligationen anzeigen, eine Datenbank erstellt mittels Excel, aktuelle Obligationen Daten wurden von der Webpage von Six (https://www.six-group.com/de/market-data/bonds/bond-explorer.html) heruntergeladen und als Datenbank in das Projekt implementiert. 
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
        st.error(f"Fehler beim Laden der Datei: {e}")

    
elif selected == "Aktien Suche":  # Fünfte Seite: Aktien suchen und Kursverlauf anzeigen
    st.title("Stock Search")

    API_KEY_FINNHUB = "cvt9u2pr01qhup0v5oa0cvt9u2pr01qhup0v5oag"

    session = requests.Session()
    session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

    ticker = st.text_input("Gib das Aktien-Ticker-Symbol ein (z.B. AAPL, IBM):")
    selected_period = st.selectbox(
        "Wähle den Zeitraum:",
        options=["1 Tag","7 Tage", "1 Monat", "3 Monate", "6 Monate", "1 Jahr", "2 Jahr", "5 Jahr", "10 Jahr"],
        index=1
    )

    period_to_outputsize = {
        "1 Tag": 1,
        "7 Tage": 7,
        "1 Monat": 30,
        "3 Monate": 90,
        "6 Monate": 180,
        "1 Jahr": 365,
        "2 Jahr": 730,
        "5 Jahr": 1825,
        "10 Jahr": 3650,
        
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

                print(df_price.head())  # Debugging: Ausgabe der ersten Zeilen des DataFrames

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
 
            
            # 1. Check if ticker is empty       
            if df_price.empty:
                st.error(f"Keine Daten für das Ticker-Symbol '{ticker}' gefunden. Bitte überprüfe den Ticker.")
            else:
                            # 1) Download full history
                start_date = "2015-01-01"
                end_date   = datetime.today().strftime("%Y-%m-%d")
                url_price = (
                    f"https://api.twelvedata.com/time_series?"
                    f"symbol={ticker}&interval=1day"
                    f"&start_date={start_date}"
                    f"&end_date={end_date}"
                    f"&apikey={API_KEY_TWELVEDATA}"
                )
                resp = session.get(url_price)
                js  = resp.json()

                if "values" not in js:
                    st.error(f"No data for '{ticker}'.")
                    st.stop()

                df = pd.DataFrame(js["values"])
                df["datetime"] = pd.to_datetime(df["datetime"])
                df.set_index("datetime", inplace=True)
                df = df.astype(float).sort_index()  


                # 2) Prepare regression
                df["Date"] = df.index
                df["Date_ordinal"] = df["Date"].map(pd.Timestamp.toordinal)

                X = df[["Date_ordinal"]]
                y = df["close"]
                if len(df) < 2:
                    st.warning("Not enough points for regression.")
                    st.stop()

                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, shuffle=False
                )
                model = LinearRegression().fit(X_train, y_train)
                df["Prediction"] = model.predict(X)

                # 3) Future dates
                last = df["Date"].max()
                future_dates = pd.date_range(
                    start=last + timedelta(days=1),
                    end= last + pd.DateOffset(years=2),
                    freq="D"
                )
                fut_ord = (
                    future_dates.map(pd.Timestamp.toordinal)
                                .to_numpy().reshape(-1,1)
                )
                future_preds = model.predict(fut_ord)

                # 4) Plot everything with markers
                fig, ax = plt.subplots(figsize=(10,6))
                ax.plot(df["Date"], y, label="Echte Kurse")
                ax.plot(df["Date"], df["Prediction"],
                        linestyle="--",
                        label="In-sample Fit")
                ax.plot(future_dates, future_preds,
                        linestyle="--",
                        label="Forecast (2 Jahre)")
                ax.set_xlabel("Datum")
                ax.set_ylabel("Kurs (USD)")
                ax.set_title(f"Vorhersage für {ticker} bis {future_dates[-1].date()}")
                ax.legend()
                st.pyplot(fig)
        except Exception as e:
            st.error(f"Fehler beim Abrufen der Daten: {e}")     

elif selected == "News":
    
    try:
        st.title("Börsennachrichten – Echtzeit")
        st.caption("Die Seite aktualisiert sich automatisch alle 60 Sekunden.")
        st_autorefresh(interval=60 * 1000, key="news_refresh")

        symbol = st.text_input("Gib ein Ticker-Symbol ein (z.B. AAPL, TSLA, IBM):")

        def get_yf_news(ticker_symbol):
            """Fetch news via yfinance (may be empty)."""
            try:
                ticker = yf.Ticker(ticker_symbol)
                items = ticker.news or []
                parsed = []
                for item in items:
                    if "title" in item and "provider" in item and "link" in item:
                        parsed.append({
                            "Titel": item["title"],
                            "Quelle": item["provider"].get("displayName", "Unbekannt"),
                            "Veröffentlicht am": item.get("providerPublishTime", 0),
                            "Link": item["link"]
                        })
                return parsed
            except Exception as e:
                st.error(f"Fehler beim Abrufen der yfinance-Nachrichten: {e}")
                return []

        def get_google_news(ticker_symbol):
            """Fetch news from Google News RSS as fallback."""
            # build the RSS URL (German edition)
            rss_url = (
                "https://news.google.com/rss/search?"
                f"q={ticker_symbol}%20Aktien&hl=de&gl=DE&ceid=DE:de"
            )
            feed = feedparser.parse(rss_url)  # Feedparser returns entries in date order :contentReference[oaicite:0]{index=0}
            parsed = []
            for entry in feed.entries[:10]:
                parsed.append({
                    "Titel": entry.title,
                    "Quelle": entry.get("source", {}).get("title", "Google News"),
                    "Veröffentlicht am": entry.get("published", ""),
                    "Link": entry.link
                })
            return parsed

        def normalize_and_display(news_list):
            df = pd.DataFrame(news_list)
            # try numeric timestamps first; if that fails, parse strings
            df["Veröffentlicht am"] = pd.to_datetime(
                df["Veröffentlicht am"], 
                unit="s", errors="coerce"
            ).fillna(pd.to_datetime(df["Veröffentlicht am"], errors="coerce"))
            df.sort_values("Veröffentlicht am", ascending=False, inplace=True)
            df = df.head(10)
            df["Link"] = df["Link"].apply(
                lambda url: f'<a href="{url}" target="_blank">Öffnen</a>'
            )
            st.markdown("### Aktuelle Nachrichten:")
            st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)

        if symbol:
            news = get_yf_news(symbol)
            if not news:
                st.info(f"Keine yfinance-News für `{symbol}`—hole Google News RSS als Fallback.")
                news = get_google_news(symbol)

            if news:
                normalize_and_display(news)
            else:
                st.info("Auch über RSS keine Nachrichten verfügbar.")
        else:
            st.info("Bitte gib ein Ticker-Symbol ein, um Nachrichten zu sehen.")

    except Exception as e:
        st.error(f"Fehler beim Laden der Nachrichten-Seite: {e}")
