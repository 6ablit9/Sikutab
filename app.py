import os
import time

import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="SikuTab", page_icon="🎶", layout="wide")

# --- CSS DEFINITIVO: PALETA DE COLORES ORIGINAL ---
st.markdown(
    """
    <style>
    /* 1. Fondo general de la página */
    .stApp {
        background-color: #1e1e1e;
        color: #f0f0f0;
    }

    /* 2. Botones del Siku (Tubos) */
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
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        border-color: #9b59b6 !important;
        color: #9b59b6 !important;
        background-color: #3a3a3a !important;
    }

    /* 3. Etiquetas Laterales */
    .row-label { font-weight: bold; font-size: 16px; display: flex; align-items: center; height: 75px; color: white; }
    .arka-label { color: #9b59b6; }
    .ira-label { color: #e67e22; }

    /* 4. Cuadro de Guía Desplegable (Texto Negro Legible) */
    .top-info-box {
        background-color: #f4ecf7;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #9b59b6;
        color: #000000 !important;
        font-size: 14px;
        line-height: 1.4;
    }
    .top-info-box b { color: #000000; }

    /* 5. Cuadro de Código (Resultado) */
    div[data-testid="stCodeBlock"] pre {
        background-color: #000000 !important;
        color: #00ff00 !important;
        border: 1px solid #333;
    }

    /* Compresión visual */
    [data-testid="stHorizontalBlock"] {
        width: fit-content !important;
        gap: 4px !important;
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
            b.innerText.includes('\\n') || (b.innerText.length < 10 && /\\d/.test(b.innerText))
        );
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
st.caption("Prof. Pablo Olivero - Liceo San José del Carmen")

col_controles, col_guia = st.columns([1, 1.5])

with col_controles:
    st.subheader("⚙️ Configuración")
    original_tonica = st.selectbox("Tonalidad Original", NOTAS_MUSICALES)
    modo = st.radio("Modo", ["Mayor", "Menor"], horizontal=True)


with col_guia:
    with st.expander("📖 Guía de Octavas y Registro Real", expanded=True):
        st.markdown(
            """
        <div class="top-info-box">
            <b>Cómo escribir las notas:</b><br>
            • <b>Registro Agudo:</b> Agrega un <b>2</b> (ej: sol2, la2).<br>
            • <b>Registro Medio:</b> Escribe la nota normal (ej: sol, la, si).<br>
            • <b>Registro Grave:</b> Agrega un <b>0</b> (ej: re0, mi0).<br><hr>
            <b>Notas en el Siku (Arka 7 / Ira 6):</b><br>
            Sol2 a Si2 | Sol a Fa# | Re0 a Fa#0
        </div>
        """,
            unsafe_allow_html=True,
        )

st.write("---")

entrada = st.text_area(
    "📝 Escribe la melodía aquí:", placeholder="Ejemplo: sol la si do2 re2", height=100
)

if entrada:
    ref_original = generar_escala(original_tonica, modo.lower())
    dest = (
        ["Sol", "La", "Si", "Do", "Re", "Mi", "Fa#"]
        if modo == "Mayor"
        else ["Mi", "Fa#", "Sol", "La", "Si", "Do", "Re"]
    )

    notas_usuario = [n.strip() for n in entrada.split() if n.strip()]
    f_arka_n, f_ira_n = "ARKA (Notas): ", "IRA  (Notas): "
    f_arka_v, f_ira_v = "ARKA (Num):   ", "IRA  (Num):   "
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

            if nota_t in ARKA:
                f_arka_n += nota_t.ljust(ancho)
                f_ira_n += " " * ancho
                f_arka_v += str(num_t).ljust(ancho)
                f_ira_v += " " * ancho
            else:
                f_arka_n += " " * ancho
                f_ira_n += nota_t.ljust(ancho)
                f_arka_v += " " * ancho
                f_ira_v += str(num_t).ljust(ancho)

    st.markdown("### 🎼 Resultado")
    st.code(f"{f_arka_n}\n{f_ira_n}\n{'-' * (len(f_arka_n))}\n{f_arka_v}\n{f_ira_v}")

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

# ARKA
c_arka = st.columns([1.5, 1, 1, 1, 1, 1, 1, 1])
with c_arka[0]:
    st.markdown(
        '<div class="row-label arka-label">ARKA (1-7)</div>', unsafe_allow_html=True
    )
for i, n in enumerate(ARKA):
    num = TABLATURA.get(n, "")
    with c_arka[i + 1]:
        st.button(f"{num}\n{n}", key=f"v_a_{n}", on_click=tocar, args=(n,))

# IRA
c_ira = st.columns([1.5, 0.5, 1, 1, 1, 1, 1, 1])
with c_ira[0]:
    st.markdown(
        '<div class="row-label ira-label">IRA (Q-Y)</div>', unsafe_allow_html=True
    )
for i, n in enumerate(IRA):
    num = TABLATURA.get(n, "")
    with c_ira[i + 2]:
        st.button(f"{num}\n{n}", key=f"v_i_{n}", on_click=tocar, args=(n,))
