import tkinter as tk
import cx_Oracle

#ejemplo de numero 788537 
# Datos de conexión (puedes gestionar estos datos de manera más segura)
host = '129.151.97.98'
port = 1521
service_name = 'INTDB5_pdb1.sub12222046451.net1.oraclevcn.com'
user = 'INTH1070$NICO'
password = 'NIco*(78227$$13'

# Crear el string de conexión
try:
    connection = cx_Oracle.connect(f"{user}/{password}@{host}:{port}/{service_name}")
except cx_Oracle.DatabaseError as e:
    print("Error de conexión a la base de datos:", str(e))
    exit(1)

# Crear la ventana
root = tk.Tk()
root.title("Consulta de Remito")

# Crear etiqueta e input para el código de remito
label_codigo = tk.Label(root, text="Código de Remito:")
label_codigo.pack()
entry_codigo = tk.Entry(root)
entry_codigo.pack()

# Definir la función consultar_remito
def consultar_remito():
# Obtener el código de remito ingresado por el usuario
    codigo = entry_codigo.get()
    
# Realizar la consulta SQL con el código ingresado y mostrar los resultados
    cursor = connection.cursor()
    query = f"SELECT CODI AS remito, EMPR0110$NSUC as desde, stkd0100$id_orig as hasta, FDES as fecha_de_envio, FING as fecha_recibido, AUDI0100$ID FROM erp$stkm0100 WHERE CODI = {codigo} AND EMPR0100$ID = 1"
    cursor.execute(query)
    resultado = cursor.fetchone()
    
    if resultado:
        remito_label.config(text=f"Remito: {resultado[0]}")
        desde_label.config(text=f"Desde: {resultado[1]}")
        hasta_label.config(text=f"Hasta: {resultado[2]}")
        fecha_envio_label.config(text=f"Fecha de Envío: {resultado[3]}")
        fecha_recibido_label.config(text=f"Fecha Recibido: {resultado[4]}")

        # Obtener la persona asociada al remito
        cursor.execute(f"SELECT USRN FROM ERP$AUDI0100 WHERE ID = {resultado[5]}")
        usuario = cursor.fetchone()

        if usuario:
            usuario_label.config(text=f"Persona Asociada: {usuario[0]}")
        else:
            usuario_label.config(text="No se encontró la persona asociada.")
    else:
        remito_label.config(text="No se encontraron resultados.")

# Botón para realizar la consulta
consultar_button = tk.Button(root, text="Consultar", command=consultar_remito)
consultar_button.pack()

# Etiquetas para mostrar los resultados
remito_label = tk.Label(root, text="")
remito_label.pack()
desde_label = tk.Label(root, text="")
desde_label.pack()
hasta_label = tk.Label(root, text="")
hasta_label.pack()
fecha_envio_label = tk.Label(root, text="")
fecha_envio_label.pack()
fecha_recibido_label = tk.Label(root, text="")
fecha_recibido_label.pack()
usuario_label = tk.Label(root, text="")
usuario_label.pack()

# Cierre de la conexión al salir de la aplicación
root.protocol("WM_DELETE_WINDOW", lambda: (connection.close(), root.destroy()))

root.mainloop()