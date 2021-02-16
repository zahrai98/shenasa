### separator
a small script that create a pair dataset with face images and classifiy them in two same and diffrent folders

![python](https://img.shields.io/badge/python-v3.8-blue)
![build](https://img.shields.io/badge/build-passing-success)

<h3>Table of Contents</h3>

- [Requirement](#requirement)
- [Usage](#usage)


<h4 id="requirement">Requirement</h4>

- [python ](https://www.python.org/)3.8+
- directory that contain index and others folder (Image name in index folder is id of face which may have another image in others folder with that id.)

<h4 id="usage">Usage</h4>
you can run the script with bellow command 

<code>python separator.py  -s  "source_path" -d  "destination_path" </code>

source_path is directory containing the index faces folder and other faces folder<br/>
destination_path is directory that script create same and different faces folders in it

for more information you can run <code>python separator.py  -h </code>

