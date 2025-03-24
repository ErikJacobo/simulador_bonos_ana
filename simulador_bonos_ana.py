import streamlit as st

def calcular_bono_produccion(prima_cobrada, crecimiento):
    notas = []
    if crecimiento < 5:
        return 0, "❌ No se cumple el crecimiento mínimo del 5%.", ["Se requiere al menos un 5% de crecimiento para acceder al bono."]
    if prima_cobrada < 600000:
        return 0, "❌ Prima cobrada menor al mínimo requerido.", ["El mínimo de prima cobrada es $600,000 para aplicar al bono."]
    elif prima_cobrada < 900000:
        return 0.02, "✅ Se aplica bono del 2%.", []
    elif prima_cobrada < 1250000:
        return 0.04, "✅ Se aplica bono del 4%.", []
    elif prima_cobrada < 1750000:
        return 0.05, "✅ Se aplica bono del 5%.", []
    elif prima_cobrada < 3000000:
        return 0.06, "✅ Se aplica bono del 6%.", []
    else:
        return 0.07, "✅ Se aplica bono del 7%.", []

def calcular_bono_crecimiento(pagos_2024, pagos_2025, siniestralidad):
    crecimiento = ((pagos_2025 - pagos_2024) / pagos_2024) * 100 if pagos_2024 > 0 else 0
    notas = []
    if crecimiento <= 20:
        return 0, "❌ Crecimiento insuficiente para aplicar bono.", ["El crecimiento debe superar el 20% para aplicar bono."]
    elif crecimiento > 40:
        if siniestralidad < 65:
            return 0.05, "✅ Crecimiento >40% y siniestralidad <65%.", []
        else:
            return 0.025, "✅ Crecimiento >40% y siniestralidad >65%.", ["⚠ Se reduce el bono por siniestralidad mayor al 65%."]
    elif crecimiento > 30:
        if siniestralidad < 65:
            return 0.04, "✅ Crecimiento >30% y siniestralidad <65%.", []
        else:
            return 0.02, "✅ Crecimiento >30% y siniestralidad >65%.", ["⚠ Se reduce el bono por siniestralidad mayor al 65%."]
    else:  # 20% < crecimiento ≤ 30%
        if siniestralidad < 65:
            return 0.03, "✅ Crecimiento >20% y siniestralidad <65%.", []
        else:
            return 0.015, "✅ Crecimiento >20% y siniestralidad >65%.", ["⚠ Se reduce el bono por siniestralidad mayor al 65%."]

# Interfaz Streamlit
st.markdown("<h1 style='text-align: center;'>Simulador de Bonos</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>ANA Seguros 2025</h2>", unsafe_allow_html=True)
st.markdown("---")

# Campo nombre
nombre_agente = st.text_input("🧑 Nombre del agente")

# Tipo de bono
tipo_bono = st.selectbox("📊 Tipo de Bono", ["Selecciona...", "Producción", "Crecimiento"])

if tipo_bono == "Producción":
    st.markdown("### ➤ Datos Ingresados")
    prima = st.number_input("💰 Prima Cobrada (neto pagado a ANA)", min_value=0.0, step=1000.0, format="%.2f")
    crecimiento = st.number_input("📈 Crecimiento respecto a 2024 (%)", min_value=0.0, step=0.1, format="%.2f")

    if st.button("Calcular Bono de Producción"):
        porcentaje, mensaje, notas = calcular_bono_produccion(prima, crecimiento)
        bono = prima * porcentaje

        st.markdown("### ✅ Resultado para **" + nombre_agente + "**")
        st.markdown(f"- Bono de Producción: **{porcentaje*100:.2f}%**")
        st.markdown(f"- Monto del bono: **${bono:,.2f}**")
        st.markdown(f"- Resultado: {mensaje}")

        if notas:
            st.markdown("### 📌 Notas:")
            for nota in notas:
                st.markdown(f"- {nota}")

elif tipo_bono == "Crecimiento":
    st.markdown("### ➤ Datos Ingresados")
    pagos_2024 = st.number_input("💵 Primas pagadas 2024 ($)", min_value=0.0, step=1000.0, format="%.2f")
    pagos_2025 = st.number_input("💵 Primas pagadas 2025 ($)", min_value=0.0, step=1000.0, format="%.2f")
    siniestralidad = st.number_input("⚠ Siniestralidad (%)", min_value=0.0, max_value=100.0, step=0.1, format="%.2f")

    if st.button("Calcular Bono de Crecimiento"):
        crecimiento_real = ((pagos_2025 - pagos_2024) / pagos_2024) * 100 if pagos_2024 > 0 else 0
        porcentaje, mensaje, notas = calcular_bono_crecimiento(pagos_2024, pagos_2025, siniestralidad)
        bono = (pagos_2025 - pagos_2024) * porcentaje

        st.markdown("### ✅ Resultado para **" + nombre_agente + "**")
        st.markdown(f"- Crecimiento Real: **{crecimiento_real:.2f}%**")
        st.markdown(f"- Bono de Crecimiento: **{porcentaje*100:.2f}%**")
        st.markdown(f"- Monto del bono: **${bono:,.2f}**")
        st.markdown(f"- Resultado: {mensaje}")

        if notas:
            st.markdown("### 📌 Notas:")
            for nota in notas:
                st.markdown(f"- {nota}")

st.markdown("---")
st.caption("📝 Sujeto a términos y condiciones del cuaderno oficial de incentivos ANA Seguros 2025.")
