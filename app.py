import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt


# =====================================================
# CONFIGURACIÓN DE PÁGINA
# =====================================================

st.set_page_config(
    page_title="Especialización en Python for Analytics",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.main-title {
    text-align:center;
    font-size:42px;
    font-weight:700;
    color:#1f4e79;
}

.section-title {
    font-size:26px;
    font-weight:600;
    color:#2c3e50;
}

.insight-box{
background-color:#f0f2f6;
padding:10px;
border-radius:8px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📘 Especialización en Python for Analytics</div>', unsafe_allow_html=True)


# =====================================================
# FUNCIONES
# =====================================================

@st.cache_data
def cargar_datos(file):
    return pd.read_csv(file)


def clasificar_variables(df):

    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include=["object","category"]).columns.tolist()

    resumen = pd.DataFrame({
        "Tipo":["Numéricas","Categóricas"],
        "Cantidad":[len(num_cols),len(cat_cols)]
    })

    return resumen,num_cols,cat_cols



# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("📌 Menú de Navegación")

modulo = st.sidebar.selectbox(
    "Elegir módulo",
    [
        "🏠 Home",
        "📂 Módulo 1 (Carga)",
        "📊 Módulo 2 (EDA I)",
        "📈 Módulo 3 (EDA II)",
        "🔎 Módulo 4 (EDA III)",
        "⚙️ Módulo 5 (Selección)",
        "💡 Módulo 6 (Hallazgos)"
    ]
)



# =====================================================
# HOME  (SIN MODIFICAR CONTENIDO)
# =====================================================

if modulo == "🏠 Home":

    st.subheader("Bienvenido al análisis de churn de clientes")

    descripcion = pd.DataFrame({

        "Elemento":[
            "Título del Proyecto",
            "Autor",
            "Programa",
            "Objetivo del Proyecto",
            "Descripción del Dataset",
            "Variables Principales",
            "Tecnologías Utilizadas"
        ],

        "Descripción":[
            "Análisis Exploratorio del abandono de clientes (Customer Churn)",
            "Daniel Eduardo Lopez Shapiama",
            "Especialización Python for Analytics",
            "Identificar patrones y factores que influyen en la cancelación del servicio por parte de los clientes.",
            "El dataset Telco Customer Churn contiene información sobre clientes de una empresa de telecomunicaciones incluyendo características demográficas, servicios contratados, facturación y estado del cliente.",
            "Tenure, MonthlyCharges, Contract, InternetService, Churn",
            "Python, Pandas, Streamlit, Matplotlib"
        ]

    })

    st.table(descripcion)



# =====================================================
# MODULO 1 CARGA
# =====================================================

elif modulo == "📂 Módulo 1 (Carga)":

    st.markdown("## 📂 Carga de Dataset")

    archivo = st.file_uploader("Sube tu archivo CSV",type=["csv"])

    if archivo is not None:

        df = cargar_datos(archivo)

        st.session_state["df"] = df

        filas,columnas = df.shape

        col1,col2,col3 = st.columns(3)

        col1.metric("👥 Clientes",filas)
        col2.metric("📊 Variables",columnas)
        col3.metric("🔢 Datos totales",filas*columnas)

        st.markdown("### Vista previa")

        st.dataframe(df.head())

    else:

        st.info("Sube un dataset para comenzar")



# =====================================================
# MODULO 2 EDA I
# =====================================================

elif modulo == "📊 Módulo 2 (EDA I)":

    if "df" not in st.session_state:

        st.warning("Primero carga el dataset")

    else:

        df = st.session_state["df"]

        st.markdown("## 📊 Exploratory Data Analysis")

        st.markdown("### Información del Dataset")

        info_df = pd.DataFrame({
            "Columna":df.columns,
            "Tipo":df.dtypes.values,
            "Valores nulos":df.isnull().sum().values
        })

        st.dataframe(info_df)

        st.markdown("### Clasificación de Variables")

        resumen,num_cols,cat_cols = clasificar_variables(df)

        col1,col2 = st.columns(2)

        col1.metric("🔢 Variables Numéricas",len(num_cols))
        col2.metric("🔤 Variables Categóricas",len(cat_cols))

        st.dataframe(resumen)

        st.markdown("### Estadística Descriptiva")

        st.dataframe(df.describe())

        st.markdown("### Valores faltantes")

        missing = df.isnull().sum()
        missing = missing[missing>0]

        if len(missing)>0:

            st.bar_chart(missing)

        else:

            st.success("No existen valores faltantes")



# =====================================================
# MODULO 3 DISTRIBUCIONES
# =====================================================

elif modulo == "📈 Módulo 3 (EDA II)":

    if "df" not in st.session_state:

        st.warning("Primero carga el dataset")

    else:

        df = st.session_state["df"]

        st.markdown("## 📈 Distribución de Variables Numéricas")

        num_cols = df.select_dtypes(include=np.number).columns.tolist()

        variable = st.selectbox("Selecciona una variable",num_cols)

        if st.button("Generar análisis"):

            col1,col2 = st.columns(2)

            with col1:

                fig,ax = plt.subplots(figsize=(5,3))

                ax.hist(df[variable].dropna(),bins=30,color="#1f77b4")

                ax.grid(True,linestyle="--",alpha=0.5)

                ax.set_title(variable)

                st.pyplot(fig)

            with col2:

                st.dataframe(df[variable].describe())



# =====================================================
# MODULO 4 BIVARIADO (INSIGHTS INCLUIDOS)
# =====================================================

elif modulo == "🔎 Módulo 4 (EDA III)":

    if "df" not in st.session_state:

        st.warning("Primero carga el dataset")

    else:

        df = st.session_state["df"]

        st.markdown("## 🔎 Análisis Bivariado")

        if "Churn" in df.columns:

            st.markdown("### MonthlyCharges vs Churn")

            fig,ax = plt.subplots(figsize=(5,3))

            df.boxplot(column="MonthlyCharges",by="Churn",ax=ax)

            ax.grid(True)

            plt.suptitle("")

            st.pyplot(fig)

            promedio_charges = df.groupby("Churn")["MonthlyCharges"].mean()

            col1,col2 = st.columns(2)

            col1.metric("💸 Promedio Churn",round(promedio_charges["Yes"],2))
            col2.metric("💰 Promedio No Churn",round(promedio_charges["No"],2))

            if promedio_charges["Yes"] > promedio_charges["No"]:

                st.info("📌 Los clientes que abandonan presentan cargos mensuales más altos.")

            st.markdown("### Tenure vs Churn")

            fig,ax = plt.subplots(figsize=(5,3))

            df.boxplot(column="tenure",by="Churn",ax=ax)

            ax.grid(True)

            plt.suptitle("")

            st.pyplot(fig)

            promedio_tenure = df.groupby("Churn")["tenure"].mean()

            col1,col2 = st.columns(2)

            col1.metric("📉 Tenure Churn",round(promedio_tenure["Yes"],2))
            col2.metric("📈 Tenure No Churn",round(promedio_tenure["No"],2))

            if promedio_tenure["Yes"] < promedio_tenure["No"]:

                st.info("📌 Clientes con menor antigüedad presentan mayor probabilidad de churn.")



# =====================================================
# MODULO 5 SELECCIÓN
# =====================================================

elif modulo == "⚙️ Módulo 5 (Selección)":

    if "df" not in st.session_state:

        st.warning("Primero carga el dataset")

    else:

        df = st.session_state["df"]

        columnas = st.multiselect("Selecciona columnas",df.columns)

        if columnas:

            st.dataframe(df[columnas].head())



# =====================================================
# MODULO 6 HALLAZGOS
# =====================================================

elif modulo == "💡 Módulo 6 (Hallazgos)":

    if "df" not in st.session_state:

        st.warning("Primero carga el dataset")

    else:

        df = st.session_state["df"]

        st.markdown("## 💡 Hallazgos Clave")

        churn_rate = (df["Churn"]=="Yes").mean()*100

        col1,col2,col3 = st.columns(3)

        col1.metric("👥 Clientes",len(df))
        col2.metric("📉 Churn Rate",f"{churn_rate:.2f}%")
        col3.metric("💸 MonthlyCharges Prom",round(df["MonthlyCharges"].mean(),2))


        st.markdown("### Churn por tipo de contrato")

        tabla = pd.crosstab(df["Contract"],df["Churn"],normalize="index")*100

        fig,ax = plt.subplots(figsize=(5,3))

        tabla.plot(kind="bar",stacked=True,ax=ax)

        st.pyplot(fig)


        st.markdown("### Churn por InternetService")

        tabla2 = pd.crosstab(df["InternetService"],df["Churn"],normalize="index")*100

        fig,ax = plt.subplots(figsize=(5,3))

        tabla2.plot(kind="bar",stacked=True,ax=ax)

        st.pyplot(fig)


        st.markdown("### Insights de negocio")

        st.write("""

📌 Los clientes con contratos **Month-to-Month presentan mayor churn**.

📌 Clientes con **menor tenure abandonan con mayor frecuencia**.

📌 Los clientes con **MonthlyCharges más altos tienden a cancelar más**.

📌 Los contratos **One Year y Two Year muestran mayor retención**.

📌 Clientes nuevos con cargos altos representan **segmento de alto riesgo**.

""")


        st.markdown("### Recomendaciones estratégicas")

        st.write("""

✔ Incentivar migración a contratos anuales.

✔ Programas de fidelización durante el primer año.

✔ Revisar estructura de precios para clientes de alto gasto.

✔ Diseñar campañas de retención para clientes en alto riesgo.

""")