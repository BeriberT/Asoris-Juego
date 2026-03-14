import streamlit as st
import numpy as np

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="El Rescate de la Princesa", layout="centered")
st.title("👸 La Torre de la Princesa")

# --- ESTADO DEL JUEGO ---
if 'player_pos' not in st.session_state:
    st.session_state.player_pos = [5, 5]

# --- EL MAPA ---
# 1 = Pared, 2 = Cristal Mágico
tower_map = np.zeros((10, 10))
tower_map[0,:] = 1; tower_map[-1,:] = 1
tower_map[:,0] = 1; tower_map[:,-1] = 1
tower_map[8, 8] = 2

# --- CONTROLES CON LÓGICA DE COLISIÓN ---
def move_player(dr, dc):
    new_r = st.session_state.player_pos[0] + dr
    new_c = st.session_state.player_pos[1] + dc
    # Solo movemos si la nueva posición no es una pared (1)
    if tower_map[new_r, new_c] != 1:
        st.session_state.player_pos = [new_r, new_c]

col1, col2, col3 = st.columns([1,1,1])
with col2: 
    if st.button("🔼", use_container_width=True): move_player(-1, 0)
with col1: 
    if st.button("◀️", use_container_width=True): move_player(0, -1)
with col3: 
    if st.button("▶️", use_container_width=True): move_player(0, 1)
with col2: 
    if st.button("🔽", use_container_width=True): move_player(1, 0)

# --- RENDERIZADO ---
def draw_world(m, p):
    res = ""
    for r in range(len(m)):
        for c in range(len(m[0])):
            if [r, c] == p: res += "👸" # <--- ¡Aquí está la princesa!
            elif m[r, c] == 1: res += "⬛"
            elif m[r, c] == 2: res += "💎"
            else: res += "⬜"
        res += "\n"
    return res

st.text(draw_world(tower_map, st.session_state.player_pos))

# --- LÓGICA DE ACERTIZOS ---
if tower_map[st.session_state.player_pos[0], st.session_state.player_pos[1]] == 2:
    st.warning("¡Has encontrado el Cristal de la Verdad!")
    respuesta = st.text_input("¿Qué es aquello que si lo nombras, desaparece?")
    if respuesta.lower() in ["silencio", "el silencio"]:
        st.balloons()
        st.success("¡Has escapado de la torre!")