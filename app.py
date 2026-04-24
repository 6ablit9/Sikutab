import os
import time

import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="SikuTab", page_icon="🎶", layout="wide")

# --- CSS: CÍRCULOS Y DISEÑO ---
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
    .stButton > button:hover {
        border-color: #9b59b6 !important;
        color: #9b59b6 !important;
    }
    .row-label { font-weight: bold; font-size: 16px; display: flex; align-items: center; height: 75px; }
    .arka-label { color: #9b59b6; }
    .ira-label { color: #e67e22; }
    [data-testid="stHorizontalBlock"] { width: fit-content !important; gap: 12px !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- JAVASCRIPT: DETECTOR DE TECLAS (MÉTODO DE POSICIÓN) ---
# Este script cuenta los botones en la página y los pulsa según su orden
components.html(
    """
<script>
const doc = window.parent.document;
doc.addEventListener('keydown', function(e) {
    const key = e.key.toLowerCase();
    const allBtns = doc.querySelectorAll('button');

    // Mapeo de tecla a índice de botón (empezando desde el primero del teclado virtual)
    // Asumiendo que los primeros botones de la página son los del Arka e Ira
    const map = {
        '1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, // Arka
        'q': 7, 'w': 8, 'e': 9, 'r': 10, 't': 11, 'y': 12     // Ira
    };

    if (map[key] !== undefined) {
        // Buscamos los botones que están dentro del Siku Virtual
        // Filtramos para evitar pulsar botones de los selectores de arriba
        const sikuBtns = Array.from(allBtns).filter(b =>
            b.innerText.includes('\\n') ||
            (b.innerText.length < 10 && /\\d/.test(b.innerText))
        );

        if (sikuBtns[map[key]]) {
            sikuBtns[map[key]].click();
        }
    }
});
</script>
""",
    height=0,
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
    if t_limpia not in NOTAS_MUSICALES:
        return None
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

if "audio_file" not in st.session_state:
    st.session_state.audio_file = None


def tocar(nota):
    st.session_state.audio_file = f"{nota}.wav"


# --- INTERFAZ SUPERIOR ---
st.title("🎶 SikuTab: Transpositor y Teclado")

col_t, col_m = st.columns(2)
with col_t:
    original_tonica = st.selectbox("Tonalidad Original", NOTAS_MUSICALES)
with col_m:
    modo = st.radio("Modo", ["Mayor", "Menor"], horizontal=True)

entrada = st.text_input("Escribe la melodía aquí:")
if entrada:
    ref_original = generar_escala(original_tonica, modo.lower())
    dest = (
        ["Sol", "La", "Si", "Do", "Re", "Mi", "Fa#"]
        if modo == "Mayor"
        else ["Mi", "Fa#", "Sol", "La", "Si", "Do", "Re"]
    )
    notas_usuario = [n.strip() for n in entrada.split() if n.strip()]
    f_arka_n, f_ira_n = "ARKA: ", "IRA:  "
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
            if nota_t in ARKA:
                f_arka_n += nota_t.ljust(8)
                f_ira_n += " " * 8
            else:
                f_arka_n += " " * 8
                f_ira_n += nota_t.ljust(8)
    st.code(f"{f_arka_n}\n{f_ira_n}")

st.write("---")

# --- SIKU VIRTUAL ---
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

# ARKA (1-7)
c_arka = st.columns([1.5, 1, 1, 1, 1, 1, 1, 1, 2])
with c_arka[0]:
    st.markdown(
        '<div class="row-label arka-label">ARKA (1-7)</div>', unsafe_allow_html=True
    )
for i, n in enumerate(ARKA):
    num = TABLATURA.get(n, "")
    with c_arka[i + 1]:
        st.button(f"{num}\n{n}", key=f"v_a_{n}", on_click=tocar, args=(n,))

# IRA (Q-Y)
c_ira = st.columns([1.5, 0.6, 1, 1, 1, 1, 1, 1, 2.5])
with c_ira[0]:
    st.markdown(
        '<div class="row-label ira-label">IRA (Q-Y)</div>', unsafe_allow_html=True
    )
for i, n in enumerate(IRA):
    num = TABLATURA.get(n, "")
    with c_ira[i + 2]:
        st.button(f"{num}\n{n}", key=f"v_i_{n}", on_click=tocar, args=(n,))
