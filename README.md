# LLMs

**Help desk** allows you to create a Question Answering bot with a streamlit UI using your company Confluence data.

<p align="center">
  <img src="./images/help_desk.gif" alt="animated" />
</p>

# Prerequisites

- Create a virtual environnement:
    - `python3.10 -m venv .venv`
    - `source .venv/bin/activate`
    - `pip install -r requirements.txt`

- Copy the env.template and fill your environment variables
     - `cp .env.template .env`

- Check the `config.py` and `env.template` file.
- To collect data from Confluence you will have to:
  - Create your own Conluence space with page informations
  - Create and feed your API key [here]('https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/')
  - Insert in the  `env` file:
    -  the space_key: `https://yoursite.atlassian.com/wiki/spaces/<space_key>/pages/`
    -  the space_name: `<space_name>/spaces/<space_key>/pages/`
    -  the email adress you used for your Confluence space
    -  the OpenAI API key

- To run the streamlit app run:
```
cd src
streamlit run streamlit.py
```

- To evaluate the quality of the RAG model:
```
# First replace the evaluation dataset file in the data folder with your topic questions
cd src
python evaluate.py
```

- To use and deep dive with the notebook
```
ipython kernel install --name RAG --user  # Add the notebook kernel
jupyter lab
```

## How it works ?
The process is the following:
- Loading data from Confluence
  - You can keep the Markdown style using the `keep_markdown_format` option added in our [MR]('https://github.com/langchain-ai/langchain/pull/8246')
  - See the `help_desk.ipynb` for a more deep dive analysis
  - Otherwise you cannot split text in a smart manner using the [MarkdownHeaderTextSplitter]('https://python.langchain.com/docs/modules/data_connection/document_transformers/text_splitters/markdown_header_metadata')
- Load data
- Markdown and RecursiveCharacterTextSplitter
- Open AI LLM et embedding
- QARetrievalChain
- Streamlit for visualizing data

