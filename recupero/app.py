import streamlit as st
import pandas as pd
import chardet
import os
st.set_page_config(page_title="APP recupero", page_icon="https://raw.githubusercontent.com/adrian-camillo/repo_imagenes_nico/bc6185aef3016dfba0eb753a8b9a5b6c7d05dc4a/SVG%20ROJO.svg")

def cargar_archivos():
    st.sidebar.header("Cargar archivos")
    
    # Obtener el directorio del script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Archivo de clientes
    clientes_file = st.sidebar.file_uploader("Seleccione el archivo de clientes a consultar", type=["csv", "xlsx"])
    clientes_path = guardar_archivo(script_directory, clientes_file)
    
    # Archivo de ventas
    ventas_file = st.sidebar.file_uploader("Seleccione el archivo de ventas", type=["csv", "xlsx"])
    ventas_path = guardar_archivo(script_directory, ventas_file)
    
    return clientes_path, ventas_path

def eliminar_archivo_si_existe(archivo_path):
    if os.path.exists(archivo_path):
        os.remove(archivo_path)
        st.info(f"Se eliminó el archivo existente: {archivo_path}")

def guardar_archivo(script_directory, uploaded_file):
    if uploaded_file:
        # Obtener la ruta completa y eliminar el archivo si ya existe
        archivo_path = os.path.join(script_directory, uploaded_file.name)
        eliminar_archivo_si_existe(archivo_path)

        # Guardar el archivo
        with open(archivo_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        st.success(f"Se cargó el archivo: {archivo_path}")
        return archivo_path
    return None

def detectar_codificacion(archivo_path):
    if archivo_path.lower().endswith('.csv'):
        # Si es un archivo CSV, intentar detectar la codificación usando chardet
        with open(archivo_path, 'rb') as f:
            result = chardet.detect(f.read())
        
        # Leer las primeras 10 líneas para encontrar la línea problemática
        with open(archivo_path, 'r', encoding='utf-8', errors='replace') as f:
            lines = [next(f) for _ in range(10)]

        return result['encoding'] if result['encoding'] else 'ISO-8859-1', lines
    else:
        # Si es un archivo Excel (xlsx), no necesitamos detectar la codificación
        return None, None

def filtrar_registros(clientes_df, ventas_df):
    # Extraer la columna "DNI" del archivo de clientes
    clientes_dnies = clientes_df['DNI'].astype(str)

    # Utilizar str.contains para buscar coincidencias parciales en el archivo de ventas
    resultados_df = ventas_df[ventas_df['DNI'].astype(str).apply(lambda x: any(dni in x for dni in clientes_dnies))]

    return resultados_df

def main():
    st.title("Aplicación de Filtrado de Clientes")
    
    clientes_path, ventas_path = cargar_archivos()
    
    if clientes_path and ventas_path:
        # Detectar codificación de clientes_file
        clientes_encoding, clientes_lines = detectar_codificacion(clientes_path)
        
        try:
            # Cargar datos en pandas DataFrame
            if clientes_path.lower().endswith('.csv'):
                clientes_df = pd.read_csv(clientes_path, encoding=clientes_encoding)
            elif clientes_path.lower().endswith('.xlsx'):
                clientes_df = pd.read_excel(clientes_path)
            else:
                st.error("Formato de archivo no compatible. Utilice archivos CSV o Excel.")
                return
        except pd.errors.ParserError:
            st.error("Error al leer el archivo de clientes. Verifica el formato y delimitador del archivo.")
            st.error(f"Líneas del archivo de clientes: {clientes_lines}")
            return
        
        # Detectar codificación de ventas_file
        ventas_encoding, _ = detectar_codificacion(ventas_path)
        
        try:
            if ventas_path.lower().endswith('.csv'):
                ventas_df = pd.read_csv(ventas_path, encoding=ventas_encoding)
            elif ventas_path.lower().endswith('.xlsx'):
                ventas_df = pd.read_excel(ventas_path)
            else:
                st.error("Formato de archivo no compatible. Utilice archivos CSV o Excel.")
                return
        except pd.errors.ParserError:
            st.error("Error al leer el archivo de ventas. Verifica el formato y delimitador del archivo.")
            return

        # Filtrar registros solo si se cargaron ambos DataFrames correctamente
        st.subheader(f"Clientes a Consultar ({len(clientes_df)} filas):")
        st.write(clientes_df)
        
        st.subheader(f"Archivo de Ventas ({len(ventas_df)} filas):")
        st.write(ventas_df)
        
        resultados_df = filtrar_registros(clientes_df, ventas_df)

        st.subheader(f"Resultados del Filtrado ({len(resultados_df)} filas):")
        st.write(resultados_df)
    else:
        st.warning("Por favor, cargue ambos archivos.")

if __name__ == "__main__":
    main()
