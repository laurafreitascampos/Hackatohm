import streamlit as st
import pandas as pd
# import requests
# from arcgis.gis import GIS

# Configuração da Página (DEVE SER O 1º COMANDO)
st.set_page_config(
    page_title="PIRA - Plataforma de Riscos CBMMG",
    page_icon="🔥",
    layout="wide"
)

# Dicionário de Unidades Operacionais
UNIDADES_OPERACIONAIS = {
    "Selecione uma unidade...": None,
    "1º BBM - Belo Horizonte": "BH",
    "2º BBM - Contagem": "Contagem",
    "3º BBM - Belo Horizonte": "BH_3",
    "4º BBM - Juiz de Fora": "JuizDeFora",
    "5º BBM - Uberlândia": "Uberlandia",
    "6º BBM - Gov. Valadares": "GovValadares",
    "7º BBM - Montes Claros": "MontesClaros",
    "8º BBM - Uberaba": "Uberaba",
    "9º BBM - Varginha": "Varginha",
    "10º BBM - Divinópolis": "Divinopolis",
    "11º BBM - Ipatinga": "Ipatinga",
    "12º BBM - Patos de Minas": "PatosDeMinas",
    "BOA - Belo Horizonte": "BOA_BH",
    "BEMAD - Belo Horizonte": "BEMAD_BH",
    "1ª CIA IND - Poços de Caldas": "PocosDeCaldas",
    "2ª CIA IND - Barbacena": "Barbacena",
    "5ª CIA IND - Sete Lagoas": "SeteLagoas",
    "6ª CIA IND - Diamantina": "Diamantina",
    "7ª CIA IND - Pouso Alegre": "PousoAlegre"
}

# --- Barra Lateral (Filtros) ---
st.sidebar.title("Filtros de Articulação")
unidade_selecionada = st.sidebar.selectbox(
    "Selecione a Unidade Operacional:",
    list(UNIDADES_OPERACIONAIS.keys())
)

# --- Página Principal ---
st.title("🔥 PIRA - Plataforma Integrada de Riscos e Alertas")
st.caption("Uso interno do Corpo de Bombeiros Militar de Minas Gerais (CBMMG)")

# --- Lógica Principal da Página ---
if unidade_selecionada != "Selecione uma unidade...":

    regiao_id = UNIDADES_OPERACIONAIS[unidade_selecionada]

    st.header(f"Situação de Risco para: {unidade_selecionada}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Risco (Lógica Fuzzy)")
        st.metric(label="Nível de Risco", value="Calculando...") 
    with col2:
        st.subheader("Dados (APIs)")
        st.metric(label="Chuva Acumulada (24h)", value="-- mm")
    with col3:
        st.subheader("Dados (Sensores IoT)")
        st.metric(label="Umidade do Solo (Local)", value="-- %")

    st.subheader("Mapa de Risco")
    # Exemplo simples de mapa
    if regiao_id == "JuizDeFora":
        df_mapa = pd.DataFrame({'lat': [-21.7646], 'lon': [-43.3496]})
        st.map(df_mapa, zoom=10)
    else:
        st.map(pd.DataFrame({'lat': [-19.9167], 'lon': [-43.9333]}), zoom=7)

else:
    st.info("Por favor, selecione uma Unidade Operacional na barra lateral esquerda para começar.")