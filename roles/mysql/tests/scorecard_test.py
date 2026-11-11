"""Exercise the generated expression locally; this is not a MySQL integration test."""
import pathlib
import re
import sqlite3
import unittest

import yaml  # Already required by the Ansible controller.


class ScorecardTests(unittest.TestCase):
    def setUp(self):
        tasks = yaml.safe_load((pathlib.Path(__file__).parents[1] / 'tasks/scorecard.yml').read_text())
        queries = tasks[1]['community.mysql.mysql_query']['query']
        ddl = re.sub(r' ENGINE=InnoDB DEFAULT CHARSET=utf8mb4\s*$', '', queries[0])
        self.db = sqlite3.connect(':memory:')
        self.addCleanup(self.db.close)
        self.db.execute(ddl)
        self.db.execute(queries[1])

    def test_seed_roster_passes(self):
        self.assertEqual(self.db.execute('SELECT scorecard_status FROM sandlot_scorecard').fetchall(), [('PASS',)] * 5)

    def test_tamper_recomputes_and_recovers(self):
        self.db.execute('UPDATE sandlot_scorecard SET total_bases=9 WHERE id=1')
        self.assertEqual(self.db.execute('SELECT scorecard_status FROM sandlot_scorecard WHERE id=1').fetchone(), ('FAIL',))
        self.db.execute('UPDATE sandlot_scorecard SET total_bases=8 WHERE id=1')
        self.assertEqual(self.db.execute('SELECT scorecard_status FROM sandlot_scorecard WHERE id=1').fetchone(), ('PASS',))

    def test_negative_counts_fail_even_with_matching_total(self):
        self.db.execute('UPDATE sandlot_scorecard SET singles=-1,total_bases=5 WHERE id=1')
        self.assertEqual(self.db.execute('SELECT scorecard_status FROM sandlot_scorecard WHERE id=1').fetchone(), ('FAIL',))

    def test_status_cannot_be_assigned(self):
        with self.assertRaises(sqlite3.OperationalError):
            self.db.execute("UPDATE sandlot_scorecard SET scorecard_status='PASS' WHERE id=1")


if __name__ == '__main__':
    unittest.main()
