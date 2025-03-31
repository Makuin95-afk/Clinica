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

# Obtener todos los consultorios
@app.route('/consultorios', methods=['GET'])
def get_consultorios():
    conexion = conexionMySQL()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Consultorio")
        consultorios = cursor.fetchall()
        conexion.close()
        consultorios_lista = [dict(zip([column[0] for column in cursor.description], row)) for row in consultorios]
        return jsonify(consultorios_lista)
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

# Agregar un consultorio
@app.route('/consultorios', methods=['POST'])
def add_consultorio():
    data = request.json
    consulta = "INSERT INTO Consultorio (ID_Consultorio, Nombre, Ubicacion) VALUES (?, ?, ?)"
    parametros = (data['ID_Consultorio'], data['Nombre'], data['Ubicacion'])
    conexion = conexionMySQL()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute(consulta, parametros)
        conexion.commit()
        conexion.close()
        return jsonify({'message': 'Consultorio agregado exitosamente'}), 201
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

# Actualizar un consultorio
@app.route('/consultorios/<int:id>', methods=['PUT'])
def update_consultorio(id):
    data = request.json
    consulta = "UPDATE Consultorio SET Nombre = ?, Ubicacion = ? WHERE ID_Consultorio = ?"
    parametros = (data['Nombre'], data['Ubicacion'], id)
    conexion = conexionMySQL()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute(consulta, parametros)
        conexion.commit()
        conexion.close()
        return jsonify({'message': 'Consultorio actualizado exitosamente'}), 200
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

# Eliminar un consultorio
@app.route('/consultorios/<int:id>', methods=['DELETE'])
def delete_consultorio(id):
    conexion = conexionMySQL()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Consultorio WHERE ID_Consultorio = ?", (id,))
        conexion.commit()
        conexion.close()
        return jsonify({'message': 'Consultorio eliminado exitosamente'}), 200
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

if __name__ == '__main__':
    app.run(debug=True)
