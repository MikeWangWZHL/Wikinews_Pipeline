import wptools

def get_page_en_to_lang(title, lang_variant='en'):
    page = wptools.page(title, lang='en')
    
    if lang_variant != 'en':
        try:
            # find title in another language using wikidata
            page_title_in_lang_variant = wptools.page(wikibase = page.get_parse().data['wikibase'], lang = lang_variant).get_wikidata().data['title']
            page = wptools.page(page_title_in_lang_variant, lang = lang_variant)
        except:
            print(f'{title}: page not found in {lang_variant}')
            return None
    try:
        page.get_parse()
        return page.data
    except LookupError:
        print(f'{title}: page not found in En')
        return None


english_page_title = "Russo-Ukrainian War"
# lang = "en"

# english_page_title = "Guerra ruso-ucraniana"
lang = "es"
# lang = "ru"

page = get_page_en_to_lang(english_page_title, lang_variant=lang)
print(page.keys())


# page = wptools.page(wikibase = "Q15860072", lang='es')
# page_wikidata = page.get_wikidata().data
# lang_variant_title = page_wikidata['title']
# page = wptools.page(lang_variant_title, lang='es')
# page.get_parse()