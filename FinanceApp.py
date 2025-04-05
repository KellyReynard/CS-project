import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import numpy as np

# API Keys (Hole dir einen eigenen API Key!)
API_KEY_TWELVEDATA = "fa6409603f0f4d2d9413c1b0a01b68ed"
API_KEY_FMP = "g8o3R38ppGAobko7Iq3TFPCgQy6JjpyZ"  # Ersetze mit deinem echten API Key

# Seiten-Konfiguration
st.set_page_config(page_title="The Finance App", layout="wide")

# Seiten-Navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Overview", "Risk Profile", "Recommendation", "Obligationen Search", "Stock Search"],
        icons=["house", "bar-chart", "lightbulb", "search", "line-chart"],
        menu_icon="cast",
        default_index=0
    )

# Übersicht-Seite
if selected == "Overview":
    st.title("The Finance App - Overview")
    st.write("Willkommen zur Finance App! Hier findest du verschiedene Tools und Analysen für deine Investment-Strategie.")

# Risk Profile
if selected == "Risk Profile":
    st.title("Risk Profile")
    st.write("Wir ermitteln jetzt deine Risikobereitschaft sowie Risikofähigkeit durch verschiedene Fragen. Bitte beantworte die folgenden Fragen:")

    # 1. Frage: Alter
    age = st.slider("Wie alt bist du?", min_value=18, max_value=100, step=1)

    # 2. Frage: Anlagehorizont
    investment_horizon = st.number_input("Wie viele Jahre möchtest du anlegen?", min_value=1, step=1)

    # 3. Frage: Risikoverhalten (Slider zwischen konservativ und aggressiv)
    risk_behavior = st.slider("Wie risikofreudig bist du?", min_value=0, max_value=100, step=1, 
                              help="0 = konservativ, 100 = aggressiv")

    # 4. Frage: Verhalten bei fallenden Aktienkursen
    st.write("Wie würdest du reagieren, wenn der Aktienkurs fällt?")
    st.write("Stell dir vor, der Aktienkurs fällt um 30%. Schau dir den Graphen unten an.")

    # Beispiel für schwankenden, fallenden Aktienkurs
    dates = pd.date_range(start="2023-01-01", periods=100)
    prices = 100 - np.cumsum(np.random.randn(100) * 2)  # Schwankender Kurs
    df = pd.DataFrame({"Date": dates, "Price": prices})
    df.set_index("Date", inplace=True)

    fig = px.line(df, x=df.index, y="Price", title="Schwankender Fallender Aktienkurs")
    st.plotly_chart(fig)

    # 5. Frage: Gefühl bei finanziellen Verlusten
    loss_feeling = st.radio("Wie fühlst du dich bei finanziellen Verlusten?", 
                            options=["Kaum berührt", "Waren mir unangenehm", "Unangenehm und Befürchtung alles zu verlieren", "Keine Aussage trifft zu"])

    # 6. Frage: Anlagebetrag
    investment_amount = st.selectbox("Wie hoch ist dein Anlagebetrag?", 
                                    options=["0-10 Tausend", "10-50 Tausend", "100-500 Tausend", ">500 Tausend"])

    # Bestimmung des Anlagetypen anhand der Antworten
    if investment_horizon <= 5 and risk_behavior <= 30 and loss_feeling == "Unangenehm und Befürchtung alles zu verlieren" and investment_amount == "0-10 Tausend":
        asset_class = "Einkommen"
    elif investment_horizon <= 5 and risk_behavior <= 50 and loss_feeling in ["Unangenehm und Befürchtung alles zu verlieren", "Waren mir unangenehm"]:
        asset_class = "Defensiv"
    elif investment_horizon <= 10 and risk_behavior <= 50 and loss_feeling in ["Waren mir unangenehm", "Kaum berührt"] and investment_amount in ["10-50 Tausend", "100-500 Tausend"]:
        asset_class = "Konservativ"
    elif investment_horizon >= 10 and risk_behavior <= 70 and loss_feeling in ["Kaum berührt", "Waren mir unangenehm"]:
        asset_class = "Ausgewogen"
    elif investment_horizon >= 15 and risk_behavior >= 70 and loss_feeling == "Kaum berührt" and investment_amount == ">500 Tausend":
        asset_class = "Aktien"
    elif investment_horizon >= 10 and risk_behavior >= 60 and loss_feeling in ["Kaum berührt", "Waren mir unangenehm"]:
        asset_class = "Wachstum"
    else:
        asset_class = "Ausgewogen"  # Standardwert

    # Risiko-Rendite-Kurve mit ALLEN Anlagetypen + Markierung des ermittelten Typs
    x_risk = np.linspace(0, 100, 6)  # Risikoskala
    y_return = [1, 2.5, 4, 6.5, 9, 12]  # Renditewerte

    asset_classes = ["Einkommen", "Defensiv", "Konservativ", "Ausgewogen", "Wachstum", "Aktien"]
    asset_positions = {
        "Einkommen": (x_risk[0], y_return[0]),
        "Defensiv": (x_risk[1], y_return[1]),
        "Konservativ": (x_risk[2], y_return[2]),
        "Ausgewogen": (x_risk[3], y_return[3]),
        "Wachstum": (x_risk[4], y_return[4]),
        "Aktien": (x_risk[5], y_return[5])
    }

    fig_risk_return = px.line(x=x_risk, y=y_return, labels={"x": "Risiko", "y": "Rendite"}, 
                              title="Risikoprofil und Anlagetypen")

    for ac in asset_classes:
        x_pos, y_pos = asset_positions[ac]
        fig_risk_return.add_scatter(
            x=[x_pos], y=[y_pos], mode="markers+text",
            text=[ac], textposition="top center",
            marker=dict(size=8, color="blue")
        )

    selected_x, selected_y = asset_positions[asset_class]
    fig_risk_return.add_scatter(
        x=[selected_x], y=[selected_y], mode="markers+text",
        text=[f"➡ {asset_class} ⬅"], textposition="top center",
        marker=dict(size=12, color="red", line=dict(width=2, color="black"))
    )

    st.plotly_chart(fig_risk_return)

    st.write(f"**Basierend auf deinen Antworten ist dein Anlagetyp:** {asset_class}")
    st.session_state["asset_class"] = asset_class

# Recommendation
elif selected == "Recommendation":
    st.title("Investment Recommendation")
    st.write("Individuelle Empfehlungen basierend auf deinem Risikoprofil und Marktanalysen.")

    asset_class = st.session_state.get("asset_class", "Unbekannt")
    st.write(f"Dein ermittelter Anlagetyp: **{asset_class}**")

    recommendations = {
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

# Obligationen Search
elif selected == "Obligationen Search":
    st.title("Obligationen Search")
    st.write("Liste mit aktuell laufenden Obligationen")

    st.subheader("Obligationen Übersicht (Demo-Daten)")
    bond_data = pd.DataFrame({
        "Emittent": ["UBS", "Credit Suisse", "Nestlé"],
        "Laufzeit": ["2029", "2031", "2028"],
        "Zinssatz": [1.5, 2.0, 1.25],
        "Modified Duration": [4.5, 6.2, 3.8]
    })
    st.table(bond_data)

# Stock Search
elif selected == "Stock Search":
    st.title("Stock Search")
    ticker = st.text_input("Gib das Aktien-Ticker-Symbol ein (z.B. AAPL, IBM):")

    if ticker:
        try:
            url_price = f"https://api.twelvedata.com/time_series?symbol={ticker}&interval=1day&outputsize=100&apikey={API_KEY_TWELVEDATA}"
            response_price = requests.get(url_price)
            data_price = response_price.json()

            if "values" in data_price:
                df_price = pd.DataFrame(data_price["values"])
                df_price["datetime"] = pd.to_datetime(df_price["datetime"])
                df_price.set_index("datetime", inplace=True)
                df_price = df_price.astype(float)
                df_price.sort_index(inplace=True)

                fig_price = px.line(df_price, x=df_price.index, y="close", title=f"{ticker} Stock Price Over Time")
                st.plotly_chart(fig_price)
            else:
                st.error("Keine Daten für das eingegebene Ticker-Symbol gefunden.")

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
