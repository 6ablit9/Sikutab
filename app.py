# --- SIKU VIRTUAL (Zig-Zag Real con CSS Flexbox) ---
col_head, col_audio = st.columns([1, 1])
with col_head:
    st.subheader("🎹 Siku Virtual")
audio_placeholder = col_audio.empty()


def disparar_audio(nota):
    archivo = f"{nota}.wav"
    if os.path.exists(archivo):
        audio_placeholder.audio(archivo, format="audio/wav", autoplay=True)


# Contenedor principal para el teclado
st.markdown(
    """
    <style>
    .siku-wrapper {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 5px;
        padding: 20px;
        background-color: #121212;
        border-radius: 15px;
    }
    .siku-row {
        display: flex;
        align-items: center;
        gap: 10px; /* Espacio mínimo entre tubos */
    }
    .label-siku {
        width: 80px;
        font-weight: bold;
        font-size: 18px;
    }
    .arka-txt { color: #9b59b6; }
    .ira-txt { color: #e67e22; }

    /* El truco del zig-zag: desplazamos la fila IRA media posición de tubo */
    .ira-offset {
        margin-left: 125px; /* Ajuste manual para que el 1 de IRA quede entre el 1 y 2 de ARKA */
        margin-top: -15px;  /* Los pegamos un poco más verticalmente */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Renderizado del teclado
with st.container():
    # --- FILA ARKA ---
    col_a_label, *col_a_btns = st.columns([1.5, 1, 1, 1, 1, 1, 1, 1])
    with col_a_label:
        st.markdown(
            '<div class="row-label arka-label">ARKA</div>', unsafe_allow_html=True
        )

    for i, n in enumerate(ARKA):
        num = TABLATURA.get(n, "")
        with col_a_btns[i]:
            if st.button(f"{num}\n{n}", key=f"v_a_{n}"):
                disparar_audio(n)

    # --- FILA IRA (Intercalada) ---
    # Usamos un set de columnas diferente para forzar el zigzag
    # [Etiqueta, Medio Espacio, Tubo1, Tubo2...]
    col_i_label, offset, *col_i_btns = st.columns([1.5, 0.5, 1, 1, 1, 1, 1, 1])
    with col_i_label:
        st.markdown(
            '<div class="row-label ira-label">IRA</div>', unsafe_allow_html=True
        )

    # El 'offset' queda vacío para empujar los botones a la derecha
    for i, n in enumerate(IRA):
        num = TABLATURA.get(n, "")
        with col_i_btns[i]:
            if st.button(f"{num}\n{n}", key=f"v_i_{n}"):
                disparar_audio(n)
