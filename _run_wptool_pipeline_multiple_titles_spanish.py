import subprocess
import os
import json
from glob import glob

output_root = '/shared/nas/data/m1/wangz3/mongoDB_wiki/kairos_phase2b_scenarios/scenario_news_spanish'
# input_wikilinks_dir = "/shared/nas/data/m1/wangz3/mongoDB_wiki/kairos_phase2b_scenarios/scenario_titles_wikilinks"
input_wikilinks_dir = "/shared/nas/data/m1/wangz3/mongoDB_wiki/kairos_phase2b_scenarios/scenario_titles_wikilinks_dryrun"
lang_vairant = 'es'

## all scenarios
scenarios = sorted([os.path.basename(item)[:-5] for item in glob(os.path.join(input_wikilinks_dir,'*.json'))])
print(scenarios)
print(len(scenarios))

# scenarios = ['dummy_scenario']

for scenario_name in scenarios:
    input_json = os.path.join(input_wikilinks_dir, f"{scenario_name}.json")
    output_dir_path = os.path.join(output_root, scenario_name)
    os.makedirs(output_dir_path, exist_ok=True)
    cmd = f'python run_wptool.py --output_root "{output_dir_path}" --input_json "{input_json}" --lang_variant "{lang_vairant}"'
    print("command:", cmd + '\n')
    try:
        subprocess.call(cmd, shell=True)
    except Exception as e:
        print('unexpected error')
        print(e)