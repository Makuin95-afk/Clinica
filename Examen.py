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

def ejecutarSQL(consulta, parametros=None, recibir_datos=False):
    conexion = conexionMySQL()
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

@app.route('/examenes', methods=['GET'])
def obtener_examenes():
    consulta = "SELECT * FROM Examenes"
    filas = ejecutarSQL(consulta, recibir_datos=True)
    examenes = [
        {"ID_Examen": fila[0], "ID_Paciente": fila[1], "ID_Area": fila[2], "ID_Tipo_Examen": fila[3], "Fecha": fila[4], "Hora": fila[5], "Resultados": fila[6]} 
        for fila in filas
    ]
    return jsonify(examenes)

@app.route('/examenes', methods=['POST'])
def crear_examen():
    datos = request.json
    consulta = "INSERT INTO Examenes (ID_Examen, ID_Paciente, ID_Area, ID_Consultorio, Fecha, Hora, Resultados) VALUES (?, ?, ?, ?, ?, ?, ?)"
    parametros = (datos['ID_Examen'], datos['ID_Paciente'], datos['ID_Area'], datos['ID_Tipo_Examen'], datos['Fecha'], datos['Hora'], datos['Resultados'])
    ejecutarSQL(consulta, parametros)
    return jsonify({'mensaje': 'Examen creado exitosamente'}), 201

@app.route('/examenes/<int:id_examen>', methods=['PUT'])
def actualizar_examen(id_examen):
    datos = request.json
    consulta = "UPDATE Examenes SET ID_Paciente=?, ID_Area=?, ID_Consultorio=?, Fecha=?, Hora=?, Resultados=? WHERE ID_Examen=?"
    parametros = (datos['ID_Paciente'], datos['ID_Area'], datos['ID_Tipo_Examen'], datos['Fecha'], datos['Hora'], datos['Resultados'], id_examen)
    ejecutarSQL(consulta, parametros)
    return jsonify({'mensaje': 'Examen actualizado exitosamente'})

@app.route('/examenes/<int:id_examen>', methods=['DELETE'])
def borrar_examen(id_examen):
    consulta = "DELETE FROM Examenes WHERE ID_Examen=?"
    ejecutarSQL(consulta, (id_examen,))
    return jsonify({'mensaje': 'Examen eliminado exitosamente'})

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=5000)

