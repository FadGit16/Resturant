from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import pymysql

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'  
app.config['MYSQL_DB'] = 'coffee_shop'

mysql = MySQL(app)

# Route to add a menu item
@app.route('/add-menu', methods=['POST'])
def add_menu_item():
    try:
        # Get data from the request
        data = request.json
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        category = data.get('category')

        # Validate input
        if not name or not price:
            return jsonify({'error': 'Name and price are required fields'}), 400

        # Insert into the database
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO menu (name, description, price, category)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (name, description, price, category))
            connection.commit()

        return jsonify({'message': 'Menu item added successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        connection.close()

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
