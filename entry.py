from tkinter import BROWSE
import PySimpleGUI as sg
import json

from fonds import Fond


SAVE_FILE = 'kek.json'
LOG_FILE = 'out.log'


with open(SAVE_FILE, 'r') as read_file: #reading savefile
    data = json.load(read_file)

with open(LOG_FILE, 'r') as log:
    history = log.readlines()


for tmp in data:
    Fond(tmp["fond_name"], tmp["percentage"], tmp["sum"])

# Add a touch of color
sg.theme('DarkPurple5')

# All the stuff inside your window.
layout = [  [sg.Text(f'Всего средств: {Fond.total}', auto_size_text=True, key='-TOTAL-')],
            [sg.Input(default_text='0', key='-ADD_MONEY_INPUT-'), sg.Button(button_text='Внести', key='-ADD_MONEY_BTN-')],
            [sg.Table([[x.name, str(x.perc), str(x.sum)] for x in Fond.fond_list], key='-TABLE-', headings=['Фонд', 'Процент', 'Сумма'], select_mode=BROWSE, expand_x=True, expand_y=True, right_click_selects=True)],
            [sg.Combo([x.name for x in Fond.fond_list], key='-SELECTED_NAME-', enable_events=True), sg.Input(default_text='0', key='-TAKE_MONEY_INPUT-'), sg.Button(button_text='Списать', key='-TAKE_MONEY_BTN-', disabled=True)],
            [sg.Multiline("".join(history), size=(100, 10), key='-LOG-', auto_refresh=True)]
            ]

# Create the Window
window = sg.Window('Window Title', layout, resizable=True, auto_size_text=True, auto_size_buttons=True, font="35")

def updateStatic():
    window['-TABLE-'].update([[x.name, str(x.perc), str(x.sum)] for x in Fond.fond_list])
    window['-TOTAL-'].update(f'Всего средств: {Fond.total}')
    with open(LOG_FILE, 'r') as log:
        history = log.readlines()
        window['-LOG-'].update(''.join(history))


def writeLog(message):
    with open(LOG_FILE, 'a') as log:
        log.write(message)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    # if user closes window or clicks cancel
    if event == sg.WIN_CLOSED: 
        break
    
    # if user click add button
    if event == '-ADD_MONEY_BTN-':
        if values['-ADD_MONEY_INPUT-'].isdecimal():
            ok, message = Fond.addMoney(float(values['-ADD_MONEY_INPUT-']))
            if(ok):
                writeLog(message)
                updateStatic()
        else:
            sg.popup_error("Введенное значение не является числом")
    
    # if name selected
    if event == '-SELECTED_NAME-':
        window['-TAKE_MONEY_BTN-'].update(disabled=False)
    
    # if user click take button
    if event == '-TAKE_MONEY_BTN-':
        if values['-TAKE_MONEY_INPUT-'].isdecimal(): # check if enterd string is number
            ok, message = Fond.takeMoney(values['-SELECTED_NAME-'], float(values['-TAKE_MONEY_INPUT-']))
            if(ok):
                writeLog(message)
                updateStatic()
            else: sg.popup_error(message)
        else: sg.popup_error("Введенное значение не является числом")

with open(SAVE_FILE, "w") as write_file:
    json.dump([{"fond_name": x.name, "percentage": x.perc, "sum": x.sum} for x in Fond.fond_list], write_file)

window.close()