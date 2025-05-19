import pandas as pd
import plotly.express as px
import streamlit as st

# --- Cargar datos ---
df = pd.read_csv("data.csv")

# --- Título y descripción ---
st.title("Dashboard de Ventas de Tienda de Conveniencia")
st.markdown("""
Este dashboard presenta las visualizaciones más relevantes para comprender la evolución de las ventas,
el comportamiento de los clientes y sus preferencias de pago. Se incluyen filtros para analizar por sucursal,
línea de producto y tipo de cliente.
""")

# --- Filtros interactivos ---
st.sidebar.header("Filtros")
branch = st.sidebar.multiselect("Sucursal", options=df["Branch"].unique(), default=df["Branch"].unique())
product_line = st.sidebar.multiselect("Línea de Producto", options=df["Product line"].unique(), default=df["Product line"].unique())
customer_type = st.sidebar.multiselect("Tipo de Cliente", options=df["Customer type"].unique(), default=df["Customer type"].unique())

# --- Aplicar filtros ---
df_filtered = df[
    (df["Branch"].isin(branch)) &
    (df["Product line"].isin(product_line)) &
    (df["Customer type"].isin(customer_type))
]

# --- KPIs destacados ---
st.metric("Ventas Totales", f"${df_filtered['Total'].sum():,.2f}")
st.metric("Ingreso Bruto", f"${df_filtered['gross income'].sum():,.2f}")
st.metric("Promedio de Calificación", f"{df_filtered['Rating'].mean():.2f}")

# --- Visualizaciones ---
st.markdown("## 1. Evolución de las Ventas Totales")
ventas_diarias = df_filtered.groupby("Date")["Total"].sum().reset_index()
fig1 = px.line(ventas_diarias, x="Date", y="Total", title="Evolución de las Ventas Totales")
st.plotly_chart(fig1)

st.markdown("## 2. Ingresos por Línea de Producto")
ingresos_producto = df_filtered.groupby("Product line")["Total"].sum().reset_index()
fig2 = px.bar(ingresos_producto, x="Product line", y="Total", color="Product line", title="Ingresos por Línea de Producto")
st.plotly_chart(fig2)

st.markdown("## 3. Gasto por Tipo de Cliente")
fig3 = px.box(df_filtered, x="Customer type", y="Total", color="Customer type", title="Gasto por Tipo de Cliente")
st.plotly_chart(fig3)

st.markdown("## 4. Métodos de Pago Preferidos")
payment_counts = df_filtered["Payment"].value_counts().reset_index()
payment_counts.columns = ["Payment Method", "Count"]
fig4 = px.pie(payment_counts, names="Payment Method", values="Count", title="Métodos de Pago Preferidos")
st.plotly_chart(fig4)
