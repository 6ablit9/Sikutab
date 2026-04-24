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
        line-height: 1.2 !important;
    }
    .stButton > button:hover {
        border-color: #9b59b6 !important;
        color: #9b59b6 !important;
    }
    /* Estilo para los nombres laterales */
    .row-label {
        font-weight: bold;
        font-size: 20px;
        display: flex;
        align-items: center;
        height: 80px;
    }
    .arka-label { color: #9b59b6; }
    .ira-label { color: #e67e22; }

    /* Contenedor para desplazar la Ira y que encaje entre los tubos del Arka */
    .ira-container {
        padding-left: 20px;
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


# --- DISPOSICIÓN Y TABLATURA ---
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


def reproducir(nota):
    archivo = f"{nota}.wav"
    if os.path.exists(archivo):
        # El reproductor aparece arriba (donde se llama a esta función)
        return archivo
    return None


# --- INTERFAZ SUPERIOR ---
st.title("🎶 SikuTab: Transpositor y Teclado")
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

# --- SIKU VIRTUAL (AL FINAL) ---
col_title, col_audio = st.columns([1, 1])
with col_title:
    st.subheader("🎹 Siku Virtual")

# Espacio para el audio (fijo arriba del teclado)
audio_placeholder = col_audio.empty()

# Filas del teclado con etiquetas a la izquierda
# Fila ARKA
c_label, *c_tubos = st.columns([1, 1, 1, 1, 1, 1, 1, 1])
with c_label:
    st.markdown('<div class="row-label arka-label">ARKA</div>', unsafe_allow_html=True)

for i, n in enumerate(ARKA):
    num = TABLATURA.get(n, "")
    with c_tubos[i]:
        # El nombre del botón incluye el número arriba y la nota abajo
        if st.button(f"{num}\n{n}", key=f"a_{n}"):
            res = reproducir(n)
            if res:
                audio_placeholder.audio(res, format="audio/wav", autoplay=True)

# Fila IRA
st.markdown('<div class="ira-container">', unsafe_allow_html=True)
# Usamos un desfase en las columnas para que la Ira encaje visualmente
c_label_i, spacer, *c_tubos_i = st.columns([1, 0.5, 1, 1, 1, 1, 1, 1])
with c_label_i:
    st.markdown('<div class="row-label ira-label">IRA</div>', unsafe_allow_html=True)

for i, n in enumerate(IRA):
    num = TABLATURA.get(n, "")
    with c_tubos_i[i]:
        if st.button(f"{num}\n{n}", key=f"i_{n}"):
            res = reproducir(n)
            if res:
                audio_placeholder.audio(res, format="audio/wav", autoplay=True)
st.markdown("</div>", unsafe_allow_html=True)
