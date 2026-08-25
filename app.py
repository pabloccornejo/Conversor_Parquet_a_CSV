import streamlit as st
import pandas as pd
import os

# Configuración de la página web
st.set_page_config(page_title="Conversor Parquet a CSV", page_icon="🔄", layout="centered")

# Título y descripción
st.title("🔄 Conversor de Parquet a CSV")
st.write("Sube tu archivo con extensión `.parquet` y descarga inmediatamente la versión `.csv`.")

# Caja para subir el archivo
uploaded_file = st.file_uploader("Arrastra tu archivo aquí o haz clic para buscar", type=['parquet'])

if uploaded_file is not None:
    try:
        st.info("⏳ Procesando archivo pesado... Esto puede tomar un momento.")
        
        # 1. Leer archivo parquet
        df = pd.read_parquet(uploaded_file)
        st.success("¡Archivo leído correctamente!")
        
        # 2. Mostrar una pequeña vista previa
        st.write("Vista previa de los datos (primeras 5 filas):")
        st.dataframe(df.head())
        
        # 3. ESTA ES LA CLAVE: Guardar temporalmente en el disco en vez de la RAM
        ruta_temporal = "archivo_temporal.csv"
        df.to_csv(ruta_temporal, index=False)
        
        # 4. Arreglar el nombre del archivo para la descarga
        nombre_original = uploaded_file.name
        if nombre_original.endswith('.parquet.parquet'):
            nombre_nuevo = nombre_original.replace('.parquet.parquet', '.csv')
        elif nombre_original.endswith('.parquet'):
            nombre_nuevo = nombre_original.replace('.parquet', '.csv')
        else:
            nombre_nuevo = "archivo_convertido.csv"
            
        # 5. Botón de descarga leyendo directamente desde el disco
        with open(ruta_temporal, "rb") as f:
            st.download_button(
                label="📥 Descargar archivo CSV de 1GB ahora",
                data=f,
                file_name=nombre_nuevo,
                mime="text/csv",
                type="primary"
            )
            
    except Exception as e:
        st.error(f"Hubo un error al procesar el archivo: {e}")
