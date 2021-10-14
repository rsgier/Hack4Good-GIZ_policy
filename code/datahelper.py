import pandas as pd
import os


def get_docs_df_from_folder(policy_doc_folder):
    """
    Takes in a folder (can also be with different subfolders) with policy-related text documents 
    and gathers txt docs to analyze from those folders and makes a dataframe of their names and paths.
    
    NOTE: If want to preserve names and paths of the documents and make them easily searchable, it might be useful 
    to export the dictionary/keep that as well to add more summary information about the document for instance. 
    """
    #get the paths and file names
    policy_doc_names, policy_doc_paths = list_docs(policy_doc_folder)
    #print the number of docs and the names of some of them
    print(("There are %d policy docs" % (len(policy_doc_names))),
          "Some of the policy docs include: ", policy_doc_names[:10])

    policy_doc_dict = {
        'policy_doc_names': policy_doc_names,
        'policy_doc_paths': policy_doc_paths
    }
    policy_doc_df = pd.DataFrame(data=policy_doc_dict, dtype='string')
    #set index as policy doc names (can clean up/add other column with a neater name without the .txt pieces later)
    policy_doc_df['policy_doc_name_clean'] = (
        policy_doc_df['policy_doc_names'].apply(
            lambda x: x.split('.txt')[0].split('.pdf.ocr')[0]))
    policy_doc_df.index = policy_doc_df['policy_doc_names']
    del policy_doc_df['policy_doc_names']  #remove duplicate column
    return policy_doc_df


def list_docs(folder):
    """
    Generates a list of document names for reference and tracking. 
    This command currently extracts the .txt documents from all the subfolders of a parent folder, 
    and filters out the ones containing source information, which we might not want to use in our analysis.
    """
    doc_names = []
    doc_paths = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.txt') and (file not in [
                    'Source.txt', 'Source Link.txt', 'Source Links.txt'
            ]):
                doc_names.append(file)
                doc_paths.append(os.path.join(root, file))
    return doc_names, doc_paths


if __name__ == "__main__":
    print(list_docs("texts"))