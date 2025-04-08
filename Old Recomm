import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Empfehlung", layout="wide")

st.title("💡 Anlageempfehlung")

# Sicherstellen, dass ein Risikoprofil vorhanden ist
if "asset_class" not in st.session_state:
    st.warning("Bitte zuerst das Risikoprofil auf der Seite 'Risk Profile' ausfüllen.")
    st.stop()

# Empfohlenes Profil laden
asset_class = st.session_state["asset_class"]

# Beispielhafte Empfehlungen pro Anlagetyp
recommendations = {
    "Einkommen": {
        "description": "Konservativer Ansatz mit Fokus auf Kapitalerhalt. Ideal für Anleger mit geringer Risikobereitschaft.",
        "allocation": {"Obligationen": 70, "Geldmarkt": 20, "Aktien": 10}
    },
    "Defensiv": {
        "description": "Defensive Strategie mit Fokus auf Stabilität und begrenztem Wachstum.",
        "allocation": {"Obligationen": 60, "Geldmarkt": 15, "Aktien": 25}
    },
    "Konservativ": {
        "description": "Geringes bis moderates Risiko mit ausgewogener Diversifikation.",
        "allocation": {"Obligationen": 50, "Aktien": 40, "Alternative Anlagen": 10}
    },
    "Ausgewogen": {
        "description": "Balance zwischen Risiko und Rendite. Mittel- bis langfristiger Anlagehorizont.",
        "allocation": {"Aktien": 50, "Obligationen": 30, "Immobilienfonds": 20}
    },
    "Wachstum": {
        "description": "Höhere Renditechancen mit erhöhter Volatilität. Für langfristige Anleger.",
        "allocation": {"Aktien": 70, "Alternative Anlagen": 20, "Obligationen": 10}
    },
    "Aktien": {
        "description": "Stark wachstumsorientiert. Fokus auf Aktien mit hoher Volatilität.",
        "allocation": {"Aktien": 90, "Krypto/Alternativen": 10}
    }
}

data = recommendations.get(asset_class, {})
if not data:
    st.error("Es konnte keine Empfehlung geladen werden.")
    st.stop()

st.subheader(f"Dein Anlagetyp: {asset_class}")
st.write(data["description"])

# Kuchendiagramm zur Visualisierung der Asset Allocation
allocation_df = px.data.tips()  # Dummy ersetzen
labels = list(data["allocation"].keys())
values = list(data["allocation"].values())

fig = px.pie(
    names=labels,
    values=values,
    title="Empfohlene Portfolioaufteilung",
    hole=0.4
)
st.plotly_chart(fig)

st.info("Hinweis: Diese Empfehlung ist generisch und ersetzt keine individuelle Anlageberatung.")
