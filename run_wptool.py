import json
import os
import argparse 
import shutil
from tqdm import tqdm
from glob import glob
from get_external_link import get_page, get_page_en_to_lang, get_ref_links_from_page_data, write_page_data_to_jsonl
from crawl_news_from_url import get_news_from_jsonl
from process_crawled_tmp_to_single_json import process_tmp


def get_rsd_from_processed_tmp(processed_tmp_dir, rsd_output_dir):
    url_jsonls = glob(os.path.join(processed_tmp_dir,'*.jsonl'))
    
    for input_jsonl in url_jsonls:
        title = os.path.basename(input_jsonl)[:-6]
        
        rsd_output_subdir = os.path.join(rsd_output_dir,title)
        if os.path.exists(rsd_output_subdir):
            shutil.rmtree(rsd_output_subdir)
        os.makedirs(rsd_output_subdir)
        
        with open(input_jsonl) as f:
            doc_idx = 0
            for line in f:
                news_object = json.loads(line)
                with open(os.path.join(rsd_output_subdir,f'{title}-{doc_idx}.rsd.txt'),'w') as out:
                    for news_line in news_object['text']:
                        out.write(news_line)
                        out.write('\n')
                doc_idx += 1



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_root', type=str, default=".", required = True)
    parser.add_argument('--input_json', type=str, default='none', required = True)
    parser.add_argument('--lang_variant', type=str, default='en', required = False) # input english title, output wikipage in <lang_vairant>

    # english: en
    # spanish: es
    # russian: ru

    args = parser.parse_args() 

    # get query
    input_json = json.load(open(args.input_json))
    output_root = args.output_root

    titles = input_json["titles"]
    
    print(titles)
    
    # page title mapping from english to other language variant
    title_mapping = {}

    for title in titles:
        output_name = 'page__'+title
        
        # page_data = get_page(title, lang=args.lang) # get page using wptool
        page_data = get_page_en_to_lang(title, lang_variant=args.lang_variant) # get page using wptool
        
        if page_data is None:
            print("ERROR: no pages found, skip...\n\n")
            continue

        # set up output dir
        if not os.path.exists(output_root):
            os.makedirs(output_root)
        # set up intermidate and output dirs
        jsonl_dir = os.path.join(output_root,'jsonl')
        tmp_dir = os.path.join(output_root,'tmp')
        processed_tmp_dir = os.path.join(output_root,'processed_tmp')
        rsd_dir = os.path.join(output_root,'rsd')
        os.makedirs(jsonl_dir, exist_ok=True)
        os.makedirs(tmp_dir, exist_ok=True)
        os.makedirs(rsd_dir, exist_ok=True)
        os.makedirs(processed_tmp_dir, exist_ok=True)

        # add urls to page_data
        page_data["urls"] = get_ref_links_from_page_data(page_data)
        
        # write out
        jsonl_output_path, title_in_en, title_in_lang_variant = write_page_data_to_jsonl(page_data, jsonl_dir, output_name)

        title_mapping[title_in_en] = title_in_lang_variant

        # get news from url
        get_news_from_jsonl(jsonl_output_path, tmp_dir, filter_language = args.lang_variant)

        # process tmp dir
        process_tmp(tmp_dir, processed_tmp_dir) 

        # get rsd 
        get_rsd_from_processed_tmp(processed_tmp_dir, rsd_dir)
    
    # output title mapping
    title_mapping_output_path = os.path.join(output_root,'title_mapping_to_lang_variant.json')
    with open(title_mapping_output_path, 'w') as out:
        json.dump(title_mapping, out, indent=4)


if __name__ == "__main__":
    main()