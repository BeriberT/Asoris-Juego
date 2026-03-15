import streamlit as st
import numpy as np
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Aventura en la Torre", layout="centered")

# --- ORDEN DE LOS ESCENARIOS ---
escenarios = ["Torre", "Cocina", "Comedor", "Biblioteca", "Sala del Tesoro", "Observatorio"]

# --- ESTADO DEL JUEGO ---
if 'room_index' not in st.session_state:
    st.session_state.room_index = 0
if 'player_pos' not in st.session_state:
    st.session_state.player_pos = [1, 1]
if 'direction' not in st.session_state:
    st.session_state.direction = "derecha"
if 'player_name' not in st.session_state:
    st.session_state.player_name = ""

room_actual = escenarios[st.session_state.room_index]
st.title(f"🏰 {room_actual}")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    .mirror-img img { transform: scaleX(-1); display: inline-block; }
    </style>
""", unsafe_allow_html=True)

# --- DATOS E IDENTIDAD ---
if st.session_state.room_index == 0:
    st.session_state.player_name = st.text_input("¿Cómo te llamas?", value=st.session_state.player_name)

personajes = {
    "Princesa (F_04)": "F_04.png", "Princesa (aF_04)": "aF_04.png", "Mago (aM_02)": "aM_02.png", "Mago (aM_05)": "aM_05.png"
}
hero_choice = st.selectbox("Héroe:", list(personajes.keys()))
IMG_HERO = personajes[hero_choice]

# --- MAPA (8x8) ---
tower_map = np.zeros((8, 8))
tower_map[0,:] = 1; tower_map[-1,:] = 1; tower_map[:,0] = 1; tower_map[:,-1] = 1
tower_map[6, 6] = 2 # Meta

# --- LÓGICA DE MOVIMIENTO ---
def move_player(dr, dc):
    new_r = st.session_state.player_pos[0] + dr
    new_c = st.session_state.player_pos[1] + dc
    if dc > 0: st.session_state.direction = "derecha"
    elif dc < 0: st.session_state.direction = "izquierda"
    
    if 0 <= new_r < 8 and 0 <= new_c < 8:
        if tower_map[new_r, new_c] != 1:
            st.session_state.player_pos = [new_r, new_c]

# --- RENDERIZADO ---
for r in range(8):
    cols = st.columns(8)
    for c in range(8):
        with cols[c]:
            if [r, c] == st.session_state.player_pos:
                if os.path.exists(IMG_HERO):
                    if st.session_state.direction == "izquierda":
                        st.markdown('<div class="mirror-img">', unsafe_allow_html=True)
                        st.image(IMG_HERO, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else: st.image(IMG_HERO, use_container_width=True)
                else: st.write("👸")
            elif tower_map[r, c] == 1: st.write("⬛")
            elif tower_map[r, c] == 2: st.write("🚪")
            else: st.write("⬜")

# --- CONTROLES ---
st.write("---")
c1, c2, c3 = st.columns([1,1,1])
with c2: st.button("🔼", on_click=move_player, args=(-1, 0))
with c1: st.button("◀️", on_click=move_player, args=(0, -1))
with c3: st.button("▶️", on_click=move_player, args=(0, 1))
with c2: st.button("🔽", on_click=move_player, args=(1, 0))

# --- CAMBIO DE NIVEL ---
if st.session_state.player_pos == [6, 6]:
    if st.session_state.room_index < len(escenarios) - 1:
        if st.button(f"Ir a la {escenarios[st.session_state.room_index+1]}"):
            st.session_state.room_index += 1
            st.session_state.player_pos = [1, 1]
            st.rerun()
    else:
        st.balloons()
        st.success(f"¡Increíble {st.session_state.player_name}! Completaste el Observatorio final.")