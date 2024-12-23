from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# 配置数据库连接
config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'demo',
    'raise_on_warnings': True
}

# 连接数据库
def get_db_connection():
    cnx = mysql.connector.connect(**config)
    return cnx



# 显示信息
@app.route('/show')
def show():
    cnx = get_db_connection()
    cursor = cnx.cursor()
    query = """
SELECT
    department,
    occupation,
    COUNT(*) AS numberOfEmployees,
    ROUND(AVG(baseSalary + benefit + bonus - unemploymentInsurance - providentFund),2) AS averageSalary,
    SUM(baseSalary + benefit + bonus - unemploymentInsurance - providentFund) AS totalSalary
FROM
    employees
WHERE
    (department = '经理室' OR occupation = '经理') OR
    (department = '财务科' OR occupation = '会计') OR
    (department = '技术科' OR occupation = '工程师') OR
    (department = '销售科' OR occupation = '销售员')
GROUP BY
    department,
    occupation

UNION ALL

SELECT
    '全部门' AS department,
    '全职业' AS occupation,
    COUNT(*) AS numberOfEmployees,
    ROUND(AVG(baseSalary + benefit + bonus - unemploymentInsurance - providentFund),2) AS averageSalary,
    SUM(baseSalary + benefit + bonus - unemploymentInsurance - providentFund) AS totalSalary
FROM
    employees
WHERE
    (department = '经理室' OR occupation = '经理') OR
    (department = '财务科' OR occupation = '会计') OR
    (department = '技术科' OR occupation = '工程师') OR
    (department = '销售科' OR occupation = '销售员');
    """
    cursor.execute(query)
    employees = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template('show.html', employees=employees)

# 查找所有员工信息
@app.route('/')
def index():
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template('index.html', employees=employees)

# 添加新员工
@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        department = request.form['department']
        occupation = request.form['occupation']
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        baseSalary = request.form['baseSalary']
        benefit = request.form['benefit']
        bonus = request.form['bonus']
        unemploymentInsurance = request.form['unemploymentInsurance']
        providentFund = request.form['providentFund']

        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("INSERT INTO  employees(department, occupation, name, age, gender, baseSalary, benefit, bonus, unemploymentInsurance, providentFund) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (department,occupation,name,age,gender,baseSalary,benefit,bonus,unemploymentInsurance,providentFund))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/search', methods=['POST'])
def search():
    cnx = get_db_connection()
    query = request.form['query']
    # 执行查询
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM employees WHERE id=%s", (query,))
    results = cursor.fetchall()
    
    # 返回结果
    return render_template('test.html', employees=results)

# 删除员工
@app.route('/delete/<id>')
def delete(id):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM employees WHERE id=%s", (id,))
    cnx.commit()
    cursor.close()
    cnx.close()
    return redirect(url_for('index'))

# 更新员工信息
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_employee(id):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    if request.method == 'POST':
        department = request.form['department']
        occupation = request.form['occupation']
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        baseSalary = request.form['baseSalary']
        benefit = request.form['benefit']
        bonus = request.form['bonus']
        unemploymentInsurance = request.form['unemploymentInsurance']
        providentFund = request.form['providentFund']
        cursor.execute("UPDATE employees SET department=%s, occupation=%s, name=%s, age=%s, gender=%s, baseSalary=%s, benefit=%s, bonus=%s, unemploymentInsurance=%s, providentFund=%s WHERE id=%s", (department,occupation,name,age,gender,baseSalary,benefit,bonus,unemploymentInsurance,providentFund,id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect(url_for('index'))
    cursor.execute("SELECT * FROM employees WHERE id=%s", (id,))
    employee = cursor.fetchone()
    cursor.close()
    cnx.close()
    return render_template('edit.html', employee=employee)


if __name__ == '__main__':
    app.run(debug=True)
