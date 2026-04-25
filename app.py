import os
import time

import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="SikuTab", page_icon="🎶", layout="wide")

# --- CSS: ESTÉTICA Y COMPRESIÓN ---
st.markdown(
    """
    <style>
    .stApp { background-color: #1e1e1e; color: #f0f0f0; }

    /* Botones Circulares del Siku */
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
        font-size: 13px !important;
    }
    .stButton > button:hover { border-color: #9b59b6 !important; color: #9b59b6 !important; background-color: #3a3a3a !important; }

    .row-label { font-weight: bold; font-size: 16px; display: flex; align-items: center; height: 75px; color: white; }
    .arka-label { color: #9b59b6; }
    .ira-label { color: #e67e22; }

    /* Cuadro de código verde compacto */
    div[data-testid="stCodeBlock"] pre {
        background-color: #000000 !important;
        color: #00ff00 !important;
        padding: 10px !important;
        font-size: 16px !important;
    }

    audio { height: 30px; width: 180px; filter: invert(100%); }
    [data-testid="stHorizontalBlock"] { width: fit-content !important; gap: 4px !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- JAVASCRIPT: ASIGNACIÓN DE TECLAS (1-7 y Q-Y) ---
components.html(
    """
<script>
const doc = window.parent.document;

doc.addEventListener('keydown', function(e) {
    // No activar si el usuario está escribiendo en el cuadro de texto
    const tag = e.target.tagName.toLowerCase();
    if (tag === 'input' || tag === 'textarea') return;

    const key = e.key.toLowerCase();

    // Mapeo exacto: 1-7 Arka, Q-Y Ira
    const keyMap = {
        '1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6,  // Arka
        'q': 7, 'w': 8, 'e': 9, 'r': 10, 't': 11, 'y': 12       // Ira
    };

    if (keyMap.hasOwnProperty(key)) {
        // Buscamos todos los botones que contienen un número y una nota (tienen salto de línea)
        const allButtons = Array.from(doc.querySelectorAll('button'));
        const sikuButtons = allButtons.filter(btn => btn.innerText.includes('\\n'));

        const targetIndex = keyMap[key];
        if (sikuButtons[targetIndex]) {
            e.preventDefault(); // Evita scrolls accidentales
            sikuButtons[targetIndex].click();
        }
    }
});
</script>
""",
    height=0,
)

# --- LÓGICA MUSICAL ---
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


TABLATURA = {
    "Re0": "7",
    "Mi0": "6",
    "Fa#0": "6",
    "Sol": "5",
    "La": "5",
    "Si": "4",
    "Do": "4",
    "Re": "3",
    "Mi": "3",
    "Fa#": "2",
    "Sol2": "2",
    "La2": "1",
    "Si2": "1",
}
NOTAS_ARKA = ["Re0", "Fa#0", "La", "Do", "Mi", "Sol2", "Si2"]

if "audio_file" not in st.session_state:
    st.session_state.audio_file = None


def tocar(nota):
    st.session_state.audio_file = f"{nota}.wav"


# --- INTERFAZ ---
st.title("🎶 SikuTab")
col_t, col_m = st.columns([1, 1])
with col_t:
    original_tonica = st.selectbox("Tonalidad Original", NOTAS_MUSICALES)
with col_m:
    modo = st.radio("Modo", ["Mayor", "Menor"], horizontal=True)

with st.expander("📖 Guía rápida", expanded=False):
    st.write("Usa '2' para agudos y '0' para graves. Ejemplo: sol la si do2")

st.write("---")

entrada = st.text_input("📝 Escribe la melodía aquí:", placeholder="Ej: sol la si do2")

if entrada:
    ref = generar_escala(original_tonica, modo.lower())
    dest = (
        ["Sol", "La", "Si", "Do", "Re", "Mi", "Fa#"]
        if modo == "Mayor"
        else ["Mi", "Fa#", "Sol", "La", "Si", "Do", "Re"]
    )

    notas_usuario = [n.strip() for n in entrada.split() if n.strip()]
    linea_notas = ""
    linea_nums = ""

    for nota_raw in notas_usuario:
        sufijo = (
            "0" if nota_raw.endswith("0") else ("2" if nota_raw.endswith("2") else "")
        )
        n_nombre = nota_raw[:-1] if sufijo else nota_raw
        n_limpia = "".join(
            [c for c in n_nombre if c.isalpha() or c == "#"]
        ).capitalize()
        n_limpia = BEMOLES.get(n_limpia, n_limpia)

        if n_limpia in ref:
            nota_t = dest[ref.index(n_limpia)] + sufijo
            num_t = TABLATURA.get(nota_t, "?")
            prefijo = "(A)" if nota_t in NOTAS_ARKA else "(I)"

            bloque_n = f"{prefijo}{nota_t}".ljust(8)
            bloque_v = f"[{num_t}]".ljust(8)
            linea_notas += bloque_n
            linea_nums += bloque_v

    st.code(f"{linea_notas}\n{linea_nums}")

st.write("---")

# --- SIKU VIRTUAL Y REPRODUCTOR ---
col_tit, col_aud = st.columns([1.2, 3])
with col_tit:
    st.subheader("🎹 Siku Virtual")
with col_aud:
    if st.session_state.audio_file:
        if os.path.exists(st.session_state.audio_file):
            st.audio(st.session_state.audio_file, autoplay=True)
            st.session_state.audio_file = None

# FILA ARKA (Teclas 1-7)
c_arka = st.columns([1.5, 1, 1, 1, 1, 1, 1, 1])
with c_arka[0]:
    st.markdown(
        '<div class="row-label arka-label">ARKA (1-7)</div>', unsafe_allow_html=True
    )
for i, n in enumerate(["Si2", "Sol2", "Mi", "Do", "La", "Fa#0", "Re0"]):
    with c_arka[i + 1]:
        st.button(f"{TABLATURA.get(n)}\n{n}", key=f"a_{n}", on_click=tocar, args=(n,))

# FILA IRA (Teclas Q-Y)
c_ira = st.columns([1.5, 0.5, 1, 1, 1, 1, 1, 1])
with c_ira[0]:
    st.markdown(
        '<div class="row-label ira-label">IRA (Q-Y)</div>', unsafe_allow_html=True
    )
for i, n in enumerate(["La2", "Fa#", "Re", "Si", "Sol", "Mi0"]):
    with c_ira[i + 2]:
        st.button(f"{TABLATURA.get(n)}\n{n}", key=f"i_{n}", on_click=tocar, args=(n,))
