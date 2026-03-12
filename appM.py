import hashlib
import unicodedata
import requests
import streamlit as st
import base64
import os

# Configuración de página
st.set_page_config(page_title="El Desafío de las Puertas", page_icon="🏰", layout="centered")

# Función para cargar imagen local como fondo
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Cambia 'fondo.jpg' por el nombre de tu archivo de imagen en GitHub
nombre_archivo = "ima/Torre.jpg" 

b64_string = ""
if os.path.exists(nombre_archivo):
    b64_string = get_base64_of_bin_file(nombre_archivo)

# CSS Avanzado con Imagen de Fondo Local
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

    .stApp {{
        background-image: url("data:image/png;base64,{b64_string}");
        background-attachment: fixed;
        background-size: cover;
    }}

    .main {{
        background: rgba(11, 13, 23, 0.8);
        color: #e0d5b0;
        font-family: 'VT323', monospace;
        padding: 20px;
        border-radius: 15px;
    }}
    
    h1 {{
        color: #d4af37 !important;
        text-shadow: 3px 3px #000000;
        text-align: center;
        font-size: 3.5em !important;
    }}

    .stMetric {{
        background: rgba(26, 28, 44, 0.9) !important;
        border: 2px solid #d4af37 !important;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
    }}

    label[data-testid=\"stMetricLabel\"] {{
        color: #d4af37 !important;
        font-size: 1.5em !important;
    }}

    .stButton>button {{
        background-color: #4a148c;
        color: #d4af37;
        border: 2px solid #d4af37;
        font-family: 'VT323', monospace;
        font-size: 1.5em;
        width: 100%;
    }}

    .stTextInput>div>div>input {{
        background-color: #0b0d17;
        color: #e0d5b0;
        border: 1px solid #d4af37;
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
FINAL = "¡Lo Lograste!🎉🥳🎉, muy biennnnnn"

def normalizar(txt):
    txt = txt.lower()
    txt = "".join(c for c in unicodedata.normalize("NFD", txt) if unicodedata.category(c) != "Mn")
    return txt.strip()

def notificar(p):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": f"Puerta {p} abierta"})
    except: pass

if "puertas" not in st.session_state:
    st.session_state.puertas = [False] * 10
if "ultimo_mensaje" not in st.session_state:
    st.session_state.ultimo_mensaje = None
if "ultima_puerta" not in st.session_state:
    st.session_state.ultima_puerta = -1

st.title("🏰 EL MISTERIO DE LAS 10 PUERTAS 🏰")

if all(st.session_state.puertas):
    st.balloons()
    st.success(FINAL)
else:
    cols = st.columns(2)
    for i, abierta in enumerate(st.session_state.puertas):
        with cols[i % 2]:
            st.metric(label=f"Puerta {i+1}", value="DESBLOQUEADA ✨" if abierta else "SELLADA 🔒")
            if st.session_state.ultima_puerta == i and st.session_state.ultimo_mensaje:
                st.info(st.session_state.ultimo_mensaje)

    st.write(" ")
    clave = st.text_input("Introduce la palabra de poder:", placeholder="...", key="input_clave")
    
    if st.button("Conjurar Apertura"):
        n = normalizar(clave)
        h = hashlib.sha256(("kCiyNtw4VH9RhI9t" + n).encode()).hexdigest()
        encontrada = False
        for i in range(10):
            if not st.session_state.puertas[i] and h == HASHES[i]:
                st.session_state.puertas[i] = True
                st.session_state.ultima_puerta = i
                st.session_state.ultimo_mensaje = MENSAJES[i]
                notificar(i+1)
                encontrada = True
                st.rerun()
        if not encontrada: 
            st.error("Clave incorrecta")