from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Подключение к базе данных
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Реализация функций
def get_avaliable_constructions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM constructions')
    constructions = cursor.fetchall()
    conn.close()
    return constructions

def get_avaliable_materials(construction_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM materials WHERE construction_id = ?', (construction_id,))
    materials = cursor.fetchall()
    conn.close()
    return materials

def get_avaliable_defects(construction_id, material_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, name FROM defects WHERE construction_id = ? AND material_id = ?', 
        (construction_id, material_id)
    )
    defects = cursor.fetchall()
    conn.close()
    return defects

def get_parameters(defect_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT options_JSON FROM parameters WHERE defect_id = ?', (defect_id,))
    parameters = cursor.fetchone()
    conn.close()
    return parameters

# Роуты API
@app.route('/api', methods=['POST'])
def api():
    try:
        print(request.json)
        data = request.json
        action_type = data.get('action_type')
        print(action_type)
        query = data.get('query')

        if action_type == 'request_objects':
            constructions = get_avaliable_constructions()
            return jsonify({"objects": [dict(row) for row in constructions]})

        elif action_type == 'request_materials':
            materials = get_avaliable_materials(query)
            return jsonify({"materials": [dict(row) for row in materials]})

        elif action_type == 'request_defects':
            construction_id, material_id = query
            defects = get_avaliable_defects(construction_id, material_id)
            return jsonify({"defects": [dict(row) for row in defects]})

        elif action_type == 'request_parameters':
            parameters = get_parameters(query)
            return jsonify({"parameters": parameters["options_JSON"] if parameters else None})

        else:
            return jsonify({"error": "Invalid action_type"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True)

