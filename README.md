### Instruction
Depending on if the wikipedia page is in our current MongoDB dump (only some newest wikipages may not be found) do the following:

- **Option 1: Using wptools**: [ Update 10/28 ] New pipeline using wptools to find pages (works on more recent pages, e.g., after 2022). Check `_run_wptool_pipeline_multiple_titles.py` on how to run the pipeline; The main script `run_wptool.py` takes in a json file as input which contains at lease a field named `titles` that stores a list of wikipage titles to be queried. Check `example_input_json/` for an example input.

- **Option 2: Using MongoDB (On Blender02 Server only)**: log in on `blender02`, try running `run.sh` with the wikipedia page title of interest, if it exists in the MongoDB, it will directly output the scraled news article in the reference in both jsonl and rsd format (text only).

<!-- - **Option 2: Using wptools**: if above does not work, run each component individually using "wptools" package instead of the MongoDB dump,
    - first run: `get_external_link.py` to get the links in a json file with the help of wptools
    - then run: `crawl_news_from_url.py`  to get the news in a tmp dir (this is modified from Zoey's code)
    - then run: `process_crawled_tmp_to_single_json.py` to process the tmp dir

    There are some example code under `if __name__ == '__main__':` in each scripts -->


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