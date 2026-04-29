import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="TP Propulsión", layout="wide")

# =========================
# MENU
# =========================

menu = st.sidebar.selectbox("Navegación", ["Inicio", "Simulación"])

# =========================
# PAGINA INICIO (CARATULA)
# =========================

if menu == "Inicio":
    st.title("📘 TP Nº1")
    st.header("DISEÑO Y OPTIMIZACIÓN DE CICLOS TERMODINÁMICOS")

    st.markdown("---")

    st.subheader("👨‍🚀 Integrantes")

    st.write("- Barbeito, Matias")
    st.write("- Cavanes, Tomas Ezequiel")
    st.write("- Lahan, Alberto Nicolas")
    st.write("- Rodriguez Aguado, Jose Luis")

    st.markdown("---")

    st.info("Aplicación interactiva para análisis de ciclos Otto, Diesel y Sabathé")

# =========================
# SIMULACION
# =========================

elif menu == "Simulación":

    st.title("🔧 Simulación de ciclos")

    st.sidebar.header("⚙️ Parámetros")

    ciclo = st.sidebar.selectbox("Tipo de ciclo", ["Otto", "Diesel", "Sabathé"])

    T1 = st.sidebar.number_input("T1 [K]", value=288.0)
    P1 = st.sidebar.number_input("P1 [Pa]", value=101325.0)

    r = st.sidebar.slider("Relación de compresión", 5.0, 25.0, 12.0)
    gamma = st.sidebar.slider("Gamma", 1.1, 1.67, 1.4)
    T3 = st.sidebar.slider("T3 [K]", 1000.0, 3500.0, 2800.0)
    rc = st.sidebar.slider("Relación de corte", 1.0, 5.0, 2.0)

    R = 287
    cv = R / (gamma - 1)

    v1 = R * T1 / P1

    # CICLOS
    if ciclo == "Otto":
        T2 = T1 * r**(gamma - 1)
        P2 = P1 * r**gamma
        v2 = v1 / r

        P3 = P2 * T3 / T2
        v3 = v2

        T4 = T3 * r**(-(gamma - 1))
        P4 = P3 * r**(-gamma)
        v4 = v1

    elif ciclo == "Diesel":
        T2 = T1 * r**(gamma - 1)
        P2 = P1 * r**gamma
        v2 = v1 / r

        v3 = v2 * rc
        T3 = T2 * rc
        P3 = P2

        T4 = T3 * (v3 / v1)**(gamma - 1)
        P4 = P3 * (v3 / v1)**gamma
        v4 = v1

    else:  # Sabathe
        T2 = T1 * r**(gamma - 1)
        P2 = P1 * r**gamma
        v2 = v1 / r

        P3 = P2 * (T3 / T2)
        v3 = v2 * rc

        T4 = T3 * (v3 / v1)**(gamma - 1)
        P4 = P3 * (v3 / v1)**gamma
        v4 = v1

    # ENERGIA
    qin = cv * (T3 - T2)
    qout = cv * (T4 - T1)
    wnet = qin - qout
    eta = wnet / qin

    # TABLA
    df = pd.DataFrame({
        "Estado": [1, 2, 3, 4],
        "T [K]": [T1, T2, T3, T4],
        "P [Pa]": [P1, P2, P3, P4],
        "v [m³/kg]": [v1, v2, v3, v4]
    })

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Estados")
        st.dataframe(df)

    with col2:
        st.subheader("Resultados")
        st.write(f"Rendimiento: {eta*100:.2f}%")
        st.write(f"Trabajo neto: {wnet/1e6:.2f} MJ/kg")

    # =========================
    # PLOT P-v MEJORADO
    # =========================

    v = np.linspace(v2, v1, 100)
    P = P1 * (v1 / v)**gamma

    fig1, ax1 = plt.subplots()
    ax1.plot(v, P)
    ax1.scatter([v1, v2, v3, v4], [P1, P2, P3, P4])
    ax1.set_xlabel("v")
    ax1.set_ylabel("P")
    ax1.set_title("Diagrama P-v")

    # =========================
    # T-s SIMPLIFICADO
    # =========================

    s = [0, 0, 1, 1, 0]
    T = [T1, T2, T3, T4, T1]

    fig2, ax2 = plt.subplots()
    ax2.plot(s, T)
    ax2.set_title("Diagrama T-s (aprox)")

    col3, col4 = st.columns(2)

    with col3:
        st.pyplot(fig1)

    with col4:
        st.pyplot(fig2)

    # =========================
    # EXCEL CORREGIDO
    # =========================

    st.subheader("📥 Exportar")

    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)

    st.download_button(
        label="Descargar Excel",
        data=buffer,
        file_name="resultados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )