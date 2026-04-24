import streamlit as st

# --- LÓGICA DE ESCALAS ---
NOTAS_MUSICALES = ["Do", "Do#", "Re", "Re#", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "La#", "Si"]
BEMOLES = {"Reb": "Do#", "Mib": "Re#", "Solb": "Fa#", "Lab": "Sol#", "Sib": "La#"}

def generar_escala(tonica, modo):
    pasos = [2, 2, 1, 2, 2, 2, 1] if modo == "mayor" else [2, 1, 2, 2, 1, 2, 2]
    t_limpia = tonica.capitalize().replace(" ", "")
    t_limpia = BEMOLES.get(t_limpia, t_limpia)
    if t_limpia not in NOTAS_MUSICALES: return None
    idx = NOTAS_MUSICALES.index(t_limpia)
    escala = []
    actual = idx
    for p in pasos:
        escala.append(NOTAS_MUSICALES[actual % 12])
        actual += p
    return escala

# --- REPARTO Y TABLATURA ---
TABLATURA = {
    "Re0": "7", "Mi0": "6", "Fa#0": "6", "Si0": "7",
    "Sol": "5", "La": "5", "Si": "4", "Do": "4", "Re": "3", "Mi": "3", "Fa#": "2",
    "Sol2": "2", "La2": "1", "Si2": "1"
}
NOTAS_ARKA = ["Re0", "Fa#0", "La", "Do", "Mi", "Sol2", "Si2"]
NOTAS_IRA  = ["Si0", "Mi0", "Sol", "Si", "Re", "Fa#", "La2"]

# --- INTERFAZ WEB ---
st.set_page_config(page_title="SikuTab", page_icon="🎶", layout="wide")
st.title("🎶 SikuTab: Transpositor Arka/Ira")
st.caption("Prof. Pablo Olivero - Liceo San José del Carmen")

# --- CONFIGURACIÓN ---
col_t, col_m = st.columns([1, 1])
with col_t:
    original_tonica = st.selectbox("Tonalidad Original", NOTAS_MUSICALES)
with col_m:
    modo = st.radio("Modo", ["Mayor", "Menor"], horizontal=True)

# --- GUÍA DESPLEGABLE ---
with st.expander("📖 Guía de Octavas y Límites del Instrumento"):
    st.write("""
    **Cómo escribir las notas:**
    - **Registro Medio:** Escribe la nota normal (ej: `do`, `re`, `fa#`).
    - **Registro Agudo:** Agrega un **2** (ej: `do2`, `re2`).
    - **Registro Grave:** Agrega un **0** (ej: `re0`, `mi0`).

    **⚠️ Nota Importante sobre los Límites:**
    El Siku tiene un registro físico limitado. Si al transponer una nota esta cae fuera de los límites (Re0 a Si2),
    el sistema mostrará un **[?]**. En ese caso, deberás **adaptar la melodía** subiendo o bajando la octava de esa nota
    específica en tu entrada original para que el resultado sea ejecutable en el instrumento.

    *Límites del Siku:*
    - **Grave:** Re0, Mi0, Fa#0, Si0
    - **Medio:** Sol, La, Si, Do, Re, Mi, Fa#
    - **Agudo:** Sol2, La2, Si2
    """)

entrada = st.text_area("Escribe la melodía aquí:", placeholder="Ejemplo: re0 mi0 sol la do2", height=150)

# Botón para procesar
procesar = st.button("🚀 Procesar Melodía")

if procesar and entrada:
    ref_original = generar_escala(original_tonica, modo.lower())
    dest, nombre_final = (["Sol", "La", "Si", "Do", "Re", "Mi", "Fa#"], "SOL MAYOR") if modo == "Mayor" else (["Mi", "Fa#", "Sol", "La", "Si", "Do
