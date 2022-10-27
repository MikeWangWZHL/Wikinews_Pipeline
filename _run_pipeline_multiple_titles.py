import subprocess
import os
import json

output_root = '/shared/nas/data/m1/wangz3/mongoDB_wiki/kairos_phase2b_scenarios/scenario_news'

## test batch
# scenarios = ["_test", "_test_2"]

## batch one 10/24
# scenarios = ["General_Crime", "Political_Corruption", "State_visits", "International_Negotiation", "Medical_research", "Chemical_Warfare"]

## batch one 10/26
scenarios = ["Diplomacy", "Health_Care", "Medical_Procedure", "Organizational_Conflict", "Protest", "Sanction"]


for scenario_name in scenarios:
    titles_links = json.load(open(os.path.join("/shared/nas/data/m1/wangz3/mongoDB_wiki/kairos_phase2b_scenarios/scenario_titles_wikilinks", f"{scenario_name}.json")))
    output_dir_path = os.path.join(output_root, scenario_name)
    os.makedirs(output_dir_path, exist_ok=True)
    for title in titles_links['titles']:
        cmd = f'python3 run.py --output_root "{output_dir_path}" --title "{title}" --host 0.0.0.0 --port 27017 --db_name enwiki'
        print("command:", cmd + '\n')
        try:
            subprocess.call(cmd, shell=True)
        except Exception as e:
            print('unexpected error')
            print(e)