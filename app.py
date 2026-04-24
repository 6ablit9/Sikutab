import os
import time

import streamlit as st

# --- CONFIGURACIÓN E INYECCIÓN DE DISEÑO (Círculos Intercalados) ---
st.set_page_config(page_title="SikuTab", page_icon="🎶", layout="wide")

st.markdown(
    """
    <style>
    /* Estilo de los tubos */
    .stButton > button {
        border-radius: 50% !important;
        width: 85px !important;
        height: 85px !important;
        border: 2px solid #555 !important;
        background-color: #2e2e2e !important;
        color: white !important;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        line-height: 1.1 !important;
    }
    .stButton > button:hover {
        border-color: #9b59b6 !important;
        color: #9b59b6 !important;
    }
    /* Etiquetas laterales */
    .row-label {
        font-weight: bold;
        font-size: 18px;
        display: flex;
        align-items: center;
        height: 85px;
    }
    .arka-label { color: #9b59b6; }
    .ira-label { color: #e67e22; }

    /* Ajuste para intercalado perfecto */
    .ira-row {
        margin-top: -10px;
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
    if t_limpia not in NOTAS_MUSICALES:
        return None
    idx = NOTAS_MUSICALES.index(t_limpia)
    escala = []
    actual = idx
    for p in pasos:
        escala.append(NOTAS_MUSICALES[actual % 12])
        actual += p
    return escala


# --- DISPOSICIÓN ---
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

# --- INTERFAZ SUPERIOR ---
st.title("🎶 SikuTab: Transpositor y Siku Virtual")
st.caption("Prof. Pablo Olivero - Liceo San José del Carmen")

col_t, col_m = st.columns(2)
with col_t:
    original_tonica = st.selectbox("Tonalidad Original", NOTAS_MUSICALES)
with col_m:
    modo = st.radio("Modo", ["Mayor", "Menor"], horizontal=True)

st.write("---")

# --- TRANSPOSICIÓN ---
entrada = st.text_input(
    "Escribe la melodía aquí y presiona ENTER:", placeholder="Ej: re0 mi0 sol la do2"
)

if entrada:
    ref_original = generar_escala(original_tonica, modo.lower())
    dest = (
        ["Sol", "La", "Si", "Do", "Re", "Mi", "Fa#"]
        if modo == "Mayor"
        else ["Mi", "Fa#", "Sol", "La", "Si", "Do", "Re"]
    )

    notas_usuario = [n.strip() for n in entrada.split() if n.strip()]
    f_arka_n, f_ira_n, f_arka_num, f_ira_num = (
        "ARKA (Notas):  ",
        "IRA  (Notas):  ",
        "ARKA (Num):    ",
        "IRA  (Num):    ",
    )
    ancho = 8

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
                f_arka_num += num_t.ljust(ancho)
                f_ira_num += " " * ancho
            else:
                f_arka_n += " " * ancho
                f_ira_n += nota_t.ljust(ancho)
                f_arka_num += " " * ancho
                f_ira_num += num_t.ljust(ancho)

    st.code(f"{f_arka_n}\n{f_ira_n}\n{'-' * 30}\n{f_arka_num}\n{f_ira_num}")

st.write("---")

# --- SIKU VIRTUAL (Intercalado) ---
col_head, col_audio = st.columns([1, 1])
with col_head:
    st.subheader("🎹 Siku Virtual")
audio_placeholder = col_audio.empty()


# Función para disparar audio con clave única para repeticiones
def disparar_audio(nota):
    archivo = f"{nota}.wav"
    if os.path.exists(archivo):
        # Usamos time.time para que la clave siempre sea distinta y la barra refresque
        audio_placeholder.audio(archivo, format="audio/wav", autoplay=True)


# FILA ARKA (Etiqueta + 7 Notas)
c_label, *c_arka_tubos = st.columns([1.5, 1, 1, 1, 1, 1, 1, 1])
with c_label:
    st.markdown('<div class="row-label arka-label">ARKA</div>', unsafe_allow_html=True)

for i, n in enumerate(ARKA):
    num = TABLATURA.get(n, "")
    with c_arka_tubos[i]:
        if st.button(f"{num}\n{n}", key=f"btn_a_{n}"):
            disparar_audio(n)

# FILA IRA (Etiqueta + Desfase de media columna para intercalar + 6 Notas)
st.markdown('<div class="ira-row">', unsafe_allow_html=True)
# El desfase '0.5' después de la etiqueta es la clave del intercalado
c_label_i, desfase, *c_ira_tubos = st.columns([1.5, 0.5, 1, 1, 1, 1, 1, 1])
with c_label_i:
    st.markdown('<div class="row-label ira-label">IRA</div>', unsafe_allow_html=True)

for i, n in enumerate(IRA):
    num = TABLATURA.get(n, "")
    with c_ira_tubos[i]:
        if st.button(f"{num}\n{n}", key=f"btn_i_{n}"):
            disparar_audio(n)
st.markdown("</div>", unsafe_allow_html=True)
