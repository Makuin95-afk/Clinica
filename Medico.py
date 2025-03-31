from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Conexión a Mysql
def conexionMySQL():
    try:
        conexion = mysql.connector.connect(
            host='localhost',  # Cambia esto si tu base de datos no está en localhost
            user='root',  # Usuario de MySQL
            password='Ujcv2025@',  # Contraseña de MySQL
            database='ClinicaHospitalariaH'  # Nombre de la base de datos
        )
        return conexion
    except mysql.connector.Error as e:
        return None

# Obtener todos los médicos
@app.route('/medicos', methods=['GET'])
def get_medicos():
    conexion = conexionMySQL()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Medico")
        medicos = cursor.fetchall()
        conexion.close()
        medicos_lista = [dict(zip([column[0] for column in cursor.description], row)) for row in medicos]
        return jsonify(medicos_lista)
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

# Agregar un médico
@app.route('/medicos', methods=['POST'])
def add_medico():
    data = request.json
    medico_data = (
        data['MedId'], data['MedNom'], data['MedApe'],
        data['MedIDEspecialidad'], data['MedTel'], data['MedEmail'],
        data['MedDir'], data['MedNumLic']
    )
    consulta = "INSERT INTO Medico (ID_Medico, Nombre, Apellido, ID_Especialidad, Telefono, Email, Direccion, Numero_Licencia) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    conexion = conexionMySQL()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute(consulta, medico_data)
        conexion.commit()
        conexion.close()
        return jsonify({'message': 'Médico agregado exitosamente'}), 201
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

# Actualizar un médico
@app.route('/medicos/<int:id>', methods=['PUT'])
def update_medico(id):
    data = request.json
    consulta = "UPDATE Medico SET Nombre = ?, Apellido = ?, ID_Especialidad = ?, Telefono = ?, Email = ?, Direccion = ?, Numero_Licencia = ? WHERE ID_Medico = ?"
    medico_data = (
        data['MedNom'], data['MedApe'], data['MedIDEspecialidad'],
        data['MedTel'], data['MedEmail'], data['MedDir'],
        data['MedNumLic'], id
    )
    conexion = conexionMySQL()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute(consulta, medico_data)
        conexion.commit()
        conexion.close()
        return jsonify({'message': 'Médico actualizado exitosamente'}), 200
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

# Eliminar un médico
@app.route('/medicos/<int:id>', methods=['DELETE'])
def delete_medico(id):
    conexion = conexionMySQL()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Medico WHERE ID_Medico = ?", (id,))
        conexion.commit()
        conexion.close()
        return jsonify({'message': 'Médico eliminado exitosamente'}), 200
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

