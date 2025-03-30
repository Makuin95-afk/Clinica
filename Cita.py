from flask import Flask, request, jsonify
import datetime

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

# Función para ejecutar SQL
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

# Función para validar y convertir la hora
def validar_y_convertir_hora(hora_str):
    formatos_validos = ["%H:%M:%S", "%H:%M"]  # Consideramos también el formato sin segundos
    for formato in formatos_validos:
        try:
            hora_valida = datetime.datetime.strptime(hora_str, formato).time()
            return hora_valida.strftime("%H:%M:%S")  # Retorna la hora en formato HH:MM:SS
        except ValueError:
            continue
    raise ValueError("Formato de hora inválido. Debe ser HH:MM o HH:MM:SS")

# Endpoints de la API RESTful

# Crear cita
@app.route('/citas', methods=['POST'])
def crear_cita():
    try:
        data = request.get_json()
        id_cita = int(data['ID_Cita'])
        id_paciente = int(data['ID_Paciente'])
        id_medico = int(data['ID_Medico'])
        id_consultorio = int(data['ID_Consultorio'])
        fecha = data['Fecha']
        hora = validar_y_convertir_hora(data['Hora'])
        estado = data['Estado']

        parametros = (id_cita, id_paciente, id_medico, id_consultorio, fecha, hora, estado)
        consulta = "INSERT INTO Cita (ID_Cita, ID_Paciente, ID_Medico, ID_Consultorio, Fecha, Hora, Estado) VALUES (?, ?, ?, ?, ?, ?, ?)"
        ejecutarSQL(consulta, parametros)
        return jsonify({"mensaje": "Registro de cita creado con éxito"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Obtener todas las citas
@app.route('/citas', methods=['GET'])
def obtener_citas():
    try:
        consulta = "SELECT * FROM Cita"
        filas = ejecutarSQL(consulta, recibir_datos=True)
        citas = []
        for fila in filas:
            citas.append({
                "ID_Cita": fila[0],
                "ID_Paciente": fila[1],
                "ID_Medico": fila[2],
                "ID_Consultorio": fila[3],
                "Fecha": fila[4],
                "Hora": fila[5],
                "Estado": fila[6]
            })
        return jsonify(citas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Actualizar cita
@app.route('/citas/<int:id_cita>', methods=['PUT'])
def actualizar_cita(id_cita):
    try:
        data = request.get_json()
        parametros = (
            data['ID_Paciente'], data['ID_Medico'], data['ID_Consultorio'],
            data['Fecha'], data['Hora'], data['Estado'], id_cita
        )
        consulta = "UPDATE Cita SET ID_Paciente=?, ID_Medico=?, ID_Consultorio=?, Fecha=?, Hora=?, Estado=? WHERE ID_Cita=?"
        ejecutarSQL(consulta, parametros)
        return jsonify({"mensaje": "Cita actualizada con éxito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Eliminar cita
@app.route('/citas/<int:id_cita>', methods=['DELETE'])
def eliminar_cita(id_cita):
    try:
        parametros = (id_cita,)
        consulta = "DELETE FROM Cita WHERE ID_Cita=?"
        ejecutarSQL(consulta, parametros)
        return jsonify({"mensaje": "Cita eliminada con éxito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Obtener citas por año
@app.route('/citas/anio/<int:anio>', methods=['GET'])
def obtener_citas_por_anio(anio):
    try:
        consulta = "SELECT * FROM Cita WHERE SUBSTRING(Fecha, 1, 4) = ?"
        filas = ejecutarSQL(consulta, parametros=(str(anio),), recibir_datos=True)
        citas = []
        for fila in filas:
            citas.append({
                "ID_Cita": fila[0],
                "ID_Paciente": fila[1],
                "ID_Medico": fila[2],
                "ID_Consultorio": fila[3],
                "Fecha": fila[4],
                "Hora": fila[5],
                "Estado": fila[6]
            })
        return jsonify(citas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Iniciar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)
