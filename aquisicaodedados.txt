# Importa bibliotecas necessárias
import requests
import datetime
import random
import pprint
import unicodedata # Para remover acentos
import re         # Para remover caracteres especiais

# --- CONFIGURAÇÃO DO SISTEMA IoT ---

# 1. MAPA REGIÃO -> CIDADES
MAPA_REGIAO_CIDADES = {
    "regiao_central": ["Belo Horizonte", "Sete Lagoas", "Divinópolis", "Nova Serrana", "Curvelo"],
    "triangulo_mineiro": ["Uberlândia", "Uberaba", "Araguari", "Ituiutaba", "Patos de Minas"],
    "zona_da_mata": ["Juiz de Fora", "Muriaé", "Ubá", "Viçosa", "Leopoldina"],
    "norte_de_minas": ["Montes Claros", "Janaúba", "Januária", "Salinas", "Pirapora"],
    "leste_de_minas": ["Governador Valadares", "Ipatinga", "Teófilo Otoni", "Coronel Fabriciano", "Manhuaçu"],
    "sul_de_minas": ["Poços de Caldas", "Pouso Alegre", "Varginha", "Alfenas", "Passos"]
}

# 2. MAPA CIDADE -> LISTA DE SISTEMAS (com 3 IDs cada)
#    (!!! CRÍTICO: PREENCHA ISTO COM OS IDs REAIS !!!)
#    Cada cidade tem uma lista. Cada item na lista é um dicionário
#    representando UM sistema IoT completo naquela cidade.
MAPA_CIDADE_SENSORES = {
    # Região Central
    "belo_horizonte": [
        {"sistema_id": "bh_sys_01", "pluviometro_id": "pluv_bh_01", "umidade_id": "umid_bh_01", "acelerometro_id": "acel_bh_01"}
        # , {"sistema_id": "bh_sys_02", ...} # Adicione mais sistemas se BH tiver mais de um
    ],
    "sete_lagoas": [
        {"sistema_id": "sl_sys_01", "pluviometro_id": "pluv_sl_01", "umidade_id": "umid_sl_01", "acelerometro_id": "acel_sl_01"}
    ],
    "divinopolis": [
        {"sistema_id": "div_sys_01", "pluviometro_id": "pluv_div_01", "umidade_id": "umid_div_01", "acelerometro_id": "acel_div_01"}
    ],
     "nova_serrana": [
         {"sistema_id": "ns_sys_01", "pluviometro_id": "pluv_ns_01", "umidade_id": "umid_ns_01", "acelerometro_id": "acel_ns_01"}
     ],
     "curvelo": [
         {"sistema_id": "cv_sys_01", "pluviometro_id": "pluv_cv_01", "umidade_id": "umid_cv_01", "acelerometro_id": "acel_cv_01"}
     ],
    # Triângulo Mineiro
    "uberlandia": [
        {"sistema_id": "udi_sys_01", "pluviometro_id": "pluv_udi_01", "umidade_id": "umid_udi_01", "acelerometro_id": "acel_udi_01"}
    ],
     "uberaba": [
         {"sistema_id": "uba_sys_01", "pluviometro_id": "pluv_uba_01", "umidade_id": "umid_uba_01", "acelerometro_id": "acel_uba_01"}
     ],
     "araguari": [
         {"sistema_id": "arg_sys_01", "pluviometro_id": "pluv_arg_01", "umidade_id": "umid_arg_01", "acelerometro_id": "acel_arg_01"}
     ],
     "ituiutaba": [
         {"sistema_id": "itb_sys_01", "pluviometro_id": "pluv_itb_01", "umidade_id": "umid_itb_01", "acelerometro_id": "acel_itb_01"}
     ],
     "patos_de_minas": [
         {"sistema_id": "pdm_sys_01", "pluviometro_id": "pluv_pdm_01", "umidade_id": "umid_pdm_01", "acelerometro_id": "acel_pdm_01"}
     ],
    # Zona da Mata
    "juiz_de_fora": [
        {"sistema_id": "jf_sys_01", "pluviometro_id": "pluv_jf_01", "umidade_id": "umid_jf_01", "acelerometro_id": "acel_jf_01"}
    ],
    "muriae": [
        {"sistema_id": "mur_sys_01", "pluviometro_id": "pluv_mur_01", "umidade_id": "umid_mur_01", "acelerometro_id": "acel_mur_01"}
    ],
    "uba": [
        {"sistema_id": "ub_sys_01", "pluviometro_id": "pluv_ub_01", "umidade_id": "umid_ub_01", "acelerometro_id": "acel_ub_01"}
    ],
    "vicosa": [
        {"sistema_id": "vic_sys_01", "pluviometro_id": "pluv_vic_01", "umidade_id": "umid_vic_01", "acelerometro_id": "acel_vic_01"}
    ],
    "leopoldina": [
        {"sistema_id": "leo_sys_01", "pluviometro_id": "pluv_leo_01", "umidade_id": "umid_leo_01", "acelerometro_id": "acel_leo_01"}
    ],
    # Norte de Minas
    "montes_claros": [
        {"sistema_id": "moc_sys_01", "pluviometro_id": "pluv_moc_01", "umidade_id": "umid_moc_01", "acelerometro_id": "acel_moc_01"}
    ],
    "janauba": [
        {"sistema_id": "jnb_sys_01", "pluviometro_id": "pluv_jnb_01", "umidade_id": "umid_jnb_01", "acelerometro_id": "acel_jnb_01"}
    ],
    "januaria": [
        {"sistema_id": "jnr_sys_01", "pluviometro_id": "pluv_jnr_01", "umidade_id": "umid_jnr_01", "acelerometro_id": "acel_jnr_01"}
    ],
    "salinas": [
        {"sistema_id": "sal_sys_01", "pluviometro_id": "pluv_sal_01", "umidade_id": "umid_sal_01", "acelerometro_id": "acel_sal_01"}
    ],
    "pirapora": [
        {"sistema_id": "pir_sys_01", "pluviometro_id": "pluv_pir_01", "umidade_id": "umid_pir_01", "acelerometro_id": "acel_pir_01"}
    ],
    # Leste de Minas
    "governador_valadares": [
        {"sistema_id": "gv_sys_01", "pluviometro_id": "pluv_gv_01", "umidade_id": "umid_gv_01", "acelerometro_id": "acel_gv_01"}
    ],
    "ipatinga": [
        {"sistema_id": "ipa_sys_01", "pluviometro_id": "pluv_ipa_01", "umidade_id": "umid_ipa_01", "acelerometro_id": "acel_ipa_01"}
    ],
    "teofilo_otoni": [
        {"sistema_id": "teo_sys_01", "pluviometro_id": "pluv_teo_01", "umidade_id": "umid_teo_01", "acelerometro_id": "acel_teo_01"}
    ],
    "coronel_fabriciano": [
        {"sistema_id": "cf_sys_01", "pluviometro_id": "pluv_cf_01", "umidade_id": "umid_cf_01", "acelerometro_id": "acel_cf_01"}
    ],
    "manhuacu": [
        {"sistema_id": "mcu_sys_01", "pluviometro_id": "pluv_mcu_01", "umidade_id": "umid_mcu_01", "acelerometro_id": "acel_mcu_01"}
    ],
    # Sul de Minas
    "pocos_de_caldas": [
        {"sistema_id": "pc_sys_01", "pluviometro_id": "pluv_pc_01", "umidade_id": "umid_pc_01", "acelerometro_id": "acel_pc_01"}
    ],
    "pouso_alegre": [
        {"sistema_id": "pa_sys_01", "pluviometro_id": "pluv_pa_01", "umidade_id": "umid_pa_01", "acelerometro_id": "acel_pa_01"}
    ],
    "varginha": [
        {"sistema_id": "var_sys_01", "pluviometro_id": "pluv_var_01", "umidade_id": "umid_var_01", "acelerometro_id": "acel_var_01"}
    ],
    "alfenas": [
        {"sistema_id": "alf_sys_01", "pluviometro_id": "pluv_alf_01", "umidade_id": "umid_alf_01", "acelerometro_id": "acel_alf_01"}
    ],
    "passos": [
        {"sistema_id": "pas_sys_01", "pluviometro_id": "pluv_pas_01", "umidade_id": "umid_pas_01", "acelerometro_id": "acel_pas_01"}
    ],
}

# 3. ENDPOINT CENTRAL (Simulado)
API_BASE_URL = "http://localhost:8000/api/sensor" # Exemplo

# --- FUNÇÕES AUXILIARES ---

def _normalizar_nome(nome):
    """Normaliza um nome (cidade ou região) para usar como chave."""
    if not nome: return None
    nfkd_form = unicodedata.normalize('NFKD', nome)
    sem_acentos = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    chave = re.sub(r'\s+', '_', sem_acentos.lower())
    chave = re.sub(r'[^a-z0-9_]', '', chave)
    return chave

# --- FUNÇÕES DE AQUISIÇÃO ---

def _fetch_single_sensor_reading(sensor_id):
    """
    Função PRIVADA que busca a LEITURA de UM sensor específico.
    *** SIMULAÇÃO PARA O HACKATHON ***
    Retorna apenas o VALOR da leitura (ou None se falhar).
    """
    # print(f"--- [Simulação] Buscando leitura para sensor: {sensor_id} ---") # Opcional: Muito verbose
    
    # ----- INÍCIO DA SIMULAÇÃO -----
    # TODO: Substituir pela chamada REAL (requests, MQTT, DB...)
    # A chamada real pegaria o valor e o timestamp da última leitura daquele sensor_id.
    try:
        if random.random() < 0.05: # Simula 5% de falha por sensor
            raise ConnectionError("Simulação: Leitura falhou")

        # Simula o valor baseado no TIPO de sensor (inferido pelo prefixo do ID)
        valor_simulado = None
        if sensor_id.startswith("pluv_"):
            valor_simulado = round(random.uniform(0, 15), 1) # mm/h
        elif sensor_id.startswith("umid_"):
            valor_simulado = round(random.uniform(10, 98), 1) # %
        elif sensor_id.startswith("acel_"):
            valor_simulado = round(random.uniform(0.5, 8.0), 2) # Hz
        else:
            print(f"AVISO: ID de sensor desconhecido para simulação: {sensor_id}")
            valor_simulado = -1 # Valor indicando erro ou tipo desconhecido

        # print(f"--- [Simulação] Leitura para {sensor_id}: {valor_simulado}") # Opcional
        return valor_simulado

    except Exception as e:
        print(f"ERRO (simulado) ao buscar leitura para {sensor_id}: {e}")
        return None # Retorna None em caso de falha na leitura
    # ----- FIM DA SIMULAÇÃO -----

def get_dados_sensores_por_regiao(nome_regiao_selecionada):
    """
    Função PRINCIPAL que o dashboard vai chamar.
    Busca os dados mais recentes de TODOS os sistemas IoT (pluviômetro, umidade, acelerômetro)
    de TODAS as cidades mapeadas para uma dada REGIÃO.

    Args:
        nome_regiao_selecionada (str): O nome da região (ex: "Região Central").

    Returns:
        dict: Dicionário onde chaves são NOMES ORIGINAIS das cidades e valores são
              listas de dicionários, cada um representando um SISTEMA IoT completo
              com as leituras de seus 3 sensores. Retorna dicionário vazio se
              nenhum dado for encontrado.
              Ex:
              {
                  "Poços de Caldas": [
                      {
                          "sistema_id": "pc_sys_01",
                          "timestamp": "...", # Idealmente, o timestamp da leitura MAIS RECENTE entre os 3 sensores
                          "pluviometro_id": "pluv_pc_01",
                          "leitura_pluviometro_mm_h": 5.2, # Pode ser None se falhar
                          "umidade_id": "umid_pc_01",
                          "leitura_umidade_solo_percent": 65.0, # Pode ser None se falhar
                          "acelerometro_id": "acel_pc_01",
                          "leitura_acelerometro_freq_hz": 1.2 # Pode ser None se falhar
                      }
                  ], ...
              }
    """
    chave_regiao = _normalizar_nome(nome_regiao_selecionada)
    if not chave_regiao: return {}

    print(f"\nIniciando aquisição de dados IoT para a REGIÃO: {nome_regiao_selecionada} (chave: {chave_regiao})")

    lista_cidades_na_regiao = MAPA_REGIAO_CIDADES.get(chave_regiao, [])
    if not lista_cidades_na_regiao: return {}

    print(f"Cidades mapeadas para '{chave_regiao}': {lista_cidades_na_regiao}")

    dados_finais_regiao = {}
    timestamp_geral_leitura = datetime.datetime.now().isoformat(timespec='seconds') # Timestamp da busca

    for nome_cidade_original in lista_cidades_na_regiao:
        chave_cidade_atual = _normalizar_nome(nome_cidade_original)
        sistemas_na_cidade = MAPA_CIDADE_SENSORES.get(chave_cidade_atual, [])

        if not sistemas_na_cidade:
            print(f"-- AVISO: Nenhum sistema IoT mapeado para '{nome_cidade_original}'. Pulando.")
            continue

        print(f"-- Processando cidade: {nome_cidade_original} ({len(sistemas_na_cidade)} sistemas)")
        dados_desta_cidade = [] # Lista para guardar dados dos sistemas desta cidade

        # Itera sobre cada SISTEMA IoT na cidade
        for sistema_info in sistemas_na_cidade:
            sistema_id = sistema_info.get("sistema_id", "ID_Nao_Definido")
            pluv_id = sistema_info.get("pluviometro_id")
            umid_id = sistema_info.get("umidade_id")
            acel_id = sistema_info.get("acelerometro_id")

            print(f"--- Coletando dados para Sistema: {sistema_id} (Pluv: {pluv_id}, Umid: {umid_id}, Acel: {acel_id})")

            # Busca a leitura de CADA sensor individualmente
            leitura_pluv = _fetch_single_sensor_reading(pluv_id) if pluv_id else None
            leitura_umid = _fetch_single_sensor_reading(umid_id) if umid_id else None
            leitura_acel = _fetch_single_sensor_reading(acel_id) if acel_id else None

            # Monta o dicionário de resultados para ESTE sistema IoT
            # Inclui os IDs e as leituras (que podem ser None se a leitura falhar)
            dados_sistema_atual = {
                "sistema_id": sistema_id,
                "timestamp": timestamp_geral_leitura, # Usamos um timestamp da busca toda
                "pluviometro_id": pluv_id,
                "leitura_pluviometro_mm_h": leitura_pluv,
                "umidade_id": umid_id,
                "leitura_umidade_solo_percent": leitura_umid,
                "acelerometro_id": acel_id,
                "leitura_acelerometro_freq_hz": leitura_acel
            }
            dados_desta_cidade.append(dados_sistema_atual)

        # Adiciona os dados desta cidade ao resultado final, se houver algum sistema
        if dados_desta_cidade:
            dados_finais_regiao[nome_cidade_original] = dados_desta_cidade
            print(f"-- Concluído para {nome_cidade_original}: Dados de {len(dados_desta_cidade)} sistemas coletados.")
        else:
             print(f"-- Nenhum sistema encontrado ou respondeu para {nome_cidade_original}.")


    print(f"\nAquisição concluída para REGIÃO '{nome_regiao_selecionada}'. Dados coletados de {len(dados_finais_regiao)} cidades.")
    return dados_finais_regiao

# --- BLOCO DE TESTE ---
if __name__ == "__main__":

    # --- CONFIGURE SEU TESTE AQUI ---
    REGIAO_PARA_TESTAR = "Sul de Minas" # Mude aqui para testar outras regiões
    # ---------------------------------

    print("="*50)
    print(f"--- INICIANDO TESTE DO MÓDULO 'aquisicaodedados' (MODO IoT por Região/Cidade/Sensor) ---")
    print(f"--- REGIÃO ALVO: {REGIAO_PARA_TESTAR} ---")
    print("="*50)

    # Chama a função principal
    dados_iot_coletados = get_dados_sensores_por_regiao(REGIAO_PARA_TESTAR)

    print(f"\n--- RESULTADO FINAL PARA REGIÃO '{REGIAO_PARA_TESTAR}' ---")
    if dados_iot_coletados:
        pprint.pprint(dados_iot_coletados)
    else:
        chave_teste = _normalizar_nome(REGIAO_PARA_TESTAR)
        print(f"Nenhum dado de sensor retornado para a região '{REGIAO_PARA_TESTAR}'.")
        # (Mensagens de erro detalhadas já são impressas dentro da função principal)

    print("\n="*50)
    print("--- TESTE FINALIZADO ---")
    print("="*50)