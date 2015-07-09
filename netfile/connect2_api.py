import json
import csv
import logging
import sys

logger = logging.getLogger(__name__)

from swaggerpy.client import SwaggerClient

CONNECT2_SPEC = "https://netfile.com/Connect2/api/resources"

def paginated_query(func):
    """
    Paginated Query Decorator

    Decorates the query by returning a generator, making
    additional requests for each page of responses.
    """

    def _paginated_query(self, query):
        page_index = 0
        query.update({
            'currentPageIndex': page_index,
            })

        response = func(self, query)
        assert response.status_code == 200

        pages = response.json()['totalMatchingPages']
        logger.info("Fetching page %d of %d pages available" % (page_index, pages))
        pages = min(pages, 2) #TODO Once the queries are set, unlimit this. For now, limit to two pages of data

        results = response.json()['results']
        while True:
            page_index += 1
            for result in results:
                yield result

            if page_index >= pages:
                break

            # Fetch another page
            query['currentPageIndex'] = page_index
            logger.info("Fetching page %d of %d pages available" % (page_index, pages))
            response = func(self, query)
            assert response.status_code == 200
            results = response.json()['results']

    return _paginated_query



class Connect2API(object):
    """Netfile Connect2 API"""

    def __init__(self):
        self.api = SwaggerClient(CONNECT2_SPEC)

    def getpubliccampaignagencies(self):
        """
        GET /pubic/campaign/agencies
        """
        response = self.api.public.getpubliccampaignagencies()
        assert response.status_code == 200

        data = response.json()
        assert data.has_key('agencies')

        return data['agencies']

    @paginated_query
    def postpubliccampaignsearchtransactionquery(self, query):
        """
        POST /public/campaign/search/transaction/query
        """
        return self.api.public.postpubliccampaignsearchtransactionquery(Query=query)

    def getpubliccampaignlisttransactiontypes(self):
        """
        GET /pubic/campaign/list/transaction/types
        """
        response = self.api.public.getpubliccampaignlisttransactiontypes()
        assert response.status_code == 200

        data = response.json()
        assert data.has_key('items')

        return data['items']

    @paginated_query
    def postpubliccampaignexportcal201transactionyear(self, query):
        """
        POST /public/campaign/export/cal201/transaction/year
        """
        return self.api.public.postpubliccampaignexportcal201transactionyear(ByYear=query)



def demo():
    connect2 = Connect2API()
    csvfile = sys.stdout


    transactions = connect2.postpubliccampaignsearchtransactionquery({
        #'TransactionType': transaction_id,
        #'Agency': 52, # SF Ethics Commission
        'Aid': 'CA', # 
        'Year': 2014,
        #'Agency': 129, # California SOS
        #'transactionType': 30, # Form 460
        #'DateStart': '2015-01-01T00:00:00Z',
        'sortOrder': 1, # DateDescending
        })

    # Transactions in SF
    transaction = transactions.next() # Work-around generator magic
    headers = transaction.keys()
    transaction_csv = csv.DictWriter(csvfile, headers)
    transaction_csv.writeheader()
    for transaction in transactions:
        transaction_csv.writerow(transaction)
    return

    # Agencies
    agencies = connect2.getpubliccampaignagencies()
    headers = agencies[0].keys()
    agency_csv = csv.DictWriter(csvfile, headers)
    agency_csv.writeheader()
    for agency in agencies:
        agency_csv.writerow(agency)

    transactions = connect2.postpubliccampaignsearchtransactionquery({
        'Agency': 52, # SF Ethics Commission
        #'Agency': 129, # California SOS
        #'transactionType': 30, # Form 460
        'DateStart': '2015-01-01T00:00:00Z',
        'sortOrder': 1, # DateDescending
        })

    # Transactions in SF
    transaction = transactions.next() # Work-around generator magic
    headers = transaction.keys()
    transaction_csv = csv.DictWriter(csvfile, headers)
    transaction_csv.writeheader()
    for transaction in transactions:
        transaction_csv.writerow(transaction)


if __name__ == '__main__':
    demo()
