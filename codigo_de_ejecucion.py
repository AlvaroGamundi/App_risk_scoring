#1.LIBRERIAS
import numpy as np
import pandas as pd
import pickle

from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import Binarizer
from sklearn.preprocessing import MinMaxScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingRegressor

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline





def ejecutar_modelos(df):
    #5.CALIDAD Y CREACION DE VARIABLES
    x_pd = df.copy()
    x_ead = df.copy()
    x_lgd = df.copy()


    #6.CARGA PIPES DE EJECUCION
    with open('pipe_ejecucion_pd.pickle', mode='rb') as file:
       pipe_ejecucion_pd = pickle.load(file)

    with open('pipe_ejecucion_ead.pickle', mode='rb') as file:
       pipe_ejecucion_ead = pickle.load(file)

    with open('pipe_ejecucion_lgd.pickle', mode='rb') as file:
       pipe_ejecucion_lgd = pickle.load(file)


    #7.EJECUCION
    scoring_pd = pipe_ejecucion_pd.predict_proba(x_pd)[:, 1]
    ead = pipe_ejecucion_ead.predict(x_ead)
    lgd = pipe_ejecucion_lgd.predict(x_lgd)


    #8.RESULTADO
    principal = x_pd.principal
    EL = pd.DataFrame({'principal':principal,
                       'pd':scoring_pd,
                       'ead':ead,
                       'lgd':lgd
                       })
    EL['perdida_esperada'] = round(EL.pd * EL.principal * EL.ead * EL.lgd,2)

    return(EL)
