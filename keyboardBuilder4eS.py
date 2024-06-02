import os
import unicodedata
from flask import Flask, request, jsonify, session, render_template
from src import unicode_categories as uc

app = Flask(__name__)
app.secret_key = os.urandom(24)

def get_unicode_characters(start, limit):
    return [chr(i) for i in range(start, start + limit)]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/live_search_unicode_name', methods=['POST'])
def live_search_unicode_name():
    data = request.json
    partial_name = data.get('partial_name').lower()
    matching_names = []

    for codepoint in range(0x110000):  # Unicode range limit
        if len(matching_names) >= 100:  # Limit to 100 results
            break
        try:
            name = unicodedata.name(chr(codepoint)).lower()
            if partial_name in name:
                char = chr(codepoint)
                matching_names.append({"name": name, "character": char})
        except ValueError:
            continue

    return jsonify(matching_names)

@app.route('/get_unicode_characters', methods=['GET'])
def get_unicode_characters_endpoint():
    start = int(request.args.get('start', 0))
    limit = int(request.args.get('limit', 40))
    category = request.args.get('category', None)
    unicode_chars = []

    if category and category in uc.unicode_category_ranges:
        category_range = uc.unicode_category_ranges[category]
        codepoint = category_range[0] + start
        end_codepoint = category_range[1]
        while len(unicode_chars) < limit and codepoint <= end_codepoint:
            try:
                char = chr(codepoint)
                name = unicodedata.name(char)
                unicode_chars.append({"character": char, "name": name})
            except ValueError:
                pass
            codepoint += 1
    else:
        codepoint = start
        while len(unicode_chars) < limit and codepoint < 0x110000:  # Unicode range limit
            try:
                char = chr(codepoint)
                name = unicodedata.name(char)
                unicode_chars.append({"character": char, "name": name})
            except ValueError:
                pass
            codepoint += 1

    return jsonify(unicode_chars)

@app.route('/get_unicode_categories', methods=['GET'])
def get_unicode_categories():
    categories = list(uc.unicode_category_ranges.keys())
    return jsonify(categories)

@app.route('/add_character', methods=['POST'])
def add_character():
    data = request.json
    character = data.get('character')
    name = unicodedata.name(character)
    row = data.get('row')
    column = data.get('column')

    if 'custom_characters' not in session:
        session['custom_characters'] = []

    session['custom_characters'].append({
        'character': character,
        'row': row,
        'column': column,
        'name': name
    })

    session.modified = True  # Ensure session changes are saved
    return jsonify(session['custom_characters'])

@app.route('/remove_character', methods=['POST'])
def remove_character():
    data = request.json
    character = data.get('character')

    # Get the current custom characters from the session
    custom_characters = session.get('custom_characters', [])

    # Filter out the character to be removed
    updated_characters = [
        char_obj for char_obj in custom_characters
        if char_obj["character"] != character
    ]

    session['custom_characters'] = updated_characters
    session.modified = True  # Ensure session changes are saved

    return jsonify({"message": "Character removed successfully!"})

@app.route('/get_characters', methods=['GET'])
def get_characters():
    custom_characters = session.get('custom_characters', [])
    return jsonify({'characters': custom_characters})

@app.route('/clear_characters', methods=['POST'])
def clear_characters():
    session.pop('custom_characters', None)
    return jsonify({"status": "cleared"})

@app.route('/match_character', methods=['POST'])
def match_character():
    data = request.json
    characters = data.get('characters')

    if not characters:
        return jsonify({"message": "No characters provided!"}), 400

    valid_characters = []
    for char in characters:
        try:
            if char.isprintable() and char not in valid_characters:  # Check if the character is a valid Unicode character
                valid_characters.append(char)
        except:
            continue

    if 'custom_characters' not in session:
        session['custom_characters'] = []

    custom_characters = session['custom_characters']

    # Add the new characters to the session
    for char in valid_characters:
        custom_characters.append({
            'character': char,
            'row': 0,
            'column': 0,
            'name': unicodedata.name(char)
        })

    row_limit = session.get('row_limit', 10)

    # Recalculate rows and columns
    for i, char_obj in enumerate(custom_characters):
        char_obj['row'] = i // row_limit
        char_obj['column'] = i % row_limit

    session['custom_characters'] = custom_characters
    session.modified = True

    return jsonify({"message": "Characters matched and added successfully!", "valid_characters": valid_characters})

@app.route('/update_custom_order', methods=['POST'])
def update_custom_order():
    data = request.json
    new_order = data.get('order', [])

    custom_characters = session.get('custom_characters', [])
    character_dict = {char['character']: char for char in custom_characters}

    row_limit = session.get('row_limit', 10)  # Get the current row limit from the session
    updated_characters = []

    for i, char in enumerate(new_order):
        if char in character_dict:
            char_obj = character_dict[char]
            char_obj['row'] = i // row_limit
            char_obj['column'] = i % row_limit
            updated_characters.append(char_obj)

    session['custom_characters'] = updated_characters
    session.modified = True

    return jsonify({"status": "success"})

@app.route('/update_row_limit', methods=['POST'])
def update_row_limit():
    data = request.json
    row_limit = data.get('row_limit')
    session['row_limit'] = row_limit

    # Recalculate row and column values for existing characters
    custom_characters = session.get('custom_characters', [])
    for i, char_obj in enumerate(custom_characters):
        char_obj['row'] = i // row_limit
        char_obj['column'] = i % row_limit
        
    session['custom_characters'] = custom_characters
    session.modified = True
    
    return jsonify({"status": "success", "row_limit": row_limit})

@app.route('/recalculate_rows_columns', methods=['POST'])
def recalculate_rows_columns():
    custom_characters = session.get('custom_characters', [])
    row_limit = session.get('row_limit', 10)

    # Recalculate rows and columns
    for i, char_obj in enumerate(custom_characters):
        char_obj['row'] = i // row_limit
        char_obj['column'] = i % row_limit

    session['custom_characters'] = custom_characters
    session.modified = True

    return jsonify({"status": "success"})

@app.route('/download_characters', methods=['POST'])
def download_characters():
    data = request.json
    keyboard_name = data.get('keyboard_name', 'my_keyboard')  # Get the keyboard name from the request
    custom_characters = session.get('custom_characters', [])
    
    response = {
        "version": "0.1",
        "author": "Virtual Keyboard Builder for eScriptorium v0.1",
        "name": keyboard_name,  # Include the keyboard name in the response
        "characters": 
            [
                {
                    "character": char['character'],
                    "row": char['row'],
                    "column": char['column']
                }
                for char in custom_characters
            ]
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
    