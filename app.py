import os

import streamlit as st

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="SikuTab", page_icon="🎶", layout="wide")

# --- CSS PARA CÍRCULOS PEGADOS Y ZIGZAG ---
st.markdown(
    """
    <style>
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
    .row-label {
        font-weight: bold;
        font-size: 16px;
        display: flex;
        align-items: center;
        height: 70px;
    }
    .arka-label { color: #9b59b6; }
    .ira-label { color: #e67e22; }

    /* Forzar que las columnas no se estiren en pantallas grandes */
    [data-testid="stHorizontalBlock"] {
        width: fit-content !important;
        gap: 5px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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

# --- MANEJO DE ESTADO DE AUDIO ---
if "audio_key" not in st.session_state:
    st.session_state.audio_key = 0
if "current_file" not in st.session_state:
    st.session_state.current_file = None


def tocar(nota):
    st.session_state.current_file = f"{nota}.wav"
    st.session_state.audio_key += 1


# --- INTERFAZ ---
st.title("🎶 SikuTab")

# --- SIKU VIRTUAL ---
st.subheader("🎹 Siku Virtual")

# REPRODUCTOR (Solo aparece si hay algo que tocar)
if st.session_state.current_file and os.path.exists(st.session_state.current_file):
    st.audio(
        st.session_state.current_file,
        autoplay=True,
        key=f"p_{st.session_state.audio_key}",
    )

# FILA ARKA (Etiqueta + 7 Notas + Aire)
c_arka = st.columns([1.2, 1, 1, 1, 1, 1, 1, 1, 2])
with c_arka[0]:
    st.markdown('<div class="row-label arka-label">ARKA</div>', unsafe_allow_html=True)
for i, n in enumerate(ARKA):
    num = TABLATURA.get(n, "")
    with c_arka[i + 1]:
        st.button(f"{num}\n{n}", key=f"v_a_{n}", on_click=tocar, args=(n,))

# FILA IRA (Etiqueta + DESFASE 0.5 + 6 Notas + Aire)
c_ira = st.columns([1.2, 0.5, 1, 1, 1, 1, 1, 1, 2.5])
with c_ira[0]:
    st.markdown('<div class="row-label ira-label">IRA</div>', unsafe_allow_html=True)
for i, n in enumerate(IRA):
    num = TABLATURA.get(n, "")
    with c_ira[i + 2]:
        st.button(f"{num}\n{n}", key=f"v_i_{n}", on_click=tocar, args=(n,))
