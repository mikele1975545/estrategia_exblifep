
import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# --- Datos ficticios de ejemplo ---
zonas = ["Cataluña", "Madrid", "Andalucía"]
provincias = {
    "Cataluña": ["Barcelona", "Girona", "Lleida", "Tarragona"],
    "Madrid": ["Madrid"],
    "Andalucía": ["Sevilla", "Málaga", "Granada"]
}

bacterias_disponibles = [
    "Klebsiella pneumoniae",
    "Escherichia coli",
    "Pseudomonas aeruginosa",
    "Acinetobacter baumannii"
]

resistencias_disponibles = ["OXA-48", "BLEE", "NDM", "VIM"]

antibioticos = {
    "Cefepime/Enmetazobactam": {
        "Ventajas": "Mejor actividad frente a OXA-48 y BLEE. Amplio espectro.",
        "Desventajas": "Menos datos frente a NDM y no cubre anaerobios."
    },
    "Ceftazidima/Avibactam": {
        "Ventajas": "Activo frente a OXA-48 y algunas BLEE. Buena experiencia clínica.",
        "Desventajas": "Menor actividad frente a Pseudomonas multirresistente."
    },
    "Ceftolozano/Tazobactam": {
        "Ventajas": "Buena cobertura frente a Pseudomonas. Activo frente a BLEE.",
        "Desventajas": "No cubre OXA-48 ni NDM."
    }
}

siglas_info = {
    "OXA-48": "Betalactamasa de tipo OXA, común en Enterobacterias.",
    "BLEE": "Betalactamasas de espectro extendido.",
    "NDM": "Metalo-betalactamasa New Delhi.",
    "VIM": "Metalo-betalactamasa tipo Verona."
}

hospital_data = {}

# --- PDF exportación ---
def exportar_pdf(nombre_hospital, zona, provincia, bacterias, resistencias, estrategia):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Estrategia Exblifep - {nombre_hospital}", ln=True)
    pdf.cell(200, 10, f"Fecha: {datetime.today().strftime('%Y-%m-%d')}", ln=True)
    pdf.cell(200, 10, f"Zona: {zona} / Provincia: {provincia}", ln=True)
    pdf.cell(200, 10, "Bacterias y prevalencias:", ln=True)
    for b, p in bacterias:
        pdf.cell(200, 10, f"- {b}: {p}", ln=True)
    pdf.cell(200, 10, "Resistencias y prevalencias:", ln=True)
    for r, p in resistencias:
        pdf.cell(200, 10, f"- {r}: {p}", ln=True)
    pdf.multi_cell(200, 10, f"Estrategia recomendada:
{estrategia}")
    filename = f"/mnt/data/estrategia_{nombre_hospital.replace(' ', '_')}.pdf"
    pdf.output(filename)
    return filename

# --- UI ---
st.title("Estrategia Exblifep - Actualizado")
seccion = st.sidebar.radio("Selecciona una sección:", ["Estrategia por hospital", "Comparativa entre antibióticos"])

if seccion == "Estrategia por hospital":
    st.header("Estrategia personalizada")
    nombre_hospital = st.text_input("Nombre del hospital")
    zona = st.selectbox("Selecciona la comunidad autónoma", zonas)
    provincia = st.selectbox("Selecciona la provincia", provincias[zona])

    st.subheader("Bacterias más frecuentes")
    bacterias_elegidas = st.multiselect("Selecciona bacterias", bacterias_disponibles)
    bacterias = [(b, st.selectbox(f"Prevalencia de {b}", ["<10%", "10-25%", "25-50%", ">50%"], key=b)) for b in bacterias_elegidas]

    st.subheader("Resistencias más frecuentes")
    resistencias_elegidas = st.multiselect("Selecciona resistencias", resistencias_disponibles)
    resistencias = [(r, st.selectbox(f"Prevalencia de {r}", ["<10%", "10-25%", "25-50%", ">50%"], key=r)) for r in resistencias_elegidas]

    if st.button("Analizar estrategia"):
        estrategia = "Usar Cefepime/Enmetazobactam como primera línea por actividad frente a BLEE y OXA-48. "
        if any(r[0] == "NDM" for r in resistencias):
            estrategia += "Considerar alternativas por presencia de NDM."
        st.success(estrategia)

        hospital_data[nombre_hospital] = {
            "zona": zona, "provincia": provincia,
            "bacterias": bacterias, "resistencias": resistencias, "estrategia": estrategia
        }

        pdf_file = exportar_pdf(nombre_hospital, zona, provincia, bacterias, resistencias, estrategia)
        with open(pdf_file, "rb") as f:
            st.download_button("📄 Descargar estrategia en PDF", f, file_name=pdf_file.split("/")[-1])

elif seccion == "Comparativa entre antibióticos":
    st.header("Comparativa entre antibióticos")
    opciones = list(antibioticos.keys())
    a1 = st.selectbox("Antibiótico 1", opciones)
    a2 = st.selectbox("Antibiótico 2", opciones, index=1)

    if a1 != a2:
        st.markdown(f"**{a1}**")
        st.markdown(f"- **Ventajas**: {antibioticos[a1]['Ventajas']}")
        st.markdown(f"- **Desventajas**: {antibioticos[a1]['Desventajas']}")
        st.markdown("---")
        st.markdown(f"**{a2}**")
        st.markdown(f"- **Ventajas**: {antibioticos[a2]['Ventajas']}")
        st.markdown(f"- **Desventajas**: {antibioticos[a2]['Desventajas']}")

# Leyenda
with st.expander("📘 Leyenda de abreviaturas"):
    for sigla, definicion in siglas_info.items():
        st.markdown(f"- **{sigla}**: {definicion}")
