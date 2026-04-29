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
# PORTADA MEJORADA
# =========================

if menu == "Inicio":

    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://modatek.co.uk/wp-content/uploads/2023/07/Cosworth-CA2010-Display-Engine-6.jpg");
            background-size: cover;
            background-position: center;
        }

        .card {
            max-width: 700px;
            margin: 80px auto;
            padding: 40px;
            border-radius: 20px;
            background: rgba(0, 0, 0, 0.65);
            backdrop-filter: blur(10px);
            color: white;
            text-align: center;
            box-shadow: 0px 0px 25px rgba(0,0,0,0.5);
        }

        .title {
            font-size: 40px;
            font-weight: bold;
        }

        .subtitle {
            font-size: 22px;
            margin-bottom: 20px;
        }

        .section {
            margin-top: 20px;
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
                <b>Integrantes</b><br>
                Barbeito, Matias<br>
                Cavanes, Tomas Ezequiel<br>
                Lahan, Alberto Nicolas<br>
                Rodriguez Aguado, Jose Luis
            </div>

            <div class="section">
                <b>UTN Facultad Regional Haedo</b><br>
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

    st.sidebar.header("🏎️ Motor")
    cilindrada = st.sidebar.number_input("Cilindrada [L]", value=2.0)
    n_cil = st.sidebar.number_input("Número de cilindros", value=4)
    rpm = st.sidebar.number_input("RPM", value=3000)
    afr = st.sidebar.number_input("Relación aire-combustible", value=14.7)

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

    Pmax = max(P1, P2, P3, P4)
    Tmax = max(T1, T2, T3, T4)
    pme = wnet / (v1 - v2)

    df = pd.DataFrame({
        "Estado": [1,2,3,4],
        "T [K]": [T1,T2,T3,T4],
        "P [Pa]": [P1,P2,P3,P4],
        "v [m³/kg]": [v1,v2,v3,v4]
    })

    st.markdown("---")
    st.markdown("## 📊 Resultados del ciclo")

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(df)

    with col2:
        st.write(f"Rendimiento: {eta*100:.2f}%")
        st.write(f"Trabajo neto: {wnet/1e6:.2f} MJ/kg")
        st.write(f"P máx: {Pmax:.0f} Pa")
        st.write(f"T máx: {Tmax:.0f} K")
        st.write(f"PME: {pme:.0f} Pa")

    # P-v
    v_12 = np.linspace(v1, v2, 100)
    P_12 = P1 * (v1 / v_12)**gamma
    v_34 = np.linspace(v3, v4, 100)
    P_34 = P3 * (v3 / v_34)**gamma

    fig1, ax1 = plt.subplots()
    ax1.plot(v_12, P_12, label="1-2 Compresión")
    ax1.plot([v2, v3], [P2, P3], label="2-3 Calentamiento")
    ax1.plot(v_34, P_34, label="3-4 Expansión")
    ax1.plot([v4, v1], [P4, P1], label="4-1 Rechazo")
    ax1.legend()
    st.pyplot(fig1)

    # CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Descargar CSV", csv, "resultados.csv", "text/csv")