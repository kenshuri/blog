import os
from os import listdir
from os.path import isfile, join
import subprocess
path = 'blogApp/static/images/welcome/'
os.chdir(path)
onlyfiles = [f for f in listdir('jpg/') if isfile(join('jpg/', f))]

for file in onlyfiles:
    subprocess.run(f'.\\cwebp.exe jpg/{file} -q 50 -o webp/{file}.webp')