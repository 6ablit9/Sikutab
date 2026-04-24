import os

import streamlit as st

# --- CONFIGURACIÓN E INYECCIÓN DE DISEÑO ---
st.set_page_config(page_title="SikuTab", page_icon="🎶", layout="wide")

st.markdown(
    """
    <style>
    /* Estilo de los tubos (círculos) */
    .stButton > button {
        border-radius: 50% !important;
        width: 80px !important;
        height: 80px !important;
        border: 2px solid #555 !important;
        background-color: #2e2e2e !important;
        color: white !important;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        line-height: 1.1 !important;
        padding: 0 !important;
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
        height: 80px;
    }
    .arka-label { color: #9b59b6; }
    .ira-label { color: #e67e22; }

    /* Pegar las filas verticalmente para el zigzag */
    .stVerticalBlock {
        gap: 0rem !important;
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


def disparar_audio(nota, placeholder):
    archivo = f"{nota}.wav"
    if os.path.exists(archivo):
        placeholder.audio(archivo, format="audio/wav", autoplay=True)


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
entrada = st.text_input("Escribe la melodía aquí (ENTER para procesar):")

if entrada:
    ref_original = generar_escala(original_tonica, modo.lower())
    dest = (
        ["Sol", "La", "Si", "Do", "Re", "Mi", "Fa#"]
        if modo == "Mayor"
        else ["Mi", "Fa#", "Sol", "La", "Si", "Do", "Re"]
    )

    notas_usuario = [n.strip() for n in entrada.split() if n.strip()]
    f_arka_n, f_ira_n, f_arka_num, f_ira_num = "ARKA: ", "IRA:  ", "NUM:  ", "NUM:  "
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
            else:
                f_arka_n += " " * ancho
                f_ira_n += nota_t.ljust(ancho)

    st.code(f"{f_arka_n}\n{f_ira_n}")

st.write("---")

# --- SIKU VIRTUAL (Zigzag corregido) ---
col_head, col_audio = st.columns([1, 1])
with col_head:
    st.subheader("🎹 Siku Virtual")
audio_placeholder = col_audio.empty()

# Ajuste de columnas para el zigzag:
# Arka: [Etiqueta(1), Nota1(1), Nota2(1)...]
# Ira:  [Etiqueta(1), Espacio(0.5), Nota1(1), Nota2(1)...]

# FILA ARKA
c_label_a, *c_arka_tubos = st.columns([1, 1, 1, 1, 1, 1, 1, 1])
with c_label_a:
    st.markdown('<div class="row-label arka-label">ARKA</div>', unsafe_allow_html=True)

for i, n in enumerate(ARKA):
    num = TABLATURA.get(n, "")
    with c_arka_tubos[i]:
        if st.button(f"{num}\n{n}", key=f"v_a_{n}"):
            disparar_audio(n, audio_placeholder)

# FILA IRA
c_label_i, desfase, *c_ira_tubos = st.columns([1, 0.5, 1, 1, 1, 1, 1, 1])
with c_label_i:
    st.markdown('<div class="row-label ira-label">IRA</div>', unsafe_allow_html=True)

for i, n in enumerate(IRA):
    num = TABLATURA.get(n, "")
    with c_ira_tubos[i]:
        if st.button(f"{num}\n{n}", key=f"v_i_{n}"):
            disparar_audio(n, audio_placeholder)
