import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from collections import defaultdict
from solution import fetch_page, process_page, get_animals_count, write_to_csv
import csv
import os

class TestAnimalCount(unittest.IsolatedAsyncioTestCase):
    
    async def test_fetch_page_success(self):
        mock_session = MagicMock()
        mock_response = AsyncMock()
        mock_response.text.return_value = "<html>test content</html>"
        mock_session.get.return_value.__aenter__.return_value = mock_response
        
        result = await fetch_page(mock_session, "http://test.url")
        self.assertEqual(result, "<html>test content</html>")
    
    @patch('solution.BeautifulSoup')
    async def test_process_page_with_valid_data(self, mock_bs):
        mock_soup = MagicMock()
        mock_bs.return_value = mock_soup
        
        mock_category_block = MagicMock()
        mock_soup.find.return_value = mock_category_block
        
        mock_group1 = MagicMock()
        mock_h3_1 = MagicMock()
        mock_h3_1.text.strip.return_value = 'А'
        mock_group1.find.return_value = mock_h3_1
        mock_li_1 = [MagicMock(), MagicMock(), MagicMock()]
        mock_group1.find_all.return_value = mock_li_1
        
        mock_group2 = MagicMock()
        mock_h3_2 = MagicMock()
        mock_h3_2.text.strip.return_value = 'Б'
        mock_group2.find.return_value = mock_h3_2
        mock_li_2 = [MagicMock(), MagicMock()]
        mock_group2.find_all.return_value = mock_li_2
        
        mock_category_block.find_all.return_value = [mock_group1, mock_group2]
        
        mock_next_page = MagicMock()
        mock_next_page.__getitem__.return_value = "/next_page"
        mock_soup.find.side_effect = [mock_category_block, mock_next_page]
        
        mock_session = MagicMock()
        mock_response = AsyncMock()
        mock_response.text.return_value = "<html>test</html>"
        mock_session.get.return_value.__aenter__.return_value = mock_response
        
        counts = defaultdict(int)
        url = "http://test.url"
        
        result = await process_page(mock_session, url, counts)
        
        self.assertEqual(result, "https://ru.wikipedia.org/next_page")
        self.assertEqual(counts['А'], 3, "Должно быть 3 элемента для буквы А")
        self.assertEqual(counts['Б'], 2, "Должно быть 2 элемента для буквы Б")
    
    @patch('solution.BeautifulSoup')
    async def test_process_page_with_english_letter(self, mock_bs):
        mock_soup = MagicMock()
        mock_category_block = MagicMock()
        mock_soup.find.return_value = mock_category_block
        
        mock_group = MagicMock()
        mock_h3 = MagicMock()
        mock_h3.text.strip.return_value = 'A'
        mock_group.find.return_value = mock_h3
        mock_category_block.find_all.return_value = [mock_group]
        
        mock_bs.return_value = mock_soup
        
        mock_session = MagicMock()
        mock_response = AsyncMock()
        mock_response.text.return_value = "<html>test</html>"
        mock_session.get.return_value.__aenter__.return_value = mock_response
        
        counts = defaultdict(int)
        result = await process_page(mock_session, "http://test.url", counts)
        
        self.assertEqual(result, 'break')
        self.assertEqual(len(counts), 0)
    
    @patch('solution.process_page')
    async def test_get_animals_count(self, mock_process_page):
        mock_process_page.side_effect = [
            "http://page2",
            "http://page3",
            "break"
        ]
        
        counts = await get_animals_count()
        self.assertIsInstance(counts, defaultdict)
        self.assertEqual(mock_process_page.call_count, 3)

class TestCSVWriting(unittest.TestCase):
    
    def setUp(self):
        self.test_counts = {'А': 10, 'Б': 5, 'В': 3}
        self.filename = 'beasts.csv'
    
    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
    
    def test_write_to_csv(self):
        write_to_csv(self.test_counts)
        
        self.assertTrue(os.path.exists(self.filename))
        
        with open(self.filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
        expected_rows = [['А', '10'], ['Б', '5'], ['В', '3']]
        self.assertEqual(rows, expected_rows)

if __name__ == "__main__":
    unittest.main()