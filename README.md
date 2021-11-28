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

## Add your files

- [ ] [Create](https://gitlab.com/-/experiment/new_project_readme_content:c8025276be15008bbf49a9722415d683?https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://gitlab.com/-/experiment/new_project_readme_content:c8025276be15008bbf49a9722415d683?https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://gitlab.com/-/experiment/new_project_readme_content:c8025276be15008bbf49a9722415d683?https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.com/analytics-club/hack4good/hack4good-fall-2021/giz-policy/giz-policy.git
git branch -M main
git push -uf origin main
```


***

## Tracing policy implementation of NDCs (Paris Agreement on climate change)
The goal of this project is to develop an NLP solution that processes documents that might be of interest to evaluating progress towards contributions outlined in the Paris Agreement on climate change, or other policy frameworks. The solution uses a variety of NLP processing techniques, keyword searching, and sentence embedding through a pretrained neural network to create metrics which are tied together in a coherence score, used to indicate how strongly a document relates to the subjects imporntant to the policy framework in question. 

## Overview
The root directory contains dependency files and a setup python executable to aid in setting up your coding environment. The following directories are present

- __code__: contains all python executables and jupyter notebooks which carry out computations for meeting project goals. All python executables contain documented, modularized functions. The jupyter notebooks serve to demonstrate the functionality of these executables.
- __ndc_keywords__: contains `.json` files with keywords related to some of the NDCs for Ethiopia and South Africa. The notebook files in the code directory will load keywords from these files. 
- __test_resources__: contains transcripts (OCR'd from PDF documents) of legislation and reports that are used in example analysis


## Project Description
[Link](https://docs.google.com/document/d/1TQnZ45oP10e3H9UsYSj_V2Pc01tcDRCa)  


## Important links
[Google Drive](https://drive.google.com/drive/u/3/folders/10Yh1W-qwxJoWgeznRIGU5LQ7GQbf2ldK)  
[Polybox](https://polybox.ethz.ch/index.php/f/2556775543)  
[Gitlab (you're already there ;) )](https://gitlab.com/analytics-club/hack4good/hack4good-fall-2021/giz-policy)  
[Welcome booklet](https://drive.google.com/file/d/1NZ00G48gG8IADXyNZE4_LfaIMTBI__jx/view?usp=sharing)  

## Team

**H4G project responsible:** Gianluca gianluca.mancini@analytics-club.org  
**NGO representative:** Erik Lehmann  
**Mentor:** Fran Peric fran.peric@statworx.com  
  
**Team members:**
- Emily Robitschek
- Raphael Sgier
- Jonathan Doorn
- Paul Türtscher

**meetings:**
- 04.10.2021 project outline meeting 

