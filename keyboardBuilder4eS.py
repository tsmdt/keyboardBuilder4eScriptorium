import unicodedata
import os
from flask import Flask, request, jsonify, session, render_template

app = Flask(__name__)
app.secret_key = os.urandom(24)

unicode_category_ranges = {
    "Adlam": (0x1E900, 0x1E95F),
    "Aegean Numbers": (0x10100, 0x1013F),
    "Alphabetic Presentation Forms": (0xFB00, 0xFB4F),
    "Anatolian Hieroglyphs": (0x14400, 0x1467F),
    "Ancient Greek Musical Notation": (0x1D200, 0x1D24F),
    "Ancient Greek Numbers": (0x10140, 0x1018F),
    "Ancient Symbols": (0x10190, 0x101CF),
    "Arabic": (0x0600, 0x06FF),
    "Arabic Extended-A": (0x08A0, 0x08FF),
    "Arabic Presentation Forms-A": (0xFB50, 0xFDFF),
    "Arabic Presentation Forms-B": (0xFE70, 0xFEFF),
    "Arabic Supplement": (0x0750, 0x077F),
    "Armenian": (0x0530, 0x058F),
    "Arrows": (0x2190, 0x21FF),
    "Balinese": (0x1B00, 0x1B7F),
    "Bamum": (0xA6A0, 0xA6FF),
    "Bamum Supplement": (0x16800, 0x16A38),
    "Bassa Vah": (0x16AD0, 0x16AFF),
    "Batak": (0x1BC0, 0x1BFF),
    "Bengali": (0x0980, 0x09FF),
    "Bhaiksuki": (0x11C00, 0x11C6F),
    "Block Elements": (0x2580, 0x259F),
    "Bopomofo": (0x3100, 0x312F),
    "Bopomofo Extended": (0x31A0, 0x31BF),
    "Box Drawing": (0x2500, 0x257F),
    "Brahmi": (0x11000, 0x1107F),
    "Braille Patterns": (0x2800, 0x28FF),
    "Buginese": (0x1A00, 0x1A1F),
    "Buhid": (0x1740, 0x175F),
    "Byzantine Musical Symbols": (0x1D000, 0x1D0FF),
    "Canadian Aboriginal Syllabics Extended": (0x18B0, 0x18FF),
    "Carian": (0x102A0, 0x102DF),
    "Caucasian Albanian": (0x10530, 0x1056F),
    "Chakma": (0x11100, 0x1114F),
    "Cham": (0xAA00, 0xAA5F),
    "Cherokee": (0x13A0, 0x13FF),
    "Cherokee Supplement": (0xAB70, 0xABBF),
    "Chorasmian": (0x10FB0, 0x10FDF),
    "CJK Compatibility": (0x3300, 0x33FF),
    "CJK Compatibility Forms": (0xFE30, 0xFE4F),
    "CJK Compatibility Ideographs": (0xF900, 0xFAFF),
    "CJK Compatibility Ideographs Supplement": (0x2F800, 0x2FA1F),
    "CJK Radicals Supplement": (0x2E80, 0x2EFF),
    "CJK Strokes": (0x31C0, 0x31EF),
    "CJK Symbols and Punctuation": (0x3000, 0x303F),
    "CJK Unified Ideographs": (0x4E00, 0x9FFF),
    "CJK Unified Ideographs Extension A": (0x3400, 0x4DBF),
    "CJK Unified Ideographs Extension B": (0x20000, 0x2A6DF),
    "CJK Unified Ideographs Extension C": (0x2A700, 0x2B73F),
    "CJK Unified Ideographs Extension D": (0x2B740, 0x2B81F),
    "CJK Unified Ideographs Extension E": (0x2B820, 0x2CEAF),
    "CJK Unified Ideographs Extension F": (0x2CEB0, 0x2EBEF),
    "Combining Diacritical Marks": (0x0300, 0x036F),
    "Combining Diacritical Marks Extended": (0x1AB0, 0x1AFF),
    "Combining Diacritical Marks Supplement": (0x1DC0, 0x1DFF),
    "Combining Half Marks": (0xFE20, 0xFE2F),
    "Combining Marks for Symbols": (0x20D0, 0x20FF),
    "Common Indic Number Forms": (0xA830, 0xA83F),
    "Control Pictures": (0x2400, 0x243F),
    "Coptic": (0x2C80, 0x2CFF),
    "Coptic Epact Numbers": (0x102E0, 0x102FF),
    "Cuneiform": (0x12000, 0x123FF),
    "Currency Symbols": (0x20A0, 0x20CF),
    "Cypriot Syllabary": (0x10800, 0x1083F),
    "Cyrillic": (0x0400, 0x04FF),
    "Cyrillic Extended-A": (0x2DE0, 0x2DFF),
    "Cyrillic Extended-B": (0xA640, 0xA69F),
    "Cyrillic Extended-C": (0x1C80, 0x1C8F),
    "Cyrillic Supplement": (0x0500, 0x052F),
    "Deseret": (0x10400, 0x1044F),
    "Devanagari": (0x0900, 0x097F),
    "Devanagari Extended": (0xA8E0, 0xA8FF),
    "Dingbats": (0x2700, 0x27BF),
    "Dives Akuru": (0x11900, 0x1195F),
    "Dogra": (0x11800, 0x1184F),
    "Duployan": (0x1BC00, 0x1BC9F),
    "Early Dynastic Cuneiform": (0x12480, 0x1254F),
    "Egyptian Hieroglyph Format Controls": (0x13430, 0x1345F),
    "Egyptian Hieroglyphs": (0x13000, 0x1342F),
    "Elbasan": (0x10500, 0x1052F),
    "Elymaic": (0x10FE0, 0x10FFF),
    "Ethiopic": (0x1200, 0x137F),
    "Ethiopic Extended": (0x2D80, 0x2DDF),
    "Ethiopic Extended-A": (0xAB00, 0xAB2F),
    "Ethiopic Supplement": (0x1380, 0x139F),
    "General Punctuation": (0x2000, 0x206F),
    "Geometric Shapes": (0x25A0, 0x25FF),
    "Georgian": (0x10A0, 0x10FF),
    "Georgian Extended": (0x1C90, 0x1CBF),
    "Georgian Supplement": (0x2D00, 0x2D2F),
    "Glagolitic": (0x2C00, 0x2C5F),
    "Glagolitic Supplement": (0x1E000, 0x1E02F),
    "Gothic": (0x10330, 0x1034F),
    "Grantha": (0x11300, 0x1137F),
    "Greek and Coptic": (0x0370, 0x03FF),
    "Greek Extended": (0x1F00, 0x1FFF),
    "Gujarati": (0x0A80, 0x0AFF),
    "Gunjala Gondi": (0x11D60, 0x11DAF),
    "Gurmukhi": (0x0A00, 0x0A7F),
    "Halfwidth and Fullwidth Forms": (0xFF00, 0xFFEF),
    "Hangul Compatibility Jamo": (0x3130, 0x318F),
    "Hangul Jamo": (0x1100, 0x11FF),
    "Hangul Jamo Extended-A": (0xA960, 0xA97F),
    "Hangul Jamo Extended-B": (0xD7B0, 0xD7FF),
    "Hangul Syllables": (0xAC00, 0xD7AF),
    "Hanifi Rohingya": (0x10D00, 0x10D3F),
    "Hanunoo": (0x1720, 0x173F),
    "Hatran": (0x108E0, 0x108FF),
    "Hebrew": (0x0590, 0x05FF),
    "High Private Use Surrogates": (0xDB80, 0xDBFF),
    "High Surrogates": (0xD800, 0xDB7F),
    "Hiragana": (0x3040, 0x309F),
    "Ideographic Description Characters": (0x2FF0, 0x2FFF),
    "Imperial Aramaic": (0x10840, 0x1085F),
    "Indic Siyaq Numbers": (0x1EC70, 0x1ECBF),
    "Inscriptional Pahlavi": (0x10B60, 0x10B7F),
    "Inscriptional Parthian": (0x10B40, 0x10B5F),
    "IPA Extensions": (0x0250, 0x02AF),
    "Javanese": (0xA980, 0xA9DF),
    "Kaithi": (0x11080, 0x110CF),
    "Kana Extended-A": (0x1B100, 0x1B12F),
    "Kana Supplement": (0x1B000, 0x1B0FF),
    "Kanbun": (0x3190, 0x319F),
    "Kangxi Radicals": (0x2F00, 0x2FDF),
    "Kannada": (0x0C80, 0x0CFF),
    "Katakana": (0x30A0, 0x30FF),
    "Katakana Phonetic Extensions": (0x31F0, 0x31FF),
    "Kayah Li": (0xA900, 0xA92F),
    "Kharoshthi": (0x10A00, 0x10A5F),
    "Khitan Small Script": (0x18B00, 0x18CFF),
    "Khmer": (0x1780, 0x17FF),
    "Khmer Symbols": (0x19E0, 0x19FF),
    "Khojki": (0x11200, 0x1124F),
    "Khudawadi": (0x112B0, 0x112FF),
    "Lao": (0x0E80, 0x0EFF),
    "Latin Extended-A": (0x0100, 0x017F),
    "Latin Extended-B": (0x0180, 0x024F),
    "Latin Extended-C": (0x2C60, 0x2C7F),
    "Latin Extended-D": (0xA720, 0xA7FF),
    "Latin Extended-E": (0xAB30, 0xAB6F),
    "Latin Extended Additional": (0x1E00, 0x1EFF),
    "Latin-1 Supplement": (0x0080, 0x00FF),
    "Lepcha": (0x1C00, 0x1C4F),
    "Letterlike Symbols": (0x2100, 0x214F),
    "Limbu": (0x1900, 0x194F),
    "Linear A": (0x10600, 0x1077F),
    "Linear B Ideograms": (0x10080, 0x100FF),
    "Linear B Syllabary": (0x10000, 0x1007F),
    "Lisu": (0xA4D0, 0xA4FF),
    "Lycian": (0x10280, 0x1029F),
    "Lydian": (0x102A0, 0x102DF),
    "Mahajani": (0x11150, 0x1117F),
    "Makasar": (0x11EE0, 0x11EFF),
    "Malayalam": (0x0D00, 0x0D7F),
    "Mandaic": (0x0840, 0x085F),
    "Manichaean": (0x10AC0, 0x10AFF),
    "Marchen": (0x11C70, 0x11CBF),
    "Masaram Gondi": (0x11D00, 0x11D5F),
    "Mathematical Alphanumeric Symbols": (0x1D400, 0x1D7FF),
    "Mathematical Operators": (0x2200, 0x22FF),
    "Mayan Numerals": (0x1D2E0, 0x1D2FF),
    "Medefaidrin": (0x16E40, 0x16E9F),
    "Meetei Mayek": (0xABC0, 0xABFF),
    "Meetei Mayek Extensions": (0xAAE0, 0xAAFF),
    "Mende Kikakui": (0x1E800, 0x1E8DF),
    "Meroitic Cursive": (0x109A0, 0x109FF),
    "Meroitic Hieroglyphs": (0x10980, 0x1099F),
    "Miao": (0x16F00, 0x16F9F),
    "Miscellaneous Mathematical Symbols-A": (0x27C0, 0x27EF),
    "Miscellaneous Mathematical Symbols-B": (0x2980, 0x29FF),
    "Miscellaneous Symbols": (0x2600, 0x26FF),
    "Miscellaneous Symbols and Arrows": (0x2B00, 0x2BFF),
    "Miscellaneous Technical": (0x2300, 0x23FF),
    "Modi": (0x11600, 0x1165F),
    "Modifier Tone Letters": (0xA700, 0xA71F),
    "Mongolian": (0x1800, 0x18AF),
    "Mongolian Supplement": (0x11660, 0x1167F),
    "Mro": (0x16A40, 0x16A6F),
    "Multani": (0x11280, 0x112AF),
    "Musical Symbols": (0x1D100, 0x1D1FF),
    "Myanmar": (0x1000, 0x109F),
    "Myanmar Extended-A": (0xAA60, 0xAA7F),
    "Myanmar Extended-B": (0xA9E0, 0xA9FF),
    "NKo": (0x07C0, 0x07FF),
    "Nabataean": (0x10880, 0x108AF),
    "Nandinagri": (0x119A0, 0x119FF),
    "New Tai Lue": (0x1980, 0x19DF),
    "Newa": (0x11400, 0x1147F),
    "Number Forms": (0x2150, 0x218F),
    "Nushu": (0x1B170, 0x1B2FF),
    "Nyiakeng Puachue Hmong": (0x1E100, 0x1E14F),
    "Ogham": (0x1680, 0x169F),
    "Ol Chiki": (0x1C50, 0x1C7F),
    "Old Hungarian": (0x10C80, 0x10CFF),
    "Old Italic": (0x10300, 0x1032F),
    "Old North Arabian": (0x10A80, 0x10A9F),
    "Old Permic": (0x10350, 0x1037F),
    "Old Persian": (0x103A0, 0x103DF),
    "Old Sogdian": (0x10F00, 0x10F2F),
    "Old South Arabian": (0x10A60, 0x10A7F),
    "Old Turkic": (0x10C00, 0x10C4F),
    "Oriya": (0x0B00, 0x0B7F),
    "Ornamental Dingbats": (0x1F650, 0x1F67F),
    "Osage": (0x104B0, 0x104FF),
    "Osmanya": (0x10480, 0x104AF),
    "Pahawh Hmong": (0x16B00, 0x16B8F),
    "Palmyrene": (0x10860, 0x1087F),
    "Pau Cin Hau": (0x11AC0, 0x11AFF),
    "Phags-pa": (0xA840, 0xA87F),
    "Phoenician": (0x10900, 0x1091F),
    "Phonetic Extensions": (0x1D00, 0x1D7F),
    "Phonetic Extensions Supplement": (0x1D80, 0x1DBF),
    "Playing Cards": (0x1F0A0, 0x1F0FF),
    "Psalter Pahlavi": (0x10B80, 0x10BAF),
    "Rejang": (0xA930, 0xA95F),
    "Rumi Numeral Symbols": (0x10E60, 0x10E7F),
    "Runic": (0x16A0, 0x16FF),
    "Samaritan": (0x0800, 0x083F),
    "Saurashtra": (0xA880, 0xA8DF),
    "Sharada": (0x11180, 0x111DF),
    "Shavian": (0x10450, 0x1047F),
    "Shorthand Format Controls": (0x1BCA0, 0x1BCAF),
    "Siddham": (0x11580, 0x115FF),
    "Sinhala": (0x0D80, 0x0DFF),
    "Sinhala Archaic Numbers": (0x111E0, 0x111FF),
    "Small Form Variants": (0xFE50, 0xFE6F),
    "Sogdian": (0x10F30, 0x10F6F),
    "Sora Sompeng": (0x110D0, 0x110FF),
    "Soyombo": (0x11A50, 0x11AAF),
    "Spacing Modifier Letters": (0x02B0, 0x02FF),
    "Specials": (0xFFF0, 0xFFFF),
    "Sundanese": (0x1B80, 0x1BBF),
    "Sundanese Supplement": (0x1CC0, 0x1CCF),
    "Superscripts and Subscripts": (0x2070, 0x209F),
    "Supplemental Arrows-A": (0x27F0, 0x27FF),
    "Supplemental Arrows-B": (0x2900, 0x297F),
    "Supplemental Mathematical Operators": (0x2A00, 0x2AFF),
    "Supplemental Punctuation": (0x2E00, 0x2E7F),
    "Sutton SignWriting": (0x1D800, 0x1DAAF),
    "Syloti Nagri": (0xA800, 0xA82F),
    "Syriac": (0x0700, 0x074F),
    "Syriac Supplement": (0x0860, 0x086F),
    "Tagalog": (0x1700, 0x171F),
    "Tagbanwa": (0x1760, 0x177F),
    "Tai Le": (0x1950, 0x197F),
    "Tai Tham": (0x1A20, 0x1AAF),
    "Tai Viet": (0xAA80, 0xAADF),
    "Tai Xuan Jing Symbols": (0x1D300, 0x1D35F),
    "Takri": (0x11680, 0x116CF),
    "Tamil": (0x0B80, 0x0BFF),
    "Tamil Supplement": (0x11FC0, 0x11FFF),
    "Tangsa": (0x16A70, 0x16ACF),
    "Tangut": (0x17000, 0x187FF),
    "Telugu": (0x0C00, 0x0C7F),
    "Thaana": (0x0780, 0x07BF),
    "Thai": (0x0E00, 0x0E7F),
    "Tibetan": (0x0F00, 0x0FFF),
    "Tifinagh": (0x2D30, 0x2D7F),
    "Tirhuta": (0x11480, 0x114DF),
    "Transport and Map Symbols": (0x1F680, 0x1F6FF),
    "Ugaritic": (0x10380, 0x1039F),
    "Unified Canadian Aboriginal Syllabics": (0x1400, 0x167F),
    "Unified Canadian Aboriginal Syllabics Extended": (0x18B0, 0x18FF),
    "Vai": (0xA500, 0xA63F),
    "Vedic Extensions": (0x1CD0, 0x1CFF),
    "Vertical Forms": (0xFE10, 0xFE1F),
    "Vithkuqi": (0x10570, 0x105BF),
    "Wancho": (0x1E2C0, 0x1E2FF),
    "Warang Citi": (0x118A0, 0x118FF),
    "Yezidi": (0x10E80, 0x10EBF),
    "Yi Radicals": (0xA490, 0xA4CF),
    "Yi Syllables": (0xA000, 0xA48F),
    "Yijing Hexagram Symbols": (0x4DC0, 0x4DFF),
    "Zanabazar Square": (0x11A00, 0x11A4F)
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

@app.route('/download_characters', methods=['POST'])
def download_characters():
    data = request.json
    keyboard_name = data.get('keyboard_name', 'my_keyboard')  # Get the keyboard name from the request
    custom_characters = session.get('custom_characters', [])
    
    response = {
        "version": "0.1",
        "author": "Virtual Keyboard Builder for eScriptorium v0.1",
        "name": keyboard_name,  # Include the keyboard name in the response
        "characters": custom_characters
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
    