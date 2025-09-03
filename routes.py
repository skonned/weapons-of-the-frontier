from flask import Flask, render_template
import os


app = Flask(__name__)


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
        name = os.path.splitext(filename)[0].replace('_', ' ').replace('%27', "'")
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
        name = os.path.splitext(filename)[0].replace('_', ' ').replace('%27', "'")
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
        name = os.path.splitext(filename)[0].replace('_', ' ').replace('%27', "'")
        weapons.append((filename, name))
    return render_template('ranged.html', title='RANGED', weapons=weapons)


@app.route('/hybrid')
def hybrid():
    # Path to the hybrid images folder
    hybrid_folder = os.path.join(app.static_folder, 'images', 'hybrid')
    # List all image files in the hybrid folder
    weapon_files = [f for f in os.listdir(hybrid_folder) if f.endswith('.webp')]
    # Create display names from filenames
    weapons = []
    for filename in weapon_files:
        # Remove extension and replace underscores with spaces for display
        name = os.path.splitext(filename)[0].replace('_', ' ').replace('%27', "'")
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
        name = os.path.splitext(filename)[0].replace('_', ' ').replace('%27', "'")
        weapons.append((filename, name))
    return render_template('unique.html', title="UNIQUE", weapons=weapons)


if __name__ == '__main__':
    app.run(debug=True)