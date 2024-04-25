from datetime import datetime
import os

import pandas as pd
import requests
from tqdm import tqdm

RULE_URL = "https://www.federalregister.gov/api/v1/documents.json?fields[]=abstract&fields[]=docket_id&fields[]=document_number&fields[]=effective_on&fields[]=pdf_url&fields[]=topics&per_page=1000&conditions[agencies][]=centers-for-medicare-medicaid-services&conditions[type][]=RULE"
PRORULE_URL = "https://www.federalregister.gov/api/v1/documents.json?fields[]=abstract&fields[]=docket_id&fields[]=document_number&fields[]=effective_on&fields[]=pdf_url&fields[]=topics&per_page=1000&conditions[agencies][]=centers-for-medicare-medicaid-services&conditions[type][]=PRORULE"
PUBLIC_INSPECTION_URL = "https://www.federalregister.gov/api/v1/public-inspection-documents.json?fields[]=agency_names&fields[]=pdf_url&fields[]=publication_date&fields[]=title&per_page=1000&conditions[available_on]=2024-04-24&conditions[agencies][]=centers-for-medicare-medicaid-services&conditions[type][]=RULE"


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


def get_public_inspection_json(doc_limit=None, date=None):
    if not date:
        date = datetime.today().strftime("%Y-%m-%d")
    url = PUBLIC_INSPECTION_URL.replace("2024-04-24", date)
    pi_json = requests.get(url).json()['results']
    needed_data = [ item for item in pi_json if 'Centers for Medicare & Medicaid Services' in item['agency_names']]
    if doc_limit:
        return needed_data[:doc_limit]
    else:
        return needed_data


def save_pdf(save_dir, url, check_exists):
    save_loc = f'{save_dir}/{url.split("/")[-1]}'
    response = requests.get(url)
    current_files = [ f"{save_dir}/{filename}" for filename in os.listdir(save_dir) ]
    if check_exists and save_loc in current_files:
        print(f"File {save_loc.split("/")[-1]} already exists, skipping")
    with open(save_loc, 'wb') as f:
        f.write(response.content)
        print(f"Saved to {save_loc}")


def save_cms_docs(save_dir, rule_type, doc_limit=None, check_exists=True, date=None):
    if rule_type not in ('rule', 'prorule', 'public_inspection'):
        print("Rule type must be rule or prorule")
        return
    if rule_type == 'public_inspection':
        rule_json = get_public_inspection_json(doc_limit=doc_limit, date=date)
    else:
        rule_json = get_rule_json(rule_type, doc_limit)
    for rule in rule_json:
        save_pdf(save_dir, rule['pdf_url'], check_exists)


def get_cms_rule_lookup(rule_type, doc_limit=None, save_csv=False, save_loc=None):
    rule_json = get_rule_json(rule_type, doc_limit)
    df = pd.DataFrame(rule_json)
    df['implied_pdf_name'] = df['pdf_url'].apply(lambda x: x.split("/")[-1])
    if save_csv:
        df.to_csv(save_loc, index=False)
    else:
        return df







