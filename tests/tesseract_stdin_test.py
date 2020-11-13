

from subprocess import Popen
import subprocess

import os
tessercat_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"



with open(r"C:\yuval\computer\Projects\aiopytesseract\test_images\test1.JPG", "rb") as fd:
    image = fd.read()


proc = Popen(executable=tessercat_path, args=("-", image.decode("latin-1"), "-"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)


stdout, stderr = proc.communicate()


print(stdout.decode())
print(stderr.decode())
