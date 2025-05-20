import pandas as pd
import plotly.express as px
import streamlit as st

# --- Cargar datos ---
df = pd.read_csv("data.csv")

# --- Asegurar formato de fecha ---
df["Date"] = pd.to_datetime(df["Date"])

# --- Título y descripción ---
st.title("Análisis Visual de Ventas - Tienda de Conveniencia")
st.markdown("""
Este dashboard interactivo permite explorar las ventas de una tienda de conveniencia, 
proporcionando una visión clara del comportamiento de los clientes, líneas de productos, 
métodos de pago y desempeño general por sucursal.

Utiliza los filtros de la barra lateral para personalizar el análisis según tus necesidades.
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
col1, col2, col3 = st.columns(3)
col1.metric("Ventas Totales", f"${df_filtered['Total'].sum():,.2f}")
col2.metric("Ingreso Bruto", f"${df_filtered['gross income'].sum():,.2f}")
col3.metric("Calificación Promedio", f"{df_filtered['Rating'].mean():.2f}")

# --- Visualizaciones ---
st.markdown("## 1. Evolución de las Ventas Totales por Fecha")
ventas_diarias = df_filtered.groupby("Date")["Total"].sum().reset_index().sort_values("Date")
fig1 = px.line(ventas_diarias, x="Date", y="Total",
               title="Tendencia de Ventas Diarias",
               labels={"Total": "Ventas ($)", "Date": "Fecha"})
st.plotly_chart(fig1, use_container_width=True)

st.markdown("## 2. Ingresos por Línea de Producto")
ingresos_producto = df_filtered.groupby("Product line")["Total"].sum().reset_index()
fig2 = px.bar(ingresos_producto, x="Product line", y="Total", color="Product line",
              title="Ingresos Totales por Categoría de Producto",
              labels={"Total": "Ingresos ($)", "Product line": "Categoría"})
st.plotly_chart(fig2, use_container_width=True)

st.markdown("## 3. Comparación del Gasto por Tipo de Cliente")
fig3 = px.box(df_filtered, x="Customer type", y="Total", color="Customer type",
              title="Distribución del Gasto por Tipo de Cliente",
              labels={"Total": "Total Gasto ($)", "Customer type": "Tipo de Cliente"})
st.plotly_chart(fig3, use_container_width=True)

st.markdown("## 4. Preferencias de Método de Pago")
payment_counts = df_filtered["Payment"].value_counts().reset_index()
payment_counts.columns = ["Método de Pago", "Cantidad"]
fig4 = px.pie(payment_counts, names="Método de Pago", values="Cantidad",
              title="Distribución de Métodos de Pago Preferidos")
st.plotly_chart(fig4, use_container_width=True)

# --- Visualización 5: Gráfico 3D de Costo, Ganancia y Precio ---
st.markdown("## 5. Relación 3D: Costo, Ganancia y Precio Unitario")
fig5 = px.scatter_3d(
    df_filtered,
    x='cogs',
    y='gross income',
    z='Unit price',
    color='Product line',
    title='Relación 3D: Costo, Ganancia y Precio',
    opacity=0.7
)
st.plotly_chart(fig5)

# --- Visualización 6: Matriz de Correlación ---
st.markdown("## 6. Matriz de Correlación de Variables Numéricas")
numeric_cols = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross income', 'Rating']
corr = df_filtered[numeric_cols].corr()
fig6 = px.imshow(corr, text_auto=True, title='Matriz de Correlación', color_continuous_scale='Viridis')
st.plotly_chart(fig6)

# --- Visualización 7: Ingreso Bruto por Sucursal y Línea de Producto (Sunburst) ---
st.markdown("## 7. Ingreso Bruto por Sucursal y Línea de Producto")
sunburst_data = df_filtered.groupby(['Branch', 'Product line'])['gross income'].sum().reset_index()
fig7 = px.sunburst(sunburst_data, path=['Branch', 'Product line'], values='gross income', title='Ingreso Bruto por Sucursal y Línea de Producto')
st.plotly_chart(fig7)
