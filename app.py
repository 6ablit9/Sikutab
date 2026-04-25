import os
import time

import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="SikuTab", page_icon="🎶", layout="wide")

# --- CSS: CÍRCULOS TOCÁNDOSE POR 1 PIXEL ---
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
        line-height: 1.1 !important;
        padding: 0 !important;
        font-size: 13px !important;
    }
    .stButton > button:hover { border-color: #9b59b6 !important; color: #9b59b6 !important; }
    .row-label { font-weight: bold; font-size: 16px; display: flex; align-items: center; height: 75px; }
    .arka-label { color: #9b59b6; }
    .ira-label { color: #e67e22; }

    /* El secreto: Gap de 1px para que apenas se toquen */
    [data-testid="stHorizontalBlock"] {
        width: fit-content !important;
        gap: 1px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- JAVASCRIPT: DETECTOR DE TECLAS ---
components.html(
    """
<script>
const doc = window.parent.document;
doc.addEventListener('keydown', function(e) {
    const tag = e.target.tagName.toLowerCase();
    if (tag === 'input' || tag === 'textarea' || tag === 'select') return;
    const key = e.key.toLowerCase();
    const allBtns = doc.querySelectorAll('button');
    const map = {
        '1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6,
        'q': 7, 'w': 8, 'e': 9, 'r': 10, 't': 11, 'y': 12
    };
    if (map[key] !== undefined) {
        const sikuBtns = Array.from(allBtns).filter(b =>
            b.innerText.includes('\\n') ||
            (b.innerText.length < 10 && /\\d/.test(b.innerText))
        );
        if (sikuBtns[map[key]]) { sikuBtns[map[key]].click(); }
    }
});
</script>
""",
    height=0,
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

if "audio_file" not in st.session_state:
    st.session_state.audio_file = None


def tocar(nota):
    st.session_state.audio_file = f"{nota}.wav"


# --- INTERFAZ ---
st.title("🎶 SikuTab: Transpositor y Teclado")
# (Lógica de escalas y entrada de texto igual que antes...)

st.write("---")

# --- SIKU VIRTUAL (ZIGZAG MILIMÉTRICO) ---
col_head, col_audio = st.columns([1, 1])
with col_head:
    st.subheader("🎹 Siku Virtual")

audio_placeholder = col_audio.empty()
if st.session_state.audio_file:
    if os.path.exists(st.session_state.audio_file):
        audio_placeholder.audio(st.session_state.audio_file, autoplay=True)
        time.sleep(1.2)
        audio_placeholder.empty()
        st.session_state.audio_file = None
        st.rerun()

# --- FILAS CON ALINEACIÓN MATEMÁTICA ---
# Para que se toquen por 1px, las columnas de notas deben tener el mismo peso (1)
# Arka: 1.5 de etiqueta + 7 notas
layout_arka = [1.5, 1, 1, 1, 1, 1, 1, 1]
# Ira: 1.5 de etiqueta + 0.5 de DESFASE EXACTO + 6 notas
layout_ira = [1.5, 0.5, 1, 1, 1, 1, 1, 1]

# FILA ARKA
c_arka = st.columns(layout_arka)
with c_arka[0]:
    st.markdown(
        '<div class="row-label arka-label">ARKA (1-7)</div>', unsafe_allow_html=True
    )
for i, n in enumerate(ARKA):
    num = TABLATURA.get(n, "")
    with c_arka[i + 1]:
        st.button(f"{num}\n{n}", key=f"v_a_{n}", on_click=tocar, args=(n,))

# FILA IRA
c_ira = st.columns(layout_ira)
with c_ira[0]:
    st.markdown(
        '<div class="row-label ira-label">IRA (Q-Y)</div>', unsafe_allow_html=True
    )
# c_ira[1] es el desfase de 0.5 (media nota) para el zigzag perfecto
for i, n in enumerate(IRA):
    num = TABLATURA.get(n, "")
    with c_ira[i + 2]:
        st.button(f"{num}\n{n}", key=f"v_i_{n}", on_click=tocar, args=(n,))
