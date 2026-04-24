import os
import time

import streamlit as st

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="SikuTab", page_icon="🎶", layout="wide")

# --- CSS PARA CÍRCULOS PEGADOS Y ZIGZAG ---
st.markdown(
    """
    <style>
    /* Estilo de los tubos */
    .stButton > button {
        border-radius: 50% !important;
        width: 70px !important;
        height: 70px !important;
        border: 2px solid #555 !important;
        background-color: #2e2e2e !important;
        color: white !important;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        line-height: 1 !important;
        padding: 0 !important;
        font-size: 13px !important;
    }
    .stButton > button:hover {
        border-color: #9b59b6 !important;
        color: #9b59b6 !important;
    }
    /* Etiquetas laterales */
    .row-label {
        font-weight: bold;
        font-size: 16px;
        display: flex;
        align-items: center;
        height: 70px;
    }
    .arka-label { color: #9b59b6; }
    .ira-label { color: #e67e22; }

    /* Forzar que las columnas no se estiren */
    [data-testid="stHorizontalBlock"] {
        width: fit-content !important;
        gap: 0.5rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- LÓGICA DE ESCALAS ---
NOTAS_MUSICALES = [
    "Do",
    "Do#",
    "Re",
    "Re#",
    "Mi",
    "Fa",
    "Fa#",
    "Sol",
    "Sol#",
    "La",
    "La#",
    "Si",
]
BEMOLES = {"Reb": "Do#", "Mib": "Re#", "Solb": "Fa#", "Lab": "Sol#", "Sib": "La#"}


def generar_escala(tonica, modo):
    pasos = [2, 2, 1, 2, 2, 2, 1] if modo == "mayor" else [2, 1, 2, 2, 1, 2, 2]
    t_limpia = BEMOLES.get(tonica.capitalize(), tonica.capitalize())
    idx = NOTAS_MUSICALES.index(t_limpia)
    escala = []
    actual = idx
    for p in pasos:
        escala.append(NOTAS_MUSICALES[actual % 12])
        actual += p
    return escala


# --- DATOS DEL SIKU ---
ARKA = ["Si2", "Sol2", "Mi", "Do", "La", "Fa#0", "Re0"]
IRA = ["La2", "Fa#", "Re", "Si", "Sol", "Mi0"]
TABLATURA = {
    "Re0": "7",
    "Mi0": "6",
    "Fa#0": "6",
    "Si": "4",
    "Do": "4",
    "Re": "3",
    "Mi": "3",
    "Fa#": "2",
    "Sol": "5",
    "La": "5",
    "Sol2": "2",
    "La2": "1",
    "Si2": "1",
}

# --- ESTADO DE AUDIO ---
# Inicializamos el sonido en el estado de la sesión
if "last_note" not in st.session_state:
    st.session_state.last_note = None
if "audio_trigger" not in st.session_state:
    st.session_state.audio_trigger = 0


def click_tubo(nota):
    st.session_state.last_note = nota
    st.session_state.audio_trigger += 1  # Cambiamos el trigger para forzar recarga


# --- INTERFAZ ---
st.title("🎶 SikuTab: Transpositor y Siku Virtual")
st.caption("Prof. Pablo Olivero - Liceo San José del Carmen")

# (Sección de transposición omitida para brevedad, mantener la que ya tienes)

st.write("---")

# --- SIKU VIRTUAL ---
col_head, col_audio = st.columns([1, 2])
with col_head:
    st.subheader("🎹 Siku Virtual")

# REPRODUCTOR DINÁMICO: Cambia su KEY en cada clic para sonar siempre
with col_audio:
    if st.session_state.last_note:
        archivo = f"{st.session_state.last_note}.wav"
        if os.path.exists(archivo):
            # El key dinámico es el secreto del reseteo del sonido
            st.audio(
                archivo,
                format="audio/wav",
                autoplay=True,
                key=f"play_{st.session_state.last_note}_{st.session_state.audio_trigger}",
            )

# FILA ARKA
# Usamos anchos fijos pequeños para que se peguen
c_arka = st.columns([1, 1, 1, 1, 1, 1, 1, 1])
with c_arka[0]:
    st.markdown('<div class="row-label arka-label">ARKA</div>', unsafe_allow_html=True)
for i, n in enumerate(ARKA):
    with c_arka[i + 1]:
        num = TABLATURA.get(n, "")
        st.button(f"{num}\n{n}", key=f"v_a_{n}", on_click=click_tubo, args=(n,))

# FILA IRA (ZIGZAG)
# El secreto: La columna de desfase es de 0.5 para que caiga justo al medio
c_ira = st.columns([1, 0.5, 1, 1, 1, 1, 1, 1])
with c_ira[0]:
    st.markdown('<div class="row-label ira-label">IRA</div>', unsafe_allow_html=True)
# c_ira[1] queda vacío como espacio de zigzag
for i, n in enumerate(IRA):
    with c_ira[i + 2]:
        num = TABLATURA.get(n, "")
        st.button(f"{num}\n{n}", key=f"v_i_{n}", on_click=click_tubo, args=(n,))
