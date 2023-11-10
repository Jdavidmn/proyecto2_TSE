SUMMARY = "bitbake-layers recipe"
DESCRIPTION = "Recipe created by bitbake-layers"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"
SRC_URI += "file://haarcascade_frontalface_default.xml \ 
	    file://emotions.py \
	    file://model.tflite \
	    file://gui.py \
	    file://red.sh \		
	   "

S = "${WORKDIR}"


do_install() {
	install -d ${D}${bindir}
	install -m 0755 emotions.py ${D}${bindir}
	install -m 0755 haarcascade_frontalface_default.xml ${D}${bindir}
	install -m 0755 model.tflite ${D}${bindir}
	install -m 0755 gui.py ${D}${bindir}
	install -m 0755 red.sh ${D}${bindir}
}
