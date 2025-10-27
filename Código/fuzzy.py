import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
#-----------------------------------------------------------------------------#
#Definicao do sistema Fuzzy - Antecedentes e Funcoes de pertinencia:

#Antecedentes:
intensidade_de_chuva = ctrl.Antecedent(np.arange(0,10,0.1), 'intensidade_de_chuva') #unidade em mm
umidade_do_solo = ctrl.Antecedent(np.arange(), 'umidade_do_solo')
vibracao_do_solo = ctrl.Antecedent(np.arange(), 'vibracao_do_solo')

#Funcoes de Pertinencia (baseadas nas legendas dos mapas fornecidos)
intensidade_de_chuva['sem_chuva'] = fuzz.trapmf(intensidade_de_chuva.universe[0,0])