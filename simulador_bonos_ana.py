import streamlit as st

def calcular_bono_produccion(prima_cobrada, crecimiento_pct):
    notas = []
    if crecimiento_pct < 5:
        return 0, "❌ No se cumple el crecimiento mínimo del 5%.", ["Se requiere al menos un 5% de crecimiento para aplicar al bono de producción."]
    if prima_cobrada < 600000:
        return 0, "❌ Prima cobrada menor al mínimo requerido.", ["El mínimo de prima cobrada es $600,000 para aplicar al bono."]
    elif prima_cobrada < 900000:
        return 0.02, "✅ Aplica bono del 2%.", []
    elif prima_cobrada < 1250000:
        return 0.04, "✅ Aplica bono del 4%.", []
    elif prima_cobrada < 1750000:
        return 0.05, "✅ Aplica bono del 5%.", []
    elif prima_cobrada < 3000000:
        return 0.06, "✅ Aplica bono del 6%.", []
    else:
        return 0.07, "✅ Aplica bono del 7%.", []

def calcular_bono_crecimiento(prod_2024, prod_2025, siniestralidad):
    crecimiento = ((prod_2025 - prod_2024) / prod_2024) * 100 if prod_2024 > 0 else 0
    notas = []
    if crecimiento <= 20:
        return crecimiento, 0, "❌ Crecimiento insuficiente para aplicar bono.", ["El crecimiento debe superar el 20% para aplicar bono."]
    elif crecimiento > 40:
        if siniestralidad < 65:
            return crecimiento, 0.05, "✅ Aplica bono del 5%.", []
        else:
            return crecimiento, 0.025, "✅ Aplica bono del 2.5%.", ["⚠ Siniestralidad mayor a 65%. Se reduce el porcentaje del bono."]
    elif crecimiento > 30:
        if siniestralidad < 65:
            return crecimiento, 0.04, "✅ Aplica bono del 4%.", []
        else:
            return crecimiento, 0.02, "✅ Aplica bono del 2%.", ["⚠ Siniestralidad mayor a 65%. Se reduce el porcentaje del bono."]
    else:  # 20 < crecimiento <= 30
        if siniestralidad < 65:
            return crecimiento, 0.03, "✅ Aplica bono del 3%.", []
        else:
            return crecimiento, 0.015, "✅ Aplica bono del 1.5%.", ["⚠ Siniestralidad mayor a 65%. Se reduce el porcentaje del bono."]

# Interfaz Streamlit
st.set_page_config(page_title="Simulador ANA 2025", layout="centered")
st.markdown("<h1 style='text-align: center;'>Simulador de Bonos</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>ANA Seguros 2025</h2>", unsafe_allow_html=True)

# Formulario
nombre_agente = st.text_input("Nombre del Agente")
tipo_bono = st.selectbox("Tipo de Bono", ["Autos"])  # Manténlo aunque solo haya uno, por formato estándar
prod_2024 = st.number_input("Producción 2024 (en pesos)", min_value=0.0, step=1000.0, format="%.2f")
prod_2025 = st.number_input("Producción 2025 (en pesos)", min_value=0.0, step=1000.0, format="%.2f")
siniestralidad = st.number_input("Siniestralidad (%)", min_value=0.0, max_value=100.0, step=0.1, format="%.2f")

if st.button("Calcular Bonos"):
    crecimiento_pct = ((prod_2025 - prod_2024) / prod_2024) * 100 if prod_2024 > 0 else 0

    # Cálculo Producción
    prod_pct, prod_msg, prod_notas = calcular_bono_produccion(prod_2025, crecimiento_pct)
    bono_produccion = prod_2025 * prod_pct

    # Cálculo Crecimiento
    crecimiento, crec_pct, crec_msg, crec_notas = calcular_bono_crecimiento(prod_2024, prod_2025, siniestralidad)
    bono_crecimiento = (prod_2025 - prod_2024) * crec_pct

    total_bono = bono_produccion + bono_crecimiento

    # Resultados
    st.markdown(f"### Resultado para **{nombre_agente}**")
    st.markdown("#### 📊 Datos Ingresados:")
    st.markdown(f"- Producción 2024: **${prod_2024:,.2f}**")
    st.markdown(f"- Producción 2025: **${prod_2025:,.2f}**")
    st.markdown(f"- Crecimiento Real: **{crecimiento_pct:.2f}%**")
    st.markdown(f"- Siniestralidad: **{siniestralidad:.2f}%**")

    st.markdown("#### 💵 Resultados de Bono:")
    st.markdown(f"- Bono de Producción: **{prod_pct*100:.2f}%** → **${bono_produccion:,.2f}** → {prod_msg}")
    st.markdown(f"- Bono de Crecimiento: **{crec_pct*100:.2f}%** → **${bono_crecimiento:,.2f}** → {crec_msg}")
    st.markdown(f"### 🧾 Total del Bono: **${total_bono:,.2f}**")

    if prod_notas or crec_notas:
        st.markdown("#### 📌 Notas Aclaratorias:")
        for nota in prod_notas + crec_notas:
            st.markdown(f"- {nota}")

st.markdown("---")
st.caption("Aplican restricciones y condiciones conforme al cuaderno oficial de ANA Seguros 2025.")
