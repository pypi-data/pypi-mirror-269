# chemsource v1.0.0
`chemsource` is a tool to classify novel drugs and other chemicals by source that is currently offered in Python. The current iteration, `v1.0.0`, relies on information scraped from [Wikipedia](https://www.wikipedia.org/) and the NLM's [PubMed](https://pubmed.ncbi.nlm.nih.gov/) abstract database. Information retrieved is classified using OpenAI's [ChatGPT API](https://platform.openai.com/docs/api-reference) into a combination of 5 categories, `MEDICAL, ENDOGENOUS, FOOD, PERSONAL CARE,` or `INDUSTRIAL`. Chemicals without enough available information will be classified with the tag `INFO`.

## Installation & Setup
`chemsource` is available on `pypi` or can alternatively be downloaded directly from the GitHub repository. To use the classification feature of `chemsource`, users must have an OpenAI API key that can be provided to the model along with credits associated with the key. Information on where to find the key can be found [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key). Credits can be added to your OpenAI account [here](https://platform.openai.com/account/billing/overview). 
See `Cost` for more information.

## Usage

## Cost
`chemsource` as a package is available with no additional charge to all users. However, the use of OpenAI's ChatGPT models within the classification step of the package is a service that costs money due to the energetically demanding nature of Large Language Models. 