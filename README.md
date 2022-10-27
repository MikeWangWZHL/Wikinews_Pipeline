### Instruction
Depending on if the wikipedia page is in our current MongoDB dump (only some newest wikipages may not be found) do the following:

- **Option 1: Using MongoDB**: log in on `blender02` (note that MongoDB only works on blender02) , try running `run.sh` with the wikipedia page title of interest, if it exists in the MongoDB, it will directly output the scraled news article in the reference in both jsonl and rsd format (text only).

- **Option 2: Using wptools**: if above does not work, run each component individually using "wptools" package instead of the MongoDB dump,
    - first run: `get_external_link.py` to get the links in a json file with the help of wptools
    - then run: `crawl_news_from_url.py`  to get the news in a tmp dir (this is modified from Zoey's code)
    - then run: `process_crawled_tmp_to_single_json.py` to process the tmp dir

    There are some example code under `if __name__ == '__main__':` in each scripts

### Requirments
```
pymongo
wptools
spacy
spacy_langdetect
newspaper
nltk
tqdm
```