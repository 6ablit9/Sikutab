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
st.set_page_config(page_title="SikuTab", page_icon="🎶", layout="wide") # Layout ancho para mejorar proporciones
st.title("🎶 SikuTab: Transpositor Arka/Ira")
st.caption("Prof. Pablo Olivero - Liceo San José del Carmen")

# --- SECCIÓN DE CONFIGURACIÓN (Diseño según imagen editada) ---
# Usamos columnas para agrupar los controles a la izquierda
col_izquierda, col_espacio = st.columns([4, 6]) # 40% controles, 60% espacio libre

with col_izquierda:
    # Sub-columnas para Tonalidad y Modo
    col_ton, col_modo = st.columns(2)

    with col_ton:
        original_tonica = st.selectbox("Tonalidad Original", NOTAS_MUSICALES)

    with col_modo:
        modo = st.radio("Modo", ["Mayor", "Menor"])

    # La Guía de Octavas justo debajo de Tonalidad/Modo
    st.info("""
    **Guía de Octavas:**
    - **Agudo:** Agrega un **2** (ej: `do2`).
    - **Grave:** Agrega un **0** (ej: `do0`).

    *Límites del Siku:*
    - Re0 a Fa#0
    - Sol a Fa#
    - Sol2 a Si2
    """)

# Área de texto centrada o alineada según el nuevo layout
entrada = st.text_area("Escribe la melodía aquí:", placeholder="Ejemplo: do do2 sol la re0 mi0", height=120)

if entrada:
    ref_original = generar_escala(original_tonica, modo.lower())
    dest, nombre_final = (["Sol", "La", "Si", "Do", "Re", "Mi", "Fa#"], "SOL MAYOR") if modo == "Mayor" else (["Mi", "Fa#", "Sol", "La", "Si", "Do", "Re"], "MI MENOR")

    notas_usuario = [n.strip() for n in entrada.split() if n.strip()]
    f_arka_n, f_ira_n = "ARKA (Notas):  ", "IRA  (Notas):  "
    f_arka_num, f_ira_num = "ARKA (Num):    ", "IRA  (Num):    "

    ancho = 8

    for nota_raw in notas_usuario:
        sufijo = "0" if nota_raw.endswith("0") else ("2" if nota_raw.endswith("2") else "")
        n_nombre = nota_raw[:-1] if sufijo
