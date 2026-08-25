import streamlit as st
import pyarrow.parquet as pq
import os
import zipfile

# Configuración de la página web
st.set_page_config(page_title="Conversor Parquet a CSV", page_icon="🔄", layout="centered")

st.title("🔄 Conversor de Parquet a CSV (Modo ZIP)")
st.write("Sube tu archivo `.parquet`. Para evitar colapsos en el servidor web por el peso, el archivo CSV se entregará comprimido en un `.zip`.")

uploaded_file = st.file_uploader("Arrastra tu archivo aquí o haz clic para buscar", type=['parquet'])

if uploaded_file is not None:
    try:
        st.info("⏳ Procesando y comprimiendo... Esto tomará un momento.")
        
        # Nombres de archivos temporales
        ruta_parquet = "temp_uploaded.parquet"
        ruta_csv = "temp_convertido.csv"
        ruta_zip = "archivo_final.zip"
        
        # 1. Bajar el archivo al disco
        with open(ruta_parquet, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        # 2. Convertir por bloques (cuidando la RAM)
        archivo_pq = pq.ParquetFile(ruta_parquet)
        es_primer_lote = True
        
        for batch in archivo_pq.iter_batches():
            df_lote = batch.to_pandas()
            df_lote.to_csv(
                ruta_csv, 
                mode='a' if not es_primer_lote else 'w', 
                index=False, 
                header=es_primer_lote
            )
            es_primer_lote = False
            
        # 3. Comprimir el CSV de 1GB a un ZIP de ~100MB
        # Limpiar el nombre original para que el CSV y el ZIP se llamen igual
        nombre_base = uploaded_file.name.replace('.parquet.parquet', '').replace('.parquet', '')
        nombre_csv_interno = f"{nombre_base}.csv"
        nombre_zip_descarga = f"{nombre_base}.zip"
        
        with zipfile.ZipFile(ruta_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write(ruta_csv, arcname=nombre_csv_interno)
            
        st.success("¡Archivo procesado y comprimido con éxito!")
        
        # 4. Botón de descarga (Ahora lee un ZIP liviano)
        with open(ruta_zip, "rb") as f:
            st.download_button(
                label="📥 Descargar archivo ZIP",
                data=f,
                file_name=nombre_zip_descarga,
                mime="application/zip",
                type="primary"
            )
            
    except Exception as e:
        st.error(f"Hubo un error al procesar el archivo: {e}")
