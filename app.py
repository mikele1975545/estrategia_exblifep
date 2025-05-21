
import streamlit as st
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="Estrategia Exblifep", layout="wide")

st.title("Estrategia Exblifep - Actualizado")
st.markdown("Esta es la versión final con comparativas, PDFs, siglas explicadas y estrategia por hospital.")

tab1, tab2 = st.tabs(["📊 Estrategia por hospital", "⚖️ Comparativa entre antibióticos"])

bacterias = ["Klebsiella pneumoniae", "Escherichia coli", "Pseudomonas aeruginosa"]
resistencias = ["BLEE", "OXA-48", "KPC", "NDM"]
porcentajes = ["<10%", "10-25%", "25-50%", ">50%"]

abreviaturas = {
    "BLEE": "Betalactamasas de espectro extendido",
    "OXA-48": "Oxacilinasa tipo 48",
    "KPC": "Klebsiella pneumoniae carbapenemasa",
    "NDM": "New Delhi metalo-beta-lactamasa",
}

antibioticos = {
    "Cefepime/enmetazobactam": {
        "Ventajas": "Alta actividad frente a BLEE y OXA-48.",
        "Desventajas": "Menos experiencia clínica disponible.",
    },
    "Ceftazidima/avibactam": {
        "Ventajas": "Experiencia clínica y buena cobertura BLEE/OXA-48.",
        "Desventajas": "Ineficaz frente a NDM.",
    },
}

# TAB 1
with tab1:
    hospital = st.text_input("Nombre del hospital")
    comunidad = st.selectbox("Comunidad autónoma", ["Cataluña", "Madrid", "Andalucía"])
    provincia = st.text_input("Provincia")

    st.subheader("Bacterias más frecuentes")
    bacterias_sel = st.multiselect("Selecciona bacterias", bacterias)
    bac_pct = {b: st.selectbox(f"{b} (%)", porcentajes, key=b) for b in bacterias_sel}

    st.subheader("Resistencias más frecuentes")
    resistencias_sel = st.multiselect("Selecciona resistencias", resistencias)
    res_pct = {r: st.selectbox(f"{r} (%)", porcentajes, key=r) for r in resistencias_sel}

    estrategia = f"Estrategia recomendada para {hospital} en {provincia}, {comunidad}:
"
    estrategia += "Bacterias:
" + "\n".join([f"- {b}: {bac_pct[b]}" for b in bac_pct]) + "\n"
    estrategia += "Resistencias:
" + "\n".join([f"- {r}: {res_pct[r]} ({abreviaturas.get(r, '')})" for r in res_pct])

    if st.button("Ver estrategia"):
        st.text_area("Resultado", estrategia, height=300)

    if st.button("Exportar a PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(200, 10, estrategia)
        nombre = f"estrategia_{hospital.replace(' ', '_')}.pdf"
        path = f"/mnt/data/{nombre}"
        pdf.output(path)
        with open(path, "rb") as f:
            st.download_button("📥 Descargar PDF", f, file_name=nombre)

# TAB 2
with tab2:
    a1 = st.selectbox("Antibiótico 1", list(antibioticos.keys()), key="a1")
    a2 = st.selectbox("Antibiótico 2", list(antibioticos.keys()), key="a2")

    if a1 != a2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"### {a1}")
            st.markdown(f"**Ventajas**: {antibioticos[a1]['Ventajas']}")
            st.markdown(f"**Desventajas**: {antibioticos[a1]['Desventajas']}")
        with col2:
            st.markdown(f"### {a2}")
            st.markdown(f"**Ventajas**: {antibioticos[a2]['Ventajas']}")
            st.markdown(f"**Desventajas**: {antibioticos[a2]['Desventajas']}")

# Leyenda
with st.expander("📘 Leyenda de abreviaturas"):
    for sigla, texto in abreviaturas.items():
        st.markdown(f"- **{sigla}**: {texto}")
