import streamlit as st
import pandas as pd

st.set_page_config(page_title="Kalkulačka uhlíkové stopy", layout="wide")

st.title("🌍 Kalkulačka uhlíkové stopy firmy")
st.write("Jednoduchý prototyp pro výpočet emisí Scope 1 a Scope 2.")

st.sidebar.header("Nastavení")
firma = st.sidebar.text_input("Název firmy")
rok = st.sidebar.number_input("Rok", min_value=2020, max_value=2035, value=2025)

st.header("1. Energie")

elektrina = st.number_input("Spotřeba elektřiny (kWh)", min_value=0.0)
zemni_plyn = st.number_input("Spotřeba zemního plynu (m³)", min_value=0.0)
teplo = st.number_input("Odběr tepla (GJ)", min_value=0.0)

st.header("2. Pohonné hmoty")

benzin = st.number_input("Benzin (litry)", min_value=0.0)
nafta = st.number_input("Nafta (litry)", min_value=0.0)

# Emisní faktory – zjednodušené pracovní hodnoty
EF = {
    "Elektřina": 0.38,      # kg CO2e / kWh
    "Zemní plyn": 2.02,    # kg CO2e / m3
    "Teplo": 56.0,         # kg CO2e / GJ
    "Benzin": 2.31,        # kg CO2e / litr
    "Nafta": 2.68          # kg CO2e / litr
}

vysledky = {
    "Elektřina": elektrina * EF["Elektřina"],
    "Zemní plyn": zemni_plyn * EF["Zemní plyn"],
    "Teplo": teplo * EF["Teplo"],
    "Benzin": benzin * EF["Benzin"],
    "Nafta": nafta * EF["Nafta"]
}

df = pd.DataFrame({
    "Kategorie": vysledky.keys(),
    "Emise kg CO₂e": vysledky.values()
})

df["Emise t CO₂e"] = df["Emise kg CO₂e"] / 1000

celkem = df["Emise t CO₂e"].sum()

st.header("Výsledky")

st.metric("Celková uhlíková stopa", f"{celkem:.2f} t CO₂e")

st.dataframe(df)

st.bar_chart(df.set_index("Kategorie")["Emise t CO₂e"])

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Stáhnout výsledky jako CSV",
    data=csv,
    file_name=f"uhlikova_stopa_{firma}_{rok}.csv",
    mime="text/csv"
)
