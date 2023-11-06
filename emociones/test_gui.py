import PySimpleGUI as sg
import cv2
from path import Path
from typing import List


def read_data() -> List[Path]:
    """

    """

    results_path = Path('results')

    if not results_path.exists():
        return 0, []

    paths = sum([results_path.files(f'*.{ext}')
                 for ext in ['png']], [])

    return len(paths), sorted(paths)


sg.theme('DarkGrey7')   # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Text('Conexión: '),
           sg.Text('DESCONECTADO', key='sys_status'),
           sg.Text('     '),
           sg.Text('Funcionamiento: '),
           sg.Text('APAGADO', key='app_status')],
          [sg.Text('Tiempo de muestreo: '),
           sg.Slider((1, 10), orientation='h', s=(10, 15)),
           sg.Text('    '),
           sg.Button('Encender aplicación')],
          [sg.Text('               '),
           sg.Button('Configurar'),
           sg.Text('                             '),
           sg.Button('Leer datos', key='datos')],
          [sg.Image(key='image')],
          [sg.Button('Anterior', key='previa', visible=False),
           sg.Button('Siguiente', key='siguiente', visible=False),
           sg.Button('Cerrar imagen', key='cerrar', visible=False)],
          [sg.Button('Cerrar')]
          ]

# Create the Window
window = sg.Window('Detector de emociones', layout)
images = []
idx = 0
num_images = 0

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    # if user closes window or clicks cancel
    if event in (sg.WIN_CLOSED, 'Cerrar'):
        break
    elif event == 'datos':
        num_images, images = read_data()
        if num_images != 0:
            window['datos'].update(visible=False)
            window['image'].update(filename=images[0])
            window['previa'].update(visible=True)
            window['siguiente'].update(visible=True)
            window['cerrar'].update(visible=True)
        else:
            print('No se han cargado datos')

    elif event == 'siguiente':
        idx = (idx + 1) % num_images
        window['image'].update(filename=images[idx])

    elif event == 'previa':
        idx = (idx - 1) % num_images
        window['image'].update(filename=images[idx])

    elif event == 'cerrar':
        window['image'].update()
        window['datos'].update(visible=True)
        window['previa'].update(visible=False)
        window['cerrar'].update(visible=False)
        window['siguiente'].update(visible=False)
        idx = 0


window.close()
