# Segundo Proyecto Sistemas Embebidos
# Sistema Embebido para el Reconocimiento y Clasificación de Expreseiones Faciales 
## 1.Creacción de la imagen mínima con Yocto Project
Yocto es una herramienta que nos permite crear imágenes a la medida mediante el sistema modular de Linux, para esto usamos el componente Poky, que contienen toda la información necesaria para poder llevar a cabo el desarrollo de dichas imágenes, por lo que debemos instalar Yocto, junto con algunas de sus dependencias y clonar el repositorio para poder iniciar, para ello debemos usar: 
```bash
sudo apt install gawk wget git diffstat unzip texinfo gcc build-essential chrpath socat cpio python3 python3-pip python3-pexpect xz-utils debianutils iputils-ping python3-git python3-jinja2 libegl1-mesa libsdl1.2-dev pylint3 xterm python3-subunit mesa-common-dev zstd liblz4-tool
git clone git://git.yoctoproject.org/poky
```
Una vez tenemos el repo en nuestra carpeta debemos acceder a él con el comando `cd poky`, una vez tenemos esto, debemos definir con cual versión de yocto vamos a trabajar, en este caso se usa la versión **4.0 Langdale**, por lo que se usan los siguientes comandos
```bash
git checkout -t origin/langdale -b my-langdale
git pull
```
> [!IMPORTANT]
> Es importante que la versión sea LTS y tenga soporte durante el desarrollo.

Con esto ya podemos cargar los recursos y emepezar a configurar la imagen mínima, para cargar estos recursos se debe usar
```bash
source oe-init-build-env
```

Y una vez se inicie el entorno se dirige a la ubicación de configuración mediente:

```bash
cd build/conf
vim local.conf
```

Este archivo de `local.conf` contiene la información correspondiente a las características que esperemos que tenga nuestra imagen, como la máquina la cual se configura para que sea `MACHINE ??="raspberrypi2"`, dentro de los primeros pasos debemos asegurarnos de descomentar las siguientes líneas del archivo, para acelerar el proceso de construcción

```vim
BB_HASHSERVE_UPSTREAM = "hashserv.yocto.io:8687"
SSTATE_MIRRORS ?= "file://.* https://sstate.yoctoproject.org/all/PATH;downloadfilename=PATH"
BB_SIGNATURE_HANDLER = "OEEquivHash"
BB_HASHSERVE = "auto"
```

Y agregar al final del archivo la indicación `IMAGE_FSTYPES = "tar.xz ext3 rpi-sdimg"` para que a la hora de que se cree la imagen, se genere un archivo con la extensión adecuada para poder correr la imágen en la Raspberry pi 2, con esto ya definido se puede proceder a generar la imágen, para ello se usa 

> [!NOTE]
> La extensión rpi-sdimg, no es obligatoria en todos los casos, pero es requerida para este proyecto para poder bootear la Raspberry pi 2 .


Antes de iniciar con la creación de la imagen se deben incluir algunas recetas y meta para el correcto funcionamiento del equipo, inicialmente se procede a clonar el meta de raspberry el cual nos permite crear la imagen con la extensión correcta, mediante el comando:

```bash
git clone -b langdale https://github.com/agherzan/meta-raspberrypi.git
bitbake-layers add-layer meta-raspberrypi
```

Con esto se puede proceder a generar la imagen correspondiente mediante el comando

```bash
bitbake -k core-image-base
```

Y una vez finalizado el proceso se exporta a la computadura local mediente el comando `scp` en la consola **cmd** con las siguiente indicación
### Importar imagen a escritorio local
```bash
scp jordanimejia@172.176.181.48:/home/jordanimejia/yocto/poky/build/tmp/deploy/images/raspberrypi2/core-image-base-raspberrypi2.rpi-sdimg "D:\Taller_Emb"
```

Se procede a configurar la memoria de la Raspberry Pi por medio de la herramienta **Raspberry pi Imager v1.8.1**, para ello se debe escoger el equipo con el que se trabaja

![image](https://github.com/Jdavidmn/proyecto2_TSE/assets/99856936/fd745a2c-f340-4e21-83cb-0fbbaf2e534f)

Una vez se tiene se debe escoger la imagen que se vaya a utilizar en este caso la imagen corresponde a `core-image-base-raspberrypi2.rpi-sdimg` la cual se debe escoger en la configuración, con esto finalmente se escoge el dispositivo de almacenamiento y se debería observar algo como esto:

![image](https://github.com/Jdavidmn/proyecto2_TSE/assets/99856936/c90cb26d-8ab4-4e55-852e-1d5ce0b3f5d7)

Y se procede a iniciar con la escritura, esto nos permite obtener una memoria configurada con el sistema de arranque específicado y creado a partir de la imagen de YoctoProject.


Con esta imagen base agregada el arranque en la raspberry se debería generar algo como esto en el monitor
![image](https://github.com/Jdavidmn/proyecto2_TSE/assets/99856936/896ad2ae-2999-4b4e-8ee4-6a8ebe8c96a5)

El user `root` es generado por defecto y permite llevar a cabo tareas administrativas con credenciales de súper usuario, por defecto este es el user que traen configurado los sistemas raspbian.


## 2.Agregar recetas a mi imagen 
Para agregar recetas a la imagen se descarga del repositorio de langdale la rama de `meta-openembedded` que posee un conjunto de recetas y configuraciones prácticas para nuestra imagen, como lo puede ser agregar `python3`, lo que a su vez permite utilizar bibliotecas como `OpenCV` entre otras cosas, para esto debemos clonar el repo con el siguiente comando:
```bash
git clone -b langdale https://github.com/openembedded/meta-openembedded.git
bitbake-layers add-layer /meta-openembedded/meta-oe/
bitbake-layers add-layer /meta-openembedded/meta-python/
bitbake-layers add-layer /meta-openembedded/meta-networking/
bitbake-layers add-layer /meta-openembedded/meta-multimedia/

git clone -b langdale git://git.yoctoproject.org/meta-tensorflow
git clone -b langdale git://git.yoctoproject.org/meta-java
bitbake-layers add-layer meta-tensorflow/
bitbake-layers add-layer meta-java/
```

Durante la creación se encontraron errores con diversas metas, debido a que no tienen compatibilidad con la versión `Kirkstone`, mostrando el siguiente error

>ERROR! Branch kirkstone in https://github.com//java.git does not exist!

Si se ejecuta el comando de forma general sin buscar la compatibilidad con el comando 

```bash
git clone git://git.yoctoproject.org/meta-java
```
Se produce un error integración al sistema al ambiente que estamos desarrollando, donde se muestra

>ERROR! repository available with Langdale version, try to change branch

>Using checkout or command -b "branch name"

Por esta razón se mudó el sistema de Kirkstone a Langdale debido a la compatibilidad de todas las meta.





Esto es de suma importancia para esta demostración, ya que nos permite agregar el `meta-oe` que a su vez nos permite usar herramientas como **_vim_** que son editores de texto o incluso **_ssh_** para servicios de red, al aplicar estos comandos, el archivo `bblayers.conf` se debería de ver como:
```vim
# POKY_BBLAYERS_CONF_VERSION is increased each time build/conf/bblayers.conf
# changes incompatibly
POKY_BBLAYERS_CONF_VERSION = "2"

BBPATH = "${TOPDIR}"
BBFILES ?= ""

BBLAYERS ?= " \
  /home/jordanimejia/yocto/poky/meta \
  /home/jordanimejia/yocto/poky/meta-poky \
  /home/jordanimejia/yocto/poky/meta-yocto-bsp \
  /home/jordanimejia/yocto/poky/build/meta-openembedded/meta-oe \
  /home/jordanimejia/yocto/poky/build/meta-openembedded/meta-python \
  "
```
Para finalizar se debe configurar el archivo `local.conf` donde vamos a indicarle que debe instalar de las recetas que agregamos
```vim
IMAGE_INSTALL:append = " \
                 python3-pip \
                 python3-pygobject \
                 python3-paramiko \
                 vim \
                 openssh \
                 opencv \
                "
```
> [!WARNING] 
> Si se agregan herramientas que no son parte de las recetas indicadas en los layers se va a generar un error, por lo que hay que asegurarse de que todo está incorporado de forma adecuada.

Estas utilidades se escogieron debido a la necesidad del procesamiento de imágenes y video, por lo que la prueba se realiza para verificar si existe algún conflicto con estas librerías y resolverlo antes de la implementación de los programas con **_OpenVino_**, con esto claro, se procede a la creación de imagen **_base_**

```bash
bitbake core-image-base
```
> [!NOTE]
> Al usar la imagen base se obtiene una mayor funcionalidad y la posibilidad de usar más recursos.


Importamos la imagen con el comando establecido [scp](#importar-imagen-a-escritorio-local).

Para finalizar probamos el comando vim y tambien la herramienta de python, primero creamos un archivo `.py` que se llame **_hola_** y agregamos la siguiente línea de codigo
```python
print("Imagen con python3 Primer Proyecto TSE - Jordani Mejía")
```
Salimos del editor de texto y podemos visualizar si funciona como debería usando `python3 hola.py`, esto nos debería arrojar algo como lo siguiente:

![image](https://github.com/aleguillen4/20231sTSE/assets/99856936/d23dd264-e96c-4d8c-b82f-576f754591b3)

## 3.Incluir archivos desde la creación de la imagen
Es de suma importancia la capcidad de generar la imagen con los archivos necesarios para el funcionamiento del proyecto desde su núcleo, ya que facilita la obtención de los archivos y su ejecución, para ello vamos a agregar un meta nuevo donde se van a encontrar todos lo recursos necesarios para esto, la forma de lograrlo es mediante los comandos

```bash
bitbake-layers create-layer meta-layername
bitbake-layers add-layer meta-layername
```

Para este ejemplo se usó el nombre de `meta-layersources` y dentro de esto se van a encontrar diversos archivos, pero hay una carpeta de suma importancia, que se llama **_recipes-example/example_** dentro de la cual vamos a generar un espacio donde agregar nuestros archivos, para ello ejecutamos

```bash
cd recipes-example/example
mkdir files
cd files
```
Una vez acá agregamos los elementos que sean necesarios, para este ejemplo solo se usa un archivo **_.py_** llamado `incluir.py`, este se ejecutará dentro de la imagen para mostrar como funciona, pero para ello debemos configurar el documento de `example_0.1.bb`, donde vamos a agregar su licencia y archivos necesarios
```vim 
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"
SRC_URI += "file://incluir.py \ 
	   "
S = "${WORKDIR}"

do_install() {
	install -d ${D}${bindir}
	install -m 0755 incluir.py ${D}${bindir}
}
```
El código del `md5` se obtiene ejecutando este comando donde se encuentra dicho archivo de licencia
```bash
md5sum COPYING.MIT
```
Con esto podemos agregar la carpeta **_example_** al archivo de configuración `local.conf` y debería verse algo así 

```vim
IMAGE_INSTALL:append = " \
                 example \
                 python3-pip \
                 python3-pygobject \
                 python3-paramiko \
                 vim \
                 openssh \
                 opencv \
                "
```

Al agregar la carpeta ya se tiene configurada la creación de la imagen, para este caso se utiliza la versión **_core-image-x11-qemux86-64_**, de la siguiente forma

```bash
bitbake core-image-x11
```

Una vez importada y agregada la imagen al **_VirtualBox_** se navega por los archivos y se ejecuta el archivo `incluir.py`
```bash
cd ../../usr/bin
pyhton3 incluir.py
```
> [!NOTE]
> Al iniciar la imagen el directorio es /home/root pero esto puede variar, lo importante es la ubicación de nuestros archivos

El resultado se debe ver algo como esto 
![image](https://github.com/Jormq99/TSE-proyecto1/assets/99856936/f1d7002c-7bbd-41dc-a211-d370bc6ca071)


## 4.Configurar mi imagen para incluir OpenVino
Para esto primero debemos descargar los repositorios donde se inlcuyen las herramientas necesarias para agregar el ambiente de Intel, este proceso se basa en la página [Agregar OpenVINO Toolkit](https://docs.openvino.ai/2023.0/openvino_docs_install_guides_installing_openvino_yocto.html), sin embargo se deben hacer algunas configuraciones para que sea complatible con la versión `kirkstone`
```bash
git clone -b kirkstone https://git.yoctoproject.org/meta-intel
git clone -b kirkstone https://github.com/kraj/meta-clang.git
```

Una vez que los repositorios están descragados se pueden agregar a las capas de forma manual o con los comandos

```bash
bitbake-layers add-layer meta-intel
bitbake-layers add-layer meta-clang
```
> [!WARNING] 
> Para trabajar con otras versiones se debe indicar esta después del comando -b

> [!NOTE]
> Si los repos no se hacen después de cargar los recursos de poky se debe especificar la ubicación de estos

Para finalizar la configuración se debe modificar el archivo `local.conf`, para indicar motores de inferencia y otras características

```vim
PACKAGECONFIG:append:pn-openvino-inference-engine = " opencl"
PACKAGECONFIG:append:pn-openvino-inference-engine = " python3"

IMAGE_INSTALL:append = " \
                 example \
                 python3-pip \
                 python3-pygobject \
                 python3-paramiko \
                 vim \
                 openssh \
                 opencv \
		 git \
		 openvino-inference-engine \
		 openvino-inference-engine-samples \
		 openvino-inference-engine-python3 \
		 openvino-model-optimizer \
                "
```

>ERROR! el siguiente error se generó debido a no agregar la receta de MATPLOTLIB al local.conf
![image](https://github.com/browserify/syntax-error/assets/99856936/cd61c034-2191-4fb3-8da1-249b22e24a03)

Por ello se agrega la librería de python correspondiente dando como resultado la configuración

```vim
PACKAGECONFIG:append:pn-openvino-inference-engine = " opencl"
PACKAGECONFIG:append:pn-openvino-inference-engine = " python3"

IMAGE_INSTALL:append = " \
                 example \
                 python3-pip \
                 python3-pygobject \
                 python3-paramiko \
		 python3-matplotlib \
                 vim \
                 openssh \
                 opencv \
		 git \
		 openvino-inference-engine \
		 openvino-inference-engine-samples \
		 openvino-inference-engine-python3 \
		 openvino-model-optimizer \
                "
```


Con esto se agregan herramientas y la distribución de `OpenVino`

> [!WARNING] 
> Los modelos OpenVino traen sus sistemas entrenados en la red por lo que es importante establecer una conexión a la red

### Configuración de Ethernet
Debido a que se debe descargar información es necesario configurar nuestra máquina virtual, para ello se le deden asignar permisos desde la aplicación de VirtualBox, por lo que se debe tener la computadora virtual apagada y proceder a darle acceso a nuestra red, para ello se hacer los siguientes cambios
```tree
TSE/

Configuraciones/
	RED
	->Adaptador 1
	  ->Adapatdator de puente
	  ->Permitir todos
```

Una vez que se tiene esto se debe incluir a los archivos de la imagen un doc llamado `red.sh` este archivo debe ser **_bash_** para que la configuración se pueda realizar y el código sería

```bash
ifconfig eth0 up
udhcpc -i eth0
```
Una vez construida la imagen verificamos la configuracon de red que tienen inicialmente
![image](https://github.com/Jormq99/TSE-Proyecto_1_copy/assets/99856936/67c20a33-a7d0-4ff6-89ee-edebf262ae85)

Y se procede a correr el comando para obetener la IP adecuada a partir de un broadcasting dicover 
```bash
bash red.sh
```
Lo que debría dar como resultado

![image](https://github.com/Jormq99/TSE-Proyecto_1_copy/assets/99856936/02f37803-97b6-4177-8aa4-2f6162775f1d)



>ERROR! Una vez se corrió el modelo se produjo el siguiente error
![image](https://github.com/browserify/syntax-error/assets/99856936/eba90de3-94e8-4377-af4c-470691e0740c)

Se incluyeron los siguientes plugins de Gstreamer

```vim
VIDEO_TOOLS = " \
            gstreamer1.0 \
            gstreamer1.0-libav \
            gstreamer1.0-plugins-good \ 
            gstreamer1.0-plugins-base \ 
            gstreamer1.0-plugins-bad \
            gstreamer1.0-plugins-ugly \
           "
```

Resultado Final

![image](https://github.com/Jormq99/TSE-proyecto1/assets/99856936/847ceaaa-4fdd-4574-a7d3-6a3b3d954a6b)
