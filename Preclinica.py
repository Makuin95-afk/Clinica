from flask import Flask, request, jsonify


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

# Obtener todas las consultas preclínicas
@app.route('/preclinica', methods=['GET'])
def obtener_preclinica():
    conexion = conexionSQLServer()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Preclinica")
        filas = cursor.fetchall()
        conexion.close()
        
        resultados = [{"Id_Preclinica": fila[0], "Id_Consultorio": fila[1], "Id_Paciente": fila[2], "Fecha": str(fila[3]), "Hora": str(fila[4]), "Sintomas": fila[5], "Temperatura": fila[6], "Presion": fila[7], "Peso": fila[8]} for fila in filas]
        return jsonify(resultados)
    return jsonify({"error": "Error de conexión a la base de datos"}), 500

# Agregar una nueva consulta preclínica
@app.route('/preclinica', methods=['POST'])
def agregar_preclinica():
    datos = request.json
    conexion = conexionSQLServer()
    if conexion:
        cursor = conexion.cursor()
        consulta = "INSERT INTO Preclinica (Id_Preclinica, Id_Consultorio, Id_Paciente, Fecha, Hora, Sintomas, Temperatura, Presion, Peso) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(consulta, (datos['Id_Preclinica'], datos['Id_Consultorio'], datos['Id_Paciente'], datos['Fecha'], datos['Hora'], datos['Sintomas'], datos['Temperatura'], datos['Presion'], datos['Peso']))
        conexion.commit()
        conexion.close()
        return jsonify({"mensaje": "Registro agregado correctamente"})
    return jsonify({"error": "Error de conexión a la base de datos"}), 500

# Actualizar una consulta preclínica existente
@app.route('/preclinica/<int:id_preclinica>', methods=['PUT'])
def actualizar_preclinica(id_preclinica):
    datos = request.json
    conexion = conexionSQLServer()
    if conexion:
        cursor = conexion.cursor()
        consulta = "UPDATE Preclinica SET Id_Consultorio = ?, Id_Paciente = ?, Fecha = ?, Hora = ?, Sintomas = ?, Temperatura = ?, Presion = ?, Peso = ? WHERE Id_Preclinica = ?"
        cursor.execute(consulta, (datos['Id_Consultorio'], datos['Id_Paciente'], datos['Fecha'], datos['Hora'], datos['Sintomas'], datos['Temperatura'], datos['Presion'], datos['Peso'], id_preclinica))
        conexion.commit()
        conexion.close()
        return jsonify({"mensaje": "Registro actualizado correctamente"})
    return jsonify({"error": "Error de conexión a la base de datos"}), 500

# Eliminar una consulta preclínica
@app.route('/preclinica/<int:id_preclinica>', methods=['DELETE'])
def eliminar_preclinica(id_preclinica):
    conexion = conexionSQLServer()
    if conexion:
        cursor = conexion.cursor()
        consulta = "DELETE FROM Preclinica WHERE Id_Preclinica = ?"
        cursor.execute(consulta, (id_preclinica,))
        conexion.commit()
        conexion.close()
        return jsonify({"mensaje": "Registro eliminado correctamente"})
    return jsonify({"error": "Error de conexión a la base de datos"}), 500

if __name__ == '__main__':
    app.run(debug=True)
