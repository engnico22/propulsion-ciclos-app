import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Ciclos Termodinámicos", layout="wide")

st.title("🔧 Análisis de Ciclos Termodinámicos")
st.markdown("Simulación de ciclos Otto, Diesel y Sabathé")

# =========================
# SIDEBAR - ENTRADAS
# =========================
st.sidebar.header("⚙️ Parámetros de entrada")

# Tipo de ciclo
ciclo = st.sidebar.selectbox("Tipo de ciclo", ["Otto", "Diesel", "Sabathé"])

# Condiciones atmosféricas
st.sidebar.subheader("🌍 Condiciones ambientales")
T1 = st.sidebar.number_input("Temperatura inicial [K]", value=288.0)
P1 = st.sidebar.number_input("Presión inicial [Pa]", value=101325.0)

# Parámetros del ciclo
st.sidebar.subheader("🔥 Parámetros del ciclo")
r = st.sidebar.slider("Relación de compresión", 5.0, 25.0, 12.0)
gamma = st.sidebar.slider("Gamma (γ)", 1.1, 1.67, 1.4)
T3 = st.sidebar.slider("Temperatura máxima [K]", 1000.0, 3500.0, 2800.0)

# Diesel/Sabathe extra
rc = st.sidebar.slider("Relación de corte (Diesel/Sabathe)", 1.0, 5.0, 2.0)

# Motor
st.sidebar.subheader("🏎️ Parámetros del motor")
cilindrada = st.sidebar.number_input("Cilindrada [L]", value=2.4)
rpm = st.sidebar.number_input("RPM", value=17000)

# =========================
# CÁLCULOS
# =========================

R = 287
cv = R / (gamma - 1)

v1 = R * T1 / P1

# ---- CICLO OTTO ----
if ciclo == "Otto":
    T2 = T1 * r**(gamma - 1)
    P2 = P1 * r**gamma
    v2 = v1 / r

    P3 = P2 * T3 / T2
    v3 = v2

    T4 = T3 * r**(-(gamma - 1))
    P4 = P3 * r**(-gamma)
    v4 = v1

# ---- CICLO DIESEL ----
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

# ---- CICLO SABATHE ----
elif ciclo == "Sabathé":
    T2 = T1 * r**(gamma - 1)
    P2 = P1 * r**gamma
    v2 = v1 / r

    # fase mixta
    T3 = T3
    P3 = P2 * (T3 / T2)
    v3 = v2 * rc

    T4 = T3 * (v3 / v1)**(gamma - 1)
    P4 = P3 * (v3 / v1)**gamma
    v4 = v1

# =========================
# ENERGÍA
# =========================

qin = cv * (T3 - T2)
qout = cv * (T4 - T1)
wnet = qin - qout
eta = wnet / qin

# =========================
# TABLA DE ESTADOS
# =========================

df_estados = pd.DataFrame({
    "Estado": [1, 2, 3, 4],
    "Temperatura [K]": [T1, T2, T3, T4],
    "Presión [Pa]": [P1, P2, P3, P4],
    "Volumen específico [m³/kg]": [v1, v2, v3, v4]
})

# =========================
# RESULTADOS
# =========================

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Estados termodinámicos")
    st.dataframe(df_estados)

with col2:
    st.subheader("⚡ Resultados energéticos")
    st.write(f"Calor aportado: {qin/1e6:.2f} MJ/kg")
    st.write(f"Calor rechazado: {qout/1e6:.2f} MJ/kg")
    st.write(f"Trabajo neto: {wnet/1e6:.2f} MJ/kg")
    st.write(f"Rendimiento: {eta*100:.2f} %")

# =========================
# GRÁFICOS
# =========================

st.subheader("📈 Diagramas")

fig1, ax1 = plt.subplots()
ax1.plot([v1, v2, v3, v4, v1], [P1, P2, P3, P4, P1])
ax1.set_xlabel("Volumen específico")
ax1.set_ylabel("Presión")
ax1.set_title("Diagrama P-v")

fig2, ax2 = plt.subplots()
ax2.plot([T1, T2, T3, T4, T1])
ax2.set_title("Diagrama T-s (simplificado)")

col3, col4 = st.columns(2)

with col3:
    st.pyplot(fig1)

with col4:
    st.pyplot(fig2)

# =========================
# EXPORTAR A EXCEL
# =========================

st.subheader("📥 Exportar resultados")

df_resumen = pd.concat([df_estados], axis=0)

excel = df_resumen.to_excel("resultados.xlsx", index=False)

with open("resultados.xlsx", "rb") as file:
    st.download_button(
        label="Descargar Excel",
        data=file,
        file_name="resultados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )