#!pip install wikipedia
#IMPORTANT IN FINAL VERSION, FIGURE OUT HOW TO EITHER QUERY WITHOUT
#PUBMED KEY OR HOW TO GET A PUBMED KEY FROM USER

from .exceptions import XMLParseError, XMLRetrievalError
from .exceptions import XMLParseError2, XMLRetrievalError2, JoinError

from lxml import etree
import re
import requests as r
import wikipedia

SEARCH_PARAMS = {'db': 'pubmed',
                 'term': '',
                 'retmax': '3',
                 'usehistory': 'n',
                 'sort': 'relevance',
                 'api_key': None
                 }

XML_RETRIEVAL_PARAMS = {'db': 'pubmed',
                        'query_key': '1',
                        'WebEnv': '',
                        'rettype': 'abstract',
                        'retmax': '3',
                        'api_key': None
                        }

def retrieve(name, priority="WIKIPEDIA", single_source=False, ncbikey=None):
    if (priority == "WIKIPEDIA" and not single_source):
        try:
            description = wikipedia_retrieve(name)
            info_source = "WIKIPEDIA"
        except:
            try:
                description = pubmed_retrieve(name, ncbikey)
                info_source = "PUBMED"
            except:
                description = None
                info_source = None
    elif (priority == "PUBMED" and not single_source):
        try:
            description = pubmed_retrieve(name, ncbikey)
            info_source = "PUBMED"
        except:
            try:
                description = wikipedia_retrieve(name)
                info_source = "WIKIPEDIA"
            except:
                description = None
                info_source = None
    
    elif (priority == "WIKIPEDIA" and single_source):
        try:
            description = wikipedia_retrieve(name)
            info_source = "WIKIPEDIA"
        except:
            description = None
            info_source = None
    
    elif (priority == "PUBMED" and single_source):
        try:
            description = pubmed_retrieve(name, ncbikey)
            info_source = "PUBMED"
        except:
            description = None
            info_source = None
    
    else:
        raise ValueError("priority must be either WIKIPEDIA or PUBMED" 
                         + "and single_source must be a boolean value")

    return info_source, description
    
def pubmed_retrieve(drug, ncbikey=None):
    temp_search_params = SEARCH_PARAMS
    temp_search_params['api_key'] = ncbikey

    if (temp_search_params["api_key"] is None):
        del temp_search_params["api_key"]
    temp_search_params['term'] = drug + '[ti]'

    try:
        xml_content = etree.fromstring(r.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?", 
                                             params=temp_search_params).content)
    except:
        raise XMLParseError
    try:
        if (str(xml_content.find(".//Count").text) == 0):
            return 'NO_RESULTS'
    except:
        raise XMLRetrievalError
    else:
        temp_retrieval_params = XML_RETRIEVAL_PARAMS
        temp_retrieval_params['api_key'] = ncbikey

        if (temp_retrieval_params["api_key"] is None):
            del temp_retrieval_params["api_key"]
        temp_retrieval_params['WebEnv'] = xml_content.find(".//WebEnv").text
        try:
            retrieval_content = etree.fromstring(r.get(('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?'), 
                                                       params=temp_retrieval_params
                                                       ).content)
        except:
            raise XMLParseError2
        try:
            abstracts = retrieval_content.findall(".//AbstractText")
        except:
            raise XMLRetrievalError2
        result = ''
        try:
            for abstract in abstracts:
                result = result + ' ' + abstract.text
        except:
            raise JoinError
        return result

def wikipedia_retrieve(drug):
    description = wikipedia.page(drug, auto_suggest=False).content
    description = description.replace('\n', ' ')
    description = description.replace('\t', ' ')
    description = ' '.join(description.split())
    return description