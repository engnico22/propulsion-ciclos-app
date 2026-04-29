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
    st.title("📘 TP Nº1")
    st.header("DISEÑO Y OPTIMIZACIÓN DE CICLOS TERMODINÁMICOS")

    st.image("https://upload.wikimedia.org/wikipedia/commons/3/3a/V8_engine_block.jpg")

    st.markdown("---")

    st.subheader("👨‍🚀 Integrantes")
    st.write("Barbeito, Matias")
    st.write("Cavanes, Tomas Ezequiel")
    st.write("Lahan, Alberto Nicolas")
    st.write("Rodriguez Aguado, Jose Luis")

    st.markdown("---")
    st.markdown("**UTN Facultad Regional Haedo**")
    st.markdown("Cátedra: Propulsión")

# =========================
# SIMULACION
# =========================

else:
    st.title("🔧 Simulación de ciclos termodinámicos")
    st.markdown("## ⚙️ Configuración del problema")

    # =========================
    # ENTRADAS
    # =========================

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

    # =========================
    # CALCULOS
    # =========================

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

    else:  # Sabathé
        v2 = v1 / r
        T2 = T1 * r**(gamma - 1)
        P2 = P1 * r**gamma

        v3 = v2 * rc
        P3 = P2 * (T3 / T2)

        v4 = v1
        T4 = T3 * (v3 / v1)**(gamma - 1)
        P4 = P3 * (v3 / v1)**gamma

    # =========================
    # ENERGIA
    # =========================

    qin = cv * (T3 - T2)
    qout = cv * (T4 - T1)
    wnet = qin - qout
    eta = wnet / qin

    # =========================
    # PARAMETROS MOTOR
    # =========================

    Pmax = max(P1, P2, P3, P4)
    Tmax = max(T1, T2, T3, T4)
    pme = wnet / (v1 - v2)

    # =========================
    # TABLA
    # =========================

    df = pd.DataFrame({
        "Estado": [1, 2, 3, 4],
        "T [K]": [T1, T2, T3, T4],
        "P [Pa]": [P1, P2, P3, P4],
        "v [m³/kg]": [v1, v2, v3, v4]
    })

    st.markdown("---")
    st.markdown("## 📊 Resultados del ciclo")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Estados termodinámicos")
        st.dataframe(df)

    with col2:
        st.subheader("Parámetros")
        st.write(f"Rendimiento: {eta*100:.2f}%")
        st.write(f"Trabajo neto: {wnet/1e6:.2f} MJ/kg")
        st.write(f"Presión máxima: {Pmax:.0f} Pa")
        st.write(f"Temperatura máxima: {Tmax:.0f} K")
        st.write(f"Presión media efectiva: {pme:.0f} Pa")

    # =========================
    # DIAGRAMA P-v
    # =========================

    v_12 = np.linspace(v1, v2, 100)
    P_12 = P1 * (v1 / v_12)**gamma

    v_34 = np.linspace(v3, v4, 100)
    P_34 = P3 * (v3 / v_34)**gamma

    fig1, ax1 = plt.subplots()

    ax1.plot(v_12, P_12)
    ax1.plot([v2, v3], [P2, P3])
    ax1.plot(v_34, P_34)
    ax1.plot([v4, v1], [P4, P1])

    v_points = [v1, v2, v3, v4]
    P_points = [P1, P2, P3, P4]

    ax1.scatter(v_points, P_points)

    for i, (v, P) in enumerate(zip(v_points, P_points), start=1):
        ax1.text(v, P, f"{i}", fontsize=12)

    ax1.set_xlabel("Volumen específico [m³/kg]")
    ax1.set_ylabel("Presión [Pa]")
    ax1.set_title("Diagrama P-v")

    st.pyplot(fig1)

    # =========================
    # DIAGRAMA T-s REAL
    # =========================

    def ds(Ta, Tb, va, vb):
        return cv*np.log(Tb/Ta) + R*np.log(vb/va)

    s1 = 0
    s2 = s1 + ds(T1, T2, v1, v2)
    s3 = s2 + ds(T2, T3, v2, v3)
    s4 = s3 + ds(T3, T4, v3, v4)

    s_vals = [s1, s2, s3, s4, s1]
    T_vals = [T1, T2, T3, T4, T1]

    fig2, ax2 = plt.subplots()
    ax2.plot(s_vals, T_vals, marker='o')

    for i, (s, T) in enumerate(zip(s_vals[:-1], T_vals[:-1]), start=1):
        ax2.text(s, T, f"{i}", fontsize=12)

    ax2.set_xlabel("Entropía [J/kgK]")
    ax2.set_ylabel("Temperatura [K]")
    ax2.set_title("Diagrama T-s")

    st.pyplot(fig2)

    # =========================
    # EXPORTAR CSV
    # =========================

    st.subheader("📥 Exportar resultados")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Descargar CSV",
        data=csv,
        file_name="resultados.csv",
        mime="text/csv"
    )