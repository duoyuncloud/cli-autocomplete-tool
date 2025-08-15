# tests/test_predictor.py
"""
Tests for the predictor module.
"""

import unittest
from core.predictor import predict_with_context, predict_rule_based
from core.utils import extract_command_context


class TestPredictor(unittest.TestCase):
    """Test cases for the predictor module."""
    
    def test_basic_command_completion(self):
        """Test basic command completion."""
        suggestions = predict_with_context("git", 3)
        self.assertIn("add", suggestions)
        self.assertIn("commit", suggestions)
        self.assertIn("push", suggestions)
    
    def test_subcommand_completion(self):
        """Test subcommand completion."""
        suggestions = predict_with_context("git comm", 8)
        self.assertIn("commit", suggestions)
    
    def test_flag_completion(self):
        """Test flag completion."""
        suggestions = predict_with_context("git commit -", 12)
        self.assertIn("-m", suggestions)
        self.assertIn("--message", suggestions)
        self.assertIn("--amend", suggestions)
    
    def test_docker_completion(self):
        """Test Docker command completion."""
        suggestions = predict_with_context("docker", 6)
        self.assertIn("run", suggestions)
        self.assertIn("build", suggestions)
        self.assertIn("pull", suggestions)
    
    def test_filtering(self):
        """Test suggestion filtering."""
        suggestions = predict_with_context("git c", 5)
        # Should return commit and checkout (both start with 'c') plus flags
        self.assertIn("commit", suggestions)
        self.assertIn("checkout", suggestions)
        # Should also include flags that start with 'c' or are common flags
        self.assertTrue(len(suggestions) >= 2)
    
    def test_empty_input(self):
        """Test empty input handling."""
        suggestions = predict_with_context("", 0)
        self.assertIsInstance(suggestions, list)
    
    def test_context_extraction(self):
        """Test command context extraction."""
        context = extract_command_context("git commit -m", 12)
        self.assertEqual(context['command'], 'git')
        self.assertEqual(context['subcommand'], 'commit')
        self.assertEqual(context['current_word'], '-m')


if __name__ == '__main__':
    unittest.main() 