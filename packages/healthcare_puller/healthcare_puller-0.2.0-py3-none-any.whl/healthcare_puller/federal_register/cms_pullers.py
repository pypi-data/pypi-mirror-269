import os

import requests
from tqdm import tqdm

RULE_URL = "https://www.federalregister.gov/api/v1/documents.json?fields[]=abstract&fields[]=docket_id&fields[]=document_number&fields[]=effective_on&fields[]=pdf_url&fields[]=topics&per_page=1000&conditions[agencies][]=centers-for-medicare-medicaid-services&conditions[type][]=RULE"
PRORULE_URL = "https://www.federalregister.gov/api/v1/documents.json?fields[]=abstract&fields[]=docket_id&fields[]=document_number&fields[]=effective_on&fields[]=pdf_url&fields[]=topics&per_page=1000&conditions[agencies][]=centers-for-medicare-medicaid-services&conditions[type][]=PRORULE"


def get_rule_json(datatype='rule', doc_limit=None):
    if datatype == 'rule':
        url = RULE_URL
    elif datatype == 'prorule':
        url = PRORULE_URL
    if doc_limit:
        url = url.replace("per_page=1000", f"per_page={doc_limit}")
    rule_json = requests.get(url).json()['results']
    if doc_limit:
        rule_json = rule_json[:doc_limit]
    return rule_json
    

def save_pdf(save_dir, url, check_exists):
    save_loc = f'{save_dir}/{url.split("/")[-1]}'
    response = requests.get(url)
    current_files = [ f"{save_dir}/{filename}" for filename in os.listdir(save_dir) ]
    if check_exists and save_loc in current_files:
        print(f"File {save_loc.split("/")[-1]} already exists, skipping")
    with open(save_loc, 'wb') as f:
        f.write(response.content)
        print(f"Saved to {save_loc}")


def save_cms_docs(save_dir, rule_type, doc_limit=None, check_exists=True):
    if rule_type not in ('rule', 'prorule'):
        print("Rule type must be rule or prorule")
        return
    rule_json = get_rule_json(rule_type, doc_limit)
    for rule in rule_json:
        save_pdf(save_dir, rule['pdf_url'], check_exists)
    print("All done!")







