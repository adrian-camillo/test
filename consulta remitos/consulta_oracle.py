import oracledb
import tkinter as tk

# Conexión a la base de datos Oracle
host = '129.151.97.98'
port = 1521
service_name = 'INTDB5_pdb1.sub12222046451.net1.oraclevcn.com'
user = 'INTH1070$NICO'
password = 'NIco*(78227$$13'
dsn = oracledb.makedsn(host, port, service_name=service_name)
connection = oracledb.connect(user, password, dsn)

# Crear una función para realizar la consulta y mostrar los resultados
def consultar_remito():
    codigo = entry_codigo.get()
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

# Crear la ventana
root = tk.Tk()
root.title("Consulta de Remito")

# Crear etiqueta e input para el código de remito
label_codigo = tk.Label(root, text="Código de Remito:")
label_codigo.pack()
entry_codigo = tk.Entry(root)
entry_codigo.pack()

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

root.mainloop()

# cambiar tipo de grafico barras y lineal
