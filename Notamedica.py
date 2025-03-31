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

# Obtener todas las notas médicas
@app.route('/notas_medicas', methods=['GET'])
def get_notas_medicas():
    conexion = conexionMySQL()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM NotaMedica")
        notas = cursor.fetchall()
        conexion.close()
        notas_lista = [dict(zip([column[0] for column in cursor.description], row)) for row in notas]
        return jsonify(notas_lista)
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

# Agregar una nota médica
@app.route('/notas_medicas', methods=['POST'])
def add_nota_medica():
    data = request.json
    consulta = "INSERT INTO NotaMedica (ID_Cita, Fecha, Hora, Notas) VALUES (?, ?, ?, ?)"
    parametros = (data['IdCita'], data['Fecha'], data['Hora'], data['Notas'])
    conexion = conexionMySQL()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute(consulta, parametros)
        conexion.commit()
        conexion.close()
        return jsonify({'message': 'Nota médica creada exitosamente'}), 201
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

# Actualizar una nota médica
@app.route('/notas_medicas/<int:id>', methods=['PUT'])
def update_nota_medica(id):
    data = request.json
    consulta = "UPDATE NotaMedica SET ID_Cita = ?, Fecha = ?, Hora = ?, Notas = ? WHERE ID_NotaMedica = ?"
    parametros = (data['IdCita'], data['Fecha'], data['Hora'], data['Notas'], id)
    conexion = conexionMySQL()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute(consulta, parametros)
        conexion.commit()
        conexion.close()
        return jsonify({'message': 'Nota médica actualizada exitosamente'}), 200
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

# Eliminar una nota médica
@app.route('/notas_medicas/<int:id>', methods=['DELETE'])
def delete_nota_medica(id):
    conexion = conexionMySQL()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM NotaMedica WHERE ID_NotaMedica = ?", (id,))
        conexion.commit()
        conexion.close()
        return jsonify({'message': 'Nota médica eliminada exitosamente'}), 200
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

