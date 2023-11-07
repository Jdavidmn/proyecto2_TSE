import PySimpleGUI as sg
import cv2
import paramiko
from path import Path
from typing import List


def connect(ip_address, username, password):
    """

    """

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip_address, username=username, password=password)
        return client
    except Exception as e:
        print('Hubo un error con la conexión: ', e)
        return None


def revisar_conexion(client_object):
    """

    """

    try:
        return client_object.get_transport().is_active()
    except AttributeError:
        return False


def turn_on():
    """

    """

    print("Esta función va a encender la aplicación en la rasp"
          " por medio de ssh")


def configure():
    """

    """

    print("Esta función va a generar el archivo de configuración"
          " y enviarlo a la rasp por ssh")


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
          [sg.Button('Configurar'),
           sg.Text('        '),
           sg.Button('Conectar', key='conectar'),
           sg.Text('        '),
           sg.Button('Revisar estados', key='check'),
           sg.Text('        '),
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
client = paramiko.SSHClient()

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

    elif event == 'conectar':
        if not revisar_conexion(client):
            client = connect('127.0.0.1', 'david', '')
            if revisar_conexion(client):
                window['conectar'].update('Desconectar')
                window['sys_status'].update('CONECTADO')
        else:
            client.close()
            window['conectar'].update('Conectar')
            window['sys_status'].update('DESCONECTADO')

    elif event == 'check':
        if revisar_conexion(client):
            window['sys_status'].update('CONECTADO')
        else:
            window['sys_status'].update('DESCONECTADO')

    elif event == 'Configurar':
        configure()

    elif event == 'Encender aplicación':
        turn_on()
        window['app_status'].update('ENCENDIDO')

client.close()
window.close()
