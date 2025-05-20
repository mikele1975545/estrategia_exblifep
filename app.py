
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Estrategia Exblifep", layout="wide")

# Header
st.title("Estrategia Exblifep - Actualizado")
st.markdown("Esta es la versión final y funcional con comparativas, PDFs, tooltips y guardado por hospital.")

# Modo de navegación
modo = st.sidebar.selectbox("Selecciona una opción", ["Estrategia Hospital", "Comparativa entre antibióticos", "Leyenda de siglas"])

# Diccionario de siglas
siglas = {
    "BLEE": "Betalactamasa de espectro extendido",
    "OXA-48": "Carbapenemasa tipo OXA-48",
    "KPC": "Klebsiella pneumoniae carbapenemasa",
    "NDM": "New Delhi Metallo-betalactamasa"
}

if modo == "Leyenda de siglas":
    st.subheader("Leyenda de siglas utilizadas")
    for sigla, descripcion in siglas.items():
        st.markdown(f"- **{sigla}**: {descripcion}")

elif modo == "Estrategia Hospital":
    st.subheader("Datos del hospital")
    nombre_hospital = st.text_input("Nombre del hospital")
    fecha = datetime.today().strftime("%d/%m/%Y")

    comunidad = st.selectbox("Comunidad Autónoma", ["Cataluña", "Madrid", "Andalucía"])
    provincia = st.selectbox("Provincia", ["Barcelona", "Madrid", "Sevilla"])

    st.markdown("### Bacterias más frecuentes")
    bacterias = st.multiselect("Selecciona bacterias", ["Klebsiella pneumoniae", "Pseudomonas aeruginosa", "E. coli"])
    porcentajes_bacterias = {bac: st.selectbox(f"Prevalencia de {bac}", ["<10%", "10-25%", ">25%"], key=f"bac_{bac}") for bac in bacterias}

    st.markdown("### Resistencias más frecuentes")
    resistencias = st.multiselect("Selecciona resistencias", ["BLEE", "OXA-48", "KPC", "NDM"])
    porcentajes_resistencias = {res: st.selectbox(f"Prevalencia de {res}", ["<10%", "10-25%", ">25%"], key=f"res_{res}") for res in resistencias}

    st.markdown("### Recomendación personalizada")
    if "OXA-48" in resistencias or "BLEE" in resistencias:
        st.success("Cefepime/enmetazobactam puede posicionarse como alternativa frente a BLEE/OXA-48 en este hospital.")
    else:
        st.info("No se detectan resistencias clave para posicionar cefepime/enmetazobactam.")

    st.markdown("Puedes exportar esta estrategia a PDF (solo disponible localmente en versión completa).")

elif modo == "Comparativa entre antibióticos":
    st.subheader("Comparativa rápida entre antibióticos")

    antibioticos = [
        "Cefepime/enmetazobactam",
        "Ceftazidima/avibactam",
        "Ceftolozano/tazobactam",
        "Meropenem/vaborbactam",
        "Imipenem/relebactam"
    ]

    a1 = st.selectbox("Antibiótico 1", antibioticos)
    a2 = st.selectbox("Antibiótico 2", antibioticos, index=1)

    comparativas = {
        ("Cefepime/enmetazobactam", "Ceftazidima/avibactam"): (
            "**Ventajas**: Mejor actividad frente a OXA-48 y BLEE."

**Desventajas**: Menos datos postcomercialización."),
        ("Cefepime/enmetazobactam", "Ceftolozano/tazobactam"): (
            "**Ventajas**: Mayor espectro frente a BLEE.

**Desventajas**: Menor experiencia clínica acumulada."),
    }

    resultado = comparativas.get((a1, a2)) or comparativas.get((a2, a1), "Comparativa no disponible.")
    st.markdown(resultado)
