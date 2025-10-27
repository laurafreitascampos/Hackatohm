import pandas as pd
import streamlit as st
import pprint  # <--- ADICIONE ESTA LINHA
import pandas as pd
import streamlit as st # Usamos o streamlit para o 'cache'

# URL ATUALIZADA: Usando o link que você encontrou.
URL_BARRAGENS_ANM = "https://dados.anm.gov.br/dados/SIGBM/Barragens.csv"

# Mapeia os IDs do seu dashboard para os nomes exatos dos municípios no CSV
MAPA_REGIOES_PARA_MUNICIPIO = {
    "BH": "BELO HORIZONTE",
    "Uberlandia": "UBERLÂNDIA",
    "JuizDeFora": "JUIZ DE FORA",
    "MontesClaros": "MONTES CLAROS",
    "GovValdares": "GOVERNADOR VALADARES",
    "PocosDeCaldas": "POÇOS DE CALDAS",
    # Adicionando cidades-chave da "região" de BH, famosas por barragens
    "BH_R1": "NOVA LIMA",
    "BH_R2": "BRUMADINHO",
    "BH_R3": "ITABIRA",
    "BH_R4": "ITABIRITO",
    "BH_R5": "OURO PRETO",
    "BH_R6": "MARIANA",
}

# --- ESTA É A LISTA QUE VOCÊ PEDIU ---
# As colunas que selecionamos como "essenciais" para o bombeiro
COLUNAS_ESSENCIAIS_BARRAGENS = [
    # Grupo 1: Identificação
    'Nome',
    'Nome da mina',
    'Município',
    'Latitude',
    'Longitude',
    
    # Grupo 2: Risco Imediato
    'Nível de Emergência',
    'Categoria de Risco - CRI',
    'Situação Operacional',
    'Status DCE RISR',
    'Status da DCO Atual',
    
    # Grupo 3: Consequência
    'Dano Potencial Associado - DPA',
    'Existência de população a jusante',
    'Número de pessoas possivelmente afetadas a jusante em caso de rompimento da barragem',
    'A Barragem armazena rejeitos/residuos que contenham Cianeto',
    'Necessita de PAEBM',
    
    # Grupo 4: Contexto Técnico
    'Altura máxima atual (m)',
    'Volume atual do Reservatório (m³)',
    'Método construtivo da barragem',
    'Minério principal presente no reservatório',
    
    # Grupo 5: Responsáveis
    'Empreendedor',
    'RT/Declaração',
    'RT/Empreendimento'
]


# A função de cache garante que não vamos baixar esse CSV gigante toda hora
@st.cache_data(ttl=3600) # ttl=3600 = Salva o cache por 1 hora (3600 segundos)
def carregar_banco_de_dados_barragens():
    """
    Baixa o arquivo CSV completo de barragens da ANM e o carrega em um DataFrame do Pandas.
    Esta função usa cache para rodar apenas uma vez por hora.
    """
    print(f"ATENÇÃO: Baixando banco de dados de barragens da ANM (cache de 1h)...")
    try:
        # Tenta ler o CSV. 
        # encoding='latin1' (ou 'ISO-8859-1') é crucial para acentos em português.
        # sep=';' informa que o separador é ponto-e-vírgula.
        df_completo = pd.read_csv(URL_BARRAGENS_ANM, encoding='latin1', sep=';')
        
        # Limpeza de Dados: Garante que o nome do município esteja em maiúsculo e sem espaços extras
        df_completo['Município'] = df_completo['Município'].str.upper().str.strip()
        
        print("Banco de dados de barragens carregado com sucesso.")
        return df_completo
    except Exception as e:
        print(f"ERRO CRÍTICO ao baixar ou processar o CSV de barragens: {e}")
        st.error(f"Falha ao carregar dados de barragens: {e}")
        return pd.DataFrame()

def get_dados_barragens(regiao_id):
    """
    Filtra o banco de dados de barragens para uma região específica.
    """
    # 1. Carrega o DataFrame completo (do cache)
    df_barragens_completo = carregar_banco_de_dados_barragens()
    
    if df_barragens_completo.empty:
        return []

    # 2. Pega o nome do município correspondente ao ID da região
    municipio_alvo = MAPA_REGIOES_PARA_MUNICIPIO.get(regiao_id)
    
    if not municipio_alvo:
        print(f"Região {regiao_id} não mapeada para barragens.")
        return []

    # 3. Filtra o DataFrame para aquele município
    print(f"Filtrando barragens para o município: {municipio_alvo}")
    df_filtrado = df_barragens_completo[df_barragens_completo['Município'] == municipio_alvo]
    
    if df_filtrado.empty:
        print(f"Nenhuma barragem de mineração encontrada para {municipio_alvo}.")
        return []

    # 4. Seleciona apenas as colunas essenciais que definimos acima
    
    # Garante que todas as colunas que queremos realmente existem no CSV
    colunas_para_extrair = [col for col in COLUNAS_ESSENCIAIS_BARRAGENS if col in df_filtrado.columns]
    
    # Cria um novo DataFrame apenas com essas colunas
    df_final = df_filtrado[colunas_para_extrair]
    
    # 5. Retorna os dados como uma lista de dicionários
    # O 'fillna' troca valores vazios (NaN) por "Não Informado", para ficar bonito no dashboard
    return df_final.fillna("Não Informado").to_dict('records')


# --- OUTRAS APIS (CEMADEN, INMET, etc.) ---
# (As funções antigas de exemplo podem ficar aqui para seus colegas)

def buscar_dados_cemaden(regiao_id):
    print(f"Buscando dados do CEMADEN para {regiao_id}...")
    # TODO: Implementar chamada real
    if regiao_id == "JuizDeFora":
        return 55.0  # mm
    return 10.0  # mm

def buscar_dados_iot():
    print("Buscando dados do sensor IoT...")
    # TODO: Implementar chamada real
    return 65.0 # % de umidade do solo

# Esta é a função "principal" que o seu dashboard vai chamar
def get_all_data(regiao_id):
    """Puxa todos os dados de todas as fontes."""
    
    # --- Dados de Barragens ---
    lista_de_barragens = get_dados_barragens(regiao_id)
    
    # --- Outros Dados ---
    chuva_24h = buscar_dados_cemaden(regiao_id)
    umidade_solo = buscar_dados_iot()
    
    # Retorna os dados prontos para o fuzzy e para o dashboard
    return {
        "barragens": lista_de_barragens,
        "chuva": chuva_24h,
        "umidade_solo": umidade_solo,
    }
    
# ... (todo o seu código de funções fica acima) ...


# --- BLOCO DE TESTE ---
# Este código só executa quando você roda o arquivo diretamente
# (ex: "python aquisicaodedados.py")
# Ele NÃO executa quando é importado por outro arquivo (como o dashboard.py)
if __name__ == "__main__":
    
    # Vamos importar o pprint para formatar a saída
    import pprint
    
    # ----------------------------------------------------
    # --- CONFIGURE SEU TESTE AQUI ---
    #
    # Mude este valor para testar diferentes Batalhões.
    # Vamos usar "BH_R1" (Nova Lima) que com certeza tem barragens.
    REGIAO_DE_TESTE_ID = "BH_R1"
    #
    # ----------------------------------------------------

    print("="*50)
    print(f"--- INICIANDO TESTE DO MÓDULO 'aquisicaodedados' ---")
    print(f"--- REGIÃO ALVO: {REGIAO_DE_TESTE_ID} ---")
    print("="*50)
    
    # Chama a função principal que o dashboard usaria
    dados_coletados = get_all_data(REGIAO_DE_TESTE_ID)
    
    print(f"\n--- RESULTADO DA COLETA DE DADOS ---")
    # Usa o pprint para imprimir o dicionário de forma legível
    pprint.pprint(dados_coletados)
    
    print("\n--- TESTE DE BARRAGENS (DETALHADO) ---")
    # Mostra quantas barragens foram encontradas
    num_barragens = len(dados_coletados.get("barragens", []))
    print(f"Total de barragens encontradas para {REGIAO_DE_TESTE_ID}: {num_barragens}")
    
    # Imprime o nome das 3 primeiras barragens
    if num_barragens > 0:
        print("\nExemplos de barragens encontradas:")
        for barragem in dados_coletados["barragens"][:3]:
            print(f"  - Nome: {barragem.get('Nome')}")
            print(f"    CRI: {barragem.get('Categoria de Risco - CRI')}")
            print(f"    DPA: {barragem.get('Dano Potencial Associado - DPA')}")
            
    print("\n="*50)
    print("--- TESTE FINALIZADO ---")
    print("="*50)