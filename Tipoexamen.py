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
                return True
    return False

@app.route('/tipo_examen', methods=['POST'])
def crear_tipo_examen():
    datos = request.json
    consulta = "INSERT INTO TipoExamen (ID_Tipo_Examen, Descripcion) VALUES (?, ?)"
    parametros = (datos['ID_Tipo_Examen'], datos['Descripcion'])
    if ejecutarSQL(consulta, parametros):
        return jsonify({'mensaje': 'Tipo de examen creado exitosamente'}), 201
    return jsonify({'error': 'No se pudo crear el tipo de examen'}), 500

@app.route('/tipo_examen', methods=['GET'])
def obtener_tipos_examen():
    consulta = "SELECT * FROM TipoExamen"
    filas = ejecutarSQL(consulta, recibir_datos=True)
    resultados = [{'ID_Tipo_Examen': fila[0], 'Descripcion': fila[1]} for fila in filas]
    return jsonify(resultados)

@app.route('/tipo_examen/<int:id>', methods=['PUT'])
def actualizar_tipo_examen(id):
    datos = request.json
    consulta = "UPDATE TipoExamen SET Descripcion = ? WHERE ID_Tipo_Examen = ?;"
    parametros = (datos['Descripcion'], id)
    if ejecutarSQL(consulta, parametros):
        return jsonify({'mensaje': 'Tipo de examen actualizado correctamente'})
    return jsonify({'error': 'No se pudo actualizar el tipo de examen'}), 500

@app.route('/tipo_examen/<int:id>', methods=['DELETE'])
def eliminar_tipo_examen(id):
    consulta = "DELETE FROM TipoExamen WHERE ID_Tipo_Examen = ?"
    parametros = (id,)
    if ejecutarSQL(consulta, parametros):
        return jsonify({'mensaje': 'Tipo de examen eliminado correctamente'})
    return jsonify({'error': 'No se pudo eliminar el tipo de examen'}), 500

if __name__ == '__main__':
    app.run(debug=True)
