###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
from unittest import TestCase
from everysk.core.compress import compress_json, compress_pickle, decompress_json, decompress_pickle
from everysk.core.datetime import DateTime, Date


class CompressJsonTestCase(TestCase):

    def test_compress(self):
        string = 'aa aa aa aa aa aa aa aa'
        self.assertEqual(compress_json(string), b'x\x9cSJLT\xc0\x86\x94\x00]\xbd\x075')

    def test_decompress(self):
        string = b'x\x9cSJLT\xc0\x86\x94\x00]\xbd\x075'
        self.assertEqual(decompress_json(string), 'aa aa aa aa aa aa aa aa')

    def test_undefined(self):
        obj_compressed = compress_json(Undefined)
        self.assertEqual(decompress_json(obj_compressed), Undefined)

    def test_complex_obj(self):
        obj = [
            {'datetime': DateTime.now()},
            {'a': 1, 'b': True},
            'Test',
            1.1,
            ['1', '2', '3', Date.today()],
            Undefined,
            {'undefined': Undefined}
        ]
        obj_compressed = compress_json(obj)
        self.assertListEqual(decompress_json(obj_compressed), obj)


class CompressPickleTestCase(TestCase):

    def setUp(self) -> None:
        self.str_repr = b'x\x9ck`\x99*\xcd\x00\x01=\xe2\x89\x89\n\xd8\xd0\x14=\x00\x9f\xef\t\x8a'

    def test_compress(self):
        string = 'aa aa aa aa aa aa aa aa'
        self.assertEqual(compress_pickle(string), self.str_repr)

    def test_decompress(self):
        self.assertEqual(decompress_pickle(self.str_repr), 'aa aa aa aa aa aa aa aa')

    def test_undefined(self):
        obj_compressed = compress_pickle(Undefined)
        self.assertEqual(decompress_pickle(obj_compressed), Undefined)

    def test_complex_obj(self):
        obj = [
            {'datetime': DateTime.now()},
            {'a': 1, 'b': True},
            'Test',
            1.1,
            ['1', '2', '3', Date.today()],
            Undefined,
            {'undefined': Undefined}
        ]
        obj_compressed = compress_pickle(obj)
        self.assertListEqual(decompress_pickle(obj_compressed), obj)
