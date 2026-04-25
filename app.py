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

    /* Cuadro de código verde compacto */
    div[data-testid="stCodeBlock"] pre {
        background-color: #000000 !important;
        color: #00ff00 !important;
        padding: 10px !important;
        font-size: 16px !important;
    }

    audio { height: 30px; width: 180px; filter: invert(100%); }
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
    if (e.target.tagName.toLowerCase() === 'input') return;
    const key = e.key.toLowerCase();
    const map = {'1':0,'2':1,'3':2,'4':3,'5':4,'6':5,'7':6,'q':7,'w':8,'e':9,'r':10,'t':11,'y':12};
    if (map[key] !== undefined) {
        const btns = Array.from(doc.querySelectorAll('button')).filter(b => b.innerText.includes('\\n'));
        if (btns[map[key]]) { e.preventDefault(); btns[map[key]].click(); }
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
    original_tonica = st.selectbox("Tonalidad", NOTAS_MUSICALES)
with col_m:
    modo = st.radio("Modo", ["Mayor", "Menor"], horizontal=True)

with st.expander("📖 Guía rápida", expanded=False):
    st.write("Usa '2' para agudos y '0' para graves. Ejemplo: sol la si do2")

st.write("---")

entrada = st.text_input("📝 Escribe la melodía:", placeholder="Ej: sol la si do2")

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

            # Formato ultra compacto: Nota con su indicador Arka/Ira y número abajo
            bloque_n = f"{prefijo}{nota_t}".ljust(8)
            bloque_v = f"[{num_t}]".ljust(8)
            linea_notas += bloque_n
            linea_nums += bloque_v

    st.code(f"{linea_notas}\n{linea_nums}")

st.write("---")

# --- SIKU VIRTUAL ---
col_tit, col_aud = st.columns([1.2, 3])
with col_tit:
    st.subheader("🎹 Siku Virtual")
with col_aud:
    if st.session_state.audio_file and os.path.exists(st.session_state.audio_file):
        st.audio(st.session_state.audio_file, autoplay=True)
        st.session_state.audio_file = None

# FILAS ARKA E IRA
c_arka = st.columns([1.5, 1, 1, 1, 1, 1, 1, 1])
with c_arka[0]:
    st.markdown(
        '<div class="row-label arka-label">ARKA (1-7)</div>', unsafe_allow_html=True
    )
for i, n in enumerate(["Si2", "Sol2", "Mi", "Do", "La", "Fa#0", "Re0"]):
    with c_arka[i + 1]:
        st.button(f"{TABLATURA.get(n)}\n{n}", key=f"a_{n}", on_click=tocar, args=(n,))

c_ira = st.columns([1.5, 0.5, 1, 1, 1, 1, 1, 1])
with c_ira[0]:
    st.markdown(
        '<div class="row-label ira-label">IRA (Q-Y)</div>', unsafe_allow_html=True
    )
for i, n in enumerate(["La2", "Fa#", "Re", "Si", "Sol", "Mi0"]):
    with c_ira[i + 2]:
        st.button(f"{TABLATURA.get(n)}\n{n}", key=f"i_{n}", on_click=tocar, args=(n,))
