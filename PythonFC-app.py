import pandas as pd
import numpy as np
import io
import streamlit as st

# Carga directa del archivo CSV desde el repositorio
try:
    # Asegúrate de que este nombre coincida EXACTAMENTE con tu archivo en GitHub
    df = pd.read_csv("3 Premier League - Datos 2020-2021 - Streamlit - (DATA_Analisis).csv", sep=';')
    
    # Cálculo de minutos en segmentos de 90
    df['90s'] = df['minutes']/90

    # Métricas por 90 minutos
    calc_elements = ['goals', 'assists', 'points']
    for each in calc_elements:
        df[f'{each}_p90'] = df[each] / df['90s']

    # Listas únicas para filtros
    positions = list(df['position'].drop_duplicates())
    teams = list(df['team'].drop_duplicates())

    # Barra lateral - títulos y filtros
    st.sidebar.markdown('### Data Filters')
    position_choice = st.sidebar.multiselect(
        'Choose position:', positions, default=positions)
    teams_choice = st.sidebar.multiselect(
        "Teams:", teams, default=teams)
    price_choice = st.sidebar.slider(
        'Max Price:', min_value=4.0, max_value=15.0, step=.5, value=15.0)

    # Aplicar filtros
    df = df[df['position'].isin(position_choice)]
    df = df[df['team'].isin(teams_choice)]
    df = df[df['cost'] < price_choice]

    # Título principal
    st.title(f"Análisis de los jugadores para ficharlos")

    # Tabla de jugadores
    st.markdown('### Base de datos de los jugadores')
    st.dataframe(df.sort_values('points',
                 ascending=False).reset_index(drop=True))

    # Gráfico costo vs puntos
    st.markdown('### Costo vs puntos en competencia 20/21')
    st.vega_lite_chart(df, {
        'mark': {'type': 'circle', 'tooltip': True},
        'encoding': {
            'x': {'field': 'cost', 'type': 'quantitative'},
            'y': {'field': 'points', 'type': 'quantitative'},
            'color': {'field': 'position', 'type': 'nominal'},
            'tooltip': [{"field": 'name', 'type': 'nominal'}, {'field': 'cost', 'type': 'quantitative'}, {'field': 'points', 'type': 'quantitative'}],
        },
        'width': 700,
        'height': 400,
    })

    # Gráfico goles por 90 vs asistencias por 90
    st.markdown('### Goles 90 minutos vs Asistencia 90 minutos')
    st.vega_lite_chart(df, {
        'mark': {'type': 'circle', 'tooltip': True},
        'encoding': {
            'x': {'field': 'goals_p90', 'type': 'quantitative'},
            'y': {'field': 'assists_p90', 'type': 'quantitative'},
            'color': {'field': 'position', 'type': 'nominal'},
            'tooltip': [{"field": 'name', 'type': 'nominal'}, {'field': 'cost', 'type': 'quantitative'}, {'field': 'points', 'type': 'quantitative'}],
        },
        'width': 700,
        'height': 400,
    })
    
except FileNotFoundError:
    st.error("""
    Error: No se encontró el archivo CSV. Por favor verifica:
    1. Que el archivo existe en el repositorio
    2. Que el nombre es exactamente:
    '3 Premier League - Datos 2020-2021 - Streamlit - (DATA_Analisis).csv'
    3. Que está en la misma carpeta que tu script
    """)
except Exception as e:
    st.error(f"Ocurrió un error inesperado: {str(e)}")

