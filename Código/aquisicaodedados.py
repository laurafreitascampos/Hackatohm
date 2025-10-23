import requests
import pandas as pd

# (Aqui você pode adicionar as bibliotecas de API: paho-mqtt, arcgis, etc.)

def buscar_dados_cemaden(regiao_id):
    """
    Simula uma chamada à API do CEMADEN.
    TODO: Substituir pela chamada real com 'requests'.
    """
    print(f"Buscando dados do CEMADEN para {regiao_id}...")
    # Lógica de exemplo
    if regiao_id == "JuizDeFora":
        return 55.0  # mm
    return 10.0  # mm

def buscar_dados_inmet(regiao_id):
    """
    Simula uma chamada à API do INMET.
    TODO: Substituir pela chamada real com 'requests'.
    """
    print(f"Buscando dados do INMET para {regiao_id}...")
    # Lógica de exemplo
    if regiao_id == "JuizDeFora":
        return 70.0  # %
    return 40.0  # %

def buscar_dados_iot():
    """
    Simula uma chamada ao seu sensor IoT (via MQTT ou FastAPI local).
    TODO: Substituir pela chamada real.
    """
    print("Buscando dados do sensor IoT...")
    # Lógica de exemplo
    return 65.0 # % de umidade do solo

# Esta é a função "principal" que o seu dashboard vai chamar
def get_all_data(regiao_id):
    """Puxa todos os dados de todas as fontes."""
    
    chuva_24h = buscar_dados_cemaden(regiao_id)
    umidade_ar = buscar_dados_inmet(regiao_id)
    umidade_solo = buscar_dados_iot()
    
    # Retorna os dados prontos para o fuzzy
    return {
        "chuva": chuva_24h,
        "umidade_solo": umidade_solo,
        "umidade_ar": umidade_ar
    }
    