import subprocess

subprocess.run("pip install -r requirements.22.11.21.txt", shell = True)
subprocess.run("python -m spacy download en_core_web_sm", shell = True)
