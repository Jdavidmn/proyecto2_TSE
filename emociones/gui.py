import PySimpleGUI as sg
import cv2
import paramiko
from path import Path
from typing import List


IP_ADDRESS = '127.0.0.1'
USERNAME = 'david'
PASSWORD = ''
EXECUTION_PATH = '/home/david/cursos/embabidos/proyecto2/proyecto2_TSE/emociones/'
APP_NAME = 'emotions.py'
SETTINGS_FILE = 'settings.json'
LOCAL_USE = True


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


def turn_on(client, path, app_name, local_use):
    """

    """
    path = Path(path)
    if not path.exists():
        print(f'La ruta {path} no existe')
        return
    if local_use:
        a, b, c = client.exec_command(f'/home/david/anaconda3/condabin/conda run -n emotion_env bash -c "cd {path} && python3 {app_name}"')
    else:
        a, b, c = client.exec_command(f'bash -c "cd {path} && python3 {app_name}"')


def turn_off(client, path, settings_file):
    """

    """

    path = Path(path)
    if not path.exists():
        print(f'La ruta {path} no existe')
        return
    client.exec_command(f'sed -i \'s/"work": true/"work": false/g\' {path/settings_file}')


def revisar_app(client, app_name):
    """

    """

    _, stdout, _ = client.exec_command(f'pgrep -f "python3 {app_name}"')
    salida = stdout.read().decode()
    return salida != ""


def configure(client, path, settings_file, spf):
    """

    """

    path = Path(path)
    if not path.exists():
        print(f'La ruta {path} no existe')
        return
    comando = 'sed -ir \'s/"spf": [0-9]\\{{1,\\}}/"spf": {}/g\' {}'
    a, b, c = client.exec_command(comando.format(spf, path/settings_file))


def read_data() -> List[Path]:
    """

    """

    results_path = Path('results')

    if not results_path.exists():
        return 0, []

    paths = sum([results_path.files(f'*.{ext}')
                 for ext in ['png']], [])

    return len(paths), sorted(paths)


def main():
    """

    """

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
               sg.Button('Encender aplicación', key='encender')],
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
        if event == 'datos':
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
                client = connect(IP_ADDRESS, USERNAME, PASSWORD)
                if revisar_conexion(client):
                    window['conectar'].update('Desconectar')
                    window['sys_status'].update('CONECTADO')
            else:
                client.close()
                window['conectar'].update('Conectar')
                window['sys_status'].update('DESCONECTADO')

        elif event == 'check':
            # Conexion
            if revisar_conexion(client):
                window['sys_status'].update('CONECTADO')
            else:
                window['sys_status'].update('DESCONECTADO')

            # Aplicacion
            if revisar_app(client, APP_NAME):
                window['app_status'].update('ENCENDIDO')
            else:
                window['app_status'].update('APAGADO')

        elif event == 'Configurar':
            configure(client, EXECUTION_PATH, SETTINGS_FILE, int(values[0]))

        elif event == 'encender':
            if not revisar_app(client, APP_NAME):
                turn_on(client, EXECUTION_PATH, APP_NAME, LOCAL_USE)
                window['app_status'].update('ENCENDIDO')
                window['encender'].update('Apagar aplicación')
            else:
                turn_off(client, EXECUTION_PATH, SETTINGS_FILE)
                window['app_status'].update('APAGADO')
                window['encender'].update('Encender aplicación')

    client.close()
    window.close()


if __name__ == '__main__':
    main()
