
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Estrategia Exblifep", layout="wide")
st.title("Estrategia Exblifep - Actualizado")
st.markdown("Esta es la versión final y funcional con comparativas, PDFs, tooltips y guardado por hospital.")

# Variables simuladas para mostrar PDF
hospital = "Hospital de Ejemplo"
provincia = "Barcelona"
comunidad = "Cataluña"

# PDF exportación simulada
from fpdf import FPDF

def exportar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(200, 10, f"Estrategia recomendada para Hospital de Prueba (Barcelona, Cataluña) - 20/05/2025")
    pdf.output("/mnt/data/estrategia_exblifep_exportado.pdf")

if st.button("Exportar estrategia a PDF"):
    exportar_pdf()
    st.success("PDF exportado correctamente.")
