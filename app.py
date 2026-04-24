import os

import streamlit as st

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
    t_limpia = tonica.capitalize().replace(" ", "")
    t_limpia = BEMOLES.get(t_limpia, t_limpia)
    if t_limpia not in NOTAS_MUSICALES:
        return None
    idx = NOTAS_MUSICALES.index(t_limpia)
    escala = []
    actual = idx
    for p in pasos:
        escala.append(NOTAS_MUSICALES[actual % 12])
        actual += p
    return escala


# --- REPARTO ESTÁNDAR (Coincide con tus archivos) ---
ARKA = ["Re0", "Fa#0", "La", "Do", "Mi", "Sol2", "Si2"]
IRA = ["Mi0", "Sol", "Si", "Re", "Fa#", "La2"]
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

# --- INTERFAZ ---
st.set_page_config(page_title="SikuTab", page_icon="🎶", layout="wide")
st.title("🎶 SikuTab: Transpositor y Teclado")
st.caption("Prof. Pablo Olivero - Liceo San José del Carmen")

# --- CONFIGURACIÓN ---
col_t, col_m = st.columns([1, 1])
with col_t:
    original_tonica = st.selectbox("Tonalidad Original", NOTAS_MUSICALES)
with col_m:
    modo = st.radio("Modo", ["Mayor", "Menor"], horizontal=True)

# --- GUÍA DESPLEGABLE ---
with st.expander("📖 Guía de Octavas y Registro Real"):
    st.markdown("### Cómo escribir:")
    st.markdown(
        "- <span style='color: #9b59b6;'>**Agudos:**</span> Agrega un **2** (ej: `sol2`).",
        unsafe_allow_html=True,
    )
    st.markdown("- **Medios:** Solo la nota (ej: `sol`).")
    st.markdown(
        "- <span style='color: #e67e22;'>**Graves:**</span> Agrega un **0** (ej: `re0`).",
        unsafe_allow_html=True,
    )
    st.markdown("### Notas en el Siku:")
    st.markdown(
        "<span style='color: #9b59b6;'>**AGUDOS:** Sol2, La2, Si2</span>",
        unsafe_allow_html=True,
    )
    st.markdown("**MEDIOS:** Sol, La, Si, Do, Re, Mi, Fa#")
    st.markdown(
        "<span style='color: #e67e22;'>**GRAVES:** Re0, Mi0, Fa#0</span>",
        unsafe_allow_html=True,
    )

# --- TECLADO VIRTUAL ---
st.subheader("🎹 Teclado de Referencia")


def reproducir(nota):
    archivo = f"{nota}.wav"
    if os.path.exists(archivo):
        st.audio(archivo, format="audio/wav")
    else:
        st.error(f"Falta: {archivo}")


c_arka, c_ira = st.columns(2)
with c_arka:
    st.markdown("<span style='color: #9b59b6;'>**ARKA**</span>", unsafe_allow_html=True)
    cols = st.columns(len(ARKA))
    for i, n in enumerate(ARKA):
        if cols[i].button(n, key=f"a_{n}"):
            reproducir(n)
with c_ira:
    st.markdown("<span style='color: #e67e22;'>**IRA**</span>", unsafe_allow_html=True)
    cols = st.columns(len(IRA))
    for i, n in enumerate(IRA):
        if cols[i].button(n, key=f"i_{n}"):
            reproducir(n)

st.write("---")

# --- ENTRADA (ENTER PARA PROCESAR) ---
entrada = st.text_input(
    "Escribe la melodía aquí y presiona ENTER:", placeholder="Ej: re0 mi0 sol la do2"
)

if entrada:
    ref_original = generar_escala(original_tonica, modo.lower())
    dest, nombre_final = (
        (["Sol", "La", "Si", "Do", "Re", "Mi", "Fa#"], "SOL MAYOR")
        if modo == "Mayor"
        else (["Mi", "Fa#", "Sol", "La", "Si", "Do", "Re"], "MI MENOR")
    )

    notas_usuario = [n.strip() for n in entrada.split() if n.strip()]
    f_arka_n, f_ira_n = "ARKA (Notas):  ", "IRA  (Notas):  "
    f_arka_num, f_ira_num = "ARKA (Num):    ", "IRA  (Num):    "
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
            elif nota_t in IRA:
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
    st.code(f"{f_arka_n}\n{f_ira_n}\n{'-' * 30}\n{f_arka_num}\n{f_ira_num}")
