import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def calcular_risco_deslizamento(leitura_pluviometro, leitura_umidade, leitura_acelerometro):
    """
    Calcula o risco de deslizamento usando um sistema de inferência fuzzy.
    Retorna um valor numérico de risco entre 0 e 10.
    """
    # Validação de entradas nulas (sensores com falha)
    if any(v is None for v in [leitura_pluviometro, leitura_umidade, leitura_acelerometro]):
        return 0 # Retorna risco mínimo se algum sensor falhar

    # Definição das variáveis de entrada (Antecedentes)
    # Universo de discurso para cada variável
    pluviometro = ctrl.Antecedent(np.arange(0, 16, 1), 'pluviometro') # Chuva em mm/h
    umidade_solo = ctrl.Antecedent(np.arange(0, 101, 1), 'umidade_solo') # Umidade em %
    vibracao_solo = ctrl.Antecedent(np.arange(0, 9, 1), 'vibracao_solo') # Vibração em Hz (simulada pelo acelerômetro)

    # Definição da variável de saída (Consequente)
    risco = ctrl.Consequent(np.arange(0, 11, 1), 'risco')

    # Criação das funções de pertinência (membership functions) para cada variável
    # Pluviômetro
    pluviometro['baixa'] = fuzz.trimf(pluviometro.universe, [0, 0, 5])
    pluviometro['media'] = fuzz.trimf(pluviometro.universe, [2, 7, 12])
    pluviometro['alta'] = fuzz.trimf(pluviometro.universe, [10, 15, 15])

    # Umidade do Solo
    umidade_solo['baixa'] = fuzz.trimf(umidade_solo.universe, [0, 0, 40])
    umidade_solo['media'] = fuzz.trimf(umidade_solo.universe, [30, 55, 80])
    umidade_solo['alta'] = fuzz.trimf(umidade_solo.universe, [70, 100, 100])

    # Vibração do Solo
    vibracao_solo['estavel'] = fuzz.trimf(vibracao_solo.universe, [0, 0, 2])
    vibracao_solo['moderada'] = fuzz.trimf(vibracao_solo.universe, [1, 4, 7])
    vibracao_solo['intensa'] = fuzz.trimf(vibracao_solo.universe, [6, 8, 8])

    # Níveis de Risco
    risco['muito_baixo'] = fuzz.trimf(risco.universe, [0, 0, 2])
    risco['baixo'] = fuzz.trimf(risco.universe, [1, 3, 5])
    risco['medio'] = fuzz.trimf(risco.universe, [4, 6, 8])
    risco['alto'] = fuzz.trimf(risco.universe, [7, 10, 10])

    # Definição das Regras Fuzzy
    # Regra 1: Se a chuva é alta OU a umidade é alta, o risco é médio.
    regra1 = ctrl.Rule(pluviometro['alta'] | umidade_solo['alta'], risco['medio'])
    
    # Regra 2: Se a chuva é alta E a umidade é alta, o risco é alto.
    regra2 = ctrl.Rule(pluviometro['alta'] & umidade_solo['alta'], risco['alto'])

    # Regra 3: Se a vibração é intensa, o risco é alto, independentemente dos outros fatores.
    regra3 = ctrl.Rule(vibracao_solo['intensa'], risco['alto'])
    
    # Regra 4: Se a umidade é média E a chuva é média, o risco é baixo.
    regra4 = ctrl.Rule(umidade_solo['media'] & pluviometro['media'], risco['baixo'])
    
    # Regra 5: Se a vibração é moderada E a umidade é alta, o risco é médio.
    regra5 = ctrl.Rule(vibracao_solo['moderada'] & umidade_solo['alta'], risco['medio'])

    # Regra 6: Se tudo está baixo/estável, o risco é muito baixo.
    regra6 = ctrl.Rule(pluviometro['baixa'] & umidade_solo['baixa'] & vibracao_solo['estavel'], risco['muito_baixo'])

    # Construção do Sistema de Controle
    sistema_controle_risco = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5, regra6])
    calculo_risco = ctrl.ControlSystemSimulation(sistema_controle_risco)

    # Passando os valores de entrada para o sistema
    calculo_risco.input['pluviometro'] = leitura_pluviometro
    calculo_risco.input['umidade_solo'] = leitura_umidade
    calculo_risco.input['vibracao_solo'] = leitura_acelerometro

    # Computando o resultado
    calculo_risco.compute()

    return calculo_risco.output['risco']

# Bloco de teste (opcional)
if __name__ == '__main__':
    # Exemplo de uso
    risco_calculado = calcular_risco_deslizamento(leitura_pluviometro=12.5, leitura_umidade=85.0, leitura_acelerometro=3.0)
    print(f"Risco Calculado: {risco_calculado:.2f}")

    risco_calculado_baixo = calcular_risco_deslizamento(leitura_pluviometro=2.0, leitura_umidade=30.0, leitura_acelerometro=1.0)
    print(f"Risco Calculado (Cenário Baixo): {risco_calculado_baixo:.2f}")
    
    risco_com_falha = calcular_risco_deslizamento(leitura_pluviometro=10.0, leitura_umidade=None, leitura_acelerometro=2.0)
    print(f"Risco Calculado (Sensor com Falha): {risco_com_falha:.2f}")