import unittest
from tba import *

class TestPowerCalculation(unittest.TestCase):
    def test_eval(self):
        self.assertEqual(0, tba_power(""))
        self.assertEqual(560, tba_power("560"))
        self.assertEqual(5*630+3*70, tba_power("5x630+3x70"))

    def test_count_mba(self):
        self.assertEqual(0, count_mba(""))
        self.assertEqual(0, count_mba("0"))
        self.assertEqual(2, count_mba("400+630"))
        self.assertEqual(1, count_mba("560"))
        self.assertEqual(2, count_mba("2x560"))
        self.assertEqual(3, count_mba("560+2x400"))
        self.assertEqual(4, count_mba("560+400+2x320"))

class TestParseRows(unittest.TestCase):
    def test_split_row(self):
        self.assertEqual(["a","b","c"], split_row("a,b,c"))

    def test_tba_from_row(self):
        self.assertEqual(
            {"type": "tba",
             "name": "Khu 8 (khu 11 cũ) thị trấn Diêm Điền",
             "owner": "DL",
             "v0": "10/0.4",
             "v1": "10/0.4",
             "v2": "10/0.4",
             "p0": "400",
             "p1": "400",
             "p2": "400"}
            ,(tba_from_row("tba,Khu 8 (khu 11 cũ) thị trấn Diêm Điền,DL,10/0.4,10/0.4,10/0.4,400,400,400")))


class TestParseData(unittest.TestCase):
    data = ("xa,xa A\n"
            +"tba,tba1,DL,10/0.4,10/0.4,10/0.4,400,400,400\n"
            + "tba,tba2,DL,10/0.4,10/0.4,10/0.4,400,400,400\n"
            + "tba,tba3,DL,10/0.4,10/0.4,10/0.4,400,400,400\n"
            + "xa,xa B\n"
            +"tba,tba 1,DL,10/0.4,10/0.4,10/0.4,400,400,400\n"
            + "tba,tba 2,DL,10/0.4,10/0.4,10/0.4,400,400,400\n"
            + "tba,tba 3,DL,10/0.4,10/0.4,10/0.4,400,400,400\n"
    )

    result = [
        {
            'name': 'xa A',
            'tbas': [{'type': 'tba', 'name': 'tba1', 'owner': 'DL',
                      'v0': '10/0.4', 'v1': '10/0.4', 'v2': '10/0.4',
                      'p0': '400', 'p1': '400', 'p2': '400'},
                     {'type': 'tba', 'name': 'tba2', 'owner': 'DL',
                      'v0': '10/0.4', 'v1': '10/0.4', 'v2': '10/0.4',
                      'p0': '400', 'p1': '400', 'p2': '400'},
                     {'type': 'tba', 'name': 'tba3', 'owner': 'DL',
                      'v0': '10/0.4', 'v1': '10/0.4', 'v2': '10/0.4',
                      'p0': '400', 'p1': '400', 'p2': '400'}]},
        {
            'name': 'xa B',
            'tbas': [{'type': 'tba', 'name': 'tba 1', 'owner': 'DL',
                      'v0': '10/0.4', 'v1': '10/0.4', 'v2': '10/0.4',
                      'p0': '400', 'p1': '400', 'p2': '400'},
                     {'type': 'tba', 'name': 'tba 2', 'owner': 'DL',
                      'v0': '10/0.4', 'v1': '10/0.4', 'v2': '10/0.4',
                      'p0': '400', 'p1': '400', 'p2': '400'},
                     {'type': 'tba', 'name': 'tba 3', 'owner': 'DL',
                      'v0': '10/0.4', 'v1': '10/0.4', 'v2': '10/0.4',
                      'p0': '400', 'p1': '400', 'p2': '400'}]}]

    def test_read_data(self):
        xas = xa_data(self.data.splitlines())
        # print(xas)
        self.assertEqual(xas, self.result)

class TestChangeTba(unittest.TestCase):
    def test_get_change_type_tba(self):
        self.assertEqual({"type": "nothing",
                          "num": 0,
                          "power": 0,
                          "voltage": "22/0.4"},
                         get_change_type_tba("22/0.4", "22/0.4",
                                             "400", "400"))
        self.assertEqual({"type": "upgrade_tba",
                          "num": 1,
                          "power": 400,
                          "voltage": "22/0.4"},
                         get_change_type_tba("10/0.4", "22/0.4",
                                             "400", "400"))
        self.assertEqual({"type": "upgrade_tba",
                          "num": 1,
                          "power": 630,
                          "voltage": "22/0.4"},
                         get_change_type_tba("10/0.4", "22/0.4",
                                             "400", "630"))
        self.assertEqual({"type": "new_tba",
                          "num": 1,
                          "power": 630,
                          "voltage": "22/0.4"},
                         get_change_type_tba("22/0.4", "22/0.4",
                                             "400", "400+630"))
        self.assertEqual({"type": "new_tba",
                          "num": 2,
                          "power": 1030,
                          "voltage": "22/0.4"},
                         get_change_type_tba("0", "22/0.4",
                                             "", "400+630"))

class TestAggregateData(unittest.TestCase):
    def test_aggregate_xa(self):
        xaA = {"name": "xa A",
               "tbas": [{'type': 'tba', 'name': 'tba1', 'owner': 'DL',
                         'v0': '10/0.4', 'v1': '10/0.4', 'v2': '10/0.4',
                        'p0': '400', 'p1': '400', 'p2': '400'},
                        {'type': 'tba', 'name': 'tba2', 'owner': 'DL',
                         'v0': '10/0.4', 'v1': '10/0.4', 'v2': '10/0.4',
                         'p0': '400', 'p1': '400', 'p2': '400'},
                        {'type': 'tba', 'name': 'tba3', 'owner': 'DL',
                         'v0': '10/0.4', 'v1': '10/0.4', 'v2': '10/0.4',
                         'p0': '400', 'p1': '400', 'p2': '400'}]}
        resultA = {'GD1': {'KH': {'New': {'22/0.4': {'power': 0, 'num': 0},
                                          'Other': {'power': 0, 'num': 0}},
                                  'Upgrade': {'22/0.4': {'power': 0, 'num': 0},
                                              'Other': {'power': 0, 'num': 0}}},
                           'DL': {'New': {'22/0.4': {'power': 0, 'num': 0},
                                          'Other': {'power': 0, 'num': 0}},
                                  'Upgrade': {'22/0.4': {'power': 0, 'num': 0},
                                              'Other': {'power': 0, 'num': 0}}}},
                   'GD2': {'KH': {'New': {'22/0.4': {'power': 0, 'num': 0},
                                          'Other': {'power': 0, 'num': 0}},
                                  'Upgrade': {'22/0.4': {'power': 0, 'num': 0},
                                              'Other': {'power': 0, 'num': 0}}},
                           'DL': {'New': {'22/0.4': {'power': 0, 'num': 0},
                                          'Other': {'power': 0, 'num': 0}},
                                  'Upgrade': {'22/0.4': {'power': 0, 'num': 0},
                                              'Other': {'power': 0, 'num': 0}}}},
                   'name': 'xa A'}

        self.assertEqual(resultA, aggregate_xa(xaA))

        xaB = {"name": "xa B",
               "tbas": [{'type': 'tba', 'name': 'tba1', 'owner': 'DL',
                         'v0': '10/0.4', 'v1': '10/0.4', 'v2': '10/0.4',
                        'p0': '400', 'p1': '400', 'p2': '630'},
                        {'type': 'tba', 'name': 'tba2', 'owner': 'DL',
                         'v0': '10/0.4', 'v1': '10/0.4', 'v2': '10/0.4',
                         'p0': '400', 'p1': '400', 'p2': '400'},
                        {'type': 'tba', 'name': 'tba3', 'owner': 'DL',
                         'v0': '10/0.4', 'v1': '10/0.4', 'v2': '10/0.4',
                         'p0': '400', 'p1': '400', 'p2': '400'}]}
        resultB = {'GD1': {'KH': {'New': {'22/0.4': {'power': 0, 'num': 0},
                                          'Other': {'power': 0, 'num': 0}},
                                  'Upgrade': {'22/0.4': {'power': 0, 'num': 0},
                                              'Other': {'power': 0, 'num': 0}}},
                           'DL': {'New': {'22/0.4': {'power': 0, 'num': 0},
                                          'Other': {'power': 0, 'num': 0}},
                                  'Upgrade': {'22/0.4': {'power': 0, 'num': 0},
                                              'Other': {'power': 0, 'num': 0}}}},
                   'GD2': {'KH': {'New': {'22/0.4': {'power': 0, 'num': 0},
                                          'Other': {'power': 0, 'num': 0}},
                                  'Upgrade': {'22/0.4': {'power': 0, 'num': 0},
                                              'Other': {'power': 0, 'num': 0}}},
                           'DL': {'New': {'22/0.4': {'power': 0, 'num': 0},
                                          'Other': {'power': 0, 'num': 0}},
                                  'Upgrade': {'22/0.4': {'power': 0, 'num': 0},
                                              'Other': {'power': 630, 'num': 1}}}},
                   'name': 'xa B'}
       
        self.assertEqual(resultB, aggregate_xa(xaB))

        xaC = {"name": "xa C",
               "tbas": [{'type': 'tba', 'name': 'tba1', 'owner': 'KH',
                         'v0': '10/0.4', 'v1': '10/0.4', 'v2': '22/0.4',
                        'p0': '400', 'p1': '400', 'p2': '630'},
                        {'type': 'tba', 'name': 'tba2', 'owner': 'DL',
                         'v0': '10/0.4', 'v1': '10/0.4', 'v2': '10/0.4',
                         'p0': '400', 'p1': '400', 'p2': '400'},
                        {'type': 'tba', 'name': 'tba3', 'owner': 'DL',
                         'v0': '10/0.4', 'v1': '22/0.4', 'v2': '22/0.4',
                         'p0': '400', 'p1': '400', 'p2': '2x400+630'}]}
        resultC = {'GD1': {'KH': {'New': {'22/0.4': {'power': 0, 'num': 0},
                                          'Other': {'power': 0, 'num': 0}},
                                  'Upgrade': {'22/0.4': {'power': 0, 'num': 0},
                                              'Other': {'power': 0, 'num': 0}}},
                           'DL': {'New': {'22/0.4': {'power': 0, 'num': 0},
                                          'Other': {'power': 0, 'num': 0}},
                                  'Upgrade': {'22/0.4': {'power': 400, 'num': 1},
                                              'Other': {'power': 0, 'num': 0}}}},
                   'GD2': {'KH': {'New': {'22/0.4': {'power': 0, 'num': 0},
                                          'Other': {'power': 0, 'num': 0}},
                                  'Upgrade': {'22/0.4': {'power': 630, 'num': 1},
                                              'Other': {'power': 0, 'num': 0}}},
                           'DL': {'New': {'22/0.4': {'power': 1030, 'num': 2},
                                          'Other': {'power': 0, 'num': 0}},
                                  'Upgrade': {'22/0.4': {'power': 0, 'num': 0},
                                              'Other': {'power': 0, 'num': 0}}}},
                   'name': 'xa C'}
       
        self.assertEqual(resultC, aggregate_xa(xaC))

        
if __name__ == "__main__":
    unittest.main()
