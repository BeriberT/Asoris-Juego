import hashlib
import unicodedata
import requests
import streamlit as st
import base64
import os
import json

st.set_page_config(page_title="El Desafío de las Puertas", page_icon="🏰", layout="centered")

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# Cargar imágenes principales
b64_fondo = get_base64("ima/Torre.jpg")
b64_tesoro = get_base64("ima/Ctesoro.jpg")
b64_vacio = get_base64("ima/Cvacio.jpg")

# Lógica de cambio de fondo total
if "mostrar_rec" not in st.session_state:
    st.session_state.mostrar_rec = -1

RECOMPENSAS = [
    {"tipo": "video", "contenido": "ima/Bala_la_la.mp4"},
    {"tipo": "texto", "contenido": "📜 te ganaste unos chicles: S8o9IS"},
    {"tipo": "none", "contenido": "💨 Una brisa suave🍃"},
    {"tipo": "texto", "contenido": "📜 puedes obtener pista: H3LP M3"},
    {"tipo": "none", "contenido": "se apago la vela🕯️, suerte para la proxima"},
    {"tipo": "imagen", "contenido": "ima/Inui.jpg"},
    {"tipo": "none", "contenido": "Aqui solo hay telarañas🕸️ y arañas🕷️."},
    {"tipo": "texto", "contenido": "📜 puedes pedri un chocolate🍫"},
    {"tipo": "texto", "contenido": "📜 Te ganaste otrs chicle: r4h83gh"},
    {"tipo": "imagen", "contenido": "ima/Invi.jpg"}
]

# Determinar qué imagen usar como fondo total
current_b64 = b64_fondo
if st.session_state.mostrar_rec != -1:
    if RECOMPENSAS[st.session_state.mostrar_rec]["tipo"] == "none":
        current_b64 = b64_vacio
    else:
        current_b64 = b64_tesoro

style_bg = f"url(data:image/jpeg;base64,{current_b64})" if current_b64 else "#0b0d17"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=VT323&family=Great+Vibes&display=swap');

.stApp {{
    background-image: {style_bg};
    background-attachment: fixed;
    background-size: cover;
    background-position: center;
}}

.main {{
    background: rgba(11, 13, 23, 0.85);
    color: #ffd700;
    font-family: 'VT323', monospace;
    padding: 20px;
    border-radius: 15px;
}}

h1 {{
    color: #d4af37 !important;
    text-shadow: 3px 3px #000000;
    text-align: center;
    font-size: 4em !important;
    font-family: 'Great Vibes', cursive;
}}

.stMetric {{
    background: rgba(26, 28, 44, 0.95) !important;
    border: 6px solid #5c3a21 !important;
    border-radius: 15px;
    padding: 10px;
    box-shadow: 0 0 0 3px #3b2414, 0 0 15px rgba(0,0,0,0.7);
}}

.stButton>button {{
    background-color: #4a148c;
    color: #d4af37;
    border: 2px solid #d4af37;
    font-family: 'VT323', monospace;
    font-size: 1.5em;
    width: 100%;
}}

.reward-container {{
    background: rgba(0, 0, 0, 0.6);
    padding: 20px;
    border-radius: 20px;
    border: 2px solid #d4af37;
}}
</style>
""", unsafe_allow_html=True)

TOKEN = "8798116628:AAGWyZmKj3SUyb0Eux1_uWYbPgVDpDtrShI"
CHAT_ID = 7177023901
SALT = "kCiyNtw4VH9RhI9t"
HASHES = ["c88fb2d67a9e16ea2d36d4526cba48c0c08a337bafc7c5e851ec16883f03dbb3", "be56a7feb47e0996c71cc9ebe8fc2b1c99340e4911dfa7b0e3131bb36c10eeb9", "df415e7b7c62c85bc9dd3578f73eebc5c44c4d488d067ce2cc6345d457096bf4", "89121310a34aec298d2d35e9b2d6f11fd6cf620300ee8813a733dae477f4935a", "98a69fdd719b9a5500d8bdcfe965cc18e566c7e26dfb3f631c67dce657b02ae7", "63706a2b1ade3088d19a2ee5b92b173c372c5b04a54928d68390881dbd447f4b", "606088e02b3b65cceedb34d7fe960b409c910ee5452505e16ff25072f832d58b", "7419baafe64f43b3e14d8e0068c2048855f7b5b5209cfa9cb36c9756e34469c4", "966099cd834ed37eb03aeeede0688c19d0546b42f0e48bb1b09a3714fe9e47ae", "8839c479607aed6292190ab7dc1e5bc70009c6c189550e28563ad1ed19046173"]

MENSAJES = [
"Bala la, la, la, ¡muy bien! primera puerta, tienes el 10%. Podrás con el resto🤔?",
"Te contare una historia... pero aun falta, llevas un 20% Si se puede! Si se puede!",
"Maitsev. Sul on 30%😲",
"Que sabia era santa clara, ¿no? vas un 40%🥳",
"Que buena respuesta😑, jajajajaja. Toda una filosofa usted. vas por la mitad 🎉 que veloz",
"Sea usted bienvenida al podcast, ay! cuantas risas nos trajo esas sesiones de grabación, ¿verdad?. vas por el 60%",
"¡Hola! Ya tienes un 70%, ya casi🤩",
"🎶Bajo del mar, bajo del mar🎶🦀. ya tenemos un 80%",
"Este debía de ser más difícil😼, o creíste que todas serian color de rosa, no, no, no🙂‍↔️. Ya casi terminas un ultimo esfuerzo💪🏻!",
"¿¡Enserio lo recordaste😶!?"
]

def normalizar(txt): return "".join(c for c in unicodedata.normalize("NFD", txt.lower()) if unicodedata.category(c) != "Mn").strip()
def notificar(t): requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": t})
def obtener_ruta(u): return f"{normalizar(u)}_prog.json"

if "usuario" not in st.session_state: st.session_state.usuario = ""
if "reclamado" not in st.session_state: st.session_state.reclamado = False

if not st.session_state.usuario:
    st.title("🔐 IDENTIFICACIÓN")
    nombre = st.text_input("Nombre:")
    if st.button("Entrar"):
        if nombre: 
            st.session_state.usuario = nombre
            path = obtener_ruta(nombre)
            st.session_state.puertas = json.load(open(path)) if os.path.exists(path) else [False]*10
            st.rerun()
else:
    if st.session_state.mostrar_rec != -1:
        idx = st.session_state.mostrar_rec
        rec = RECOMPENSAS[idx]
        st.markdown(f"<div class='reward-container'><h1>🚪 PUERTA {idx+1}</h1><p>{MENSAJES[idx]}</p></div>", unsafe_allow_html=True)
        
        if not st.session_state.reclamado:
            if st.button("💰 RECLAMAR"): st.session_state.reclamado = True; st.rerun()
        else:
            if rec["tipo"] == "video":
                if os.path.exists(rec["contenido"]):
                    st.video(rec["contenido"])
                else:
                    st.error("Video no encontrado en el servidor.")
            elif rec["tipo"] == "imagen":
                img = get_base64(rec["contenido"])
                if img: st.markdown(f'<img src="data:image/jpeg;base64,{img}" style="width:100%; border-radius:10px;">', unsafe_allow_html=True)
                else: st.error(f"Falta {rec['contenido']}")
            else: st.info(rec["contenido"])
        if st.button("✖ SALIR"): st.session_state.mostrar_rec = -1; st.session_state.reclamado = False; st.rerun()
    else:
        st.title(f"🏰 {st.session_state.usuario.upper()}")
        cols = st.columns(2)
        for i, ok in enumerate(st.session_state.puertas):
            with cols[i%2]:
                st.metric(f"Puerta {i+1}", "OK ✨" if ok else "LOCK 🔒")
                if ok and st.button(f"Ver {i+1}", key=f"v{i}"): st.session_state.mostrar_rec = i; st.session_state.reclamado = True; st.rerun()
        clave = st.text_input("Clave:")
        if st.button("Abrir"):
            h = hashlib.sha256((SALT+normalizar(clave)).encode()).hexdigest()
            encontrada = False
            for i in range(10):
                if not st.session_state.puertas[i] and h == HASHES[i]:
                    st.session_state.puertas[i] = True; st.session_state.mostrar_rec = i
                    json.dump(st.session_state.puertas, open(obtener_ruta(st.session_state.usuario), "w"))
                    notificar(f"🏰 {st.session_state.usuario} abrió puerta {i+1}"); st.rerun()
                    encontrada = true; st.rerum
            if not encontrada:
                notificar(f"❌ {st.session_state.usuario} falló con: {clave}")
            st.error("Error")