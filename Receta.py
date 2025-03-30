from flask import Flask, request, jsonify
import pyodbc

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
    conexion = conexionSQLServer()
    if conexion:
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
    return None

# Rutas CRUD para Receta
@app.route('/recetas', methods=['GET'])
def obtener_recetas():
    consulta = "SELECT * FROM Receta"
    filas = ejecutarSQL(consulta, recibir_datos=True)
    recetas = [{"ID_Receta": fila[0], "ID_Paciente": fila[1], "ID_Medico": fila[2], "Fecha": fila[3]} for fila in filas]
    return jsonify(recetas)

@app.route('/recetas', methods=['POST'])
def crear_receta():
    datos = request.json
    consulta = "INSERT INTO Receta (ID_Receta, ID_Paciente, ID_Medico, Fecha) VALUES (?, ?, ?, ?)"
    parametros = (datos['ID_Receta'], datos['ID_Paciente'], datos['ID_Medico'], datos['Fecha'])
    ejecutarSQL(consulta, parametros)
    return jsonify({"mensaje": "Receta creada exitosamente"})

@app.route('/recetas/<int:id>', methods=['PUT'])
def actualizar_receta(id):
    datos = request.json
    consulta = "UPDATE Receta SET ID_Paciente=?, ID_Medico=?, Fecha=? WHERE ID_Receta=?"
    parametros = (datos['ID_Paciente'], datos['ID_Medico'], datos['Fecha'], id)
    ejecutarSQL(consulta, parametros)
    return jsonify({"mensaje": "Receta actualizada exitosamente"})

@app.route('/recetas/<int:id>', methods=['DELETE'])
def eliminar_receta(id):
    consulta = "DELETE FROM Receta WHERE ID_Receta=?"
    parametros = (id,)
    ejecutarSQL(consulta, parametros)
    return jsonify({"mensaje": "Receta eliminada exitosamente"})

@app.route('/pacientes', methods=['GET'])
def obtener_pacientes():
    consulta = "SELECT ID_Paciente, Nombre, Apellido FROM Paciente"
    filas = ejecutarSQL(consulta, recibir_datos=True)
    pacientes = [{"ID_Paciente": fila[0], "NombreCompleto": f"{fila[1]} {fila[2]}"} for fila in filas]
    return jsonify(pacientes)

@app.route('/medicos', methods=['GET'])
def obtener_medicos():
    consulta = "SELECT ID_Medico, Nombre, Apellido FROM Medico"
    filas = ejecutarSQL(consulta, recibir_datos=True)
    medicos = [{"ID_Medico": fila[0], "NombreCompleto": f"{fila[1]} {fila[2]}"} for fila in filas]
    return jsonify(medicos)

if __name__ == '__main__':
    app.run(debug=True)
