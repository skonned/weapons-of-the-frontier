''' This is the routes file for my weapons website. '''
import sqlite3
from flask import Flask, render_template, g
import os
from urllib.parse import unquote


app = Flask(__name__)


DATABASE = os.path.join(os.path.dirname(__file__), 'weapons.db')


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def home():
    return render_template('home.html', title='HOME')


@app.route('/magic')
def magic():
    # Path to the magic images folder
    magic_folder = os.path.join(app.static_folder, 'images', 'magic')
    # List all image files in the magic folder
    weapon_files = [f for f in os.listdir(magic_folder) if f.endswith('.webp')]
    # Create display names from filenames
    weapons = []
    for filename in weapon_files:
        # Remove extension and replace underscores with spaces for display
        name = (
            os.path.splitext(filename)[0]
            .replace('_', ' ')
            .replace('%27', "'")
        )
        weapons.append((filename, name))
    return render_template('magic.html', title='MAGIC', weapons=weapons)
    

@app.route('/melee')
def melee():
    # Path to the melee images folder
    melee_folder = os.path.join(app.static_folder, 'images', 'melee')
    # List all image files in the melee folder
    weapon_files = [f for f in os.listdir(melee_folder) if f.endswith('.webp')]
    # Create display names from filenames
    weapons = []
    for filename in weapon_files:
        # Remove extension and replace underscores with spaces for display
        name = (
            os.path.splitext(filename)[0]
            .replace('_', ' ')
            .replace('%27', "'")
        )
        weapons.append((filename, name))
    return render_template('melee.html', title='MELEE', weapons=weapons)


@app.route('/ranged')
def ranged():
    # Path to the ranged images folder
    ranged_folder = os.path.join(app.static_folder, 'images', 'ranged')
    # List all image files in the ranged folder
    weapon_files = [f for f in os.listdir(ranged_folder) if f.endswith('.webp')]
    # Create display names from filenames
    weapons = []
    for filename in weapon_files:
        # Remove extension and replace underscores with spaces for display
        name = (
            os.path.splitext(filename)[0]
            .replace('_', ' ')
            .replace('%27', "'")
        )
        weapons.append((filename, name))
    return render_template('ranged.html', title='RANGED', weapons=weapons)


@app.route('/hybrid')
def hybrid():
    # Path to the hybrid images folder
    hybrid_folder = os.path.join(app.static_folder, 'images', 'hybrid')
    # List all image files in the hybrid folder
    weapon_files = [
        f for f in os.listdir(hybrid_folder)
        if f.endswith('.webp')
    ]
    # Create display names from filenames
    weapons = []
    for filename in weapon_files:
        # Remove extension and replace underscores with spaces for display
        name = (
            os.path.splitext(filename)[0]
            .replace('_', ' ')
            .replace('%27', "'")
        )
        weapons.append((filename, name))
    return render_template('hybrid.html', title="HYBRID", weapons=weapons)


@app.route('/unique')
def unique():
    # Path to the unique images folder
    unique_folder = os.path.join(app.static_folder, 'images', 'unique')
    # List all image files in the unique folder
    weapon_files = [f for f in os.listdir(unique_folder) if f.endswith('.webp')]
    # Create display names from filenames
    weapons = []
    for filename in weapon_files:
        # Remove extension and replace underscores with spaces for display
        name = (
            os.path.splitext(filename)[0]
            .replace('_', ' ')
            .replace('%27', "'")
        )
        weapons.append((filename, name))
    return render_template('unique.html', title="UNIQUE", weapons=weapons)


@app.route('/weapon/<weapon_name>')
def weapon(weapon_name):
    display_name = unquote(weapon_name).replace('_', ' ')
    cur = get_db().cursor()
    cur.execute("SELECT * FROM weapons WHERE name = ?", (display_name,))
    row = cur.fetchone()
    if row:
        weapon_data = {
            "name": row[0],
            "image": row[1],
            "type": row[2],
            "description": row[3],
            "damage": row[4]
        }
    else:
        weapon_data = None
    return render_template(
        'weapon.html',
        weapon_name=display_name,
        weapon=weapon_data
    )


if __name__ == '__main__':
    app.run(debug=True)