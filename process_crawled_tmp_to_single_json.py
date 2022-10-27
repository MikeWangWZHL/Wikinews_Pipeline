import json
from glob import glob
import os
from nltk.tokenize import sent_tokenize, word_tokenize

# input_tmp_dir = '/shared/nas/data/m1/wangz3/Claim_detection/src/tmp'
# output_dir = '/shared/nas/data/m1/wangz3/Claim_detection/data/covid_topic_news'


def process_tmp(input_tmp_dir, output_dir):
    article_dirs = glob(os.path.join(input_tmp_dir,'*'))
    # print(article_dirs)
    for article_dir in article_dirs:
        ref_jsonls = sorted(glob(os.path.join(article_dir,'*.json')))
        article_name = os.path.basename(article_dir)
        news_count = 0
        with open(os.path.join(output_dir,article_name + '.jsonl'), 'w') as out:    
            for ref in ref_jsonls:
                if os.path.getsize(ref) != 0:
                    with open(ref,'r') as f:
                        for line in f:
                            news_object = json.loads(line)
                            news_object['text'] = sent_tokenize(news_object['text'])
                            out.write(json.dumps(news_object) + '\n')
                            news_count += 1
                            break
        print(f'processed tmp for article: {article_name}, news count: {news_count}')

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

if __name__ == '__main__':
    input_tmp_dir = '/shared/nas/data/m1/wangz3/mongoDB_wiki/wikinews_pipeline/single_pages/tmp'
    output_jsonl_dir = '/shared/nas/data/m1/wangz3/mongoDB_wiki/wikinews_pipeline/single_pages/2022_Russian_invation_of_Ukraine/jsonl'
    rsd_output_dir = '/shared/nas/data/m1/wangz3/mongoDB_wiki/wikinews_pipeline/single_pages/2022_Russian_invation_of_Ukraine/rsd'
    if not os.path.exists(output_jsonl_dir):
        os.makedirs(output_jsonl_dir)
    if not os.path.exists(rsd_output_dir):
        os.makedirs(rsd_output_dir)
    process_tmp(input_tmp_dir, output_jsonl_dir)
    get_rsd_from_processed_tmp(output_jsonl_dir, rsd_output_dir)