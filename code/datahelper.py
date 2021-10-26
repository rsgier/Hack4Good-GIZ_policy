import pandas as pd
import os
from typing import List, Tuple

def list_docs(folder_path: str,
              blacklist = ['Source.txt', 'Source Link.txt', 'Source Links.txt']) -> Tuple[List[str], List[str]]:
    """Generates a list of document names for reference and tracking.
    This command currently extracts the .txt documents from all the subfolders of a parent folder,
    and filters out the ones containing source information, which we might not want to use in our analysis.

    Args:
        folder_path (str): The path to the parent folder.
        blacklist (List[str]): A list of files which should not be included.

    Returns:
        doc_names (List[str]): A list containing all names of found documents.
        doc_paths (List[str]): A list containing all paths to the found documents.
    """

    doc_names = []
    doc_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt') and (file not in blacklist):
                doc_names.append(file)
                doc_paths.append(os.path.join(root, file))

    return doc_names, doc_paths

def read_docs_to_df(folder_path: str) -> pd.DataFrame:
    """Takes in a folder (can also be with different subfolders) with policy-related text documents
    and gathers txt docs to analyze from those folders and makes a dataframe of their names and paths.

    NOTE: If want to preserve names and paths of the documents and make them easily searchable, it might be useful
    to export the dictionary/keep that as well to add more summary information about the document for instance.

    Args:
        folder_path (str): The path to the parent folder.

    Returns:
        policy_doc_df (pd.DataFrame): A pd.DataFrame containing all found files as rows and the corresponding file names
        and file paths as columns.
    """
    #get the paths and file names
    doc_names, doc_paths = list_docs(folder_path)

    doc_dict = {
        'policy_doc_names': doc_names,
        'policy_doc_paths': doc_paths
    }
    doc_df = pd.DataFrame(data=doc_dict, dtype='string')
    #set index as policy doc names (can clean up/add other column with a neater name without the .txt pieces later)
    doc_df['policy_doc_name_clean'] = (
        doc_df['policy_doc_names'].apply(
            lambda x: x.split('.txt')[0].split('.pdf.ocr')[0]))
    doc_df.index = doc_df['policy_doc_names']
    del doc_df['policy_doc_names']  #remove duplicate column
    return doc_df