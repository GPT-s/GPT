import sys

sys.path.append('../')
import unittest
from unittest.mock import patch, Mock
from datetime import datetime
from src.database import DataBase
from src.gpt import get_summary_list
from src.translator_deepl import DeeplTranslator
from src.crawler import InvestingCrawler



class TestInvestingCrawler(unittest.TestCase):
    @patch('crawler.webdriver.Chrome')
    def test_crawl_page(self, mock_driver):
        # Set up the mock driver
        mock_driver.return_value.find_element.return_value.text = 'Mock text'

        # Create an instance of InvestingCrawler
        crawler = InvestingCrawler()

        # Call the crawl_page method with a mock URL
        url = 'https://mockurl.com'
        text = crawler.crawl_page(url)

        # Assert that the mock driver was called with the correct URL
        mock_driver.return_value.get.assert_called_once_with(url)

        # Assert that the method returned the correct text
        self.assertEqual(text, 'Mock text')

        # Clean up
        crawler.driver.close()
        crawler.driver.quit()

    @patch.object(DataBase, 'insert_news')
    @patch.object(DataBase, 'select_news', return_value=[(1, 'https://mockurl1.com', '', datetime.now()), (2, 'https://mockurl2.com', '', datetime.now())])
    @patch.object(DataBase, 'update_news_summary')
    @patch.object(DeeplTranslator, 'translate', return_value='Mock summary')
    @patch('src.gpt.get_summary_list', return_value=['Mock text 1', 'Mock text 2'])
    def test_investing_latest(self, mock_gpt, mock_translator, mock_update, mock_select, mock_insert):
        # Create an instance of InvestingCrawler
        crawler = InvestingCrawler()

        # Call the investing_latest method
        latest_links, latest_text = crawler.investing_latest()

        # Assert that the select_news method was called
        mock_select.assert_called_once()

        # Assert that the crawl_page method was called for each news article
        self.assertEqual(crawler.crawl_page.call_count, 2)

        # Assert that the get_summary_list and translate methods were called with the correct arguments
        mock_gpt.assert_called_once_with(latest_text)
        mock_translator.assert_called_with('Mock text 2')

        # Assert that the update_news_summary method was called with the correct arguments
        mock_update.assert_has_calls([((1, 'Mock summary'),), ((2, 'Mock summary'),)])

        # Clean up
        crawler.driver.quit()

if __name__ == '__main__':
    unittest.main()
