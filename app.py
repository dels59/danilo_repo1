import streamlit as st
import pandas as pd

# Inicializando las bases de datos en "st.session_state" si no existen.

if "actividades" not in st.session_state:
    st.session_state.actividades = {}

def agregar_actividad(id_act,nombre_act,tipo,ppto,gasto):
    st.session_state['actividades'][id_act] = {"ID":id_act,"Nombre":nombre_act,"tipo":tipo,"PPTO":ppto,"Gasto":gasto}
    st.success(f"Se incorporó la actividad {nombre_act}.") 
    mostrar_actividad()

def mostrar_actividad():
    df = pd.DataFrame.from_dict(st.session_state['actividades'], orient='index')
    if not df.empty:
        df["Diferencia"]=df["PPTO"]-df["Gasto"]
        df["Evaluación"]=df["Diferencia"].apply(
            lambda x:"Ahorro" if x > 0
            else "Exceso" if x < 0
            else "Exacto"
        )
    st.subheader("Listado de actividades")
    st.dataframe(
        df.style.format({
            "PPTO": "S/ {:,.2f}",
            "Gasto": "S/ {:,.2f}",
            "Diferencia": "S/ {:,.2f}"
        })
    )

class Actividad:
    def __init__(self, nombre, tipo, presupuesto, gasto_real):
        self.nombre = nombre
        self.tipo = tipo
        self.presupuesto = presupuesto
        self.gasto_real = gasto_real

    def esta_en_presupuesto(self):
        return self.gasto_real <= self.presupuesto

    def mostrar_info(self):
        estado = "✅ OK" if self.esta_en_presupuesto() else "❌ Excedido"
        return f"{self.nombre} - Tipo: {self.tipo} | Presupuesto: ${self.presupuesto} | Gasto Real: ${self.gasto_real} | Estado: {estado}"

# ==== Elaboración de Home

st.title("Especialización en Python for Analytics",text_alignment="center")

st.sidebar.title("Menú de Navegación")
alternativas = st.sidebar.selectbox("Elegir Opciones",
                     ["Home",
                      "Ejercicio 1",
                      "Ejercicio 2",
                      "Ejercicio 3",
                      "Ejercicio 4"])

if alternativas == "Home":
   st.subheader("**Bienvenido al Proyecto Aplicado en Streamlit elaborado por Daniel Lopez**",text_alignment="center")
   st.write("Antes de empezar, se comparten los principales detalles del proyecto:")
  
   #Definición_del_Primer_Data_Frame
  
   cuadro_1 = pd.DataFrame(
        {
            "Items": [
                "Título del Proyecto",
                "Nombre Completo", 
                "Año del Curso", 
                "Año",
                "Tecnologías Usadas"],
            "Denominación": [
                "Proyecto Aplicado en Streamlit",
                "Daniel Eduardo Lopez Shapiama",
                "2026",
                "2026",
                "Python, Streamlit, Numpy, Pandas"]
        })
   st.table(cuadro_1)

   st.subheader("Objetivo del Proyecto")
   st.write("El siguiente proyecto tiene como principal objetivo poner en práctica nuestros Fundamentos en Python mediante distintos ejemplos.")
   st.write("A continuación, se describen los ejercicios desarrollados:")
   
   #Definición_del_Segundo_Data_Frame

   cuadro_2 = pd.DataFrame(
        {
            "Ejercicios": [
                "Ejercicio 1 ",
                "Ejercicio 2", 
                "Ejercicio 3", 
                "Ejercicio 4"],
            "Nombre del Ejercicio": [
                "Presupuesto vs Gasto",
                "Registro de Actividades Financieras",
                "Cálculo de Registro Esperado",
                "Definición de Actividades Financieras"]
        })
   st.table(cuadro_2)

# ==== Elaboración de Ejercicio 1

elif alternativas == "Ejercicio 1":
    st.subheader("Presupuesto vs Gasto")
   
    monto_presupuesto= st.number_input(
        label="Monto Presupuestado (PEN)",
        min_value=0.0,
        value=0.0,
        step=50.0,
        format="%.2f",
        help="Ingrese el monto presupuestado o use los botones")
   
    monto_gasto= st.number_input(
        label="Monto Gasto (PEN)",
        min_value=0.0,
        value=0.0,
        step=50.0,
        format="%.2f",
        help="Ingrese el monto gastado o use los botones")
    
    #Incorporando_botón_de_evaluación_presupuestal
    evaluacion = st.button("Evaluar Presupuesto vs Gasto", use_container_width=True)
    
    if evaluacion:
        diferencia = monto_presupuesto-monto_gasto

        if monto_presupuesto==0 and monto_gasto==0:
            st.warning("Ingrese monto presupuestado o  monto gastado.")
        elif diferencia > 0:
            st.success(f"✅ El presupuesto presenta un ahorro de S/ {diferencia:,.2f}.")
        elif diferencia < 0:
            st.error(f"❌ El presupuesto presenta un exceso de S/ {abs(diferencia):,.2f}.")
        elif diferencia == 0:
            st.success(f"🟰 El gasto está alineado con el presupuesto y no presenta ahorros.")
    
        
# ==== Interfaz del Ejercicio 2 en Streamlit ====

elif alternativas == "Ejercicio 2":
    st.subheader("Registro de Actividades Financieras")
    st.caption("Complete la información para registrar una nueva actividad.")

    id_act = st.text_input(
        label="ID Actividad",
        help="Ingrese código de actividad"
        )  
    nombre_act = st.text_input(
        label="Nombre de la Actividad",
        placeholder="Ejemplo: Campaña Digital - Marzo",
        help="Ingrese nombre que describa la actividad a ingresar"
        )
    tipo = st.selectbox(
        "Tipo de Actividad",
        ["Marketing","Operaciones","Logística","Comercial"],
        help="Seleccione la categoría a la que pertenece la actividad."
        )
    ppto = st.number_input(
        label="Monto Presupuestado (PEN)",
        min_value=0.0,
        value=0.0,
        step=50.0,
        format="%.2f",
        help="Ingrese el monto presupuestado o use los botones"
        )
    gasto= st.number_input(
        label="Monto Gasto (PEN)",
        min_value=0.0,
        value=0.0,
        step=50.0,
        format="%.2f",
        help="Ingrese el monto gastado o use los botones"
        )
    if st.button("Agregar Actividad"):
        agregar_actividad(id_act,nombre_act,tipo,ppto,gasto)

# ==== Interfaz del Ejercicio 3 en Streamlit ====

elif alternativas == "Ejercicio 3":
    st.subheader("Cálculo de Retorno según Actividad")
    st.caption("Seleccione la actividad e ingrese el resto de parámetros para calcular el retorno")

    actividad_disponible = False

    if "actividades" in st.session_state and st.session_state.actividades:
        act_list = [a["Nombre"] for a in st.session_state.actividades.values()]
        seleccion = st.selectbox("Selecciona una actividad", act_list)
        
        selec_retorno = next(
            a for a in st.session_state.actividades.values()
        if a["Nombre"] == seleccion
        )

        ppto_base = selec_retorno["PPTO"]
        st.write(f"💰 Presupuesto asignado: S/ {ppto_base:,.2f}")
        actividad_disponible = True
    else:
        ppto_base = None
       
    Tasa_1 = st.number_input(
        label="Tasa",
        min_value=0.0,
        max_value=200.0,
        value=0.0,
        step=2.0,
        format="%.1f",
        help="Ingrese la tasa"
        )
    meses_1= st.number_input(
        label="Cantidad de Meses",
        min_value=0.0,
        value=0.0,
        step=1.0,
        format="%.d",
        help="Ingrese cantidad de meses"
        )
    
    calculo_retorno = lambda p, t, m: p * (t/100) * m

    if st.button("Calcular Retorno", use_container_width=True):
        if not actividad_disponible:
            st.warning("No hay actividades registradas. Añadirlas en el Registro de Actividades Financieras.")
        else:
            retorno = calculo_retorno(ppto_base,Tasa_1,meses_1)
            st.success(f"📈 Retorno esperado: S/ {retorno:,.2f}")


# ==== Interfaz del Ejercicio 2 en Streamlit ====

elif alternativas == "Ejercicio 4":
    if "acciones" not in st.session_state:
        st.session_state.acciones = []

    st.subheader("📊 Incorporación de actividades")

    nombre = st.text_input("Nombre")
    tipo = st.selectbox(
        "Tipo de Actividad",
        ["Marketing","Operaciones","Logística","Comercial"],
        help="Seleccione la categoría a la que pertenece la actividad."
        )
    presupuesto = st.number_input("Presupuesto", min_value=0.0)
    gasto_real = st.number_input("Gasto Real", min_value=0.0)
    
    if st.button("Agregar"):
        nueva = Actividad(nombre, tipo, presupuesto, gasto_real)
        st.session_state.acciones.append(nueva)
        st.success("✅ Actividad agregada con éxito.")
    
    st.subheader("📋 Lista de Actividades")
    if st.session_state.acciones:
        for act in st.session_state.acciones:
            st.write(act.mostrar_info())
    else:
        st.info("No hay actividades registradas.")