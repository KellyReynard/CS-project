
import streamlit as st  # Streamlit ist Framework für Web-Apps in Python
import requests         # Damit kann man HTTP-Anfragen an APIs senden
import pandas as pd     # Für Tabellen und Daten
import plotly.express as px  # Für interaktive Graphen
from streamlit_option_menu import option_menu  # Für ein Menü in der Seitenleiste
import numpy as np      # Numpy hilft mit Zahlen und Arrays

st.set_page_config(page_title="The Finance App", layout="wide")

# Persönliche API-Schlüssel für den Zugang zu den Finanzdaten
API_KEY_TWELVEDATA = "fa6409603f0f4d2d9413c1b0a01b68ed"
API_KEY_FMP = "g8o3R38ppGAobko7Iq3TFPCgQy6JjpyZ"
with st.sidebar: # Erstellen des Navigationsmenüs in der linken Seitenleiste
    selected = option_menu(
        menu_title="Navigation",  # Titel des Menüs
        options=["Overview", "Risk Profile", "Recommendation", "Obligationen Search", "Stock Search"],  # Menüoptionen
        icons=["house", "bar-chart", "lightbulb", "search", "graph-up"],  # Symbole neben den Optionen
        menu_icon="cast",  # Icon oben links
        default_index=0  # Die erste Seite ("Overview") wird standardmäßig angezeigt
    )
if selected == "Overview":# Erste Seite: Übersicht
    st.title("The Finance App - Overview")
    st.write("Willkommen zur Finance App! Hier findest du verschiedene Tools und Analysen für deine Investment-Strategie.")
if selected == "Risk Profile":# Zweite Seite: Risikoprofil bestimmen
    st.title("Risk Profile")
    st.write("Hier wird dein Risikoprofil anhand einiger Fragen bestimmt.")
    age = st.slider("Wie alt bist du?", min_value=18, max_value=100, step=1)# Frage 1: Alter des Nutzers
    invest_horizon = st.number_input("Wie viele Jahre möchtest du anlegen?", min_value=1, step=1) # Frage 2: Anlagehorizont – Wie lange soll das Geld investiert werden?
    risk_behavior = st.slider("Wie risikofreudig bist du?", min_value=0, max_value=100, step=1, 
                              help="0 = konservativ, 100 = aggressiv")# Frage 3: Persönliche Risikobereitschaft (zwischen 0 und 100)
    st.write("Wie würdest du reagieren, wenn der Aktienkurs fällt?")   # Frage 4: Reaktion bei Kursverlusten
    st.write("Beispiel: der Kurs sinkt um 30 %")

    # Visualisierung eines fallenden Aktienkurses, um dem Nutzer ein Gefühl für Verluste zu geben.
    dates = pd.date_range(start="2023-01-01", periods=100)
    start_price = 110
    end_price = start_price * 0.8  # 20 % Verlust
    neg_trend = np.linspace(start_price, end_price, 100)
    noise = np.random.normal(loc=0, scale=2, size=100)
    fake_stock_prices = neg_trend + noise # Preis mit Trend + Schwankung berechnen
    df = pd.DataFrame({"Date": dates, "Price": fake_stock_prices})
    df.set_index("Date", inplace=True)
    fig = px.line(df, x=df.index, y="Price", title="Schwankender Fallender Aktienkurs")
    st.plotly_chart(fig)

    # Frage 5: Emotionale Reaktion auf Verluste
    loss_feeling = st.radio("Wie fühlst du dich bei finanziellen Verlusten?", 
                            options=["Kaum berührt", "Waren mir unangenehm", "Unangenehm und Befürchtung alles zu verlieren", "Keine Aussage trifft zu"])

    # Frage 6: Wie viel Geld möchte man investieren?
    invest_amount = st.selectbox("Wie hoch ist dein Anlagebetrag?", 
                                     options=["0-10 Tausend", "10-50 Tausend", "100-500 Tausend", ">500 Tausend"])

    # Klassifizierung des Nutzers in einen Anlagetyp, abhängig von seinen Antworten
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

    # Zeichnen der Risiko-Rendite-Kurve mit Markierung des Nutzerprofils
    x_risk = np.linspace(0, 100, 6)
    y_return = [1, 2.5, 4, 6.5, 9, 12]
    asset_classes = ["Einkommen", "Defensiv", "Konservativ", "Ausgewogen", "Wachstum", "Aktien"]
    asset_positions = {ac: (x_risk[i], y_return[i]) for i, ac in enumerate(asset_classes)}

    fig_risk_return = px.line(x=x_risk, y=y_return, labels={"x": "Risiko", "y": "Rendite"}, title="Risikoprofil und Anlagetypen")
    for ac in asset_classes:
        x_pos, y_pos = asset_positions[ac]
        fig_risk_return.add_scatter(x=[x_pos], y=[y_pos], mode="markers+text", text=[ac], textposition="top center", marker=dict(size=8, color="blue"))

    selected_x, selected_y = asset_positions[asset_class]
    fig_risk_return.add_scatter(x=[selected_x], y=[selected_y], mode="markers+text", 
                                textposition="top center", marker=dict(size=12, color="red", line=dict(width=2, color="black")))

    st.plotly_chart(fig_risk_return)
    st.write(f"**Basierend auf deinen Antworten ist dein Anlagetyp:** {asset_class}")
    st.session_state["asset_class"] = asset_class
elif selected == "Recommendation":# Dritte Seite: Empfehlungen je nach Profil
    st.title("Investment Recommendation")
    st.write("Empfohlene Portfolio-Zusammensetzung basierend auf deinem Profil.")

    asset_class = st.session_state.get("asset_class", "Unbekannt")
    st.write(f"Dein ermittelter Anlagetyp: **{asset_class}**")
    recommendations = {    # Definition der empfohlenen Verteilung je nach Anlagetyp
        "Einkommen": {"Aktien": 0.0, "Obligationen": 0.9, "Cash": 0.1},
        "Defensiv": {"Aktien": 0.25, "Obligationen": 0.75, "Cash": 0.1},
        "Konservativ": {"Aktien": 0.35, "Obligationen": 0.55, "Cash": 0.1},
        "Ausgewogen": {"Aktien": 0.55, "Obligationen": 0.35, "Cash": 0.1},
        "Wachstum": {"Aktien": 0.75, "Obligationen": 0.15, "Cash": 0.1},
        "Aktien": {"Aktien": 0.9, "Obligationen": 0.0, "Cash": 0.1}
    }

    if asset_class in recommendations:
        dist = recommendations[asset_class]
        df_dist = pd.DataFrame.from_dict(dist, orient='index', columns=['Anteil']).reset_index().rename(columns={"index": "Assetklasse"})
        fig_rec = px.pie(df_dist, names='Assetklasse', values='Anteil', title='Empfohlene Portfolio-Zusammensetzung')
        st.plotly_chart(fig_rec)
elif selected == "Obligationen Search":# Vierte Seite: Obligationen anzeigen
    st.title("Obligationen Search")
    st.write("Hier siehst du einige aktuelle Obligationen (nur Demo-Daten)")

    bond_data = pd.DataFrame({
        "Emittent": ["UBS", "Credit Suisse", "Nestlé"],
        "Laufzeit": ["2029", "2031", "2028"],
        "Zinssatz": [1.5, 2.0, 1.25],
        "Modified Duration": [4.5, 6.2, 3.8]
    })
    st.table(bond_data)
elif selected == "Stock Search": # Fünfte Seite: Aktien suchen und Kursverlauf anzeigen
    st.title("Stock Search")
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
            url_price = (
                f"https://api.twelvedata.com/time_series?"
                f"symbol={ticker}&interval=1day&outputsize={outputsize}&apikey={API_KEY_TWELVEDATA}" #Abruf der Kursdaten von der TwelveData API mit dynamischem Zeitraum
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
                st.error("Keine Daten für das eingegebene Ticker-Symbol gefunden.")
            # Demo-Daten für Analystenempfehlungen anzeigen
            st.subheader(f"(Demo) Analystenempfehlungen für {ticker}")
            analyst_data = pd.DataFrame({
                "Datum": ["2024-03-01", "2024-02-20", "2024-02-10"],
                "Analyst": ["John Smith", "Anna Müller", "Tom Wang"],
                "Bank": ["J.P. Morgan", "Goldman Sachs", "Morgan Stanley"],
                "Empfehlung": ["Buy", "Hold", "Sell"]
            })
            st.table(analyst_data)
        except Exception as e:
            st.error(f"Fehler beim Abrufen der Daten: {e}")
