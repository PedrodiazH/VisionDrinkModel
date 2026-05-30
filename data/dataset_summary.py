"""
Generador de Reporte Dinámico del Dataset
Lee la metadata de los archivos, cruza con biometría estática y actualiza el Markdown.
"""

import os
import re
import pandas as pd

# Rutas
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(DATA_DIR, "raw")
OUTPUT_MD = os.path.join(DATA_DIR, "..", "DATASET_SUMMARY.md")

# Diccionario de control biométrico (Actualiza con los datos reales)
PESOS_SUJETOS = {
    "Pedro": 78.5,
    "Amigo1": 80.0
}

def generar_reporte():
    if not os.path.exists(RAW_DIR):
        print("[-] Directorio raw/ no encontrado.")
        return

    archivos = [f for f in os.listdir(RAW_DIR) if f.endswith(".png")]
    datos = []

    # Parseo del formato: pedro_3cervezas_30-03-2026.png
    patron_ingesta = re.compile(r"(\d+)([a-zA-Z]+)") 

    for archivo in archivos:
        nombre_base = archivo.replace(".png", "")
        partes = nombre_base.split("_")
        
        if len(partes) == 3:
            nombre, ingesta, fecha = partes
            sujeto_cap = nombre.capitalize()
            match = patron_ingesta.match(ingesta)
            
            if match:
                cantidad, bebida = match.groups()
            else:
                cantidad, bebida = 1, ingesta
                
            datos.append({
                "Sujeto": sujeto_cap,
                "Peso (kg)": PESOS_SUJETOS.get(sujeto_cap, "N/A"),
                "Tragos": int(cantidad),
                "Bebida": bebida.capitalize(),
                "Fecha": fecha
            })

    if not datos:
        print("[-] No hay imágenes para analizar.")
        return

    df = pd.DataFrame(datos)

    # Transformación de fecha para ordenamiento analítico temporal
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce', dayfirst=True)

    # Agrupaciones
    resumen_sujetos = df.groupby(["Sujeto", "Peso (kg)"]).size().reset_index(name="Imágenes Totales")
    resumen_bebidas = df.groupby("Bebida").size().reset_index(name="Capturas Totales")
    
    # Trazabilidad temporal (Sesiones)
    historial_sesiones = df.groupby([df['Fecha'].dt.strftime('%d-%m-%Y'), "Sujeto"]).size().reset_index(name="Fotos en Sesión")
    historial_sesiones.rename(columns={'Fecha': 'Fecha Sesión'}, inplace=True)

    # Construcción del Markdown
    md = "# 📊 Estado Actual del Dataset\n\n"
    md += f"> **Total de imágenes crudas disponibles:** `{len(df)}`\n\n"
    
    md += "### 👤 Sujetos y Biometría\n"
    md += resumen_sujetos.to_markdown(index=False) + "\n\n"
    
    md += "### 🍺 Distribución por Bebida\n"
    md += resumen_bebidas.to_markdown(index=False) + "\n\n"

    md += "### 📅 Historial de Sesiones\n"
    md += historial_sesiones.to_markdown(index=False) + "\n"

    # Escribir a disco
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"[+] Reporte generado con éxito en: {OUTPUT_MD}")

if __name__ == "__main__":
    generar_reporte()