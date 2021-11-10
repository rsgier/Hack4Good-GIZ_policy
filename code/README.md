# GIZ Policy 
## Jina Example

This is a working example for jina.
So far it was just implemented with the first 60 lines from the Climate Change Whitepaper of South Africa. The goal is to expand the data input to all files.

### Requirements
1. Python 3.7
2. Install the packages from the `requirements.txt` file with `pip install -r requirements.txt`.
3. 2GB free space on your hard drive.

### Step 1: Indexing of the Data
Before we can perform neural search the data input has to be indexed. That means each sentence is transformed into a vector (embedding) which represents the semantic meaning of a sentence in a vector space.

Run:
```python jina_example.py -t index```

This will create a new folder in the code folder called `workspace`. This is where the embeddings are stored.

### Step 2: Query Your Data
Now that you ran the indexing you can query your data. The query is translated as well into the vector space. The best results are those vectors that are closest to the query vector.

Run:

```python jina_example.py -t query```

You will have to provide a query in the command line, as shown in the snapshot below, e.g. **What is Climate Change?** The results are printed below with the corresponding cosine-similarity score.

![Terminal-Snapshot](data/jina_example.png)