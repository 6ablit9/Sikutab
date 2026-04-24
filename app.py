import streamlit as st
import os

# --- CONFIGURACIÓN E INYECCIÓN DE DISEÑO (Círculos) ---
st.set_page_config(page_title="SikuTab", page_icon="🎶", layout="wide")

st.markdown("""
    <style>
    /* Estilo para convertir botones en círculos de Siku */
    .stButton > button {
        border-radius: 50% !important;
        width: 80px !important;
        height: 80px !important;
        border: 2px solid #555 !important;
        background-color: #2e2e2e !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 14px !important;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
    }
    .stButton > button:hover {
        border-color: #9b59b6 !important;
        color: #9b59b6 !important;
    }
    /* Contenedor para centrar la Ira (6 tubos) bajo el Arka (7 tubos) */
    .ira-container {
        padding-left: 45px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE ESCALAS ---
NOTAS_MUSICALES = ["Do", "Do#", "Re", "Re#", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "La#", "Si"]
BEMOLES = {"Reb": "Do#", "Mib": "Re#", "Solb": "Fa#", "Lab": "Sol#", "Sib": "La#"}

def generar_escala(tonica, modo):
    pasos = [2, 2, 1, 2, 2, 2, 1] if modo == "mayor" else [2, 1, 2, 2, 1, 2, 2]
    idx = NOTAS_MUSICALES.index(BEMOLES.get(tonica, tonica))
    escala = []
    actual = idx
    for p in pasos:
        escala.append(NOTAS_MUSICALES[actual % 12])
        actual += p
    return escala

# --- DISPOSICIÓN SEGÚN IMAGEN ---
# Arka (7 tubos): Si2 a Re0 (de izquierda a derecha según tu diagrama)
ARKA = ["Si2", "Sol2", "Mi", "Do", "La", "Fa#0", "Re0"]
# Ira (6 tubos): La2 a Mi0
IRA  = ["La2", "Fa#", "Re", "Si", "Sol", "Mi0"]

TABLATURA = {
    "Re0": "7", "Mi0": "6", "Fa#0": "6", "Si": "4", "Do": "4", "Re": "3", "Mi": "3",
    "Fa#": "2", "Sol": "5", "La": "5", "Sol2": "2", "La2": "1", "Si2": "1"
}

# --- INTERFAZ ---
st.title("🎶 SikuTab: Transpositor y Teclado")
st.caption("Prof. Pablo Olivero - Liceo San José del Carmen")

col_t, col_m = st.columns([1, 1])
with col_t:
    original_tonica = st.selectbox("Tonalidad Original", NOTAS_MUSICALES)
with col_m:
    modo = st.radio("Modo", ["Mayor", "Menor"], horizontal=True)

# --- TECLADO VISUAL (Círculos) ---
st.subheader("🎹 Mapa de Tubos")

def reproducir(nota):
    archivo = f"{nota}.wav"
    if os.path.exists(archivo):
        st.audio(archivo, format="audio/wav", autoplay=True)
    else:
        st.error(f"Falta: {archivo}")

# Fila ARKA (7 columnas)
cols_arka = st.columns(7)
for i, n in enumerate(ARKA):
    with cols_arka[i]:
        if st.button(n, key=f"a_{n}"):
            reproducir(n)

# Fila IRA (6 columnas, usamos un contenedor para desplazar)
st.markdown('<div class="ira-container">', unsafe_allow_html=True)
cols_ira = st.columns([0.5, 1, 1, 1, 1, 1, 1, 0.5]) # Columnas de relleno para centrar
for i, n in enumerate(IRA):
    with cols_ira[i+1]: # Empezamos en la segunda columna
        if st.button(n, key=f"i_{n}"):
            reproducir(n)
st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

# --- ENTRADA Y RESULTADO ---
entrada = st.text_input("Escribe la melodía aquí:", placeholder="Ej: re0 mi0 sol la do2")

if entrada:
    ref_original = generar_escala(original_tonica, modo.lower())
    dest = ["Sol", "La", "Si", "Do", "Re", "Mi", "Fa#"] if modo == "Mayor" else ["Mi", "Fa#", "Sol", "La", "Si", "Do", "Re"]

    notas_usuario = [n.strip() for n in entrada.split() if n.strip()]
    f_arka_n, f_ira_n, f_arka_num, f_ira_num = "ARKA (Notas):  ", "IRA  (Notas):  ", "ARKA (Num):    ", "IRA  (Num):    "
    ancho = 8

    for nota_raw in notas_usuario:
        sufijo = "0" if nota_raw.endswith
