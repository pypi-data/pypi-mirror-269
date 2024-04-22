

import sys
import os
import unittest

sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests'))


from alchemyrohan import get_model
from tests.test_models.Parent import Parent
from tests.test_models.Child import Child


class TestModels(unittest.TestCase):

    def test_get_models(self):

        py_path = 'tests.test_models'
        test_cases = [('parent', Parent), ('child', Child)]

        for table_name, expected_result in test_cases:
            result = get_model(table_name, py_path)
            self.assertEqual(result, expected_result)

    def test_models_str(self):

        py_path = 'tests.test_models'

        expect = 'User(id=None,name=None,age=None,height=None,is_active=None)'
        parent = get_model('parent', py_path)
        p = parent()
        self.assertEqual(str(p), expect)

        expect = 'User(id=None,parent_id=None,name=None,grade=None)'
        child = get_model('child', py_path)
        p = child()
        self.assertEqual(str(p), expect)

    def test_models_instance(self):

        py_path = 'tests.test_models'

        expect = 'User(id=None,name=Alice,age=24,height=170.3,is_active=True)'
        parent = get_model('parent', py_path)
        p = parent(name='Alice', age=24, height=170.3, is_active=True)
        self.assertEqual(str(p), expect)


if __name__ == '__main__':
    unittest.main()










