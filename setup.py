import subprocess

subprocess.run("pip install -r requirements.txt", shell = True)
subprocess.run("python -m spacy download en_core_web_sm", shell = True)
