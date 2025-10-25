from flask import Flask, render_template,request
import math

app = Flask(__name__)

@app.route('/index')
def index():
    titulo = "pagina de inicio"
    listado = ['Python','Flask', 'Jinjan2', 'HTML','CSS']
    return render_template ('index.html',titulo = titulo, listado = listado) 



@app.route('/calculos',methods=['GET','POST'])
def about2():
    if request.method == 'POST':
        numero1 = request.form['numero1']
        numero2 = request.form['numero2']
        opcin = request.form['operacion']
        if opcin == 'suma':
            res = int(numero1) + int(numero2)
        if opcin == 'resta':
            res = int(numero1) - int(numero2)
        if opcin == 'multiplicacion':
            res = int(numero1) * int(numero2)
        elif opcin == 'division':
            res = int(numero1) / int(numero2)
            
        return render_template('calculos.html', res=res,
                                numero1=numero1, numero2=numero2)
    return render_template('calculos.html')

@app.route('/distancia',methods=['GET','POST'])
def about3():
    if request.method == 'POST':
        numero1 = float (request.form['numero1']) 
        numero2 = float (request.form['numero2'])
        numero3 = float (request.form['numero3'])
        numero4 = float (request.form['numero4'])

        res = math.sqrt(math.pow((numero3 - numero1), 2) + math.pow((numero4 - numero2), 2))

        return render_template('distancia.html', res=res,
                                numero1=numero1, numero2=numero2, numero3=numero3, numero4=numero4)
    return render_template('distancia.html')


@app.route('/calculos')
def about0():
    return render_template('calculos.html')

@app.route('/distancia')
def about1():
    return render_template('distancia.html')

@app.route('/Holi')
def about():
    return "Hola otra vez "

@app.route('/user/<string:user>')
def user(user):
    return f"Holi, {user} !"

@app.route('/numero/<int:num>')
def func(num):
    return f"El numero es:  {user} !"

@app.route('/suma/<int:num1>/<int:num2>')
def suma(num1, num2):
    return f"La suma es:  {num1 + num2} !"

@app.route('/user/<int:id>/<string:username>')
def username(id,username):
    return "ID: {} nombre:  {} ".format(id,username)

@app.route('/suma/<float:n1>/<float:n2>')
def func1(n1, n2):
    return "La suma es:  {}!".format(n1+n2)

@app.route("/default/")
@app.route("/default/<string:dft>")
def func2(dft = "sss"):
    return "el valor de dft es: " + dft

@app.route("/prueba")
def func4():
    return '''

<html>
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
<title>Holis </title>
</head>
<body>
</body>
<p>es una prueba</p>
</html>

'''

if __name__ == '__main__':
    app.run(debug=True)
    