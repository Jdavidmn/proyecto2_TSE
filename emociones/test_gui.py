import PySimpleGUI as sg

sg.theme('DarkGrey7')   # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Text('Conexión: '),
           sg.Text('DESCONECTADO', key='sys_status'),
           sg.Text('APLICACIÓN NO FUNCIONANDO', key='app_status')],
          [sg.Text('Tiempo de muestreo: '),
           sg.Slider((1, 10), orientation='h', s=(10, 15))],
          [sg.Button('Ok'),
           sg.Button('Cancel')]
          ]

# Create the Window
window = sg.Window('Detección de emociones', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    # if user closes window or clicks cancel
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break

    print('You entered ', values[0], values[1])

window.close()
