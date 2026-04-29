import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="TP Propulsión", layout="wide")

# =========================
# MENU
# =========================

menu = st.sidebar.selectbox("Navegación", ["Inicio", "Simulación"])

# =========================
# PORTADA
# =========================

if menu == "Inicio":

    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://modatek.co.uk/wp-content/uploads/2023/07/Cosworth-CA2010-Display-Engine-6.jpg");
            background-size: 65%;
            background-position: 70% center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }

        .stApp::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.4);
            z-index: -1;
        }

        .card {
            max-width: 700px;
            margin: 80px auto;
            padding: 40px;
            border-radius: 12px;
            background-color: rgba(245, 245, 245, 0.9);
            border: 1px solid #ddd;
            text-align: center;
        }

        .title {
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .subtitle {
            font-size: 20px;
            margin-bottom: 25px;
        }

        .section {
            margin-top: 20px;
            font-size: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
"""
<div class="card">
    <div class="title">📘 TP Nº1</div>
    <div class="subtitle">DISEÑO Y OPTIMIZACIÓN DE CICLOS TERMODINÁMICOS</div>

    <div class="section">
        Barbeito, Matías Nicolás<br>
        Cavanes, Tomás Ezequiel<br>
        Lahan, Alberto Nicolás<br>
        Rodríguez Aguado, José Luis
    </div>

    <div class="section">
        UTN Facultad Regional Haedo<br>
        Cátedra: Propulsión
    </div>
</div>
""",
        unsafe_allow_html=True
    )

# =========================
# SIMULACION
# =========================

else:
    st.title("🔧 Simulación de ciclos termodinámicos")
    st.markdown("## ⚙️ Configuración del problema")

    # ENTRADAS
    st.sidebar.header("🌍 Condiciones ambientales")
    alt = st.sidebar.number_input("Altitud [m]", value=0.0)
    T1 = st.sidebar.number_input("Temperatura [K]", value=288.0)
    P1 = st.sidebar.number_input("Presión [Pa]", value=101325.0)

    st.sidebar.header("🔥 Parámetros del ciclo")
    ciclo = st.sidebar.selectbox("Tipo de ciclo", ["Otto", "Diesel", "Sabathé"])
    r = st.sidebar.slider("Relación de compresión", 5.0, 25.0, 12.0)
    gamma = st.sidebar.slider("Gamma (γ)", 1.1, 1.67, 1.4)
    T3 = st.sidebar.slider("Temperatura máxima [K]", 1000.0, 3500.0, 2800.0)

    if ciclo in ["Diesel", "Sabathé"]:
        rc = st.sidebar.slider("Relación de corte", 1.0, 5.0, 2.0)
    else:
        rc = None

    # CALCULOS
    R = 287
    cv = R / (gamma - 1)
    v1 = R * T1 / P1

    if ciclo == "Otto":
        v2 = v1 / r
        T2 = T1 * r**(gamma - 1)
        P2 = P1 * r**gamma

        v3 = v2
        P3 = P2 * T3 / T2

        v4 = v1
        T4 = T3 * r**(-(gamma - 1))
        P4 = P3 * r**(-gamma)

    elif ciclo == "Diesel":
        v2 = v1 / r
        T2 = T1 * r**(gamma - 1)
        P2 = P1 * r**gamma

        v3 = v2 * rc
        T3 = T2 * rc
        P3 = P2

        v4 = v1
        T4 = T3 * (v3 / v1)**(gamma - 1)
        P4 = P3 * (v3 / v1)**gamma

    else:
        v2 = v1 / r
        T2 = T1 * r**(gamma - 1)
        P2 = P1 * r**gamma

        v3 = v2 * rc
        P3 = P2 * (T3 / T2)

        v4 = v1
        T4 = T3 * (v3 / v1)**(gamma - 1)
        P4 = P3 * (v3 / v1)**gamma

    qin = cv * (T3 - T2)
    qout = cv * (T4 - T1)
    wnet = qin - qout
    eta = wnet / qin

    # RESULTADOS
    st.markdown("## 📊 Resultados")

    st.write(f"Rendimiento: {eta*100:.2f}%")
    st.write(f"Trabajo neto: {wnet/1e6:.2f} MJ/kg")

    # =========================
    # DIAGRAMA P-v
    # =========================

    v_12 = np.linspace(v1, v2, 100)
    P_12 = P1 * (v1 / v_12)**gamma

    v_34 = np.linspace(v3, v4, 100)
    P_34 = P3 * (v3 / v_34)**gamma

    fig1, ax1 = plt.subplots()

    ax1.plot(v_12, P_12, label="1-2 Compresión")
    ax1.plot([v2, v3], [P2, P3], label="2-3 Calentamiento")
    ax1.plot(v_34, P_34, label="3-4 Expansión")
    ax1.plot([v4, v1], [P4, P1], label="4-1 Rechazo")

    ax1.set_xlabel("Volumen específico")
    ax1.set_ylabel("Presión")
    ax1.set_title("Diagrama P-v")
    ax1.legend()

    st.pyplot(fig1)

    # =========================
    # DIAGRAMA T-s
    # =========================

    def ds(Ta, Tb, va, vb):
        return cv*np.log(Tb/Ta) + R*np.log(vb/va)

    s1 = 0
    s2 = s1 + ds(T1, T2, v1, v2)
    s3 = s2 + ds(T2, T3, v2, v3)
    s4 = s3 + ds(T3, T4, v3, v4)

    fig2, ax2 = plt.subplots()

    ax2.plot([s1, s2], [T1, T2], label="1-2")
    ax2.plot([s2, s3], [T2, T3], label="2-3")
    ax2.plot([s3, s4], [T3, T4], label="3-4")
    ax2.plot([s4, s1], [T4, T1], label="4-1")

    ax2.set_xlabel("Entropía")
    ax2.set_ylabel("Temperatura")
    ax2.set_title("Diagrama T-s")
    ax2.legend()

    st.pyplot(fig2)
