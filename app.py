from flask import Flask, render_template, request, redirect, url_for
import os
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Syamsundar@1234',
    'database': 'user_data',
}


def get_db():
    return mysql.connector.connect(**db_config)


def close_db(conn):
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM curd_operations')
    users = cursor.fetchall()
    close_db(conn)
    return render_template('index.html', users=users)


@app.route('/add', methods=['POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('INSERT INTO curd_operations (name, mobile) VALUES (%s, %s)', (name, mobile))
        conn.commit()
        close_db(conn)
        return redirect(url_for('index'))


@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'GET':
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM curd_operations WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        close_db(conn)
        return render_template('edit.html', user=user)

    elif request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('UPDATE curd_operations SET name=%s, mobile=%s WHERE id=%s', (name, mobile, user_id))
        conn.commit()
        close_db(conn)
        return redirect(url_for('index'))


@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('DELETE FROM curd_operations WHERE id=%s', (user_id,))
    conn.commit()
    close_db(conn)
    return redirect(url_for('index'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        n = request.form['name']
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM curd_operations WHERE name=%s", (n,))
        res = cursor.fetchall()
        close_db(conn)

        if res:
            return render_template('search.html', res=res)
        else:
            return "User doesn't exist in our database"
    else:
        return render_template('search.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

