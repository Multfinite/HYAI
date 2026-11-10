"""Regression guard: all image workflows retain the source eye-colour gate."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2] / 'core' / 'domains' / 'picture'

class EyeColourContractTests(unittest.TestCase):
    def test_rule_and_exception(self):
        text = (ROOT / 'policy.md').read_text()
        self.assertIn('`PIC-QA-11`', text)
        self.assertIn('только явное разрешение пользователя', text)

    def test_workflows_reference_gate(self):
        for name in ('instant', 'pipeline', 'series', 'style-filter', 'remediation'):
            with self.subTest(workflow=name):
                self.assertIn('PIC-QA-11', (ROOT / 'workflows' / f'{name}.md').read_text())

    def test_final_style_and_iris_source(self):
        text = (ROOT / 'workflows' / 'remediation.md').read_text()
        self.assertIn('заключительного стиль-фильтра', text)
        self.assertIn('нативный кроп глаз', text)
        self.assertIn('того же исходного оттенка', text)
        self.assertIn('без добавления свечения', text)

if __name__ == '__main__':
    unittest.main()
