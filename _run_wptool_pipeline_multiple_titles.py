import subprocess
import os
import json

output_root = '/shared/nas/data/m1/wangz3/mongoDB_wiki/kairos_phase2b_scenarios/scenario_news'
# output_root = '/shared/nas/data/m1/wangz3/mongoDB_wiki/kairos_phase2b_scenarios/_test'

## batch 3
scenarios = [
    "Warfare_related_to_Ukraine",
    "Coup",
    "Trading",
    "Transport_Accident",
    "Environmental_Protection",
    "Information_Campaign",
    "Cyber_attack",
    "Refugee_crisis",
    "Economic_recession_recovery"
]


for scenario_name in scenarios:
    input_json = os.path.join("/shared/nas/data/m1/wangz3/mongoDB_wiki/kairos_phase2b_scenarios/scenario_titles_wikilinks", f"{scenario_name}.json")
    output_dir_path = os.path.join(output_root, scenario_name)
    os.makedirs(output_dir_path, exist_ok=True)
    cmd = f'python run_wptool.py --output_root "{output_dir_path}" --input_json "{input_json}"'
    print("command:", cmd + '\n')
    try:
        subprocess.call(cmd, shell=True)
    except Exception as e:
        print('unexpected error')
        print(e)