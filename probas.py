import PySimpleGUI as sg
import pandas as pd
import magic

sg.ChangeLookAndFeel('GreenTan')

menu_def = []

layout = [
    [sg.Menu(menu_def, tearoff=True)],
    [sg.Text('CHOOSE YOUR FILE', size=(30, 1), justification='centre', font=("Helvetica", 15), relief=sg.RELIEF_RAISED, expand_x=True)],
    [sg.Text('File', size=(15, 1), auto_size_text=False, justification='right'),
     sg.InputText('Default File', key='-FILENAME-'), sg.FileBrowse(file_types=(("All Files", "*.*"),), pad=((50, 0), (0, 0)))],
    [sg.Submit(tooltip='Click to submit this form'), sg.Cancel()],
    [sg.Multiline('', size=(50, 10), key='-FILE_CONTENT-', disabled=True, auto_refresh=True, enable_events=True, horizontal_scrollbar_only=True)],
]

window = sg.Window('Everything bagel', layout, default_element_size=(40, 1), grab_anywhere=False)
event, values = window.read()

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Submit':
        selected_file = values['-FILENAME-']
        try:
            mime = magic.Magic()
            mime_type = mime.from_file(selected_file)

            if 'excel' in mime_type.lower():
                df = pd.read_excel(selected_file)
                file_content = df.to_string(index=False)
                window['-FILE_CONTENT-'].update(file_content)
            else:
                with open(selected_file, 'r') as file:
                    file_content = file.read()
                window['-FILE_CONTENT-'].update(file_content)

        except Exception as e:
            sg.popup_error(f'Error: {str(e)}')

window.close()
