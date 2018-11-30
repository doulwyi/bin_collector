import unittest

from bin_collection import get_closest_date, get_bin_collector_infos, get_info_from_server


class TestDateTime(unittest.TestCase):
    def setUp(self):
        self.date_list = ['20171228', '20180104', '20180110', '20180116', '20180123', '20180131', '20180202']
        self.date = '20180201'

    def test_date_is_valid(self):
        """Date format must be yyyymmdd"""
        wrong_date = '2018-11-29'
        with self.assertRaises(ValueError):
            get_closest_date(wrong_date, self.date_list)

    def test_date_must_be_lower_than_last_list_item(self):
        wrong_date = '20180203'
        with self.assertRaises(ValueError):
            get_closest_date(wrong_date, self.date_list)

    def test_must_returns_same_day(self):
        date = '20180110'
        expected_date = '20180110'
        self.assertEqual(expected_date, get_closest_date(date, self.date_list))

    def test_if_returns_always_next_day(self):
        date = '20180111'
        expected_date = '20180116'
        self.assertEqual(expected_date, get_closest_date(date, self.date_list))

    def test_check_list_indexes(self):
        date = '20180115'
        expected_date = '20180116'
        date_list = ['20180110', '20180116']
        self.assertEqual(expected_date, get_closest_date(date, date_list))


class TestBinCollector(unittest.TestCase):
    def setUp(self):
        self.date = '20171228'

    def test_returns_info_dict(self):
        self.assertIsInstance(get_bin_collector_infos(self.date), dict)

    def test_returns_uid_as_list(self):
        res = get_bin_collector_infos(self.date)
        self.assertIsInstance(res['uid'], list)

    def test_returns_dtstamp_as_list(self):
        res = get_bin_collector_infos(self.date)
        self.assertIsInstance(res['dtstamp'], list)

    def test_returns_dtstart_as_list(self):
        res = get_bin_collector_infos(self.date)
        self.assertIsInstance(res['dtstart'], list)

    def test_returns_summary_as_list(self):
        res = get_bin_collector_infos(self.date)
        self.assertIsInstance(res['dtstart'], list)


class TestRequestInfoFromServer(unittest.TestCase):

    def test_returns_info_from_server(self):
        res = get_info_from_server()
        with self.subTest():
            self.assertIsInstance(res, list)
            self.assertIsInstance(res[0], str)


if __name__ == '__main__':
    unittest.main()
