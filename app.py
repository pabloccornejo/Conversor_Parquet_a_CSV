import streamlit as st
import pyarrow.parquet as pq
import os

# Configuración de la página web
st.set_page_config(page_title="Conversor Parquet a CSV", page_icon="🔄", layout="centered")

st.title("🔄 Conversor de Parquet a CSV (Modo Pesado)")
st.write("Sube tu archivo con extensión `.parquet`. Esta versión procesa los datos por bloques para manejar archivos de más de 1 GB sin colapsar.")

uploaded_file = st.file_uploader("Arrastra tu archivo aquí o haz clic para buscar", type=['parquet'])

if uploaded_file is not None:
    try:
        st.info("⏳ Procesando archivo gigante por bloques... Esto mantendrá el servidor estable.")
        
        # 1. Bajar el archivo de la RAM al disco físico del servidor primero
        ruta_parquet = "temp_uploaded.parquet"
        with open(ruta_parquet, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        # 2. Procesamiento iterativo (Chunking) usando PyArrow para cuidar la RAM
        ruta_csv = "archivo_temporal.csv"
        archivo_pq = pq.ParquetFile(ruta_parquet)
        
        es_primer_lote = True
        # Leer y escribir el archivo en bloques pequeños
        for batch in archivo_pq.iter_batches():
            df_lote = batch.to_pandas()
            
            # Escribir al CSV (añadiendo al final del archivo con mode='a')
            df_lote.to_csv(
                ruta_csv, 
                mode='a' if not es_primer_lote else 'w', 
                index=False, 
                header=es_primer_lote
            )
            es_primer_lote = False
            
        st.success("¡Archivo de 1GB procesado y convertido con éxito!")
        
        # 3. Arreglar el nombre para la descarga
        nombre_original = uploaded_file.name
        if nombre_original.endswith('.parquet.parquet'):
            nombre_nuevo = nombre_original.replace('.parquet.parquet', '.csv')
        elif nombre_original.endswith('.parquet'):
            nombre_nuevo = nombre_original.replace('.parquet', '.csv')
        else:
            nombre_nuevo = "archivo_convertido.csv"
            
        # 4. Botón de descarga (Streamlit lo transmite desde el disco sin saturar la RAM)
        with open(ruta_csv, "rb") as f:
            st.download_button(
                label="📥 Descargar archivo CSV completo",
                data=f,
                file_name=nombre_nuevo,
                mime="text/csv",
                type="primary"
            )
            
    except Exception as e:
        st.error(f"Hubo un error al procesar el archivo: {e}")
