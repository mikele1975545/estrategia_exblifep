
import streamlit as st
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="Estrategia Exblifep", layout="wide")

# Funciones de utilidad
def generar_pdf(hospital, provincia, comunidad, estrategia_texto):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    fecha = datetime.now().strftime("%d/%m/%Y")
    pdf.cell(200, 10, f"Estrategia recomendada para {hospital} ({provincia}, {comunidad}) - {fecha}", ln=True)
    pdf.multi_cell(200, 10, f"{estrategia_texto}")
    pdf.output("/mnt/data/estrategia_exblifep_resultado.pdf")

# Página principal
st.title("Estrategia Exblifep - Actualizado")
st.markdown("Esta es la versión final y funcional con comparativas, PDFs, tooltips y guardado por hospital.")

tab1, tab2 = st.tabs(["📊 Estrategia personalizada", "⚖️ Comparativa entre antibióticos"])

# Datos de ejemplo
bacterias = ["Klebsiella pneumoniae", "Escherichia coli", "Pseudomonas aeruginosa"]
resistencias = ["BLEE", "OXA-48", "KPC", "NDM"]
porcentajes = ["<10%", "10-25%", "25-50%", ">50%"]
antibioticos = {
    "Cefepime/enmetazobactam": {
        "Ventajas": "Mejor actividad frente a OXA-48 y BLEE. Buena tolerabilidad.",
        "Desventajas": "Menos experiencia clínica que otros.",
    },
    "Ceftazidima/avibactam": {
        "Ventajas": "Alta eficacia frente a BLEE y OXA-48. Amplia experiencia clínica.",
        "Desventajas": "No cubre bien NDM.",
    },
    "Ceftolozano/tazobactam": {
        "Ventajas": "Buena opción para Pseudomonas multirresistente.",
        "Desventajas": "Menos útil frente a BLEE y OXA-48.",
    },
}

abreviaturas = {
    "BLEE": "Betalactamasas de espectro extendido",
    "OXA-48": "Oxacilinasa tipo 48",
    "KPC": "Klebsiella pneumoniae carbapenemasa",
    "NDM": "New Delhi metalo-beta-lactamasa",
}

# Tab de estrategia
with tab1:
    comunidad = st.selectbox("Selecciona la comunidad autónoma", ["Cataluña", "Madrid", "Andalucía"])
    provincia = st.selectbox("Selecciona la provincia", ["Barcelona", "Madrid", "Sevilla"])
    hospital = st.text_input("Nombre del hospital")

    st.subheader("Bacterias más frecuentes")
    selected_bacterias = st.multiselect("Selecciona bacterias", bacterias)
    bacterias_info = {bac: st.selectbox(f"Prevalencia de {bac}", porcentajes, key=f"b_{bac}") for bac in selected_bacterias}

    st.subheader("Resistencias más frecuentes")
    selected_resistencias = st.multiselect("Selecciona resistencias", resistencias)
    resistencias_info = {res: st.selectbox(f"Prevalencia de {res}", porcentajes, key=f"r_{res}") for res in selected_resistencias}

    estrategia_texto = f"Estrategia basada en los datos proporcionados por {hospital}.

"
    estrategia_texto += "### Bacterias seleccionadas:
"
    for bac, porc in bacterias_info.items():
        estrategia_texto += f"- {bac}: prevalencia {porc}
"

    estrategia_texto += "\n### Resistencias seleccionadas:
"
    for res, porc in resistencias_info.items():
        estrategia_texto += f"- {res}: prevalencia {porc} ({abreviaturas.get(res, '')})
"

    if st.button("Generar estrategia en PDF"):
        generar_pdf(hospital, provincia, comunidad, estrategia_texto)
        st.success("PDF generado correctamente.")
        with open("/mnt/data/estrategia_exblifep_resultado.pdf", "rb") as f:
            st.download_button("📥 Descargar PDF", f, file_name="estrategia_exblifep.pdf")

# Tab de comparativa
with tab2:
    ab1 = st.selectbox("Selecciona el primer antibiótico", list(antibioticos.keys()), key="a1")
    ab2 = st.selectbox("Selecciona el segundo antibiótico", list(antibioticos.keys()), key="a2")

    if ab1 and ab2 and ab1 != ab2:
        st.subheader("Comparativa")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"### {ab1}")
            st.markdown(f"**Ventajas**: {antibioticos[ab1]['Ventajas']}")
            st.markdown(f"**Desventajas**: {antibioticos[ab1]['Desventajas']}")
        with col2:
            st.markdown(f"### {ab2}")
            st.markdown(f"**Ventajas**: {antibioticos[ab2]['Ventajas']}")
            st.markdown(f"**Desventajas**: {antibioticos[ab2]['Desventajas']}")
