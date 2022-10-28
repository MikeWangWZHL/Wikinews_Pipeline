import subprocess
import os
import json

output_root = '/shared/nas/data/m1/wangz3/mongoDB_wiki/kairos_phase2b_scenarios/scenario_news'
# output_root = '/shared/nas/data/m1/wangz3/mongoDB_wiki/kairos_phase2b_scenarios/_test'

## batch 1,2 redo
scenarios = ["General_Crime", "Political_Corruption", "State_visits", "International_Negotiation", "Medical_research", "Chemical_Warfare", "Diplomacy", "Health_Care", "Medical_Procedure", "Organizational_Conflict", "Protest", "Sanction"]


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