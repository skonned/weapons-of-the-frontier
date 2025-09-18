"""Flask routes and database access for Weapons of the Frontier."""

import os
import sqlite3
from flask import Flask, render_template, g, request
from flask import abort
from urllib.parse import unquote


# --- Flask App Setup ---
app = Flask(__name__)


# --- Database Path ---
DATABASE = os.path.join(os.path.dirname(__file__), 'weapons.db')


# --- Database Connection Helpers ---
def get_db():
    """Get a database connection for the current request context."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Close the database connection at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# --- Home Page ---
@app.route('/')
def home():
    """Render the home page."""
    return render_template('home.html', title='HOME')


# --- Weapon Category Pages (Magic, Melee, Ranged, Hybrid, Unique) ---
def get_weapons_from_folder(folder_name):
    """
    Function to list weapon images and display names from a static folder.
    Returns a list of (filename, display_name) tuples.
    """
    folder = os.path.join(app.static_folder, 'images', folder_name)
    weapon_files = [f for f in os.listdir(folder) if f.endswith('.webp')]
    weapons = []
    for filename in weapon_files:
        # Remove extension and replace underscores with spaces for display
        name = (
            os.path.splitext(filename)[0]
            .replace('_', ' ')
            .replace('%27', "'")
        )
        weapons.append((filename, name))
    return weapons


@app.route('/magic')
def magic():
    """Render the magic weapons page."""
    weapons = get_weapons_from_folder('magic')
    return render_template('magic.html', title='MAGIC', weapons=weapons)


@app.route('/melee')
def melee():
    """Render the melee weapons page."""
    weapons = get_weapons_from_folder('melee')
    return render_template('melee.html', title='MELEE', weapons=weapons)


@app.route('/ranged')
def ranged():
    """Render the ranged weapons page."""
    weapons = get_weapons_from_folder('ranged')
    return render_template('ranged.html', title='RANGED', weapons=weapons)


@app.route('/hybrid')
def hybrid():
    """Render the hybrid weapons page."""
    weapons = get_weapons_from_folder('hybrid')
    return render_template('hybrid.html', title='HYBRID', weapons=weapons)


@app.route('/unique')
def unique():
    """Render the unique weapons page."""
    weapons = get_weapons_from_folder('unique')
    return render_template('unique.html', title='UNIQUE', weapons=weapons)


# --- Individual Weapon Detail Page ---
@app.route('/weapon/<weapon_name>')
def weapon(weapon_name):
    """
    Render the detail page for a specific weapon, including all related data.
    """
    display_name = unquote(weapon_name).replace('_', ' ')
    db = get_db()
    db.row_factory = sqlite3.Row
    cur = db.cursor()

    # Get main weapon data
    cur.execute("SELECT * FROM weapons WHERE name = ?", (display_name,))
    weapon = cur.fetchone()
    if not weapon:
        abort(404)  # Triggers 404 error if weapon not found

    # Get weapon scaling
    cur.execute(
        "SELECT class_name, scaling FROM weapon_scaling WHERE weapon_id = ?",
        (weapon['weapon_id'],)
    )
    scaling = cur.fetchall()

    # Get special abilities
    cur.execute(
        "SELECT * FROM special_abilities WHERE weapon_id = ?",
        (weapon['weapon_id'],)
    )
    abilities = cur.fetchall()

    # For each ability, get its scaling
    ability_scalings = {}
    for ability in abilities:
        cur.execute(
            (
                "SELECT class_name, scaling "
                "FROM special_ability_scaling "
                "WHERE ability_id = ? AND weapon_id = ?"
            ),
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
        source_locations[source['source_id']] = [
            row['name'] for row in cur.fetchall()
        ]

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


# --- Search Function ---
@app.route('/search', methods=['GET'])
def search():
    """
    Search for weapons by name (case-insensitive, partial match).
    Renders the search results page.
    """
    # Get the search query from the request
    query = (
        (g.get('search_query') or '').strip()
        if hasattr(g, 'search_query') else ''
    )
    if not query:
        query = (request.args.get('q') or '').strip()
    if not query:
        return render_template('search_results.html', query='', results=[])

    db = get_db()
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute("""
        SELECT * FROM weapons
        WHERE name LIKE ?
        ORDER BY name ASC
    """, (f'%{query}%',))
    results = cur.fetchall()
    return render_template('search_results.html', query=query, results=results)


@app.errorhandler(404)
def page_not_found(e):
    """Render a custom 404 error page."""
    return render_template('404.html'), 404


# --- Run the Flask App ---
if __name__ == '__main__':
    app.run(debug=True)
