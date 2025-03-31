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

# Obtener todos los empleados
@app.route('/empleados', methods=['GET'])
def get_empleados():
    conexion = conexionMySQL()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Empleado")
        empleados = cursor.fetchall()
        conexion.close()
        empleados_lista = [dict(zip([column[0] for column in cursor.description], row)) for row in empleados]
        return jsonify(empleados_lista)
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

# Agregar un empleado
@app.route('/empleados', methods=['POST'])
def add_employee():
    data = request.json
    emp_data = (
        data['EmpId'], data['EmpNom'], data['EmpApe'],
        data['EmpDNI'], data['EmpDir'], data['EmpTel'],
        data['EmpEmail'], data['EmpIDPuesto']
    )
    consulta = "INSERT INTO Empleado (ID_Empleado, Nombre, Apellido, DNI, Direccion, Telefono, Email, ID_Puesto) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    conexion = conexionMySQL()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute(consulta, emp_data)
        conexion.commit()
        conexion.close()
        return jsonify({'message': 'Empleado agregado exitosamente'}), 201
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

# Actualizar un empleado
@app.route('/empleados/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.json
    consulta = "UPDATE Empleado SET Nombre = ?, Apellido = ?, DNI = ?, Direccion = ?, Telefono = ?, Email = ?, ID_Puesto = ? WHERE ID_Empleado = ?"
    emp_data = (
        data['EmpNom'], data['EmpApe'], data['EmpDNI'],
        data['EmpDir'], data['EmpTel'], data['EmpEmail'],
        data['EmpIDPuesto'], id
    )
    conexion = conexionMySQL()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute(consulta, emp_data)
        conexion.commit()
        conexion.close()
        return jsonify({'message': 'Empleado actualizado exitosamente'}), 200
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

# Eliminar un empleado
@app.route('/empleados/<int:id>', methods=['DELETE'])
def delete_employee(id):
    conexion = conexionMySQL()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Empleado WHERE ID_Empleado = ?", (id,))
        conexion.commit()
        conexion.close()
        return jsonify({'message': 'Empleado eliminado exitosamente'}), 200
    return jsonify({'error': 'Error de conexión a la base de datos'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

