import cx_Oracle
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Configurar el título de la aplicación
st.set_page_config(page_title="VAG NICO", page_icon="https://raw.githubusercontent.com/adrian-camillo/repo_imagenes_nico/bc6185aef3016dfba0eb753a8b9a5b6c7d05dc4a/SVG%20ROJO.svg")

# Datos de conexión
host = '129.151.97.98'
port = 1521
service_name = 'INTDB5_pdb1.sub12222046451.net1.oraclevcn.com'
user = 'INTH1070$NICO'
password = 'NIco*(78227$$13'

# Lista de sucursales ordenadas de menor a mayor
sucursales = sorted([1, 2, 3, 4, 5, 7, 9, 10, 11, 12, 14, 15, 17, 18, 19, 20, 21, 22, 23, 26])

# Widget para que el usuario seleccione las sucursales
selected_sucursales = st.sidebar.multiselect("Seleccionar Sucursales", ['Todos'] + sucursales, default='Todos')

# Validar si se ha seleccionado "Todos"
if 'Todos' in selected_sucursales:
    selected_sucursales = sucursales  # Si se selecciona "Todos", se usan todas las sucursales

# Mostrar mensaje si no se selecciona ninguna sucursal
if not selected_sucursales:
    st.warning('Debe seleccionar al menos una sucursal, recuerde que puede seleccionar la opción "Todos" para visualizar todas las sucursales')
else:
    # Widget para que el usuario seleccione las fechas de inicio y fin
    start_date = st.sidebar.date_input("Fecha de Inicio", datetime.now() - pd.DateOffset(days=10))
    end_date = st.sidebar.date_input("Fecha de Fin", datetime.now())

    # Ajustar la fecha de fin para que sea inclusiva
    end_date += timedelta(days=1)

    # Formatear las fechas en el formato adecuado para la consulta
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # Calcular el período anterior
    start_date_previous = start_date - (end_date - start_date)
    end_date_previous = start_date - timedelta(days=1)
    start_date_previous_str = start_date_previous.strftime('%Y-%m-%d')
    end_date_previous_str = end_date_previous.strftime('%Y-%m-%d')

    # Widget para que el usuario seleccione cómo mostrar los datos
    option = st.sidebar.selectbox("Mostrar Datos", ["Mostrar solo Fecha", "Mostrar con Fecha y Hora", "Mes"], index=0)

    # Widget para habilitar o deshabilitar la línea de media
    show_average = st.sidebar.checkbox("Mostrar línea de media", value=True, key="show_average_checkbox")

    # Widget para que el usuario pueda habilitar la segunda gráfica
    show_second_chart = st.sidebar.checkbox("Mostrar Gráfico del Período Anterior", key="second_chart_checkbox")

    # Crear una conexión a la base de datos
    conn = cx_Oracle.connect(user, password, f'{host}:{port}/{service_name}')

    # Consulta para obtener las fechas de ventas y contar la cantidad de ventas por fecha y sucursal
    if option == "Mostrar con Fecha y Hora":
        query = f"""
        SELECT FCOM, COUNT(*) AS VENTAS
        FROM ERP$CVEN0100
        WHERE FCOM BETWEEN TO_DATE('{start_date_str}', 'YYYY-MM-DD') AND TO_DATE('{end_date_str}', 'YYYY-MM-DD')
        AND EMPR0110$NSUC IN ({', '.join(map(str, selected_sucursales))})
        GROUP BY FCOM
        """
    elif option == "Mostrar solo Fecha":
        query = f"""
        SELECT TO_CHAR(FCOM, 'YYYY-MM-DD') AS FECHA, COUNT(*) AS VENTAS
        FROM ERP$CVEN0100
        WHERE FCOM BETWEEN TO_DATE('{start_date_str}', 'YYYY-MM-DD') AND TO_DATE('{end_date_str}', 'YYYY-MM-DD')
        AND EMPR0110$NSUC IN ({', '.join(map(str, selected_sucursales))})
        GROUP BY TO_CHAR(FCOM, 'YYYY-MM-DD')
        """
    else:
        query = f"""
        SELECT TO_CHAR(FCOM, 'YYYY-MM') AS FECHA, COUNT(*) AS VENTAS
        FROM ERP$CVEN0100
        WHERE FCOM BETWEEN TO_DATE('{start_date_str}', 'YYYY-MM-DD') AND TO_DATE('{end_date_str}', 'YYYY-MM-DD')
        AND EMPR0110$NSUC IN ({', '.join(map(str, selected_sucursales))})
        GROUP BY TO_CHAR(FCOM, 'YYYY-MM')
        """

    # Ejecutar la consulta y obtener los datos en un DataFrame
    df = pd.read_sql(query, conn)

    # Ordenar el DataFrame por la columna de fechas
    df = df.sort_values(by=['FCOM' if option == "Mostrar con Fecha y Hora" else 'FECHA'], ascending=True)

    # Calcular la media de las cantidades de venta y redondear a dos decimales
    average = round(df['VENTAS'].mean(), 2)

    # Encontrar el día con la mayor cantidad de ventas
    max_day = df[df['VENTAS'] == df['VENTAS'].max()]
    max_day = max_day.iloc[0]['FCOM' if option == "Mostrar con Fecha y Hora" else 'FECHA']

    # Encontrar el día con la menor cantidad de ventas
    min_day = df[df['VENTAS'] == df['VENTAS'].min()]
    min_day = min_day.iloc[0]['FCOM' if option == "Mostrar con Fecha y Hora" else 'FECHA']

    # Calcular la cantidad de días por encima y por debajo de la media
    days_above_average = sum(df['VENTAS'] > average)
    days_below_average = sum(df['VENTAS'] < average)

    # Crear el gráfico de ventas con Plotly Express
    fig = px.bar(df, x='FCOM' if option == "Mostrar con Fecha y Hora" else 'FECHA', y='VENTAS', title='Gráfico de Ventas')

    # Modificar los colores de las barras
    fig.update_traces(marker_color=['lightblue' if v < average else 'blue' for v in df['VENTAS']])

    fig.update_xaxes(title_text='Fecha de Venta')
    fig.update_yaxes(title_text='Cantidad de Ventas')

    # Agregar la línea de la media si se selecciona la opción
    if show_average:
        average_values = [average] * len(df)
        fig.add_trace(go.Scatter(x=df['FCOM' if option == "Mostrar con Fecha y Hora" else 'FECHA'], y=average_values, mode='lines', name='Media de Ventas'))

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

    if show_second_chart:
        # Consulta para obtener las fechas de ventas y contar la cantidad de ventas por fecha y sucursal para el período anterior
        if option == "Mostrar con Fecha y Hora":
            query_previous = f"""
            SELECT FCOM, COUNT(*) AS VENTAS
            FROM ERP$CVEN0100
            WHERE FCOM BETWEEN TO_DATE('{start_date_previous_str}', 'YYYY-MM-DD') AND TO_DATE('{end_date_previous_str}', 'YYYY-MM-DD')
            AND EMPR0110$NSUC IN ({', '.join(map(str, selected_sucursales))})
            GROUP BY FCOM
            """
        elif option == "Mostrar solo Fecha":
            query_previous = f"""
            SELECT TO_CHAR(FCOM, 'YYYY-MM-DD') AS FECHA, COUNT(*) AS VENTAS
            FROM ERP$CVEN0100
            WHERE FCOM BETWEEN TO_DATE('{start_date_previous_str}', 'YYYY-MM-DD') AND TO_DATE('{end_date_previous_str}', 'YYYY-MM-DD')
            AND EMPR0110$NSUC IN ({', '.join(map(str, selected_sucursales))})
            GROUP BY TO_CHAR(FCOM, 'YYYY-MM-DD')
            """
        else:
            query_previous = f"""
            SELECT TO_CHAR(FCOM, 'YYYY-MM') AS FECHA, COUNT(*) AS VENTAS
            FROM ERP$CVEN0100
            WHERE FCOM BETWEEN TO_DATE('{start_date_previous_str}', 'YYYY-MM-DD') AND TO_DATE('{end_date_previous_str}', 'YYYY-MM-DD')
            AND EMPR0110$NSUC IN ({', '.join(map(str, selected_sucursales))})
            GROUP BY TO_CHAR(FCOM, 'YYYY-MM')
            """

        # Ejecutar la consulta y obtener los datos del período anterior en un DataFrame
        df_previous = pd.read_sql(query_previous, conn)

        # Ordenar el DataFrame del período anterior por la columna de fechas
        df_previous = df_previous.sort_values(by=['FCOM' if option == "Mostrar con Fecha y Hora" else 'FECHA'], ascending=True)

        # Calcular la media del período anterior
        average_previous = round(df_previous['VENTAS'].mean(), 2)

        # Crear el gráfico de ventas para el período anterior
        fig_previous = px.bar(df_previous, x='FCOM' if option == "Mostrar con Fecha y Hora" else 'FECHA', y='VENTAS', title='Comparativo periodo anterior')

        # Modificar los colores de las barras
        fig_previous.update_traces(marker_color=['lightcoral' if v < average_previous else 'red' for v in df_previous['VENTAS']])

        fig_previous.update_xaxes(title_text='Fecha de Venta')
        fig_previous.update_yaxes(title_text='Cantidad de Ventas')

        # Agregar la línea de la media
        if show_average:
            average_values_previous = [average_previous] * len(df_previous)
            fig_previous.add_trace(go.Scatter(x=df_previous['FCOM' if option == "Mostrar con Fecha y Hora" else 'FECHA'], y=average_values_previous, mode='lines', name='Media de Ventas'))

        # Mostrar el gráfico del período anterior en Streamlit
        st.plotly_chart(fig_previous)

    # Cerrar la conexión a la base de datos
    conn.close()

    # Crear dos columnas para "Datos de Ventas" y "Información Descriptiva"
    col1, col2 = st.columns(2)

    # Columna 1: Datos de Ventas
    with col1:
        st.header("Datos de Ventas")
        st.dataframe(df, width=800)  # Aumentar el ancho de la tabla

    # Columna 2: Información Descriptiva
    with col2:
        st.header("Información Descriptiva")
        st.write("Este gráfico muestra la cantidad de tickets a lo largo del tiempo, podemos ver que:")
        st.write(f"El momento de mayor ventas fue: {max_day}, con: {df['VENTAS'].max()} tickets.")
        st.write(f"El momento de menos ventas fue: {min_day}, con: {df['VENTAS'].min()} tickets.")
        st.write(f"La media de tickets es: {average}, con: {days_above_average} registros por encima de la media ")
