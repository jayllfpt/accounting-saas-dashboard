import unittest
import sys
import os
from dash import html

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.summary_stats import create_summary_card, create_summary_stats

class TestSummaryStats(unittest.TestCase):
    
    def test_create_summary_card(self):
        # Test with default color
        card = create_summary_card("Test Title", "Test Value")
        
        # Assert that the card is a Dash Div
        self.assertEqual(card.type, "Div")
        
        # Assert that the card has the correct className
        self.assertEqual(card.className, "summary-card")
        
        # Assert that the card has 2 children (title and value)
        self.assertEqual(len(card.children), 2)
        
        # Assert that the title is correct
        self.assertEqual(card.children[0].children, "Test Title")
        
        # Assert that the value is correct
        self.assertEqual(card.children[1].children, "Test Value")
        
        # Test with custom color
        card_custom = create_summary_card("Custom Title", "Custom Value", color="#FF0000")
        self.assertEqual(card_custom.children[1].style["color"], "#FF0000")
    
    def test_create_summary_stats(self):
        # Test with positive net cash flow
        stats = create_summary_stats(1000, 1500, 25, 500)
        
        # Assert that the stats is a Dash Div
        self.assertEqual(stats.type, "Div")
        
        # Assert that the stats has the correct className
        self.assertEqual(stats.className, "summary-stats-container")
        
        # Assert that the stats has 4 children (4 cards)
        self.assertEqual(len(stats.children), 4)
        
        # Assert that the net cash flow card has green color for positive value
        self.assertEqual(stats.children[3].children[1].style["color"], "#28a745")
        
        # Test with negative net cash flow
        stats_negative = create_summary_stats(1500, 1000, 25, -500)
        
        # Assert that the net cash flow card has red color for negative value
        self.assertEqual(stats_negative.children[3].children[1].style["color"], "#dc3545")

if __name__ == '__main__':
    unittest.main() 