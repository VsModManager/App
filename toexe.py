from cx_Freeze import setup, Executable
import os
import filecmp
import shutil
import PyInstaller.__main__


base = 'Win32GUI'

# executables = [Executable("main.py", base=base, target_name="VintageModManager.exe", icon="logo.ico")]

# include_files = [".ui", "cross.png", "tick.png", "logo.ico"]

# zip_include_packages = []

# options = {
# 	'build_exe': {
# 		'includes': zip_include_packages,
# 		'include_files': include_files,
# 		# 'zip_include_packages': includes,
# 	},
# }
PyInstaller.__main__.run([
	'main.py',
	'--onefile',
	'--windowed',
	'-n VintageModManager.exe',
	'--add-data .ui;.ui',
	'--add-data cross.png;cross.png',
	'--add-data tick.png;tick.png',
	'--add-data logo.ico;logo.ico',
])


# if os.path.isdir(r".\build\exe.win-amd64-3.9"):
# 	shutil.rmtree(r".\build\exe.win-amd64-3.9")
# setup(
# 	name='main',
# 	options=options,
# 	version="0.1.0",
# 	description='<any description>',
# 	executables=executables
# )

# fileList = []
# removelist = [
# 	r".\build\exe.win-amd64-3.9\lib\PyQt5\Qt\qml",
# 	r".\build\exe.win-amd64-3.9\lib\chardet\cli",
# 	r".\build\exe.win-amd64-3.9\lib\chardet\metatada",
# 	r".\build\exe.win-amd64-3.9\lib\distutils\command",
# 	r".\build\exe.win-amd64-3.9\lib\idna\uts46data.pyc",
# 	r".\build\exe.win-amd64-3.9\lib\numpy\testing",
# 	r".\build\exe.win-amd64-3.9\lib\numpy\__init__.pxd",
# 	r".\build\exe.win-amd64-3.9\lib\numpy\__init__.cython-30.pxd",
# 	r".\build\exe.win-amd64-3.9\lib\numpy\ma\testutils.pyc",
# 	r".\build\exe.win-amd64-3.9\lib\pkg_resources\_vendor",
# 	r".\build\exe.win-amd64-3.9\lib\pkg_resources",
# 	r".\build\exe.win-amd64-3.9\lib\pydoc_data",
# 	r".\build\exe.win-amd64-3.9\lib\setuptools\_distutils",
# 	r".\build\exe.win-amd64-3.9\lib\setuptools\_vendor",
# ]
# # C:\Users\Kirill\Desktop\CODE\PY\1\build\exe.win-amd64-3.9\lib\sqlite3
# for dirpath, dirs, files in os.walk("./build/"):
# 	if dirpath.endswith("tests") or dirpath.endswith("src") or dirpath.endswith("test"):
# 		removelist.append(dirpath)

# for key in removelist:
# 	if os.path.isfile(key):
# 		os.remove(key)
# 	if os.path.isdir(key):
# 		shutil.rmtree(key)

# for dirpath, dirs, files in os.walk("./build/"):
# 	for filename in files:
# 		fileList.append((dirpath, filename, os.path.getsize(os.path.join(dirpath, filename))))

# def compare(x, y):
# 	try:
# 		if filecmp.cmp(os.path.join(x[0], x[1]), os.path.join(y[0], y[1])):
# 			return open(os.path.join(x[0], x[1]), 'rb').read() == open(os.path.join(y[0], y[1]), 'rb').read()
# 		return False
# 	except:
# 		return False

# total = 0
# for file in fileList:
# 	# print(file)
# 	for file2 in fileList:
# 		if not file[1].endswith(".dll"): break
# 		if (file[2] == file2[2]):
# 			if (file == file2):
# 				break
# 			if compare(file, file2):
# 				os.remove(os.path.join(file[0], file[1]))
# # 				total += file[2]
# # 				print(total, file, file2)
# # 			break
# # print(fileList)
