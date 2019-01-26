from paymentmethods.currency import monero
from configurator.paymentmethods import paymentmethods_config
from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet
from decimal import Decimal
from unittest import mock
import unittest
try:
    from unittest.mock import patch, Mock, MagicMock
except ImportError:
    from mock import patch, Mock

class processpaymentsTestCase(unittest.TestCase):
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

    incoming_result = {
        'id': 0,
        'jsonrpc': '2.0',
        'result': {'in': [{
            'address': 'BhE3cQvB7VF2uuXcpXp28Wbadez6GgjypdRS1F1Mzqn8Advd6q8VfaX8ZoEDobjejrMfpHeNXoX8MjY8q8prW1PEALgr1En',
            'amount': 3000000000000,
            'double_spend_seen': False,
            'fee': 8661870000,
            'height': 1087601,
            'note': '',
            'payment_id': 'f75ad90e25d71a12',
            'subaddr_index': {'major': 0, 'minor': 1},
            'timestamp': 1517234267,
            'txid': 'f34b495cec77822a70f829ec8a5a7f1e727128d62e6b1438e9cb7799654d610e',
            'type': 'in',
            'unlock_time': 0},
            {
                'address': '9tQoHWyZ4yXUgbz9nvMcFZUfDy5hxcdZabQCxmNCUukKYicXegsDL7nQpcUa3A1pF6K3fhq3scsyY88tdB1MqucULcKzWZC',
                'amount': 10000000000000,
                'double_spend_seen': False,
                'fee': 962550000,
                'height': 1087530,
                'note': '',
                'payment_id': 'f75ad90e25d71a12',
                'subaddr_index': {'major': 0, 'minor': 0},
                'timestamp': 1517228238,
                'txid': '5c3ab739346e9d98d38dc7b8d36a4b7b1e4b6a16276946485a69797dbf887cd8',
                'type': 'in',
                'unlock_time': 0},
            {
                'address': '9tQoHWyZ4yXUgbz9nvMcFZUfDy5hxcdZabQCxmNCUukKYicXegsDL7nQpcUa3A1pF6K3fhq3scsyY88tdB1MqucULcKzWZC',
                'amount': 4000000000000,
                'double_spend_seen': False,
                'fee': 962550000,
                'height': 1087530,
                'note': '',
                'payment_id': 'f75ad90e25d71a12',
                'subaddr_index': {'major': 0, 'minor': 0},
                'timestamp': 1517228238,
                'txid': '4ea70add5d0c7db33557551b15cd174972fcfc73bf0f6a6b47b7837564b708d3',
                'type': 'in',
                'unlock_time': 0},
            {
                'address': 'BhE3cQvB7VF2uuXcpXp28Wbadez6GgjypdRS1F1Mzqn8Advd6q8VfaX8ZoEDobjejrMfpHeNXoX8MjY8q8prW1PEALgr1En',
                'amount': 7000000000000,
                'double_spend_seen': False,
                'fee': 962430000,
                'height': 1087601,
                'note': '',
                'payment_id': '0000000000000000',
                'subaddr_index': {'major': 0, 'minor': 1},
                'timestamp': 1517234267,
                'txid': '5ef7ead6a041101ed326568fbb59c128403cba46076c3f353cd110d969dac808',
                'type': 'in',
                'unlock_time': 0},
            {
                'address': '9tQoHWyZ4yXUgbz9nvMcFZUfDy5hxcdZabQCxmNCUukKYicXegsDL7nQpcUa3A1pF6K3fhq3scsyY88tdB1MqucULcKzWZC',
                'amount': 10000000000000,
                'double_spend_seen': False,
                'fee': 962550000,
                'height': 1087530,
                'note': '',
                'payment_id': '0000000000000000',
                'subaddr_index': {'major': 0, 'minor': 0},
                'timestamp': 1517228238,
                'txid': 'cc44568337a186c2e1ccc080b43b4ae9db26a07b7afd7edeed60ce2fc4a6477f',
                'type': 'in',
                'unlock_time': 0},
            {
                'address': 'Bf6ngv7q2TBWup13nEm9AjZ36gLE6i4QCaZ7XScZUKDUeGbYEHmPRdegKGwLT8tBBK7P6L32RELNzCR6QzNFkmogDjvypyV',
                'amount': 8000000000000,
                'double_spend_seen': False,
                'fee': 960990000,
                'height': 1088394,
                'note': '',
                'payment_id': '0000000000000000',
                'subaddr_index': {'major': 0, 'minor': 2},
                'timestamp': 1517335388,
                'txid': 'bc8b7ef53552c2d4bce713f513418894d0e2c8dcaf72e681e1d4d5a202f1eb62',
                'type': 'in',
                'unlock_time': 0},
            {
                'address': '9tQoHWyZ4yXUgbz9nvMcFZUfDy5hxcdZabQCxmNCUukKYicXegsDL7nQpcUa3A1pF6K3fhq3scsyY88tdB1MqucULcKzWZC',
                'amount': 2120000000000,
                'double_spend_seen': False,
                'fee': 962550000,
                'height': 1087530,
                'note': '',
                'payment_id': 'cb248105ea6a9189',
                'subaddr_index': {'major': 0, 'minor': 0},
                'timestamp': 1517228238,
                'txid': 'e9a71c01875bec20812f71d155bfabf42024fde3ec82475562b817dcc8cbf8dc',
                'type': 'in',
                'unlock_time': 0},
            {
                'address': 'Bf6ngv7q2TBWup13nEm9AjZ36gLE6i4QCaZ7XScZUKDUeGbYEHmPRdegKGwLT8tBBK7P6L32RELNzCR6QzNFkmogDjvypyV',
                'amount': 1000000000000,
                'double_spend_seen': False,
                'fee': 3528910000,
                'height': 1087606,
                'note': '',
                'payment_id': '0166d8da6c0045c51273dd65d6f63734beb8a84e0545a185b2cfd053fced9f5d',
                'subaddr_index': {'major': 0, 'minor': 2},
                'timestamp': 1517234425,
                'txid': 'a0b876ebcf7c1d499712d84cedec836f9d50b608bb22d6cb49fd2feae3ffed14',
                'type': 'in',
                'unlock_time': 0},
            {
                'address': '9tQoHWyZ4yXUgbz9nvMcFZUfDy5hxcdZabQCxmNCUukKYicXegsDL7nQpcUa3A1pF6K3fhq3scsyY88tdB1MqucULcKzWZC',
                'amount': 3140000000000,
                'double_spend_seen': False,
                'fee': 961950000,
                'height': 1087858,
                'note': '',
                'payment_id': '03f6649304ea4cb2',
                'subaddr_index': {'major': 0, 'minor': 0},
                'timestamp': 1517256811,
                'txid': 'd29264ad317e8fdb55ea04484c00420430c35be7b3fe6dd663f99aebf41a786c',
                'type': 'in',
                'unlock_time': 0}]}}

    wallet = None
    transfers_in = None
    config = None

    @patch('monero.backends.jsonrpc.requests.post')
    def setUp(self, mock_post):

        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = self.accounts_result
        self.wallet = Wallet(JSONRPCWallet())

        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = self.incoming_result
        self.transfers_in = self.wallet.incoming()

        self.config = paymentmethods_config(cfg_default=True) # monero is the default currency


    def test_new(self):
        currency = paymentmethods_config.supportedCurrencies[self.config.currency]()
        new_accounts = currency.processpayments(transfers_in=self.transfers_in,
                                                 paymentmethod=self.config, current_blockheight='1087858')
        self.assertIsInstance(new_accounts, list)
        #TODO 
        self.assertEqual(new_accounts, [
            {'username': 'f34b495cec77822a70f829ec8a5a7f1e727128d62e6b1438e9cb7799654d610e',
                'password': '1087601'},
            {'username': '5ef7ead6a041101ed326568fbb59c128403cba46076c3f353cd110d969dac808',
                'password': '1087601'}
                            ])