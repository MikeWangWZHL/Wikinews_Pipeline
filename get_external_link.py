import json
import wptools
import re
from tqdm import tqdm
from collections import defaultdict
# Footnotes

def extract_refs(text): # TO-DO: offset
    RE_P1 = re.compile(r'<ref([> ].*?)(</ref>|/>)', re.DOTALL | re.UNICODE) 
    refs = []
    for i in re.findall(RE_P1, text):
        refs.append('<ref%s</ref>' % i[0])
    return refs

def get_title_url_dict(titles):
    
    article_ref_urls = defaultdict(dict)
    print('start querying pages...')
    for title in tqdm(titles):
        page = wptools.page(title)
        try:
            page.get_parse()
        except LookupError:
            print(f'{title}: page not found')
            continue
        urls = []
        for ref in extract_refs(page.data['wikitext']):
            urls += re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ref)
        
        article_ref_urls[title]['urls'] = urls
        # article_ref_urls[title]['wikitext'] = page.data['wikitext']
        
        # for url in urls:
        #     print(url)
        print(f'found {len(urls)} ref urls')
    
    return article_ref_urls

def main():
    '''load page titles'''
    # titles = json.load(open('/shared/nas/data/m1/wangz3/schema_composition/compositional-schema/wikidata/Disease_Outbreak/Epidemics_page_titles_v2.json'))
    # titles = ['Investigations into the origin of COVID-19','Transmission of COVID-19','Treatment and management of COVID-19','COVID-19 vaccine','Workplace hazard controls for COVID-19','COVID-19 misinformation','Social distancing measures related to the COVID-19 pandemic','Face masks during the COVID-19 pandemic']
    
    '''load category_titles dict'''
    # category_titles = json.load(open('/shared/nas/data/m1/wangz3/mongoDB_wiki/mongodb/Kairos_quizlet7/category_pagetitles.json'))
    # output_dict = {}
    # for key,title_list in category_titles.items():
    #     titles = [t['title'] for t in title_list]
    #     print(f'loaded {len(titles)} titles')
    #     article_ref_urls = get_title_url_dict(titles)
    #     output_dict[key] = article_ref_urls

    # with open('/shared/nas/data/m1/wangz3/mongoDB_wiki/mongodb/Kairos_quizlet7/topic_ref_links.json','w') as out:
    #     json.dump(output_dict, out, indent = 4)

if __name__ == '__main__':
    # main()

    # titles = ['Boston Marathon bombing','2016 New York and New Jersey bombings']
    titles = ['2022 Russian invasion of Ukraine']
    ext_links = get_title_url_dict(titles)
    with open('./single_pages/ext_links-2022_Russian_invasion_of_Ukraine.json', 'w') as out:
        json.dump(ext_links,out,indent=4)


