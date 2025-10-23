import streamlit as st
import pandas as pd
# -----------------------------------------------------------------
# IMPORTANDO SEUS ARQUIVOS LOCAIS (os "módulos")
import aquisicaodedados
import fuzzy
# -----------------------------------------------------------------
# (Você pode importar o 'folium' aqui quando for usar o mapa)
# import folium
# from streamlit_folium import st_folium

# Configuração da Página
st.set_page_config(
    page_title="PIRA - Plataforma de Riscos CBMMG",
    page_icon="🔥",
    layout="wide"
)

# Dicionário de Unidades Operacionais (pode ficar aqui)
UNIDADES_OPERACIONAIS = {
    "Selecione uma unidade...": None,
    "1º BBM - Belo Horizonte": "BH",
    "4º BBM - Juiz de Fora": "JuizDeFora",
    # (etc... adicione todos os outros)
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

    # --- 1. CHAMAR O MÓDULO DE DADOS ---
    # Usamos um 'spinner' para mostrar que está carregando
    with st.spinner(f"Buscando dados para {regiao_id}..."):
        dados_atuais = aquisicaodedados.get_all_data(regiao_id)
    
    # --- 2. CHAMAR O MÓDULO FUZZY ---
    # Passamos os dados coletados para a lógica fuzzy
    risco_final_str, risco_final_num = fuzzy.calcular_risco_deslizamento(dados_atuais)

    # --- 3. EXIBIR OS RESULTADOS ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Risco (Lógica Fuzzy)")
        # Mostra o resultado final do fuzzy
        if risco_final_str == "Crítico":
            st.error(f"NÍVEL DE RISCO: {risco_final_str}")
        elif risco_final_str == "Alto":
            st.warning(f"NÍVEL DE RISCO: {risco_final_str}")
        else:
            st.success(f"NÍVEL DE RISCO: {risco_final_str}")
        
    with col2:
        st.subheader("Dados (APIs)")
        # Mostra os dados brutos que vieram das APIs
        st.metric(label="Chuva Acumulada (24h)", value=f"{dados_atuais['chuva']} mm")
    
    with col3:
        st.subheader("Dados (Sensores IoT)")
        # Mostra os dados brutos que vieram do IoT
        st.metric(label="Umidade do Solo (Local)", value=f"{dados_atuais['umidade_solo']} %")

    st.subheader("Mapa de Risco")
    # (TODO: Substituir o st.map pelo st_folium com as camadas do ArcGIS/Folium)
    st.map(pd.DataFrame({'lat': [-19.9167], 'lon': [-43.9333]}), zoom=7)

else:
    st.info("Por favor, selecione uma Unidade Operacional na barra lateral esquerda para começar.")
    