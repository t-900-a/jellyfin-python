from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet
from configurator.monerojsonrpc import RPCconfig
import unittest
try:
    from unittest.mock import patch, Mock
except ImportError:
    from mock import patch, Mock

class ConfiguratorTestCase(unittest.TestCase):
    cfg_test = None
    accounts_result = {'id': 0,
        'jsonrpc': '2.0',
        'result': {'subaddress_accounts': [{'account_index': 0,
                                         'balance': 224916129245183,
                                         'base_address': '9vgV48wWAPTWik5QSUSoGYicdvvsbSNHrT9Arsx1XBTz6VrWPSgfmnUKSPZDMyX4Ms8R9TkhB4uFqK9s5LUBbV6YQN2Q9ag',
                                         'label': 'Primary account',
                                         'unlocked_balance': 224916129245183},
                                        {'account_index': 1,
                                         'balance': 3981420960933,
                                         'base_address': 'BaCBwYSK9BGSuKxb2msXEj4mmpvZYJexYHfqx7kNPDrXDePVXSfoofxGquhXxpA4uxawcnVnouusMDgP74CACa7e9siimpj',
                                         'label': 'Untitled account',
                                         'unlocked_balance': 3981420960933},
                                        {'account_index': 2,
                                         'balance': 7256159239955,
                                         'base_address': 'BgCseuY3jFJAZS7kt9mrNg7fEG3bo5BV91CTyKbYu9GFiU6hUZhvdNWCTUdQNPNcA4PyFApsFr3EsQDEDfT3tQSY1mVZeP2',
                                         'label': 'Untitled account',
                                         'unlocked_balance': 7256159239955}],
                'total_balance': 236153709446071,
                'total_unlocked_balance': 236153709446071}}

    def setUp(self):
        self.cfg_test = RPCconfig(cfg_default=True)

    @patch('monero.backends.jsonrpc.requests.post')
    def test_config(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = self.accounts_result

        jsonRPC = JSONRPCWallet(self.cfg_test.get_protocol(), self.cfg_test.get_host(), self.cfg_test.get_port(), self.cfg_test.get_path(),
                                self.cfg_test.get_user(), self.cfg_test.get_password())
        self.assertIsInstance(Wallet(jsonRPC), Wallet)