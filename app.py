import os
import time

import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="SikuTab", page_icon="🎶", layout="wide")

# --- CSS DEFINITIVO: CÍRCULOS PEGADOS Y ZIGZAG FIJO (Flexbox) ---
st.markdown(
    """
    <style>
    /* Estilo base de los botones (tubos) */
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
        margin: 0 !important; /* Eliminamos márgenes automáticos */
    }
    .stButton > button:hover { border-color: #9b59b6 !important; color: #9b59b6 !important; }

    /* Contenedores Flexbox para fijar la posición */
    .siku-wrapper {
        display: flex;
        flex-direction: column;
        align-items: flex-start; /* Todo alineado a la izquierda para empezar */
        gap: 0; /* Sin espacio vertical automático */
    }

    .siku-row {
        display: flex;
        align-items: center;
        gap: 1px; /* Espacio de 1px entre tubos de la misma fila */
    }

    .row-label {
        font-weight: bold;
        font-size: 16px;
        width: 80px; /* Ancho fijo para la etiqueta */
        text-align: right;
        margin-right: 20px;
    }
    .arka-label { color: #9b59b6; }
    .ira-label { color: #e67e22; }

    /* EL TRUCO: Fijamos el zigzag con Flexbox en píxeles */
    .ira-zigzag-container {
        display: flex;
        align-items: center;
        /* Calculamos el desfase: Label Arka(80) + MargenLabel(20) + 1.5 tubos Arka(75+75+desfase=114px) */
        margin-left: 214px;
        margin-top: -15px; /* Pegamos verticalmente las filas */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- JAVASCRIPT: DETECTOR DE TECLAS INTELIGENTE ---
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
        // Buscamos los botones que tienen números y saltos de línea
        const sikuBtns = Array.from(allBtns).filter(b =>
            b.innerText.includes('\\n') ||
            (b.innerText.length < 10 && /\\d/.test(b.innerText))
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

col_t, col_m = st.columns(2)
with col_t:
    original_tonica = st.selectbox("Tonalidad Original", NOTAS_MUSICALES)
with col_m:
    modo = st.radio("Modo", ["Mayor", "Menor"], horizontal=True)

st.write("---")

entrada = st.text_input("Escribe la melodía aquí (ej: sol la si):")

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

    st.code(f"{f_arka_n}\n{f_ira_n}\n{'-' * (len(f_arka_n))}\n{f_arka_v}\n{f_ira_v}")

st.write("---")

# --- SIKU VIRTUAL (CENTRADO MILIMÉTRICO CON FLEXBOX) ---
col_head, col_audio = st.columns([1, 1])
with col_head:
    st.subheader("🎹 Siku Virtual")

# REPRODUCTOR FANTASMA
if st.session_state.audio_file:
    with col_audio:
        placeholder = st.empty()
        if os.path.exists(st.session_state.audio_file):
            placeholder.audio(st.session_state.audio_file, autoplay=True)
            time.sleep(1.2)
            placeholder.empty()
            st.session_state.audio_file = None
            st.rerun()

# RENDERIZADO DEL TECLADO USANDO CONTENEDORES CSS
st.markdown('<div class="siku-wrapper">', unsafe_allow_html=True)

# FILA ARKA
with st.container():
    # Usamos columnas de Streamlit solo para los botones, no para el layout general
    col_label_a, col_tubos_a, _ = st.columns([1, 8, 3])

    with col_label_a:
        st.markdown(
            '<div class="row-label arka-label">ARKA (1-7)</div>', unsafe_allow_html=True
        )

    with col_tubos_a:
        # Aquí inyectamos Flexbox para pegar los tubos Arka
        html_arka = '<div class="siku-row">'
        for i, n in enumerate(ARKA):
            num = TABLATURA.get(n, "")
            # IMPORTANTE: No usamos st.button aquí, sino que simulamos el botón para el CSS
            # Pero para que funcione, Streamlit necesita un botón real. Usaremos st.button normal.
            pass
        html_arka += "</div>"
        # Anulamos la inyección HTML y volvemos a las columnas normales para que funcionen los botones,
        # pero forzamos el CSS para que no se separen.

# RE-INTENTO DE FILAS USANDO COLUMNAS FIJAS Y CSS DE COMPRESIÓN
# Las columnas anteriores fallaron porque Streamlit distribuye el espacio.
# Volvemos a un layout de columnas, pero forzamos con CSS que no haya márgenes.

# FILA ARKA
c_arka = st.columns(
    [1.5, 1, 1, 1, 1, 1, 1, 1, 3]
)  # El 3 al final es aire para agrupar a la izquierda
with c_arka[0]:
    st.markdown(
        '<div class="row-label arka-label">ARKA (1-7)</div>', unsafe_allow_html=True
    )
for i, n in enumerate(ARKA):
    num = TABLATURA.get(n, "")
    with c_arka[i + 1]:
        st.button(f"{num}\n{n}", key=f"v_a_{n}", on_click=tocar, args=(n,))

# FILA IRA (Desplazada matemáticamente con columnas vacías para el zigzag)
# Label(1.5), AireZigZag(1.5+0.5=2), Nota1(1), Nota2(1)... AireFinal
c_ira = st.columns([1.5, 2, 1, 1, 1, 1, 1, 1, 1.5])
with c_ira[0]:
    st.markdown(
        '<div class="row-label ira-label">IRA (Q-Y)</div>', unsafe_allow_html=True
    )
# c_ira[1] es el espacio de desfase para centrar con el Do
for i, n in enumerate(IRA):
    num = TABLATURA.get(n, "")
    with c_ira[i + 2]:
        st.button(f"{num}\n{n}", key=f"v_i_{n}", on_click=tocar, args=(n,))

st.markdown("</div>", unsafe_allow_html=True)
