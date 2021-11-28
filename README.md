# Tracing policy implementation of NDCs (Paris Agreement on climate change)
The goal of this project is to develop an NLP solution that processes documents that might be of interest to evaluating progress towards contributions outlined in the Paris Agreement on climate change, or other policy frameworks. The solution uses a variety of NLP processing techniques, keyword searching, and sentence embedding through a pretrained neural network to create metrics which are tied together in a coherence score, used to indicate how strongly a document relates to the subjects imporntant to the policy framework in question.

# Overview
The root directory contains dependency files and a setup python executable to aid in setting up your coding environment. The following directories are present

- __code__: contains all python executables and jupyter notebooks which carry out computations for meeting project goals. All python executables contain documented, modularized functions. The jupyter notebooks serve to demonstrate the functionality of these executables.
- __ndc_keywords__: contains `.json` files with keywords related to some of the NDCs for Ethiopia and South Africa. The notebook files in the code directory will load keywords from these files. 
- __test_resources__: contains transcripts (OCR'd from PDF documents) of legislation and reports that are used in example analysis

# Setup GIZ Project

We will be using python 3.8.x and a virtual python environment for this project.
All tools of the project work with python 3.8.x. Other python version might cause compatibility problems.

To set up the project run the following commands:
```
git clone https://gitlab.com/analytics-club/hack4good/hack4good-fall-2021/giz-policy/giz-policy.git
cd giz-policy
python -m venv venv
source venv/bin/activate
python setup.py
```
This code block clones this repository, installs the virtual environment and installs all dependencies.

# First Steps

Now everything is ready for analyzing your array of documents. The working principle of our pipline is documented in our jupyter notebooks.
You can launch them by typing
```
jupyter-lab
```
and then just go into the `code` directory and choose the corresponding notebooks (all files ending with `.ipynb`).
To execute a code block just press `Shift + Enter`. For more information on our functions you can either make a new block (`Ctrl + B`) and execute `help(function_you_are_interested_in)`. Or you can just directly look at the documention in our module files (all files ending with `.py`)


## Team

**H4G project responsible:** Gianluca gianluca.mancini@analytics-club.org  
**NGO representative:** Erik Lehmann  
**Mentor:** Fran Peric fran.peric@statworx.com  
  
**Team members:**
- Emily Robitschek
- Raphael Sgier
- Jonathan Doorn
- Paul Türtscher

