import streamlit as st
import numpy as np
import os
import base64

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Aventura en la Torre", layout="centered")

# --- FUNCIÓN PARA CARGAR IMAGEN DE FONDO ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- ESCENARIOS (Rutas actualizadas a carpeta 'ima') ---
escenarios = [
    {"nombre": "Torre", "imagen": "ima/Torre.jpg"},
    {"nombre": "Cocina", "imagen": "ima/cocina.png"},
    {"nombre": "Comedor", "imagen": "ima/comedor.png"},
    {"nombre": "Biblioteca", "imagen": "ima/biblioteca.png"},
    {"nombre": "Sala del Tesoro", "imagen": "ima/sala del tesoro.png"},
    {"nombre": "Observatorio", "imagen": "ima/observatorio.png"}
]

# --- ESTADO ---
if 'room_index' not in st.session_state:
    st.session_state.room_index = 0
if 'player_pos' not in st.session_state:
    st.session_state.player_pos = [4, 4]
if 'direction' not in st.session_state:
    st.session_state.direction = "derecha"
if 'player_name' not in st.session_state:
    st.session_state.player_name = ""

room_actual = escenarios[st.session_state.room_index]["nombre"]
img_escenario = escenarios[st.session_state.room_index]["imagen"]

st.title(f"🏰 {room_actual}")

# --- ESTILO CSS PARA EL FONDO Y ESPEJO ---
bg_style = ""
if os.path.exists(img_escenario):
    bin_str = get_base64(img_escenario)
    bg_style = f"""
    <style>
    .stMain {{ 
        background-image: url(\"data:image/png;base64,{bin_str}\");
        background-size: cover;
        background-position: center;
    }}
    .mirror-img img {{ transform: scaleX(-1); }}
    .game-cell {{ height: 50px; display: flex; align-items: center; justify-content: center; }}
    </style>
    """
st.markdown(bg_style, unsafe_allow_html=True)

# --- SELECCIÓN (Rutas actualizadas a carpeta 'ima') ---
if st.session_state.room_index == 0:
    st.session_state.player_name = st.text_input("Nombre:", value=st.session_state.player_name)

personajes = {"Princesa": "ima/F_04.png", "Mago": "ima/aM_02.png"}
hero_choice = st.selectbox("Héroe:", list(personajes.keys()))
IMG_HERO = personajes[hero_choice]

# --- MOVIMIENTO ---
def move_player(dr, dc):
    nr, nc = st.session_state.player_pos[0] + dr, st.session_state.player_pos[1] + dc
    if 0 <= nr < 8 and 0 <= nc < 8:
        if dc > 0: st.session_state.direction = "derecha"
        elif dc < 0: st.session_state.direction = "izquierda"
        st.session_state.player_pos = [nr, nc]

# --- RENDERIZADO SOBRE EL FONDO ---
for r in range(8):
    cols = st.columns(8)
    for c in range(8):
        with cols[c]:
            st.markdown('<div class="game-cell">', unsafe_allow_html=True)
            if [r, c] == st.session_state.player_pos:
                if os.path.exists(IMG_HERO):
                    if st.session_state.direction == "izquierda":
                        st.markdown('<div class="mirror-img">', unsafe_allow_html=True)
                        st.image(IMG_HERO, width=40)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else: st.image(IMG_HERO, width=40)
                else: st.write("👸")
            elif r == 7 and c == 7: st.write("🚪")
            else: st.write("")
            st.markdown('</div>', unsafe_allow_html=True)

# --- CONTROLES ---
st.write("---")
c1, c2, c3 = st.columns([1,1,1])
with c2: st.button("🔼", on_click=move_player, args=(-1, 0))
with c1: st.button("◀️", on_click=move_player, args=(0, -1))
with c3: st.button("▶️", on_click=move_player, args=(0, 1))
with c2: st.button("🔽", on_click=move_player, args=(1, 0))

if st.session_state.player_pos == [7, 7]:
    if st.session_state.room_index < len(escenarios) - 1:
        if st.button("Siguiente Sala"):
            st.session_state.room_index += 1
            st.session_state.player_pos = [1, 1]
            st.rerun()
    else: st.success("¡Victoria!")