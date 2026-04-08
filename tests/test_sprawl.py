import unittest
import os
import tempfile
import json
import sys

# Append src to module paths dynamically allowing test environments to cleanly map the Sprawl execution logics.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import sprawl

class TestSprawlCLI(unittest.TestCase):
    
    def test_parse_package_md(self):
        """Validates that parse_package_md accurately interpolates and extracts arrays correctly."""
        test_content = """# test app
## [rules]
- PRIME_DIRECTIVE.md

## [skills]
- web_agent_folder

## [atoms]
- none

## [workflows]
- execution.md
"""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file.write(test_content)
            temp_path = temp_file.name

        try:
            reqs = sprawl.parse_package_md(temp_path)
            
            # Arrays logic mapping
            self.assertIn('PRIME_DIRECTIVE.md', reqs['rules'])
            self.assertIn('web_agent_folder', reqs['skills'])
            self.assertIn('execution.md', reqs['workflows'])
            
            # Ensure "none" triggers empty state correctly handling native rulesets filtering
            self.assertEqual(len(reqs['atoms']), 0)
        finally:
            os.remove(temp_path)

if __name__ == '__main__':
    unittest.main()
