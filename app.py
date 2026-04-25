import os
import time

import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="SikuTab", page_icon="🎶", layout="wide")

# --- CSS: ESTÉTICA Y ALINEACIÓN ---
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
        transition: all 0.2s ease;
    }
    .stButton > button:hover { border-color: #9b59b6 !important; color: #9b59b6 !important; background-color: #3a3a3a !important; }

    .row-label { font-weight: bold; font-size: 16px; display: flex; align-items: center; height: 75px; color: white; }
    .arka-label { color: #9b59b6; }
    .ira-label { color: #e67e22; }

    /* Cuadro de código verde tipo terminal */
    div[data-testid="stCodeBlock"] pre {
        background-color: #000000 !important;
        color: #00ff00 !important;
        border: 1px solid #333;
    }

    /* Reproductor pequeño y discreto */
    audio {
        height: 30px;
        width: 180px;
        filter: invert(100%) hue-rotate(180deg) brightness(1.5);
    }

    /* Compresión de espacio entre botones para zigzag */
    [data-testid="stHorizontalBlock"] { width: fit-content !important; gap: 4px !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- JAVASCRIPT: DETECTOR DE TECLAS (1-7 y Q-Y) ---
components.html(
    """
<script>
const doc = window.parent.document;
doc.addEventListener('keydown', function(e) {
    const tag = e.target.tagName.toLowerCase();
    if (tag === 'input' || tag === 'textarea') return;

    const key = e.key.toLowerCase();
    const map = {
        '1':0, '2':1, '3':2, '4':3, '5':4, '6':5, '7':6,
        'q':7, 'w':8, 'e':9, 'r':10, 't':11, 'y':12
    };

    if (map[key] !== undefined) {
        const allBtns = Array.from(doc.querySelectorAll('button'));
        // Filtramos solo los botones que tienen el formato de nota (con salto de línea)
        const sikuBtns = allBtns.filter(b => b.innerText.includes('\\n'));

        if (sikuBtns[map[key]]) {
            e.preventDefault();
            sikuBtns[map[key]].click();
        }
    }
});
</script>
""",
    height=0,
)

# --- LÓGICA DE ESCALAS Y TRANSPOSICIÓN ---
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
    if t_limpia not in NOTAS_MUSICALES:
        return None
    idx = NOTAS_MUSICALES.index(t_limpia)
    escala = []
    actual = idx
    for p in pasos:
        escala.append(NOTAS_MUSICALES[actual % 12])
        actual += p
    return escala


# --- TABLATURA Y REGISTROS ---
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
NOTAS_IRA = ["Mi0", "Sol", "Si", "Re", "Fa#", "La2"]

if "audio_file" not in st.session_state:
    st.session_state.audio_file = None


def tocar(nota):
    st.session_state.audio_file = f"{nota}.wav"


# --- INTERFAZ SUPERIOR ---
st.title("🎶 SikuTab: Transpositor Arka/Ira")
st.caption("Prof. Pablo Olivero - Liceo San José del Carmen")

col_t, col_m = st.columns([1, 1])
with col_t:
    original_tonica = st.selectbox("Tonalidad Original", NOTAS_MUSICALES)
with col_m:
    modo = st.radio("Modo", ["Mayor", "Menor"], horizontal=True)

with st.expander("📖 Guía de Octavas", expanded=False):
    st.write(
        "Escribe notas normales para registro medio, agrega '2' para agudos y '0' para graves."
    )

st.write("---")

# ENTRADA DE TEXTO (1 SOLA LÍNEA)
entrada = st.text_input(
    "📝 Escribe la melodía aquí (presiona Enter):", placeholder="Ej: sol la si do2 re2"
)

if entrada:
    ref_original = generar_escala(original_tonica, modo.lower())
    dest = (
        ["Sol", "La", "Si", "Do", "Re", "Mi", "Fa#"]
        if modo == "Mayor"
        else ["Mi", "Fa#", "Sol", "La", "Si", "Do", "Re"]
    )

    notas_usuario = [n.strip() for n in entrada.split() if n.strip()]
    f_arka_n, f_ira_n = "ARKA: ", "IRA:  "
    f_arka_v, f_ira_v = "NUM:  ", "NUM:  "
    ancho = 9

    for nota_raw in notas_usuario:
        sufijo = (
            "0" if nota_raw.endswith("0") else ("2" if nota_raw.endswith("2") else "")
        )
        n_nombre = nota_raw[:-1] if sufijo else nota_raw
        n_limpia = "".join(
            [c for c in n_nombre if c.isalpha() or c == "#"]
        ).capitalize()
        n_limpia = BEMOLES.get(n_limpia, n_limpia)

        if n_limpia in ref_original:
            nota_t = dest[ref_original.index(n_limpia)] + sufijo
            num_t = TABLATURA.get(nota_t, "?")
            if nota_t in NOTAS_ARKA:
                f_arka_n += nota_t.ljust(ancho)
                f_ira_n += " " * ancho
                f_arka_v += num_t.ljust(ancho)
                f_ira_v += " " * ancho
            else:
                f_arka_n += " " * ancho
                f_ira_n += nota_t.ljust(ancho)
                f_arka_v += " " * ancho
                f_ira_v += num_t.ljust(ancho)

    st.code(f"{f_arka_n}\n{f_ira_n}\n{'-' * (len(f_arka_n))}\n{f_arka_v}\n{f_ira_v}")

st.write("---")

# --- SIKU VIRTUAL Y AUDIO ---
col_tit, col_aud = st.columns([1.2, 3])
with col_tit:
    st.subheader("🎹 Siku Virtual")
with col_aud:
    if st.session_state.audio_file:
        if os.path.exists(st.session_state.audio_file):
            st.audio(st.session_state.audio_file, autoplay=True)
            st.session_state.audio_file = None

# FILA ARKA
c_arka = st.columns([1.5, 1, 1, 1, 1, 1, 1, 1])
with c_arka[0]:
    st.markdown(
        '<div class="row-label arka-label">ARKA (1-7)</div>', unsafe_allow_html=True
    )
ARKA_V = ["Si2", "Sol2", "Mi", "Do", "La", "Fa#0", "Re0"]
for i, n in enumerate(ARKA_V):
    with c_arka[i + 1]:
        st.button(f"{TABLATURA.get(n)}\n{n}", key=f"a_{n}", on_click=tocar, args=(n,))

# FILA IRA (Desfase de 0.5 para zigzag)
c_ira = st.columns([1.5, 0.5, 1, 1, 1, 1, 1, 1])
with c_ira[0]:
    st.markdown(
        '<div class="row-label ira-label">IRA (Q-Y)</div>', unsafe_allow_html=True
    )
IRA_V = ["La2", "Fa#", "Re", "Si", "Sol", "Mi0"]
for i, n in enumerate(IRA_V):
    with c_ira[i + 2]:
        st.button(f"{TABLATURA.get(n)}\n{n}", key=f"i_{n}", on_click=tocar, args=(n,))
