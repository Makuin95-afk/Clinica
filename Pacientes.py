from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Conexión a Mysql
def conexionMySQL():
    try:
        conexion = mysql.connector.connect(
            host='localhost',  # Cambia esto si tu base de datos no está en localhost
            user='root',  # Usuario de MySQL
            password='ujcv2025',  # Contraseña de MySQL
            database='ClinicaHospitalariaH'  # Nombre de la base de datos
        )
        return conexion
    except mysql.connector.Error as e:
        return None

# Función para ejecutar consultas SQL
def ejecutarSQL(consulta, parametros=None, recibir_datos=False):
    conexion = conexionMySQL()
    if isinstance(conexion, str):
        return conexion  # Si la conexión falló, devolvemos el error
    
    with conexion:
        cursor = conexion.cursor()
        if parametros:
            cursor.execute(consulta, parametros)
        else:
            cursor.execute(consulta)
        
        if recibir_datos:
            return cursor.fetchall()
        else:
            conexion.commit()
            return "Operación realizada con éxito"

# Ruta para obtener todos los pacientes
@app.route('/pacientes', methods=['GET'])
def obtener_pacientes():
    consulta = "SELECT * FROM Paciente"
    filas = ejecutarSQL(consulta, recibir_datos=True)
    pacientes = [
        {"ID_Paciente": fila[0], "Nombre": fila[1], "Apellido": fila[2], "Fecha_Nacimiento": fila[3],
         "DNI": fila[4], "Direccion": fila[5], "Telefono": fila[6], "Email": fila[7], "Tipo_Sangre": fila[8],
         "ID_Seguro": fila[9]} for fila in filas
    ]
    return jsonify(pacientes)

# Ruta para agregar un nuevo paciente
@app.route('/pacientes', methods=['POST'])
def agregar_paciente():
    datos = request.json
    consulta = """
        INSERT INTO Paciente (ID_Paciente, Nombre, Apellido, Fecha_Nacimiento, DNI, Direccion, Telefono, Email, Tipo_Sangre, ID_Seguro)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    parametros = (
        datos['ID_Paciente'], datos['Nombre'], datos['Apellido'], datos['Fecha_Nacimiento'],
        datos['DNI'], datos['Direccion'], datos['Telefono'], datos['Email'], datos['Tipo_Sangre'], datos['ID_Seguro']
    )
    resultado = ejecutarSQL(consulta, parametros)
    return jsonify({"mensaje": resultado})

# Ruta para actualizar un paciente
@app.route('/pacientes/<int:id_paciente>', methods=['PUT'])
def actualizar_paciente(id_paciente):
    datos = request.json
    consulta = """
        UPDATE Paciente SET Nombre=?, Apellido=?, Fecha_Nacimiento=?, DNI=?, Direccion=?,
        Telefono=?, Email=?, Tipo_Sangre=?, ID_Seguro=? WHERE ID_Paciente=?
    """
    parametros = (
        datos['Nombre'], datos['Apellido'], datos['Fecha_Nacimiento'], datos['DNI'], datos['Direccion'],
        datos['Telefono'], datos['Email'], datos['Tipo_Sangre'], datos['ID_Seguro'], id_paciente
    )
    resultado = ejecutarSQL(consulta, parametros)
    return jsonify({"mensaje": resultado})

# Ruta para eliminar un paciente
@app.route('/pacientes/<int:id_paciente>', methods=['DELETE'])
def eliminar_paciente(id_paciente):
    consulta = "DELETE FROM Paciente WHERE ID_Paciente=?"
    parametros = (id_paciente,)
    resultado = ejecutarSQL(consulta, parametros)
    return jsonify({"mensaje": resultado})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

