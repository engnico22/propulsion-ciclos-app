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
# PORTADA (FIX DEFINITIVO)
# =========================

if menu == "Inicio":

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.markdown("## 📘 TP Nº1")
        st.markdown("### DISEÑO Y OPTIMIZACIÓN DE CICLOS TERMODINÁMICOS")

        st.markdown("---")

        st.markdown("### 👨‍🚀 Integrantes")
        st.write("• Barbeito, Matias")
        st.write("• Cavanes, Tomas Ezequiel")
        st.write("• Lahan, Alberto Nicolas")
        st.write("• Rodriguez Aguado, Jose Luis")

        st.markdown("---")

        st.markdown("### 🏫 Institución")
        st.write("UTN Facultad Regional Haedo")
        st.write("Cátedra: Propulsión")

# =========================
# SIMULACION (SIN CAMBIOS)
# =========================

else:
    st.title("🔧 Simulación de ciclos termodinámicos")
    st.markdown("## ⚙️ Configuración del problema")

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

    # (TODO lo demás de tu simulación queda EXACTAMENTE igual)
