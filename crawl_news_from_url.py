import os 
import json 
import argparse 
import re 

from tqdm import tqdm 
import newspaper 
import multiprocessing as mp 
from functools import partial
from datetime import datetime 

import spacy
from spacy_langdetect import LanguageDetector
import shutil


nlp = spacy.load('en')
nlp.add_pipe(LanguageDetector(), name='language_detector', last=True)

# def worker(args, language='en', output_dir = 'tmp' ):
def worker(args, language=None, output_dir = 'tmp' ):
    idx, url = args 

    writer = open(f'{output_dir}/{idx}.json', 'w') 
    
    if url.split('.')[-1] == 'pdf':
        return 
    if ('books.google' in url) or ('page' in url) or ('parliament' in url):
        return 

    article = newspaper.Article(url)
    try:
        article.download()
        article.parse() 
    except newspaper.ArticleException:
        # print('url:{} not found'.format(url))
        return 

    
    if len(article.text) < 100:
        return 
    
    # detect language 
    doc = nlp(article.text)
    if language is not None and doc._.language['language'] !=language: # change language if needed 
        return 
    
    # TODO:check off-topic 

    kept_images = []
    for image in article.images:
        if ('logo' in image) or ('favicon' in image) or('icon' in image) or ('button' in image):
            continue 
        kept_images.append(image)
    
    article.images = kept_images
    article_json = {
        'url': url,
        'text': article.text,
        'title': article.title,
        'images': list(article.images),
        'videos': list(article.movies),
    } 

    if article.publish_date: 
        article_json['date'] = article.publish_date.strftime('%Y-%m-%d')
    
    
    
    writer.write(json.dumps(article_json) + '\n') 
    writer.close() 
    return 

def main_original():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-urls', type=str, )
    parser.add_argument('--threads', type=int, default=3)
    args = parser.parse_args() 

    ins_list = []
    with open(args.input_urls,'r') as f:
        for lidx, line in enumerate(f):
            ins_list.append((lidx, line.strip())) 
    
    os.makedirs('tmp')
    pool = mp.Pool(processes=args.threads)
    pool.map(worker, ins_list)
    pool.close()
    pool.join() 

def main_from_json():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_json', type=str)
    parser.add_argument('--threads', type=int, default=3)
    args = parser.parse_args() 


    # with open(args.input_urls,'r') as f:
    #     for lidx, line in enumerate(f):
    #         ins_list.append((lidx, line.strip())) 
    input_url_dict = json.load(open(args.input_json,'r')) 
    for key, value in input_url_dict.items():
        ins_list = []
        urls = value['urls']
        if len(urls) == 0:
            print(f'No url for article:{key}')
            continue
        for lidx, url in enumerate(urls):
            ins_list.append((lidx, url))
        key = key.replace(' ','_')
        os.makedirs(f'tmp/{key}')
        pool = mp.Pool(processes=args.threads)
        pool.map(partial(worker, output_dir = f'tmp/{key}'), ins_list)
        pool.close()
        pool.join() 
        print(f'done processing: {key}')

def get_news_from_jsonl(jsonl_path,tmp_dir,filter_language = None):
    with open(jsonl_path) as f:
        for line in tqdm(f):
            page_object = json.loads(line)
            key = page_object['title']
            ins_list = []
            urls = page_object['urls']
            print(f"crawling {len(urls)} news...\n")
            if len(urls) == 0:
                print(f'No url for article:{key}')
                continue
            for lidx, url in enumerate(urls):
                ins_list.append((lidx, url))
            key = key.replace(' ','_').replace('/','&')
            
            subdir = os.path.join(tmp_dir, key)
            if os.path.exists(subdir):
                shutil.rmtree(subdir)
            os.makedirs(subdir)
            
            pool = mp.Pool(processes=4)
            pool.map(partial(worker, output_dir = subdir, language = filter_language), ins_list)
            pool.close()
            pool.join() 
            print(f'done processing: {key}')

if __name__ == '__main__':
    
    # main_original()

    ## with an json input: modified from Zoey's code
    ''' usage example:
        python3 crawl_news_from_url.py --input-urls-json /shared/nas/data/m1/wangz3/Claim_detection/data/covid19_topic_ref_links.json
    '''
    main_from_json()
