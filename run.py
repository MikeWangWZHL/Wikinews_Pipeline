from pymongo import MongoClient
import json
import os
import argparse 
import shutil
from tqdm import tqdm
from glob import glob
from get_external_link import get_title_url_dict
from crawl_news_from_url import get_news_from_jsonl
from process_crawled_tmp_to_single_json import process_tmp
'''command for restarting mongodb:
/shared/nas/data/m1/xiaoman6/lib/mongodb-linux-x86_64-ubuntu1804-4.2.1/bin/mongod --dbpath /scratch/wangz3/db --wiredTigerCacheSizeGB 128
'''

def load_IED_jsonl(jsonl_path):
    with open(jsonl_path, 'r') as handle:
        articles = [json.loads(line) for line in handle]
    print(f'load {len(articles)} articles \n')
    return articles

def get_page(client, db_name, page_title):
    collection_name = 'pages'
    collection =  client[db_name][collection_name]
    query = {'title': page_title}
    print(f'number of documents found on page: {page_title}', collection.count_documents(query))
    # assert collection.count_documents(query) == 1
    if collection.count_documents(query) == 0:
        return None
    else:
        return collection.find(query)

# def get_page_fromQid(client, db_name, qid):
#     collection_name = 'pages'
#     collection =  client[db_name][collection_name]
#     query = {'id': qid}
#     print(f'number of documents found on {qid}', collection.count_documents(query))
#     # assert collection.count_documents(query) == 1
#     if collection.count_documents(query) == 0:
#         return None
#     else:
#         return collection.find(query)

def get_category(client, db_name,category):
    collection_name = 'pages'
    collection =  client[db_name][collection_name]
    query = {'categories': category}
    print(f'number of documents found on category: {category}', collection.count_documents(query))
    # assert collection.count_documents(query) == 1
    return collection.find(query)

def write_pages(output_dir, found_pages, title):
    output_path = os.path.join(output_dir,title.replace(' ','_').replace('/','&')+'.jsonl')
    with open(output_path,'w') as out:
        for page in tqdm(found_pages):
            title = page['title']
            url_dict = get_title_url_dict([title])
            if 'urls' not in url_dict[title]:
                continue
            page['urls'] = url_dict[title]['urls']
            out.write(json.dumps(page))
            out.write('\n')
            # out.write(json.dumps(page, indent = 4))
    return output_path


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
    parser.add_argument('--host', type=str, default = '0.0.0.0',required = True)
    parser.add_argument('--port', type=int, default = 27017, required = True)
    parser.add_argument('--db_name', type=str, default = 'enwiki', required = True)
    parser.add_argument('--title', type=str, default='none', required = False)
    parser.add_argument('--category', type=str, default="none", required = False)
    args = parser.parse_args() 

    # set up mongo db client
    host = args.host
    port = args.port
    db_name = args.db_name
    client = MongoClient(host=host, port=port)
    
    # get query
    title = args.title
    category = args.category
    output_root = args.output_root

    # get pages jsonl 
    if title == 'none' and category == 'none':
        raise ValueError('At least specify one of: \'--title\' or \'--category\' ')    
    if title != 'none':
        pages = get_page(client, db_name, title)
        output_name = 'page__'+title
    else:
        pages = get_category(client, db_name, category)
        output_name = 'category__'+category
    
    if pages is None:
        print("ERROR: no pages found, quit...\n\n")
        quit()

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

    # write out
    jsonl_output_path = write_pages(jsonl_dir, pages, output_name)

    # get news from url
    get_news_from_jsonl(jsonl_output_path, tmp_dir)

    # process tmp dir
    process_tmp(tmp_dir, processed_tmp_dir) 

    # get rsd 
    get_rsd_from_processed_tmp(processed_tmp_dir, rsd_dir)


if __name__ == '__main__':
    main()
    
    '''sanity check'''
    
    # host = '0.0.0.0'
    # port = 27017
    # client = MongoClient(host=host, port=port)
    # db_name = 'enwiki'
    # title = 'Election'
    # # title = '2016–2020 Yemen cholera outbreak'
    # pages = get_page(client, db_name, title)
    # # pages = get_category(client, db_name, 'Disease outbreaks')
    # # pages = get_category(client, db_name, 'Elections')
    # for p in pages:
    #     print(p['title'])
    #     # print(p['sections'])
    #     # print('<',p['article'],'>')
    # # write_pages(output_dir, pages, title)
    # # article = pages['article']
    # # print(article)


    ''' get IED articles '''
    # for senario in ['wiki_backpack_bombings','wiki_drone_strikes','wiki_ied_bombings','wiki_mass_car_bombings','wiki_suicide_bombings']:
    #     jsonl_path = f'/shared/nas/data/m1/wangz3/schema_composition/wikidata/data/{senario}.jsonl'
    #     output_dir = f'/shared/nas/data/m1/wangz3/schema_composition/wikidata/article_page_data/{senario}'
        
    #     print(f'===== on senario {senario} =====')


    #     # get article titles
    #     # page_titles = []
    #     page_titles = set()
    #     articles = load_IED_jsonl(jsonl_path)
    #     for article in articles:
    #         # page_titles.append(article['title'])
    #         if article['title'] in page_titles:
    #             print(f'exist title: ', article['title'] )
    #         page_titles.add(article['title'])
    #     # assert len(page_titles) == len(articles)
    #     print('page titles: ', len(page_titles))

    #     # get article from DB, and write to json
    #     for title in page_titles:
    #         write_pages(output_dir, get_page(client, db_name, title), title)

    '''get Disease Outbreak'''
    # output_dir = '/shared/nas/data/m1/wangz3/schema_composition/compositional-schema/wikidata/Disease_Outbreak/article_page_data_v2'
    # titles = json.load(open('/shared/nas/data/m1/wangz3/schema_composition/compositional-schema/wikidata/Disease_Outbreak/Epidemics_page_titles_v2.json'))
    # print(f'loaded {len(titles)} titles')
    # exist_articles = {}
    # for title in titles:
    #     if title not in exist_articles:
    #         pages = get_page(client, db_name, title)
    #         if pages is not None:
    #             # print(pages)
    #             write_pages(output_dir, pages , title)
    #             exist_articles[title] = True
    # print(f'wrote {len(exist_articles)} articles')

    '''get wiki pages from qnode'''
    # output_path = '/shared/nas/data/m1/wangz3/multimedia_attribute/qid2pages_temp.json'
    # qid2title = json.load(open('/shared/nas/data/m1/wangz3/multimedia_attribute/wiki_xiaoman/data/qid2enwiki.json'))
    # qids = ['Q7422106']
    # print(f'loaded {len(qids)} qids')
    # exist_articles = {}
    # for qid in qids:
    #     if qid not in exist_articles:
    #         if qid in qid2title:
    #             title = qid2title[qid]
    #         else:
    #             print(f'!QNODE NOT FOUND: {qid}')
    #             continue
    #         pages = get_page(client, db_name, title)
    #         if pages is not None:
    #             page_count = 0
    #             for page in pages:
    #                 exist_articles[qid] = page
    #                 page_count += 1
    #             assert page_count == 1
    #         else:
    #             print(f'!PAGE NOT FOUND: {title}')
    # print(exist_articles)


    # output_path = '/shared/nas/data/m1/wangz3/multimedia_attribute/qid2pages_temp.json'
    # qids = ['Q7422106']
    # print(f'loaded {len(qids)} qids')
    # exist_articles = {}
    # for qid in qids:
    #     if qid not in exist_articles:
    #         pages = get_page_fromQid(client, db_name, qid)
    #         if pages is not None:
    #             print(f'found {len(pages)} pages')
    #             exist_articles[qid] = [page for page in pages]
    #         print(exist_articles)




