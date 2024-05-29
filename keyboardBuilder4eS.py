import unicodedata
import os
from flask import Flask, request, jsonify, session, render_template


app = Flask(__name__)
app.secret_key = os.urandom(24)

unicode_category_ranges = {
    "Basic Latin": (0x0000, 0x007F),
    "Latin-1 Supplement": (0x0080, 0x00FF),
    "Latin Extended-A": (0x0100, 0x017F),
    "Latin Extended-B": (0x0180, 0x024F),
    "IPA Extensions": (0x0250, 0x02AF),
    "Spacing Modifier Letters": (0x02B0, 0x02FF),
    "Combining Diacritical Marks": (0x0300, 0x036F),
    "Greek and Coptic": (0x0370, 0x03FF),
    "Cyrillic": (0x0400, 0x04FF),
    "Cyrillic Supplement": (0x0500, 0x052F),
    "Armenian": (0x0530, 0x058F),
    "Hebrew": (0x0590, 0x05FF),
    "Arabic": (0x0600, 0x06FF),
    "Syriac": (0x0700, 0x074F),
    "Arabic Supplement": (0x0750, 0x077F),
    "Thaana": (0x0780, 0x07BF),
    "NKo": (0x07C0, 0x07FF),
    "Samaritan": (0x0800, 0x083F),
    "Mandaic": (0x0840, 0x085F),
    "Syriac Supplement": (0x0860, 0x086F),
    "Arabic Extended-A": (0x08A0, 0x08FF),
    "Devanagari": (0x0900, 0x097F),
    "Bengali": (0x0980, 0x09FF),
    "Gurmukhi": (0x0A00, 0x0A7F),
    "Gujarati": (0x0A80, 0x0AFF),
    "Oriya": (0x0B00, 0x0B7F),
    "Tamil": (0x0B80, 0x0BFF),
    "Telugu": (0x0C00, 0x0C7F),
    "Kannada": (0x0C80, 0x0CFF),
    "Malayalam": (0x0D00, 0x0D7F),
    "Sinhala": (0x0D80, 0x0DFF),
    "Thai": (0x0E00, 0x0E7F),
    "Lao": (0x0E80, 0x0EFF),
    "Tibetan": (0x0F00, 0x0FFF),
    "Myanmar": (0x1000, 0x109F),
    "Georgian": (0x10A0, 0x10FF),
    "Hangul Jamo": (0x1100, 0x11FF),
    "Ethiopic": (0x1200, 0x137F),
    "Ethiopic Supplement": (0x1380, 0x139F),
    "Cherokee": (0x13A0, 0x13FF),
    "Unified Canadian Aboriginal Syllabics": (0x1400, 0x167F),
    "Ogham": (0x1680, 0x169F),
    "Runic": (0x16A0, 0x16FF),
    "Tagalog": (0x1700, 0x171F),
    "Hanunoo": (0x1720, 0x173F),
    "Buhid": (0x1740, 0x175F),
    "Tagbanwa": (0x1760, 0x177F),
    "Khmer": (0x1780, 0x17FF),
    "Mongolian": (0x1800, 0x18AF),
    "Unified Canadian Aboriginal Syllabics Extended": (0x18B0, 0x18FF),
    "Limbu": (0x1900, 0x194F),
    "Tai Le": (0x1950, 0x197F),
    "New Tai Lue": (0x1980, 0x19DF),
    "Khmer Symbols": (0x19E0, 0x19FF),
    "Buginese": (0x1A00, 0x1A1F),
    "Tai Tham": (0x1A20, 0x1AAF),
    "Combining Diacritical Marks Extended": (0x1AB0, 0x1AFF),
    "Balinese": (0x1B00, 0x1B7F),
    "Sundanese": (0x1B80, 0x1BBF),
    "Batak": (0x1BC0, 0x1BFF),
    "Lepcha": (0x1C00, 0x1C4F),
    "Ol Chiki": (0x1C50, 0x1C7F),
    "Cyrillic Extended-C": (0x1C80, 0x1C8F),
    "Georgian Extended": (0x1C90, 0x1CBF),
    "Sundanese Supplement": (0x1CC0, 0x1CCF),
    "Vedic Extensions": (0x1CD0, 0x1CFF),
    "Phonetic Extensions": (0x1D00, 0x1D7F),
    "Phonetic Extensions Supplement": (0x1D80, 0x1DBF),
    "Combining Diacritical Marks Supplement": (0x1DC0, 0x1DFF),
    "Latin Extended Additional": (0x1E00, 0x1EFF),
    "Greek Extended": (0x1F00, 0x1FFF),
    "General Punctuation": (0x2000, 0x206F),
    "Superscripts and Subscripts": (0x2070, 0x209F),
    "Currency Symbols": (0x20A0, 0x20CF),
    "Combining Diacritical Marks for Symbols": (0x20D0, 0x20FF),
    "Letterlike Symbols": (0x2100, 0x214F),
    "Number Forms": (0x2150, 0x218F),
    "Arrows": (0x2190, 0x21FF),
    "Mathematical Operators": (0x2200, 0x22FF),
    "Miscellaneous Technical": (0x2300, 0x23FF),
    "Control Pictures": (0x2400, 0x243F),
    "Optical Character Recognition": (0x2440, 0x245F),
    "Enclosed Alphanumerics": (0x2460, 0x24FF),
    "Box Drawing": (0x2500, 0x257F),
    "Block Elements": (0x2580, 0x259F),
    "Geometric Shapes": (0x25A0, 0x25FF),
    "Miscellaneous Symbols": (0x2600, 0x26FF),
    "Dingbats": (0x2700, 0x27BF),
    "Miscellaneous Mathematical Symbols-A": (0x27C0, 0x27EF),
    "Supplemental Arrows-A": (0x27F0, 0x27FF),
    "Braille Patterns": (0x2800, 0x28FF),
    "Supplemental Arrows-B": (0x2900, 0x297F),
    "Miscellaneous Mathematical Symbols-B": (0x2980, 0x29FF),
    "Supplemental Mathematical Operators": (0x2A00, 0x2AFF),
    "Miscellaneous Symbols and Arrows": (0x2B00, 0x2BFF),
    "Glagolitic": (0x2C00, 0x2C5F),
    "Latin Extended-C": (0x2C60, 0x2C7F),
    "Coptic": (0x2C80, 0x2CFF),
    "Georgian Supplement": (0x2D00, 0x2D2F),
    "Tifinagh": (0x2D30, 0x2D7F),
    "Ethiopic Extended": (0x2D80, 0x2DDF),
    "Cyrillic Extended-A": (0x2DE0, 0x2DFF),
    "Supplemental Punctuation": (0x2E00, 0x2E7F),
    "CJK Radicals Supplement": (0x2E80, 0x2EFF),
    "Kangxi Radicals": (0x2F00, 0x2FDF),
    "Ideographic Description Characters": (0x2FF0, 0x2FFF),
    "CJK Symbols and Punctuation": (0x3000, 0x303F),
    "Hiragana": (0x3040, 0x309F),
    "Katakana": (0x30A0, 0x30FF),
    "Bopomofo": (0x3100, 0x312F),
    "Hangul Compatibility Jamo": (0x3130, 0x318F),
    "Kanbun": (0x3190, 0x319F),
    "Bopomofo Extended": (0x31A0, 0x31BF),
    "CJK Strokes": (0x31C0, 0x31EF),
    "Katakana Phonetic Extensions": (0x31F0, 0x31FF),
    "Enclosed CJK Letters and Months": (0x3200, 0x32FF),
    "CJK Compatibility": (0x3300, 0x33FF),
    "CJK Unified Ideographs Extension A": (0x3400, 0x4DBF),
    "Yijing Hexagram Symbols": (0x4DC0, 0x4DFF),
    "CJK Unified Ideographs": (0x4E00, 0x9FFF),
    "Yi Syllables": (0xA000, 0xA48F),
    "Yi Radicals": (0xA490, 0xA4CF),
    "Lisu": (0xA4D0, 0xA4FF),
    "Vai": (0xA500, 0xA63F),
    "Cyrillic Extended-B": (0xA640, 0xA69F),
    "Bamum": (0xA6A0, 0xA6FF),
    "Modifier Tone Letters": (0xA700, 0xA71F),
    "Latin Extended-D": (0xA720, 0xA7FF),
    "Syloti Nagri": (0xA800, 0xA82F),
    "Common Indic Number Forms": (0xA830, 0xA83F),
    "Phags-pa": (0xA840, 0xA87F),
    "Saurashtra": (0xA880, 0xA8DF),
    "Devanagari Extended": (0xA8E0, 0xA8FF),
    "Kayah Li": (0xA900, 0xA92F),
    "Rejang": (0xA930, 0xA95F),
    "Hangul Jamo Extended-A": (0xA960, 0xA97F),
    "Javanese": (0xA980, 0xA9DF),
    "Myanmar Extended-B": (0xA9E0, 0xA9FF),
    "Cham": (0xAA00, 0xAA5F),
    "Myanmar Extended-A": (0xAA60, 0xAA7F),
    "Tai Viet": (0xAA80, 0xAADF),
    "Meetei Mayek Extensions": (0xAAE0, 0xAAFF),
    "Ethiopic Extended-A": (0xAB00, 0xAB2F),
    "Meetei Mayek": (0xABC0, 0xABFF),
    "Hangul Syllables": (0xAC00, 0xD7AF),
    "Hangul Jamo Extended-B": (0xD7B0, 0xD7FF),
    "High Surrogates": (0xD800, 0xDB7F),
    "High Private Use Surrogates": (0xDB80, 0xDBFF),
    "Low Surrogates": (0xDC00, 0xDFFF),
    "Private Use Area": (0xE000, 0xF8FF),
    "CJK Compatibility Ideographs": (0xF900, 0xFAFF),
    "Alphabetic Presentation Forms": (0xFB00, 0xFB4F),
    "Arabic Presentation Forms-A": (0xFB50, 0xFDFF),
    "Variation Selectors": (0xFE00, 0xFE0F),
    "Vertical Forms": (0xFE10, 0xFE1F),
    "Combining Half Marks": (0xFE20, 0xFE2F),
    "CJK Compatibility Forms": (0xFE30, 0xFE4F),
    "Small Form Variants": (0xFE50, 0xFE6F),
    "Arabic Presentation Forms-B": (0xFE70, 0xFEFF),
    "Halfwidth and Fullwidth Forms": (0xFF00, 0xFFEF),
    "Specials": (0xFFF0, 0xFFFF)
}

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

    if category and category in unicode_category_ranges:
        category_range = unicode_category_ranges[category]
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
    categories = list(unicode_category_ranges.keys())
    return jsonify(categories)

@app.route('/add_character', methods=['POST'])
def add_character():
    data = request.json
    character = data.get('character')
    row = data.get('row')
    column = data.get('column')

    if 'custom_characters' not in session:
        session['custom_characters'] = []

    session['custom_characters'].append({
        'character': character,
        'row': row,
        'column': column
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

    # Update the session with the new list of characters
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
            'column': 0
        })

    # Get the current row limit from the session
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

@app.route('/download_characters', methods=['GET'])
def download_characters():
    custom_characters = session.get('custom_characters', [])
    json_data = {
        "version": "0.1",
        "name": "my_keyboard",
        "author": "Virtual Keyboard Builder for eScriptorium v0.1",
        "characters": custom_characters
        }
    return jsonify(json_data)

if __name__ == '__main__':
    app.run(debug=True)
    