'''
NCBI REST API for https://eutils.ncbi.nlm.nih.gov/entrez/eutils
'''
import os
import time
import urllib.parse
import logging
import logging.config
import pandas as pd
from bs4 import BeautifulSoup
import requests
from pub_worm.impact_factor.impact_factor_lookup import get_impact_factor

try:
    logging.config.fileConfig('logging.config')
except Exception:
    logging.basicConfig(filename='pub_worm_entrez.log', level=logging.DEBUG)

# Create a logger object
logger = logging.getLogger(__name__)

class EntrezAPI:

    def __init__(self):
        self.base_url_str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        self.max_retries = 3
        self.timeout = 20
        self.function = "esearch"
        self.api_key = os.environ.get('NCBI_API_KEY', None)


    def _rest_api_call(self, params, data=None):
        url_str = f"{self.base_url_str}/{self.function}.fcgi"
        params['retmode']='xml'

        if self.api_key:
            params['api_key'] = self.api_key

        query = '&'.join([f"{urllib.parse.quote(k, 'utf-8')}={urllib.parse.quote(v, 'utf-8')}" for k, v in params.items()])
        url_str = f"{url_str}?{query}"
        logger.debug(url_str)

        #self.max_retries = 3
        retry = 0
        done = False

        api_result = None
        api_error = "No Error Set"

        def handle_error(error_msg):
            print(error_msg)
            logger.debug(error_msg)
            nonlocal done, retry, api_error
            retry +=1
            if retry >= self.max_retries:
                done = True
                api_error = error_msg

        while not done:
            try:
                if data:
                    post_data = { "id": ",".join(data) } 
                    response = requests.post(url_str, data=post_data, timeout=self.timeout)
                else:
                    response = requests.get(url_str, timeout=self.timeout)

                response.raise_for_status()  # Check for HTTP errors
                if response.status_code == 200:
                    done = True
                    api_result = response.text
                elif response.status_code == 429:
                    handle_error(f"Request limiter hit. waiting 2 seconds [Retry: {retry + 1}] code: {response.status_code}")
                    time.sleep(2)
                else:
                    handle_error(f"Failed to retrieve data. | Retry- {retry +1} | Response code- {response.status_code}")

            except Exception as ex:
                aviod_logging_interpolation=f"Error while calling url_str {str(ex)}"
                logger.error(aviod_logging_interpolation)
                error_msg=f"Unexpected Error | Retry- {retry+1} | Response msg- {str(ex)}"
                if isinstance(ex, requests.exceptions.HTTPError):
                        error_msg = f"Check the format of the http request [Retry: {retry + 1}] code: {str(ex)}"
                elif isinstance(ex, requests.exceptions.ConnectionError):
                        error_msg = f"Connection Error [Retry: {retry + 1}] code: {str(ex)}"
                elif isinstance(ex, requests.exceptions.Timeout):
                        error_msg = f"Timeout Error [Retry: {retry + 1}] code: {str(ex)}"
                handle_error(error_msg)

        if api_result is None:
            api_result = f"<response><rest_api_error>{api_error}</rest_api_error></response>"

        if logger.isEnabledFor(logging.DEBUG):
            soup = BeautifulSoup(api_result, "xml")
            # Pretty-print the XML content
            pretty_data = soup.prettify()
            with open('http_response.xml', 'w') as file:
                file.write(pretty_data)
            logger.debug(pretty_data)

        return api_result


    def _get_tag(self, soup, path_names):
        root = soup
        for path_name in path_names:
            logger.debug(f"get_tag {type(root)} {root} {path_name}")
            root = root.find(path_name, default='')
        return root

    def _get_tag_text(self, doc, tag_name, attribute=None):
        if attribute:
            tag = doc.find(tag_name, attribute)
        else:
            tag = doc.find(tag_name)
        return tag.text if tag else ""


    def entreze_esearch(self, params):
        self.function="esearch"
        esearch_params = {}
        esearch_params['db']         = params.get('db', 'pubmed')
        esearch_params['retmax']     = params.get('retmax', '200')
        esearch_params['usehistory'] = "y"
        esearch_params['term']       = params.get('term', None)
        if esearch_params['term'] is None:
            logger.debug("Param 'searchTerm' is required but not passed.")

        api_result = self._rest_api_call(esearch_params)
        ret_params = self._history_key_to_json(api_result)
        return ret_params

    def entreze_epost(self, data, params={}):
        self.function="epost"
        epost_params = {}
        epost_params['db']     = params.get('db', 'pubmed')
        if data is None:
            logger.debug("Param 'data' is required but not passed.")

        api_result = self._rest_api_call(epost_params, data)
        ret_params = self._history_key_to_json(api_result)
        ret_params['count'] = len(data)
        return ret_params

    def _history_key_to_json(self, api_result):
        ret_params = {}
        ret_params['function'] = self.function
        # Parse the XML response using BeautifulSoup
        soup = BeautifulSoup(api_result, "xml")
        # Extract WebEnv and QueryKey
        count     = self._get_tag_text(soup, "Count")
        ret_max   = self._get_tag_text(soup, "RetMax")
        ret_start = self._get_tag_text(soup, "RetStart")
        web_env   = self._get_tag_text(soup, "WebEnv")
        query_key = self._get_tag_text(soup, "QueryKey")
        api_error = self._get_tag_text(soup, "rest_api_error")
        if count:
            ret_params['count'] = count
        if ret_max:
            ret_params['ret_max'] = ret_max
        if ret_start:
            ret_params['ret_start'] = ret_start

        ret_params['query_key'] = query_key
        ret_params['WebEnv']    = web_env
        if api_error:
            logger.error("Error in history_key_to_json")
            ret_params = {}
            ret_params["Error"] = api_error
        return ret_params

    def entreze_pmid_summaries(self, params):
        paper_summarys = []
        soup = self._entreze_get_data(params, "esummary")
        if soup is None:
            return paper_summarys
        
        # Extract information for each UID
        for doc in soup.find_all("DocSum"):
            uid         = self._get_tag_text(doc, "Id")
            issn        = self._get_tag_text(doc, "Item", {"Name": "ISSN"})
            essn        = self._get_tag_text(doc, "Item", {"Name": "ESSN"})
            last_author = self._get_tag_text(doc, "Item", {"Name": "LastAuthor"})
            pmc_id      = self._get_tag_text(doc, "Item", {"Name": "pmc"})
            title       = self._get_tag_text(doc, "Item", {"Name": "Title"})
            source      = self._get_tag_text(doc, "Item", {"Name": "Source"})
            
            paper_summary = {
                "uid"         : uid,
                "issn"        : issn,
                "essn"        : essn,
                "last_author" : last_author,
                "pmc_id"      : pmc_id,
                "title"       : title,
                "source"      : source
            }
            paper_summarys.append(paper_summary)

        return paper_summarys

    def entreze_efetch(self, params):
        logger.debug("Entering entreze_efetch!!")
        efetch_results = []

        rec_count = int(params.get('count', 0))
        restart = 0
        while rec_count > 0 :
            params['restart'] = restart
            soup = self._entreze_get_data(params, "efetch")
            if soup is None:
                return efetch_results
            
            root_element = soup.find()
            if root_element.name == 'PubmedArticleSet':
                logger.debug("root_element == PubmedArticleSet!!")
                pubmed_articles = self._get_pubmed_articles(soup)
                # Get PubmedArticleSet
                efetch_results += pubmed_articles

            restart   +=200 # Increment record position by 200
            rec_count -=200 # Pull the next 200 records or however many are remaining
        

        return efetch_results
    
    def _get_pubmed_articles(self, soup):
        articles = []

        pubmed_articles = soup.find_all('PubmedArticle')
        # Iterate over the <PubmedArticle> elements
        for pubmed_article in pubmed_articles:
            article = {}
            medline_citation = self._get_tag(pubmed_article, ['MedlineCitation'])
            article_details  = self._get_tag(medline_citation, ['Article'])
            abstract_details = self._get_tag(article_details, ['Abstract'])
            journal          = self._get_tag(article_details, ['Journal'])
            pub_date         = self._get_tag(journal, ['JournalIssue', 'PubDate'])

            article['pmid']     = self._get_tag_text(medline_citation, "PMID")
            article['issn']     = self._get_tag_text(journal, "ISSN", {"IssnType": "Print"})
            article['eissn']    = self._get_tag_text(journal, "ISSN", {"IssnType": "Electronic"})
            article['pub_year'] = self._get_tag_text(pub_date, "Year")
            article['pub_abbr'] = self._get_tag_text(journal, "ISOAbbreviation")
            article['title']    = self._get_tag_text(article_details, "ArticleTitle")
            article['abstract'] = self._get_tag_text(abstract_details, "AbstractText")
            if article['issn']:
                article['impact_factor'] = get_impact_factor(article['issn'])
            if 'impact_factor' not in article:
                article['impact_factor'] = get_impact_factor(article['eissn'])

            articles.append(article)

        return articles

    def _entreze_get_data(self, params, function):
        self.function = function
        efetch_params = {}
        efetch_params['db']  = params.get('db', 'pubmed')

        required_params = ['query_key', 'WebEnv']
        for param_name in required_params:
            if param_name in params:
                efetch_params[param_name] = params[param_name]
            else:
                logger.debug(f"Param '{param_name}' is required but not passed")
                return None

        api_result = self._rest_api_call(efetch_params)
        # Parse the XML response using BeautifulSoup
        soup = BeautifulSoup(api_result, "xml")

        api_error = self._get_tag_text(soup,"rest_api_error")
        if api_error:
            logger.error("Error in _entreze_get_data")
            # Maybe throw and exception here
            return None
        
        return soup
