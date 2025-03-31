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

# Obtener todos los detalles de receta
@app.route('/detallesreceta', methods=['GET'])
def get_detalles_receta():
    conexion = conexionMySQL()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM DetalleReceta")
        detalles = cursor.fetchall()
        conexion.close()
        detalles_lista = [dict(zip([column[0] for column in cursor.description], row)) for row in detalles]
        return jsonify(detalles_lista)
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

# Agregar un detalle de receta
@app.route('/detallesreceta', methods=['POST'])
def add_detalle_receta():
    data = request.json
    consulta = "INSERT INTO DetalleReceta (ID_Receta, ID_Medico, Medicamentos, Indicaciones) VALUES (%s, %s, %s, %s)"
    parametros = (data['ID_Receta'], data['ID_Medico'], data['Medicamentos'], data['Indicaciones'])
    conexion = conexionMySQL()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute(consulta, parametros)
        conexion.commit()
        conexion.close()
        return jsonify({'message': 'Detalle de receta agregado exitosamente'}), 201
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

# Actualizar un detalle de receta
@app.route('/detallesreceta/<int:id>', methods=['PUT'])
def update_detalle_receta(id):
    data = request.json
    consulta = "UPDATE DetalleReceta SET ID_Medico=?, Medicamentos=?, Indicaciones=? WHERE ID_Receta=?"
    parametros = (data['ID_Medico'], data['Medicamentos'], data['Indicaciones'], id)
    conexion = conexionMySQL()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute(consulta, parametros)
        conexion.commit()
        conexion.close()
        return jsonify({'message': 'Detalle de receta actualizado exitosamente'}), 200
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

# Eliminar un detalle de receta
@app.route('/detallesreceta/<int:id>', methods=['DELETE'])
def delete_detalle_receta(id):
    conexion = conexionMySQL()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM DetalleReceta WHERE ID_Receta = ?", (id,))
        conexion.commit()
        conexion.close()
        return jsonify({'message': 'Detalle de receta eliminado exitosamente'}), 200
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

