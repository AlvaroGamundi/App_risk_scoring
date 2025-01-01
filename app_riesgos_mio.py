from codigo_de_ejecucion_mio import *
import streamlit as st
from streamlit_echarts import st_echarts

#CONFIGURACION DE LA PÁGINA
st.set_page_config(
     page_title = 'Bank Loan Risk Score Analyzer',
     page_icon = 'risk_score.jpg',
     layout = 'wide')

#SIDEBAR
with st.sidebar:
    st.image('risk_score.jpg')

    #INPUTS DE LA APLICACION
    principal = st.number_input('Requested Amount', 500, 50000)
    finalidad = st.selectbox('Loan Purpose', ['debt_consolidation','credit_card','home_improvement','other'])
    num_cuotas = st.radio('Number of Installments', ['36 months','60 months'])
    ingresos = st.slider('Annual Income', 20000, 300000)

    #DATOS CONOCIDOS (fijadas como datos estaticos por simplicidad)
    ingresos_verificados = 'Verified'
    antiguedad_empleo = '10+ years'
    rating = 'B'
    dti = 28
    num_lineas_credito = 3
    porc_uso_revolving = 50
    tipo_interes = 7.26
    imp_cuota = 500
    num_derogatorios = 0
    vivienda = 'MORTGAGE'
    num_hipotecas=1
    porc_tarjetas_75p=41
    num_cancelaciones_12meses=0




#MAIN
st.title('BANK LOAN RISK SCORE ANALYZER')


#CALCULAR

#Crear el registro
registro = pd.DataFrame({'ingresos_verificados':ingresos_verificados,
                         'vivienda':vivienda,
                         'finalidad':finalidad,
                         'num_cuotas':num_cuotas,
                         'antiguedad_empleo':antiguedad_empleo,
                         'rating':rating,
                         'ingresos':ingresos,
                         'dti':dti,
                         'num_lineas_credito':num_lineas_credito,
                         'porc_uso_revolving':porc_uso_revolving,
                         'principal':principal,
                         'tipo_interes':tipo_interes,
                         'imp_cuota':imp_cuota,
                         'num_derogatorios':num_derogatorios,
                         'num_hipotecas':num_hipotecas,
                         'porc_tarjetas_75p':porc_tarjetas_75p,
                         'num_cancelaciones_12meses':num_cancelaciones_12meses}
                        ,index=[0])



#CALCULAR RIESGO
if st.sidebar.button('CALCULATE RISK'):
    st.write('Designed and Powered by Álvaro Gamundi')
    #Ejecutar el scoring
    EL = ejecutar_modelos(registro)

    #Calcular los kpis
    kpi_pd = int(EL.pd * 100)
    kpi_ead = int(EL.ead * 100)
    kpi_lgd = int(EL.lgd * 100)
    kpi_el = int(EL.principal * EL.pd * EL.ead * EL.lgd)

    #Velocimetros
    #Codigo de velocimetros tomado de https://towardsdatascience.com/5-streamlit-components-to-build-better-applications-71e0195c82d4
    pd_options = {
            "tooltip": {"formatter": "{a} <br/>{b} : {c}%"},
            "series": [
                {
                    "name": "PD",
                    "type": "gauge",
                    "axisLine": {
                        "lineStyle": {
                            "width": 10,
                        },
                    },
                    "progress": {"show": "true", "width": 10},
                    "detail": {"valueAnimation": "true", "formatter": "{value}"},
                    "data": [{"value": kpi_pd, "name": "PD"}],
                }
            ],
        }

    #Velocimetro para ead
    ead_options = {
            "tooltip": {"formatter": "{a} <br/>{b} : {c}%"},
            "series": [
                {
                    "name": "EAD",
                    "type": "gauge",
                    "axisLine": {
                        "lineStyle": {
                            "width": 10,
                        },
                    },
                    "progress": {"show": "true", "width": 10},
                    "detail": {"valueAnimation": "true", "formatter": "{value}"},
                    "data": [{"value": kpi_ead, "name": "EAD"}],
                }
            ],
        }

    #Velocimetro para lgd
    lgd_options = {
            "tooltip": {"formatter": "{a} <br/>{b} : {c}%"},
            "series": [
                {
                    "name": "LGD",
                    "type": "gauge",
                    "axisLine": {
                        "lineStyle": {
                            "width": 10,
                        },
                    },
                    "progress": {"show": "true", "width": 10,},
                    "detail": {"valueAnimation": "true", "formatter": "{value}"},
                    "data": [{"value": kpi_lgd, "name": "LGD"}],
                }
            ],
        }
    #Representarlos en la app
    col1,col2,col3 = st.columns(3)
    with col1:
        st_echarts(options=pd_options, width="110%", key=0)
    with col2:
        st_echarts(options=ead_options, width="110%", key=1)
    with col3:
        st_echarts(options=lgd_options, width="110%", key=2)

    #Prescripcion
    col1,col2,col3 = st.columns(3)
    with col1:
        st.write('The expected loss is:')
        st.metric(label="EXPECTED LOSS", value =f"{ kpi_el} €")
    with col2:
        st.write('Recommended additional charge:')
        st.metric(label="COMMISSION TO APPLY", value =f"{ kpi_el * 3} €") #Metido en estático por simplicidad
    with col3:
        st.write('The interest to apply is:')
        st.metric(label="INTEREST TO APPLY", value=f"{round(kpi_el * 3 / principal * 100, 2)} %")
    
else:
    st.write('DEFINE THE LOAN PARAMETERS AND CLICK ON CALCULATE RISK')
    st.write('Designed and Powered by Álvaro Gamundi')
    
    
