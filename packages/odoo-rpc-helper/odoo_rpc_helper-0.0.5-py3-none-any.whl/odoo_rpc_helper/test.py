"""
Test OdooRPCHelper functions on an already existing test database.
"""

import unittest
from rpc_helpers import OdooRPCHelper

class TestOdooRPCHelper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.bot = OdooRPCHelper('test', 'admin', 'admin')

    def tearDown(self):
        if self.partner_id:
            self.bot.unlink('res.partner', [self.partner_id])

    def test_crud(self):
        """
        A simplistic test case that cleans up after itself... or tries to.
        """
        self.partner_id = partner_id = self.bot.create(
            'res.partner',
            {'name': 'Test Partner'}
        )[0]
        self.assertIsInstance(partner_id, int)
        # Test search
        partner_ids = self.bot.search(
            'res.partner',
            [['name', '=', 'Test Partner']]
        )
        self.assertIn(partner_id, partner_ids)
        # Test search_read
        partners = self.bot.search_read(
            'res.partner',
            [['name', '=', 'Test Partner']],
            ['id', 'name'],
        )
        self.assertTrue(partners)
        for partner in partners:
            self.assertIn('id', partner)
            self.assertIn('name', partner)
            self.assertEqual(
                partner['name'],
                'Test Partner',
                'Only partners named Test Partner should be found.'
            )
        # Test write
        self.bot.write(
            'res.partner',
            [partner_id],
            {'name': 'New Name for Test Partner'},
        )
        partners = self.bot.search(
            'res.partner',
            [['name', '=', 'New Name for Test Partner']],
        )
        self.assertTrue(partners)
        # Test delete
        self.bot.unlink('res.partner', [partner_id])
        self.assertFalse(self.bot.search(
            'res.partner',
            [['id', '=', partner_id]]
        ))
        self.partner_id = None


if __name__ == '__main__':
    unittest.main()
