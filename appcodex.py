import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="TP Propulsión", layout="wide")


def calcular_ciclo(ciclo, T1, P1, r, gamma, T3_ingresada, rc):
    R = 287.0
    cv = R / (gamma - 1)
    cp = gamma * cv

    v1 = R * T1 / P1

    if ciclo == "Otto":
        v2 = v1 / r
        T2 = T1 * r ** (gamma - 1)
        P2 = P1 * r**gamma

        T3 = T3_ingresada
        v3 = v2
        P3 = P2 * T3 / T2

        v4 = v1
        T4 = T3 * r ** (-(gamma - 1))
        P4 = P3 * r ** (-gamma)

        qin = cv * (T3 - T2)
        qout = cv * (T4 - T1)

    elif ciclo == "Diesel":
        v2 = v1 / r
        T2 = T1 * r ** (gamma - 1)
        P2 = P1 * r**gamma

        v3 = v2 * rc
        T3 = T2 * rc
        P3 = P2

        v4 = v1
        T4 = T3 * (v3 / v4) ** (gamma - 1)
        P4 = P3 * (v3 / v4) ** gamma

        qin = cp * (T3 - T2)
        qout = cv * (T4 - T1)

    else:
        v2 = v1 / r
        T2 = T1 * r ** (gamma - 1)
        P2 = P1 * r**gamma

        T3a = T3_ingresada
        P3 = P2 * (T3a / T2)
        v3 = v2 * rc
        T3 = T3a * rc

        v4 = v1
        T4 = T3 * (v3 / v4) ** (gamma - 1)
        P4 = P3 * (v3 / v4) ** gamma

        qin = cv * (T3a - T2) + cp * (T3 - T3a)
        qout = cv * (T4 - T1)

    wnet = qin - qout
    eta = wnet / qin if qin != 0 else np.nan
    pme = wnet / (v1 - v2)

    estados = pd.DataFrame(
        {
            "Estado": [1, 2, 3, 4],
            "T [K]": [T1, T2, T3, T4],
            "P [Pa]": [P1, P2, P3, P4],
            "v [m³/kg]": [v1, v2, v3, v4],
        }
    )

    return {
        "R": R,
        "cv": cv,
        "estados": estados,
        "qin": qin,
        "qout": qout,
        "wnet": wnet,
        "eta": eta,
        "pme": pme,
        "Pmax": max(P1, P2, P3, P4),
        "Tmax": max(T1, T2, T3, T4),
        "puntos": {
            "T1": T1,
            "T2": T2,
            "T3": T3,
            "T4": T4,
            "P1": P1,
            "P2": P2,
            "P3": P3,
            "P4": P4,
            "v1": v1,
            "v2": v2,
            "v3": v3,
            "v4": v4,
        },
    }


def calcular_ciclo_original(ciclo, T1, P1, r, gamma, T3, rc):
    R = 287.0
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
        T4 = T3 * (v3 / v1) ** (gamma - 1)
        P4 = P3 * (v3 / v1) ** gamma

    else:
        v2 = v1 / r
        T2 = T1 * r**(gamma - 1)
        P2 = P1 * r**gamma

        v3 = v2 * rc
        P3 = P2 * (T3 / T2)

        v4 = v1
        T4 = T3 * (v3 / v1) ** (gamma - 1)
        P4 = P3 * (v3 / v1) ** gamma

    qin = cv * (T3 - T2)
    qout = cv * (T4 - T1)
    wnet = qin - qout
    eta = wnet / qin
    pme = wnet / (v1 - v2)

    estados = pd.DataFrame(
        {
            "Estado": [1, 2, 3, 4],
            "T [K]": [T1, T2, T3, T4],
            "P [Pa]": [P1, P2, P3, P4],
            "v [m³/kg]": [v1, v2, v3, v4],
        }
    )

    return {
        "R": R,
        "cv": cv,
        "estados": estados,
        "qin": qin,
        "qout": qout,
        "wnet": wnet,
        "eta": eta,
        "pme": pme,
        "Pmax": max(P1, P2, P3, P4),
        "Tmax": max(T1, T2, T3, T4),
        "puntos": {
            "T1": T1,
            "T2": T2,
            "T3": T3,
            "T4": T4,
            "P1": P1,
            "P2": P2,
            "P3": P3,
            "P4": P4,
            "v1": v1,
            "v2": v2,
            "v3": v3,
            "v4": v4,
        },
    }


def mostrar_graficos(ciclo, gamma, datos):
    p = datos["puntos"]
    cv = datos["cv"]
    R = datos["R"]

    v_12 = np.linspace(p["v1"], p["v2"], 100)
    P_12 = p["P1"] * (p["v1"] / v_12) ** gamma

    v_34 = np.linspace(p["v3"], p["v4"], 100)
    P_34 = p["P3"] * (p["v3"] / v_34) ** gamma

    fig1, ax1 = plt.subplots(figsize=(4.5, 2.4))
    ax1.plot(v_12, P_12, color="blue", label="1-2 Compresión")

    if ciclo == "Otto":
        ax1.plot([p["v2"], p["v3"]], [p["P2"], p["P3"]], color="red", label="2-3 Calentamiento (V cte)")
    elif ciclo == "Diesel":
        ax1.plot([p["v2"], p["v3"]], [p["P2"], p["P3"]], color="red", label="2-3 Calentamiento (P cte)")
    else:
        ax1.plot([p["v2"], p["v2"]], [p["P2"], p["P3"]], color="red", label="2-3 Calentamiento (V cte)")
        ax1.plot([p["v2"], p["v3"]], [p["P3"], p["P3"]], color="orange", label="3-3' Calentamiento (P cte)")

    ax1.plot(v_34, P_34, color="green", label="3-4 Expansión")
    ax1.plot([p["v4"], p["v1"]], [p["P4"], p["P1"]], color="purple", label="4-1 Rechazo calor")
    ax1.scatter([p["v1"], p["v2"], p["v3"], p["v4"]], [p["P1"], p["P2"], p["P3"], p["P4"]], color="black")

    for i, (v, P) in enumerate(zip([p["v1"], p["v2"], p["v3"], p["v4"]], [p["P1"], p["P2"], p["P3"], p["P4"]]), start=1):
        ax1.text(v, P, f"{i}")

    ax1.set_xlabel("Volumen específico [m³/kg]")
    ax1.set_ylabel("Presión [Pa]")
    ax1.set_title("Diagrama P-v")
    ax1.legend(fontsize=6)
    ax1.grid(True, alpha=0.3)
    st.pyplot(fig1, use_container_width=False)

    def ds(Ta, Tb, va, vb):
        return cv * np.log(Tb / Ta) + R * np.log(vb / va)

    s1 = 0
    s2 = s1 + ds(p["T1"], p["T2"], p["v1"], p["v2"])
    s3 = s2 + ds(p["T2"], p["T3"], p["v2"], p["v3"])
    s4 = s3 + ds(p["T3"], p["T4"], p["v3"], p["v4"])

    fig2, ax2 = plt.subplots(figsize=(4.5, 2.4))
    ax2.plot([s1, s2], [p["T1"], p["T2"]], color="blue", label="1-2 Compresión")
    ax2.plot([s2, s3], [p["T2"], p["T3"]], color="red", label="2-3 Calentamiento")
    ax2.plot([s3, s4], [p["T3"], p["T4"]], color="green", label="3-4 Expansión")
    ax2.plot([s4, s1], [p["T4"], p["T1"]], color="purple", label="4-1 Rechazo calor")
    ax2.scatter([s1, s2, s3, s4], [p["T1"], p["T2"], p["T3"], p["T4"]], color="black")

    for i, (s, T) in enumerate(zip([s1, s2, s3, s4], [p["T1"], p["T2"], p["T3"], p["T4"]]), start=1):
        ax2.text(s, T, f"{i}")

    ax2.set_xlabel("Entropía [J/kgK]")
    ax2.set_ylabel("Temperatura [K]")
    ax2.set_title("Diagrama T-s")
    ax2.legend(fontsize=6)
    ax2.grid(True, alpha=0.3)
    st.pyplot(fig2, use_container_width=False)


def mostrar_resultados_ciclo(datos):
    df = datos["estados"]

    st.markdown("---")
    st.markdown("## 📊 Resultados del ciclo")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Estados termodinámicos")
        st.dataframe(df, use_container_width=True)

    with col2:
        st.subheader("Parámetros")
        st.write(f"Rendimiento: {datos['eta'] * 100:.2f}%")
        st.write(f"Trabajo neto específico: {datos['wnet'] / 1000:.2f} kJ/kg")
        st.write(f"Calor ingresado: {datos['qin'] / 1000:.2f} kJ/kg")
        st.write(f"Calor rechazado: {datos['qout'] / 1000:.2f} kJ/kg")
        st.write(f"Presión máxima: {datos['Pmax'] / 1e5:.2f} bar")
        st.write(f"Temperatura máxima: {datos['Tmax']:.0f} K")
        st.write(f"Presión media efectiva indicada: {datos['pme'] / 1e5:.2f} bar")


def entradas_ciclo():
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

    return alt, T1, P1, ciclo, r, gamma, T3, rc


menu = st.sidebar.selectbox("Navegación", ["Inicio", "Simulación", "Diseño preliminar"])

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
            line-height: 1.7;
        }
        </style>
        """,
        unsafe_allow_html=True,
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
        unsafe_allow_html=True,
    )

elif menu == "Simulación":
    st.title("🔧 Simulación de ciclos termodinámicos")
    st.markdown("## ⚙️ Configuración del problema")

    alt, T1, P1, ciclo, r, gamma, T3, rc = entradas_ciclo()

    st.sidebar.header("🏎️ Motor")
    cilindrada = st.sidebar.number_input("Cilindrada [L]", value=2.0)
    n_cil = st.sidebar.number_input("Número de cilindros", value=4)
    rpm = st.sidebar.number_input("RPM", value=3000)
    afr = st.sidebar.number_input("Relación aire-combustible", value=14.7)

    datos = calcular_ciclo_original(ciclo, T1, P1, r, gamma, T3, rc)
    mostrar_resultados_ciclo(datos)
    mostrar_graficos(ciclo, gamma, datos)

    st.subheader("📥 Exportar resultados")
    csv = datos["estados"].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Descargar CSV",
        data=csv,
        file_name="resultados.csv",
        mime="text/csv",
    )

else:
    st.title("🛩️ Diseño preliminar desde potencia requerida")
    st.markdown("## ⚙️ Configuración del problema")

    alt, T1, P1, ciclo, r, gamma, T3, rc = entradas_ciclo()

    st.sidebar.header("🏎️ Requerimiento del motor")
    potencia_kw = st.sidebar.number_input("Potencia requerida [kW]", value=75.0, min_value=1.0)
    rpm = st.sidebar.number_input("RPM de diseño", value=3000, min_value=500, step=100)
    n_cil = st.sidebar.number_input("Número de cilindros", value=4, min_value=1, step=1)
    relacion_carrera_diametro = st.sidebar.slider("Relación carrera/diámetro", 0.6, 1.6, 1.0)
    eta_mecanica = st.sidebar.slider("Rendimiento mecánico", 0.60, 1.00, 0.85)
    afr = st.sidebar.number_input("Relación aire-combustible", value=14.7, min_value=1.0)

    if ciclo == "Otto" and r >= 16:
        st.error("Relación de compresión muy alta para ciclo Otto. Con r >= 16 el diseño es poco realista por detonación y cargas mecánicas.")
    elif ciclo == "Otto" and r >= 13:
        st.warning("Relación de compresión alta para ciclo Otto. Revisar riesgo de detonación, combustible y temperatura máxima.")

    if ciclo == "Diesel" and r < 12:
        st.warning("Relación de compresión baja para Diesel. Puede no alcanzar condiciones adecuadas de autoencendido.")
    if ciclo in ["Diesel", "Sabathé"] and r > 24:
        st.warning("Relación de compresión muy alta. Revisar presión máxima y solicitaciones mecánicas.")
    if ciclo == "Sabathé" and r < 10:
        st.warning("Relación de compresión baja para Sabathé. Revisar si representa bien un motor de encendido por compresión.")
    if T3 > 3000:
        st.warning("Temperatura máxima muy elevada. Revisar límites térmicos de materiales y refrigeración.")
    if relacion_carrera_diametro < 0.75:
        st.warning("Motor muy supercuadrado. Puede ser válido a altas RPM, pero conviene justificarlo.")
    elif relacion_carrera_diametro > 1.25:
        st.warning("Motor muy subcuadrado. Puede aumentar velocidad media del pistón y esfuerzos.")

    datos = calcular_ciclo(ciclo, T1, P1, r, gamma, T3, rc)

    if datos["pme"] <= 0:
        st.error("El ciclo entrega trabajo neto negativo o nulo. Revisar los parámetros ingresados.")
        st.stop()

    pme_efectiva = eta_mecanica * datos["pme"]
    potencia_w = potencia_kw * 1000
    cilindrada_total_m3 = potencia_w * 120 / (pme_efectiva * rpm)
    cilindrada_unitaria_m3 = cilindrada_total_m3 / n_cil
    diametro_m = (4 * cilindrada_unitaria_m3 / (np.pi * relacion_carrera_diametro)) ** (1 / 3)
    carrera_m = relacion_carrera_diametro * diametro_m
    torque_nm = potencia_w / (2 * np.pi * rpm / 60)
    velocidad_media_piston = 2 * carrera_m * rpm / 60

    if datos["Pmax"] > 9e6:
        st.warning("Presión máxima superior a 90 bar. Revisar resistencia estructural del motor.")
    if velocidad_media_piston > 18:
        st.warning("Velocidad media del pistón elevada. Revisar carrera, RPM y vida útil.")
    if cilindrada_total_m3 * 1000 > 10:
        st.warning("La cilindrada resultante es muy grande. Revisar potencia requerida, PME, RPM o cantidad de cilindros.")

    mostrar_resultados_ciclo(datos)

    st.markdown("## 🏎️ Diseño preliminar de geometría")
    df_geometria = pd.DataFrame(
        {
            "Parámetro": [
                "Potencia requerida",
                "RPM de diseño",
                "Torque requerido",
                "PME indicada",
                "PME efectiva",
                "Cilindrada total",
                "Cilindrada unitaria",
                "Diámetro",
                "Carrera",
                "Relación carrera/diámetro",
                "Velocidad media del pistón",
            ],
            "Valor": [
                f"{potencia_kw:.2f} kW",
                f"{rpm:.0f} rpm",
                f"{torque_nm:.2f} N m",
                f"{datos['pme'] / 1e5:.2f} bar",
                f"{pme_efectiva / 1e5:.2f} bar",
                f"{cilindrada_total_m3 * 1000:.3f} L",
                f"{cilindrada_unitaria_m3 * 1e6:.1f} cm³",
                f"{diametro_m * 1000:.1f} mm",
                f"{carrera_m * 1000:.1f} mm",
                f"{relacion_carrera_diametro:.2f}",
                f"{velocidad_media_piston:.2f} m/s",
            ],
        }
    )
    st.dataframe(df_geometria, use_container_width=True, hide_index=True)

    mostrar_graficos(ciclo, gamma, datos)

    st.subheader("📥 Exportar resultados")
    col_csv1, col_csv2 = st.columns(2)

    with col_csv1:
        csv_estados = datos["estados"].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Descargar estados CSV",
            data=csv_estados,
            file_name="estados_termodinamicos.csv",
            mime="text/csv",
        )

    with col_csv2:
        csv_geometria = df_geometria.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Descargar geometría CSV",
            data=csv_geometria,
            file_name="geometria_preliminar.csv",
            mime="text/csv",
        )
