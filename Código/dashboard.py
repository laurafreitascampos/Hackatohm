import streamlit as st
import pandas as pd
import time
from aquisicaodedados import get_dados_sensores_por_regiao, MAPA_REGIAO_CIDADES
from logica_fuzzy import calcular_risco_deslizamento

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Plataforma de Riscos - CBMMG",
    page_icon="🚨",
    layout="wide"
)

# --- DADOS DE GEOLOCALIZAÇÃO (SIMULADO) ---
COORDENADAS_CIDADES = {
    "Belo Horizonte": {"lat": -19.9245, "lon": -43.9352},
    "Sete Lagoas": {"lat": -19.4665, "lon": -44.2466},
    "Divinópolis": {"lat": -20.1389, "lon": -44.8844},
    "Nova Serrana": {"lat": -19.8758, "lon": -44.9856},
    "Curvelo": {"lat": -18.7561, "lon": -44.4308},
    "Uberlândia": {"lat": -18.9186, "lon": -48.2772},
    "Uberaba": {"lat": -19.7483, "lon": -47.9319},
    "Araguari": {"lat": -18.6472, "lon": -48.1917},
    "Ituiutaba": {"lat": -18.9714, "lon": -49.4658},
    "Patos de Minas": {"lat": -18.5789, "lon": -46.5142},
    "Juiz de Fora": {"lat": -21.7642, "lon": -43.3496},
    "Muriaé": {"lat": -21.1311, "lon": -42.3661},
    "Ubá": {"lat": -21.1219, "lon": -42.9419},
    "Viçosa": {"lat": -20.7541, "lon": -42.8816},
    "Leopoldina": {"lat": -21.5317, "lon": -42.6433},
    "Montes Claros": {"lat": -16.735, "lon": -43.8613},
    "Janaúba": {"lat": -15.8033, "lon": -43.3094},
    "Januária": {"lat": -15.4878, "lon": -44.3639},
    "Salinas": {"lat": -16.1683, "lon": -42.2933},
    "Pirapora": {"lat": -17.3489, "lon": -44.9411},
    "Governador Valadares": {"lat": -18.8519, "lon": -41.9492},
    "Ipatinga": {"lat": -19.4808, "lon": -42.5311},
    "Teófilo Otoni": {"lat": -17.8583, "lon": -41.5053},
    "Coronel Fabriciano": {"lat": -19.5186, "lon": -42.6283},
    "Manhuaçu": {"lat": -20.2581, "lon": -42.0331},
    "Poços de Caldas": {"lat": -21.7878, "lon": -46.5614},
    "Pouso Alegre": {"lat": -22.2303, "lon": -45.935},
    "Varginha": {"lat": -21.5542, "lon": -45.4322},
    "Alfenas": {"lat": -21.425, "lon": -45.9469},
    "Passos": {"lat": -20.7203, "lon": -46.6094}
}

# --- FUNÇÕES AUXILIARES ---
def classificar_risco(score):
    if score < 2:
        return "Muito Baixo", "🟢"
    elif score < 4:
        return "Baixo", "🟡"
    elif score < 7:
        return "Médio", "🟠"
    else:
        return "Alto", "🔴"

def processar_dados_regiao(nome_regiao):
    """Busca dados, calcula o risco e formata para exibição."""
    dados_brutos = get_dados_sensores_por_regiao(nome_regiao)
    lista_resultados = []

    for cidade, sistemas in dados_brutos.items():
        for sistema in sistemas:
            risco_calculado = calcular_risco_deslizamento(
                sistema.get('leitura_pluviometro_mm_h'),
                sistema.get('leitura_umidade_solo_percent'),
                sistema.get('leitura_acelerometro_freq_hz')
            )
            
            classificacao, emoji = classificar_risco(risco_calculado)

            resultado = {
                "Cidade": cidade,
                "Latitude": COORDENADAS_CIDADES.get(cidade, {}).get('lat'),
                "Longitude": COORDENADAS_CIDADES.get(cidade, {}).get('lon'),
                "Risco (0-10)": round(risco_calculado, 2),
                "Classificação": classificacao,
                "Status": emoji,
                "Chuva (mm/h)": sistema.get('leitura_pluviometro_mm_h'),
                "Umidade (%)": sistema.get('leitura_umidade_solo_percent'),
                "Vibração (Hz)": sistema.get('leitura_acelerometro_freq_hz'),
                "ID Sistema": sistema.get('sistema_id')
            }
            lista_resultados.append(resultado)
            
    return pd.DataFrame(lista_resultados)

# --- INTERFACE DO DASHBOARD ---
st.title("🚨 Plataforma Interativa de Riscos - CBMMG")
st.markdown("Alertas de risco de deslizamento em Minas Gerais")

# --- SIDEBAR COM NOVOS FILTROS ---
st.sidebar.header("Filtros de Visualização")

# Seleção de Região - Simplificada
regioes = {
    "Região Central": "regiao_central",
    "Triângulo Mineiro": "triangulo_mineiro", 
    "Zona da Mata": "zona_da_mata",
    "Norte de Minas": "norte_de_minas",
    "Leste de Minas": "leste_de_minas",
    "Sul de Minas": "sul_de_minas"
}

regiao_selecionada = st.sidebar.selectbox(
    "Selecione a Região:",
    options=list(regioes.keys())
)

# Processamento inicial dos dados
regiao_selecionada_key = regioes[regiao_selecionada]
df_riscos = processar_dados_regiao(regiao_selecionada)

# Filtro de Risco - Simplificado
st.sidebar.markdown("---")
niveis_risco = ["Muito Baixo", "Baixo", "Médio", "Alto"]
# Usando session_state para gerenciar o estado dos filtros
if 'niveis_selecionados' not in st.session_state:
    st.session_state.niveis_selecionados = niveis_risco

# Botões de Ação primeiro (antes do multiselect)
col1, col2 = st.sidebar.columns(2)

# Botão de Limpar Filtros
if col1.button("Limpar Filtros"):
    st.session_state.niveis_selecionados = []

# Botão de Atualizar
if col2.button("Atualizar Dados"):
    with st.spinner('Atualizando dados...'):
        time.sleep(1)
    st.sidebar.success("Dados atualizados!")

# Multiselect usando o session_state
niveis_selecionados = st.sidebar.multiselect(
    "Filtrar por Nível de Risco:",
    options=niveis_risco,
    default=st.session_state.niveis_selecionados
)

# Atualiza o session_state com a nova seleção
st.session_state.niveis_selecionados = niveis_selecionados

# Filtragem dos dados
if niveis_selecionados:
    df_filtrado = df_riscos[df_riscos['Classificação'].isin(niveis_selecionados)]
else:
    df_filtrado = df_riscos


# Adiciona informações sobre os filtros ativos
st.sidebar.markdown("---")
st.sidebar.markdown("### Filtros Ativos")
st.sidebar.markdown(f"**Região:** {regiao_selecionada}")
st.sidebar.markdown(f"**Níveis de Risco:** {', '.join(niveis_selecionados) if niveis_selecionados else 'Nenhum'}")

# --- Layout Principal com Abas ---
tab_mapa, tab_dados, tab_alertas = st.tabs(["🗺️ Mapa de Riscos", "📊 Dados Detalhados", "🚨 Alertas Críticos"])

with tab_mapa:
    st.header(f"Mapa de Riscos para: {regiao_selecionada}")
    if not df_filtrado.empty and df_filtrado[['Latitude', 'Longitude']].notna().all().all():
        st.map(df_filtrado, latitude='Latitude', longitude='Longitude', size=100, color='#FF0000')
        st.caption("Pontos no mapa indicam as cidades monitoradas. A análise detalhada do risco está na aba 'Dados Detalhados'.")
    elif not df_filtrado.empty:
        st.warning("Algumas cidades não possuem coordenadas cadastradas e não serão exibidas no mapa.")
    else:
        st.info("Nenhuma cidade corresponde aos filtros selecionados.")
        
with tab_dados:
    st.header(f"Análise Detalhada para: {regiao_selecionada}")
    st.dataframe(df_filtrado, use_container_width=True)

with tab_alertas:
    st.header("Alertas Críticos (Risco Alto)")
    
    df_alertas = df_filtrado[df_filtrado['Classificação'] == 'Alto']
    
    if not df_alertas.empty:
        for index, row in df_alertas.iterrows():
            st.error(
                f"**ALERTA ALTO RISCO NA CIDADE: {row['Cidade']}**\n"
                f"- **Nível de Risco Calculado:** {row['Risco (0-10)']}\n"
                f"- **Dados dos Sensores:** Chuva: {row['Chuva (mm/h)']} mm/h | Umidade do Solo: {row['Umidade (%)']}% | Vibração: {row['Vibração (Hz)']} Hz\n"
                f"- **ID do Sistema:** {row['ID Sistema']}",
                icon="🚨"
            )
    else:
        st.success("Nenhum alerta de risco alto para a região e filtros selecionados.")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("Desenvolvido para o Hackathon CEFET-2025 - Desafio CBMMG.")