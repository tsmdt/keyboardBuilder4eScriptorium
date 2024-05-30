# Keyboard Builder for eScriptorium ⌨️
This browser app let's you build **virtual keyboards** for [eScriptorium](https://en.wikipedia.org/wiki/EScriptorium) with ease.<br><br>It's also useful if you want to transition from another transcription client with an already existing virtual keyboard, without having to manually add all your custom Unicode characters again (*which is a drag!*).

The Keyboard Builder comes with a **set of useful features**:
* `Junicode2` as standard font for displaying the widest range of Unicodes possible. [↗ Junicode Font by Peter S. Baker](https://psb1558.github.io/Junicode-font/)
* `Filter` by Unicode categories (e.g. `Greek and Coptic`, `Hebrew`, `Latin Extended-A` ...) for easier access to the Unicode range you have in mind
* `Search` for a specific Unicode by name (e.g. `"Greek Capital Letter Omega"`). You don't have to memorize the complete name, a part is enough (e.g. `Greek Cap`) ... 
* `Paste` a **single** Unicode character you copied elsewhere and add it to your keyboard
* `Paste` a **string** of Unicode characters (e.g. `£q«±²ſē∓ↄ`) and add each individual character to your keyboard automatically
* Adjust the `order` of your keyboard via **drag** and **drop**
* Adjust the `layout` of your keyboard by increasing or decreasing the  column / row count of your grid (i.e. you can design a keyboard layout in a `2 x 10` grid or `4 x 5` and so forth...)
* `Download` your keyboard as an eScriptorium compatible `.json` file

<img width="100%" alt="keyboard_builder" src="https://github.com/th-schmidt/keyboardBuilder4eScriptorium/blob/main/assets/keyboard_builder.png">

## Table of Contents
1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Acknowledgement](#acknowledgement)

## Requirements
- Python 3.11 and above

## Installation
#### 1. Clone this repository
```shell
git clone https://github.com/th-schmidt/keyboardBuilder4eScriptorium/
```
#### 2. Change to the project folder
```shell
cd keyboardBuilder4eScriptorium
```
#### 3. Create a Python virtual environment
```python
python3.11 -m venv venv
```
#### 4. Activate your virtual environment
```shell
source venv/bin/activate
```
#### 5. Install dependencies
```python
pip install -r requirements.txt
```
#### 6. Run the app
```python
python keyboardBuilder4eS.py
```
You can access the app in your browser: `http://127.0.0.1:5000`

## Usage
### User guide
You can find a detailed user guide by clicking on the **lifebelt icon** 🛟 next to the heading.

### Import an existing virtual keyboard 
If you want to import an already existing virtual keyboard (e.g. in *Transkribus*) to eScriptorium you can use the Keyboard Builder like this: 

1. Simply paste all Unicodes of your existing keyboard in a new Transkribus document without any whitespaces between them.
2. Copy the resulting string (e.g. `£q«±²ſœē∓ↄ`) 
3. Paste this string to the "Paste character(s) here" field of the Keyboard Builder.
4. Click on the "Add Character(s)" button and every single unique character of the string will be added to your custom keyboard.

## Acknowledgement
This app was built with help from [OpenAI's GPT-4o](https://chatgpt.com/) and uses [Junicode Font by Peter S. Baker](https://psb1558.github.io/Junicode-font/), licensed under Open Font License, v. 1.1.
