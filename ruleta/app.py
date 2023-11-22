import streamlit as st
import random

# Configuración de la página
st.set_page_config(
    page_title="Ruleta Interactiva",
    page_icon="🔄",
    layout="wide"
)

# Título
st.title("Ruleta Interactiva")

# Número de opciones en la ruleta
numero_casillas = 8

# Colores para las opciones
colores = ['#ff0000', '#2E97A7']

# Contenedor de la ruleta
st.markdown("""
    <div class="contenedor-ruleta">
        <div class="ruleta" id="ruleta">
""", unsafe_allow_html=True)

# Configuración de la ruleta
with st.spinner("Cargando ruleta..."):
    # Crear la ruleta
    for i in range(1, numero_casillas + 1):
        st.markdown(f"""
            <div class="opcion opcion-{i}" style="transform: rotate({(360 / numero_casillas) * i}deg); border-bottom-color: {colores[i % len(colores)]}">
                {i}
            </div>
        """, unsafe_allow_html=True)

# Cierre del contenedor de la ruleta
st.markdown("""
        </div>
    </div>
""", unsafe_allow_html=True)

# Ruleta CSS
st.markdown("""
    <style>
        *{
            margin: 0;
            padding: 0;
        }

        body{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100vw;
            height: 100vh;
            background-color: #202020;
            overflow: hidden;
        }

        .contenedor-ruleta{
            transform: rotate(180deg);
        }

        .contenedor-ruleta::before{
            content: "";
            width: 60px;
            height: 60px;
            background-color: white;
            position: absolute;
            z-index: 99999;
            top: 55%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(45deg);
            pointer-events: none;
        }

        .ruleta{
            /*background-color: #303030;*/
            border-radius: 360px;
            position: relative;
            overflow: hidden;

            animation-timing-function: cubic-bezier(0, 0.4, 0.4, 1.04);
            animation-duration: 5.8s;
            animation-fill-mode: forwards;
            animation-iteration-count: 1;
        }

        .ruleta::before{
            content: "";
            width: 100px;
            height: 100px;
            background-color: #fff;
            position: absolute;
            z-index: 9999;
            border-radius: 360px;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            cursor: pointer;
        }

        .opcion{
            border: 0 solid transparent;
            position: absolute;
            transform-origin: top center;
            top: 50%;
        }

        .opcion::before{
            z-index: 99999;
            position: absolute;
            display: block;
            text-align: center;
            font-size: 20px;
            color: #fff;
            font-weight: bold;
            font-family: sans-serif;
            width: 40px;
            line-height: 40px;
            left: -20px;
            margin-top: 125px;
            transform: rotate(180deg);
        }
    </style>
""", unsafe_allow_html=True)

# Bloque de código JavaScript
script = """
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            var tamanyoRuleta = 360;
            var numeroCasillas = 8;
            var anguloCasillas = 360 / numeroCasillas;
            var grados = (180 - anguloCasillas) / 2;
            var alturaCasilla = Math.tan(grados * Math.PI / 180) * (tamanyoRuleta / 2);

            var ruleta = document.getElementById("ruleta");
            ruleta.style.width = tamanyoRuleta + "px";
            ruleta.style.height = tamanyoRuleta + "px";

            var styleTag = document.createElement("style");
            styleTag.id = "afterNumero";
            document.head.appendChild(styleTag);

            function getRandomColor(i) {
                var colors = ["#ff0000", "#2E97A7"];
                return colors[i % colors.length];
            }

            for (var i = 1; i <= numeroCasillas; i++) {
                var opcion = document.createElement("div");
                opcion.className = "opcion opcion-" + i;
                opcion.style.transform = "rotate(" + anguloCasillas * i + "deg)";
                opcion.style.borderBottomColor = getRandomColor(i);

                ruleta.appendChild(opcion);

                var clasS = ".opcion-" + i;

                var styleContent = "." + clasS + "::before {content: '" + i + "'}";
                styleTag.innerHTML += styleContent;

                opcion.setAttribute("data-content", i);
                opcion.setAttribute("data-ancho", tamanyoRuleta / 2 + "px");
                opcion.setAttribute("data-line", tamanyoRuleta / 2 + "px");
            }

            document.querySelectorAll(".opcion").forEach(function(opcion) {
                opcion.style.borderBottomWidth = alturaCasilla + "px";
                opcion.style.borderRightWidth = tamanyoRuleta / 2 + "px";
                opcion.style.borderLeftWidth = tamanyoRuleta / 2 + "px";
            });

            ruleta.addEventListener("click", function() {
                var num;
                var numID = "number-";
                num = 1 + Math.round(Math.random() * (numeroCasillas - 1));
                numID += num;

                var animacionRuleta = document.getElementById("animacionRuleta");
                if (animacionRuleta) {
                    animacionRuleta.remove();
                }

                var styleAnimacion = document.createElement("style");
                styleAnimacion.id = "animacionRuleta";
                styleAnimacion.innerHTML = "#" + numID + " { animation-name: number-" + num + "; } " +
                    "@keyframes number-" + num + " {" +
                    "from { transform: rotate(0); } " +
                    "to { transform: rotate(" + (360 * (numeroCasillas - 1) - anguloCasillas * num) + "deg); }" +
                    "}";
                document.head.appendChild(styleAnimacion);

                ruleta.removeAttribute("id");
                ruleta.setAttribute("id", numID);
            });
        });
    </script>
"""

# Incluir el bloque de código JavaScript
st.markdown(script, unsafe_allow_html=True)

# Botón para girar la ruleta
if st.button("Girar Ruleta"):
    opcion_seleccionada = random.randint(1, numero_casillas)
    st.success(f"¡Opción seleccionada: {opcion_seleccionada}!")
