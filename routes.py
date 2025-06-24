from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html', title='HOME')


@app.route('/magic')
def magic():
    return render_template('magic.html', title='MAGIC')
    

@app.route('/melee')
def melee():
    return render_template('melee.html', title='MELEE')


@app.route('/ranged')
def ranged():
    return render_template('ranged.html', title='RANGED')


if __name__ == '__main__':
    app.run(debug=True)