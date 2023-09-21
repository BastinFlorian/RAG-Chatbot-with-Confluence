# Imports
# Env var
import os
import sys
from dotenv import load_dotenv, find_dotenv

# Env variables
sys.path.append('../..')
_ = load_dotenv(find_dotenv())

OPEN_AI_API_KEY = os.environ['OPENAI_API_KEY']

CONFLUENCE_SPACE_NAME = os.environ['CONFLUENCE_SPACE_NAME']  # Change to your space name
CONFLUENCE_API_KEY = os.environ['CONFLUENCE_PRIVATE_API_KEY']
# https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/
CONFLUENCE_SPACE_KEY = os.environ['CONFLUENCE_SPACE_KEY']
# Hint: space_key and page_id can both be found in the URL of a page in Confluence
# https://yoursite.atlassian.com/wiki/spaces/<space_key>/pages/<page_id>
CONFLUENCE_USERNAME = os.environ['EMAIL_ADRESS']
PATH_NAME_SPLITTER = './splitted_docs.jsonl'
PERSIST_DIRECTORY = './db/chroma/'
EVALUATION_DATASET = '../data/evaluation_dataset.tsv'
