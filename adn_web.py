import streamlit as st
import random

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Simulador de ADN",
    page_icon="🧬",
    layout="centered"
)

# --- 1. LÓGICA DEL NEGOCIO (BACKEND) ---
# Como buen desarrollador, separamos la lógica de la visualización.

def obtener_color(nucleotido):
    """Retorna el color basado en tu esquema original."""
    colores = {
        'A': '#FF4B4B', # Red (Ajustado para que se vea bien en web)
        'G': '#1E90FF', # Blue
        'T': '#228B22', # Green
        'C': '#FFD700'  # Yellow
    }
    return colores.get(nucleotido, 'grey')

def obtener_complementario(nucleotido):
    """Lógica de pares de bases: A<->T y C<->G"""
    pares = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return pares.get(nucleotido, '?')

def generar_cadena_adn(longitud):
    """Genera una cadena aleatoria de ADN."""
    bases = ['A', 'C', 'G', 'T']
    # List comprehension (una forma pythonica de hacer loops)
    cadena_5 = [random.choice(bases) for _ in range(longitud)]
    return cadena_5

# --- 2. INTERFAZ DE USUARIO (FRONTEND) ---

st.title("🧬 Visualizador de ADN")
st.markdown("""
Esta aplicación simula la estructura de una cadena de ADN y su complementaria.
Basado en el código original de `turtle`, adaptado para la web.
""")

# Barra lateral para controles
with st.sidebar:
    st.header("Configuración")
    longitud = st.slider("Longitud de la cadena", min_value=5, max_value=50, value=10)
    
    if st.button("Generar Nuevo ADN", type="primary"):
        # Limpiamos el estado para forzar una regeneración
        if 'cadena_adn' in st.session_state:
            del st.session_state['cadena_adn']

# --- 3. GESTIÓN DE ESTADO (STATE MANAGEMENT) ---
# Streamlit se recarga con cada interacción. Usamos session_state para
# recordar la cadena de ADN a menos que queramos cambiarla.

if 'cadena_adn' not in st.session_state:
    st.session_state['cadena_adn'] = generar_cadena_adn(longitud)

# Recuperamos la cadena actual
cadena_5_prima = st.session_state['cadena_adn']

# Si el usuario cambió el slider, ajustamos la longitud visualmente o regeneramos
if len(cadena_5_prima) != longitud:
     st.session_state['cadena_adn'] = generar_cadena_adn(longitud)
     cadena_5_prima = st.session_state['cadena_adn']

# Generamos la complementaria (3') en tiempo real
cadena_3_prima = [obtener_complementario(base) for base in cadena_5_prima]

# --- 4. VISUALIZACIÓN ---

st.subheader("Representación Gráfica")
st.caption("Cadena 5' (Izquierda) - Enlaces - Cadena 3' (Derecha)")

# Contenedor para la visualización
container_adn = st.container()

with container_adn:
    # Iteramos sobre ambas cadenas simultáneamente usando zip()
    for base1, base2 in zip(cadena_5_prima, cadena_3_prima):
        
        c1 = obtener_color(base1)
        c2 = obtener_color(base2)
        
        # Usamos HTML/CSS para dibujar las "cajas" que antes dibujaba la tortuga
        st.markdown(f"""
<div style="display: flex; justify-content: center; align-items: center; margin-bottom: 5px;">
<!-- Esqueleto 5' -->
<div style="width: 20px; height: 30px; background-color: #333; margin-right: 5px;"></div>
<!-- Base 1 -->
<div style="
background-color: {c1}; 
width: 60px; 
height: 30px; 
color: white; 
text-align: center; 
line-height: 30px; 
font-weight: bold;
border-radius: 5px 0 0 5px;
text-shadow: 1px 1px 2px black;">
{base1}
</div>
<!-- Enlace de Hidrógeno (visual) -->
<div style="width: 20px; border-bottom: 2px dashed #999; height: 15px;"></div>                
<!-- Base 2 -->
<div style="
background-color: {c2}; 
width: 60px; 
height: 30px; 
color: white; 
text-align: center; 
line-height: 30px; 
font-weight: bold;
border-radius: 0 5px 5px 0;
text-shadow: 1px 1px 2px black;">
{base2}
</div>
<!-- Esqueleto 3' -->
<div style="width: 20px; height: 30px; background-color: #333; margin-left: 5px;"></div>
</div>
""", unsafe_allow_html=True)

# --- 5. ESTADÍSTICAS ---
st.divider()
st.subheader("Estadísticas de la Muestra")

col1, col2, col3, col4 = st.columns(4)
total = len(cadena_5_prima) * 2 # Contando ambas hebras

with col1:
    st.metric("Adenina (A)", f"{cadena_5_prima.count('A') + cadena_3_prima.count('A')}")
with col2:
    st.metric("Timina (T)", f"{cadena_5_prima.count('T') + cadena_3_prima.count('T')}")
with col3:
    st.metric("Citosina (C)", f"{cadena_5_prima.count('C') + cadena_3_prima.count('C')}")
with col4:
    st.metric("Guanina (G)", f"{cadena_5_prima.count('G') + cadena_3_prima.count('G')}")