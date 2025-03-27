import streamlit as st
from PIL import Image

def safe_float(val):
    try:
        return float(val.replace(",", "").replace("$", "").strip())
    except:
        return 0.0

def calcular_bono_produccion(prima_cobrada, crecimiento_pct):
    notas = []
    if crecimiento_pct < 15:
        return 0, "❌ No se cumple el crecimiento mínimo del 15%.", ["Se requiere al menos un 15% de crecimiento para aplicar al bono de producción."]
    if prima_cobrada < 200000:
        return 0, "❌ Prima cobrada menor al mínimo requerido.", ["El mínimo de prima cobrada es $200,000 para aplicar al bono."]
    elif prima_cobrada <= 600000:
        return 0.01, "✅ Aplica bono del 1%.", []
    elif prima_cobrada <= 900000:
        return 0.02, "✅ Aplica bono del 2%.", []
    elif prima_cobrada <= 1750000:
        return 0.03, "✅ Aplica bono del 3%.", []
    elif prima_cobrada <= 2500000:
        return 0.04, "✅ Aplica bono del 4%.", []
    elif prima_cobrada <= 3000000:
        return 0.05, "✅ Aplica bono del 5%.", []
    else:
        return 0.06, "✅ Aplica bono del 6%.", []

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
    else:
        if siniestralidad < 65:
            return crecimiento, 0.03, "✅ Aplica bono del 3%.", []
        else:
            return crecimiento, 0.015, "✅ Aplica bono del 1.5%.", ["⚠ Siniestralidad mayor a 65%. Se reduce el porcentaje del bono."]

# Página
st.set_page_config(page_title="Simulador ANA 2025", layout="centered")

# Logo + encabezado
col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.markdown("<h1 style='text-align: left;'>Simulador de Bonos</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: left;'>ANA Seguros 2025</h2>", unsafe_allow_html=True)
with col2:
    logo = Image.open("link logo.jpg")  # Usa tu imagen cargada
    st.image(logo, width=100)

# Formulario
nombre_agente = st.text_input("Nombre del Agente")
tipo_bono = st.selectbox("Tipo de Bono", ["Autos"])

prod_2024_text = st.text_input("Producción 2024 ($)", placeholder="Ej. $1,000,000.00")
prod_2025_text = st.text_input("Producción 2025 ($)", placeholder="Ej. $2,000,000.00")
prod_2024 = safe_float(prod_2024_text)
prod_2025 = safe_float(prod_2025_text)

siniestralidad = st.number_input("Siniestralidad (%)", min_value=0.0, max_value=100.0, step=0.1, format="%.2f")

if st.button("Calcular Bonos"):
    crecimiento_pct = ((prod_2025 - prod_2024) / prod_2024) * 100 if prod_2024 > 0 else 0

    # Cálculos
    prod_pct, prod_msg, prod_notas = calcular_bono_produccion(prod_2025, crecimiento_pct)
    bono_produccion = prod_2025 * prod_pct

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

    # Notas
    if prod_notas or crec_notas:
        st.markdown("#### 📌 Notas Aclaratorias:")
        for nota in prod_notas + crec_notas:
            st.markdown(f"- {nota}")

    st.markdown("---")
    st.markdown("#### ❌ Exclusiones ANA Seguros:")
    st.markdown("- Negocios con fórmula de dividendos.")
    st.markdown("- Negocios Turistas.")
    st.markdown("- Unidades de servicio público.")
    st.markdown("- Negocios con UDI.")
    st.markdown("- Equipo pesado (mayores a 7.5 toneladas).")
    st.markdown("- Agentes con disposición de primas.")
    st.markdown("- RC Plus y Obligatoria.")
    st.markdown("- Negocios y convenios especiales.")
    st.markdown("- Coberturas especiales (Defensa Jurídica, ANA Asistencia, etc.).")
    st.markdown("- Negocios de gobierno o licitaciones.")
    st.markdown("- Unidades con plataformas (apps conductores).")

    st.markdown("#### ✅ Estos bonos aplican para:")
    st.markdown("- Pólizas individuales de autos, motos y camiones ligeros hasta 7.5 toneladas (Uso Particular y Carga).")
    st.markdown("- Flotillas hasta 70 unidades hasta 7.5 toneladas (carga A y B).")
    st.markdown("- Agentes con cédula vigente durante el periodo del concurso.")

st.markdown("---")
st.caption("Aplican restricciones y condiciones conforme al cuaderno oficial de ANA Seguros 2025.")
