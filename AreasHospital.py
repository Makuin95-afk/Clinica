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

# Obtener todos los registros de área hospitalaria
@app.route('/areas', methods=['GET'])
def get_areas():
    conexion = conexionSQLServer()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM AreaHospital")
        areas = cursor.fetchall()
        conexion.close()
        areas_lista = [dict(zip([column[0] for column in cursor.description], row)) for row in areas]
        return jsonify(areas_lista)
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

# Agregar un nuevo registro de área hospitalaria
@app.route('/areas', methods=['POST'])
def add_area():
    data = request.json
    area_data = (
        data['IdArea'], data['IdConsultorio'],
        data['NombreArea'], data['Descripcion']
    )
    consulta = "INSERT INTO AreaHospital (ID_Area, ID_Consultorio, Nombre_Area, Descripcion) VALUES (?, ?, ?, ?)"
    conexion = conexionSQLServer()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute(consulta, area_data)
        conexion.commit()
        conexion.close()
        return jsonify({'message': 'Área hospitalaria agregada exitosamente'}), 201
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

# Actualizar un registro de área hospitalaria
@app.route('/areas/<int:id>', methods=['PUT'])
def update_area(id):
    data = request.json
    consulta = "UPDATE AreaHospital SET ID_Consultorio = ?, Nombre_Area = ?, Descripcion = ? WHERE ID_Area = ?"
    area_data = (
        data['IdConsultorio'], data['NombreArea'], data['Descripcion'], id
    )
    conexion = conexionSQLServer()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute(consulta, area_data)
        conexion.commit()
        conexion.close()
        return jsonify({'message': 'Área hospitalaria actualizada exitosamente'}), 200
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

# Eliminar un registro de área hospitalaria
@app.route('/areas/<int:id>', methods=['DELETE'])
def delete_area(id):
    conexion = conexionSQLServer()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM AreaHospital WHERE ID_Area = ?", (id,))
        conexion.commit()
        conexion.close()
        return jsonify({'message': 'Área hospitalaria eliminada exitosamente'}), 200
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

if __name__ == '__main__':
    app.run(debug=True)
