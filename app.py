import os
import time

import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="SikuTab", page_icon="🎶", layout="wide")

# --- CSS: CÍRCULOS Y EFECTO DE PULSACIÓN ---
st.markdown(
    """
    <style>
    .stButton > button {
        border-radius: 50% !important;
        width: 75px !important;
        height: 75px !important;
        border: 2px solid #555 !important;
        background-color: #2e2e2e !important;
        color: white !important;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        line-height: 1.2 !important;
        padding: 0 !important;
        font-size: 13px !important;
        transition: all 0.1s ease;
    }
    /* Clase para cuando se presiona la tecla física */
    .stButton > button:active, .key-active {
        background-color: #9b59b6 !important;
        transform: scale(0.9);
        border-color: white !important;
    }
    .row-label { font-weight: bold; font-size: 16px; display: flex; align-items: center; height: 75px; }
    .arka-label { color: #9b59b6; }
    .ira-label { color: #e67e22; }
    [data-testid="stHorizontalBlock"] { width: fit-content !important; gap: 12px !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- JAVASCRIPT: DETECTOR DE TECLAS ---
# Este script busca el botón correcto y le hace un "click" virtual
components.html(
    """
<script>
const doc = window.parent.document;
doc.addEventListener('keydown', function(e) {
    const keyMap = {
        '1': 'v_a_Si2', '2': 'v_a_Sol2', '3': 'v_a_Mi', '4': 'v_a_Do', '5': 'v_a_La', '6': 'v_a_Fa#0', '7': 'v_a_Re0',
        'q': 'v_i_La2', 'w': 'v_i_Fa#', 'e': 'v_i_Re', 'r': 'v_i_Si', 't': 'v_i_Sol', 'y': 'v_i_Mi0'
    };
    const buttonId = keyMap[e.key.toLowerCase()];
    if (buttonId) {
        const btn = doc.querySelector(`button[kind="secondary"] > div > p:contains("${buttonId}")`);
        // Buscamos por el aria-label o el texto del botón interno de Streamlit
        const allBtns = doc.querySelectorAll('button');
        allBtns.forEach(b => {
            if (b.innerText.includes(buttonId.replace('v_a_','').replace('v_i_',''))) {
               b.click();
            }
        });
    }
});
</script>
""",
    height=0,
)

# --- DATOS Y AUDIO ---
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

if "audio_file" not in st.session_state:
    st.session_state.audio_file = None


def tocar(nota):
    st.session_state.audio_file = f"{nota}.wav"


# --- INTERFAZ ---
st.title("🎶 SikuTab")
st.write("---")

# --- SIKU VIRTUAL ---
col_head, col_audio = st.columns([1, 1])
with col_head:
    st.subheader("🎹 Siku Virtual")

if st.session_state.audio_file:
    with col_audio:
        placeholder = st.empty()
        if os.path.exists(st.session_state.audio_file):
            placeholder.audio(st.session_state.audio_file, autoplay=True)
            time.sleep(1.2)
            placeholder.empty()
            st.session_state.audio_file = None
            st.rerun()

# FILA ARKA (1 al 7)
c_arka = st.columns([1.2, 1, 1, 1, 1, 1, 1, 1, 2])
with c_arka[0]:
    st.markdown(
        '<div class="row-label arka-label">ARKA (1-7)</div>', unsafe_allow_html=True
    )
for i, n in enumerate(ARKA):
    num = TABLATURA.get(n, "")
    with c_arka[i + 1]:
        st.button(f"{num}\n{n}", key=f"v_a_{n}", on_click=tocar, args=(n,))

# FILA IRA (Q al Y)
c_ira = st.columns([1.2, 0.6, 1, 1, 1, 1, 1, 1, 2.5])
with c_ira[0]:
    st.markdown(
        '<div class="row-label ira-label">IRA (Q-Y)</div>', unsafe_allow_html=True
    )
for i, n in enumerate(IRA):
    num = TABLATURA.get(n, "")
    with c_ira[i + 2]:
        st.button(f"{num}\n{n}", key=f"v_i_{n}", on_click=tocar, args=(n,))
