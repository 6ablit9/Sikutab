import os
import time

import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="SikuTab", page_icon="🎶", layout="wide")

# --- CSS: ESTÉTICA ORIGINAL Y COMPRESIÓN ---
st.markdown(
    """
    <style>
    .stApp { background-color: #1e1e1e; color: #f0f0f0; }

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

    .top-info-box {
        background-color: #f4ecf7;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #9b59b6;
        color: #000000 !important;
        font-size: 14px;
    }

    div[data-testid="stCodeBlock"] pre {
        background-color: #000000 !important;
        color: #00ff00 !important;
        border: 1px solid #333;
    }

    [data-testid="stHorizontalBlock"] { width: fit-content !important; gap: 4px !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- JAVASCRIPT: TECLADO FÍSICO ---
components.html(
    """
<script>
const doc = window.parent.document;
doc.addEventListener('keydown', function(e) {
    const tag = e.target.tagName.toLowerCase();
    if (tag === 'input' || tag === 'textarea' || tag === 'select') return;
    const key = e.key.toLowerCase();
    const allBtns = doc.querySelectorAll('button');
    const map = {'1':0,'2':1,'3':2,'4':3,'5':4,'6':5,'7':6,'q':7,'w':8,'e':9,'r':10,'t':11,'y':12};
    if (map[key] !== undefined) {
        const sikuBtns = Array.from(allBtns).filter(b => b.innerText.includes('\\n'));
        if (sikuBtns[map[key]]) { sikuBtns[map[key]].click(); }
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


# --- REPARTO Y TABLATURA ---
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


# --- INTERFAZ ---
st.title("🎶 SikuTab: Transpositor Arka/Ira")
st.caption("Prof. Pablo Olivero - Liceo San José del Carmen")

# CONFIGURACIÓN
col_t, col_m = st.columns([1, 1])
with col_t:
    original_tonica = st.selectbox("Tonalidad Original", NOTAS_MUSICALES)
with col_m:
    modo = st.radio("Modo", ["Mayor", "Menor"], horizontal=True)

# GUÍA DESPLEGABLE PEDAGÓGICA
with st.expander("📖 Guía de Octavas y Registro Real del Siku", expanded=True):
    st.markdown(
        """
    <div class="top-info-box">
        <b>Cómo escribir las notas:</b><br>
        • <span style='color: #9b59b6;'><b>Registro Agudo:</b></span> Agrega un <b>2</b> (ej: sol2, la2).<br>
        • <b>Registro Medio:</b> Escribe la nota normal (ej: sol, la, si).<br>
        • <span style='color: #e67e22;'><b>Registro Grave:</b></span> Agrega un <b>0</b> (ej: re0, mi0).<br>
        <hr>
        <b>Notas disponibles en el Siku:</b><br>
        • <b>AGUDOS:</b> Sol2, La2, Si2<br>
        • <b>MEDIOS:</b> Sol, La, Si, Do, Re, Mi, Fa#<br>
        • <b>GRAVES:</b> Re0, Mi0, Fa#0
    </div>
    """,
        unsafe_allow_html=True,
    )

# ENTRADA DE TEXTO
entrada = st.text_area(
    "Escribe la melodía aquí:",
    placeholder="Ejemplo: sol la si do re mi fa#",
    height=150,
)

if entrada:
    ref_original = generar_escala(original_tonica, modo.lower())
    dest = (
        ["Sol", "La", "Si", "Do", "Re", "Mi", "Fa#"]
        if modo == "Mayor"
        else ["Mi", "Fa#", "Sol", "La", "Si", "Do", "Re"]
    )
    nombre_final = "SOL MAYOR" if modo == "Mayor" else "MI MENOR"

    notas_usuario = [n.strip() for n in entrada.split() if n.strip()]
    f_arka_n, f_ira_n = "ARKA (Notas):  ", "IRA  (Notas):  "
    f_arka_num, f_ira_num = "ARKA (Num):    ", "IRA  (Num):    "
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
                f_arka_num += num_t.ljust(ancho)
                f_ira_num += " " * ancho
            elif nota_t in NOTAS_IRA:
                f_arka_n += " " * ancho
                f_ira_n += nota_t.ljust(ancho)
                f_arka_num += " " * ancho
                f_ira_num += num_t.ljust(ancho)
            else:
                f_arka_n += f"[{nota_t}?] ".ljust(ancho)
                f_ira_n += " " * ancho
                f_arka_num += "? ".ljust(ancho)
                f_ira_num += " " * ancho
        else:
            f_arka_n += "??".ljust(ancho)
            f_ira_n += " " * ancho
            f_arka_num += "??".ljust(ancho)
            f_ira_num += " " * ancho

    st.markdown(f"### 🎼 Resultado en {nombre_final}")
    st.code(f"{f_arka_n}\n{f_ira_n}\n{'-' * len(f_arka_n)}\n{f_arka_num}\n{f_ira_num}")

st.write("---")

# --- SIKU VIRTUAL ---
st.subheader("🎹 Siku Virtual")
if st.session_state.audio_file:
    placeholder = st.empty()
    if os.path.exists(st.session_state.audio_file):
        placeholder.audio(st.session_state.audio_file, autoplay=True)
        time.sleep(1.2)
        placeholder.empty()
        st.session_state.audio_file = None
        st.rerun()

# ARKA (Botones 1-7)
c_arka = st.columns([1.5, 1, 1, 1, 1, 1, 1, 1])
with c_arka[0]:
    st.markdown(
        '<div class="row-label arka-label">ARKA (1-7)</div>', unsafe_allow_html=True
    )
# Las notas del Arka en el instrumento real suelen ir de agudo a grave (Si2 a Re0)
ARKA_VIRTUAL = ["Si2", "Sol2", "Mi", "Do", "La", "Fa#0", "Re0"]
for i, n in enumerate(ARKA_VIRTUAL):
    with c_arka[i + 1]:
        st.button(f"{TABLATURA.get(n)}\n{n}", key=f"a_{n}", on_click=tocar, args=(n,))

# IRA (Botones Q-Y)
c_ira = st.columns([1.5, 0.5, 1, 1, 1, 1, 1, 1])
with c_ira[0]:
    st.markdown(
        '<div class="row-label ira-label">IRA (Q-Y)</div>', unsafe_allow_html=True
    )
IRA_VIRTUAL = ["La2", "Fa#", "Re", "Si", "Sol", "Mi0"]
for i, n in enumerate(IRA_VIRTUAL):
    with c_ira[i + 2]:
        st.button(f"{TABLATURA.get(n)}\n{n}", key=f"i_{n}", on_click=tocar, args=(n,))
