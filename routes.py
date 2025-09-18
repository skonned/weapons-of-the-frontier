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
    db = get_db()
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    # Get main weapon data
    cur.execute("SELECT * FROM weapons WHERE name = ?", (display_name,))
    weapon = cur.fetchone()
    if not weapon:
        return render_template('weapon.html', weapon_name=display_name, weapon=None)

    # Get weapon scaling
    cur.execute("SELECT class_name, scaling FROM weapon_scaling WHERE weapon_id = ?", (weapon['weapon_id'],))
    scaling = cur.fetchall()

    # Get special abilities
    cur.execute("SELECT * FROM special_abilities WHERE weapon_id = ?", (weapon['weapon_id'],))
    abilities = cur.fetchall()

    # For each ability, get its scaling
    ability_scalings = {}
    for ability in abilities:
        cur.execute(
            "SELECT class_name, scaling FROM special_ability_scaling WHERE ability_id = ? AND weapon_id = ?",
            (ability['ability_id'], weapon['weapon_id'])
        )
        ability_scalings[ability['ability_id']] = cur.fetchall()

    # Get sources and their locations
    cur.execute("""
        SELECT s.source_id, s.name, ws.price, ws.drop_chance
        FROM sources s
        JOIN weapon_sources ws ON s.source_id = ws.source_id
        WHERE ws.weapon_id = ?
    """, (weapon['weapon_id'],))
    sources = cur.fetchall()

    # For each source, get locations
    source_locations = {}
    for source in sources:
        cur.execute("""
            SELECT l.name
            FROM locations l
            JOIN source_locations sl ON l.location_id = sl.location_id
            WHERE sl.source_id = ?
        """, (source['source_id'],))
        source_locations[source['source_id']] = [row['name'] for row in cur.fetchall()]

    # Pass all data to template
    return render_template(
        'weapon.html',
        weapon_name=display_name,
        weapon=weapon,
        scaling=scaling,
        abilities=abilities,
        ability_scalings=ability_scalings,
        sources=sources,
        source_locations=source_locations
    )


if __name__ == '__main__':
    app.run(debug=True)