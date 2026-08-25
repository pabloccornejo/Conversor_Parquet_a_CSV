import streamlit as st
import pandas as pd
import io

# Configuración de la página web
st.set_page_config(page_title="Conversor Parquet a CSV", page_icon="🔄", layout="centered")

# Título y descripción
st.title("🔄 Conversor de Parquet a CSV")
st.write("Sube tu archivo con extensión `.parquet` y descarga inmediatamente la versión `.csv`. Tus datos se procesan en memoria y no se guardan en ningún servidor externo.")

# Caja para subir el archivo
uploaded_file = st.file_uploader("Arrastra tu archivo aquí o haz clic para buscar", type=['parquet'])

if uploaded_file is not None:
    try:
        # 1. Leer archivo parquet
        df = pd.read_parquet(uploaded_file)
        st.success("¡Archivo leído correctamente!")
        
        # 2. Mostrar una pequeña vista previa (opcional, ayuda al usuario a ver que funcionó)
        st.write("Vista previa de los datos (primeras 5 filas):")
        st.dataframe(df.head())
        
        # 3. Convertir los datos a formato CSV en memoria
        csv_buffer = io.BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        # 4. Arreglar el nombre del archivo para la descarga
        nombre_original = uploaded_file.name
        # Limpiar si tiene doble extensión como te pasó antes
        if nombre_original.endswith('.parquet.parquet'):
            nombre_nuevo = nombre_original.replace('.parquet.parquet', '.csv')
        elif nombre_original.endswith('.parquet'):
            nombre_nuevo = nombre_original.replace('.parquet', '.csv')
        else:
            nombre_nuevo = "archivo_convertido.csv"
            
        # 5. Mostrar el botón gigante de descarga
        st.download_button(
            label="📥 Descargar archivo CSV ahora",
            data=csv_data,
            file_name=nombre_nuevo,
            mime="text/csv",
            type="primary" # Lo hace resaltar con color
        )
        
    except Exception as e:
        st.error(f"Hubo un error al procesar el archivo: {e}")