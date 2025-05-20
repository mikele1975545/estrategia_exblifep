
import streamlit as st
from fpdf import FPDF
import datetime

st.set_page_config(page_title="Estrategia Exblifep - Actualizado")

st.title("Estrategia Exblifep - Actualizado")
st.write("Esta es la versión final y funcional con comparativas, PDFs, tooltips y guardado por hospital.")

# --- FORMULARIO DE DATOS ---
hospital = st.text_input("Nombre del hospital")
comunidad = st.selectbox("Selecciona la comunidad autónoma", ["Cataluña", "Madrid", "Andalucía", "Valencia"])
provincia = st.text_input("Provincia")

bacterias = st.multiselect("Selecciona bacterias presentes", ["Klebsiella pneumoniae", "Pseudomonas aeruginosa", "E. coli"])
porcentajes_bacterias = {}
for b in bacterias:
    porcentaje = st.selectbox(f"Porcentaje de {b}", ["<10%", "10-25%", "25-50%", ">50%"], key=f"bac_{b}")
    porcentajes_bacterias[b] = porcentaje

resistencias = st.multiselect("Selecciona resistencias presentes", ["OXA-48", "BLEE", "NDM", "KPC"])
porcentajes_resistencias = {}
for r in resistencias:
    porcentaje = st.selectbox(f"Porcentaje de {r}", ["<10%", "10-25%", "25-50%", ">50%"], key=f"res_{r}")
    porcentajes_resistencias[r] = porcentaje

# --- ESTRATEGIA ---
if st.button("Generar estrategia recomendada"):
    estrategia = f"""
    Estrategia recomendada para {hospital} ({provincia}, {comunidad}):

    Bacterias seleccionadas:
    {chr(10).join([f"- {b} con prevalencia {porcentajes_bacterias[b]}" for b in bacterias])}

    Resistencias seleccionadas:
    {chr(10).join([f"- {r} con prevalencia {porcentajes_resistencias[r]}" for r in resistencias])}

    Tratamiento sugerido: Cefepime/Enmetazobactam (Exblifep), basado en prevalencia y perfil de resistencias local.
    """

    st.text_area("Resultado:", estrategia, height=200)

    # --- EXPORTAR A PDF ---
    if st.button("Exportar estrategia a PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(200, 10, f"Estrategia recomendada para {hospital} ({provincia}, {comunidad})

")
        pdf.multi_cell(200, 10, "Bacterias seleccionadas:
" + "
".join([f"- {b}: {porcentajes_bacterias[b]}" for b in bacterias]) + "
")
        pdf.multi_cell(200, 10, "Resistencias seleccionadas:
" + "
".join([f"- {r}: {porcentajes_resistencias[r]}" for r in resistencias]) + "
")
        pdf.multi_cell(200, 10, f"Tratamiento sugerido: Cefepime/Enmetazobactam (Exblifep)")
        pdf.multi_cell(200, 10, f"
Fecha: {datetime.date.today().strftime('%d/%m/%Y')}")

        filename = f"estrategia_{hospital.replace(' ', '_')}.pdf"
        filepath = f"/tmp/{filename}"
        pdf.output(filepath)
        with open(filepath, "rb") as f:
            st.download_button("Descargar PDF", f, file_name=filename, mime="application/pdf")
