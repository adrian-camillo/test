import streamlit as st
import cx_Oracle

# Datos de conexión
host = '129.151.97.98'
port = 1521
service_name = 'INTDB5_pdb1.sub12222046451.net1.oraclevcn.com'
user = 'INTH1070$NICO'
password = 'NIco*(78227$$13'

# Crear el string de conexión
try:
    connection = cx_Oracle.connect(f"{user}/{password}@{host}:{port}/{service_name}")
except cx_Oracle.DatabaseError as e:
    st.error("Error de conexión a la base de datos: {}".format(str(e)))
    st.stop()

# Crear la interfaz de usuario con Streamlit
st.title("Consulta de Remito")

# Obtener el código de remito ingresado por el usuario
codigo = st.text_input("Código de Remito:")

# Botón para realizar la consulta
if st.button("Consultar"):
    # Realizar la consulta SQL con el código ingresado y mostrar los resultados
    cursor = connection.cursor()
    query = f"SELECT CODI AS remito, EMPR0110$NSUC as desde, stkd0100$id_orig as hasta, FDES as fecha_de_envio, FING as fecha_recibido, AUDI0100$ID FROM erp$stkm0100 WHERE CODI = {codigo} AND EMPR0100$ID = 1"
    cursor.execute(query)
    resultado = cursor.fetchone()

    if resultado:
        st.write("Remito:", resultado[0])
        st.write("Desde:", resultado[1])
        st.write("Hasta:", resultado[2])
        st.write("Fecha de Envío:", resultado[3])
        st.write("Fecha Recibido:", resultado[4])

        # Obtener la persona asociada al remito
        cursor.execute(f"SELECT USRN FROM ERP$AUDI0100 WHERE ID = {resultado[5]}")
        usuario = cursor.fetchone()

        if usuario:
            st.write("Persona Asociada:", usuario[0])
        else:
            st.warning("No se encontró la persona asociada.")
    else:
        st.warning("No se encontraron resultados.")

# Cierre de la conexión al salir de la aplicación
st.experimental_set_query_params()
connection.close()
