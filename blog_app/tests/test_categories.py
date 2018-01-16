import json
import unittest

from blog_app.tests.test_basic import BasicTest


class CategoriesTests(BasicTest):
    BASE_URL = '/api/blog/categories/'

    def test_get_all(self):
        # given
        self.__create_test_category(name='testing1')
        self.__create_test_category(name='testing2')

        # when
        result = self.app.get(self.BASE_URL + 'list')

        # then
        self.assertEqual(result.status_code, 200)
        result_data = json.loads(result.data)
        self.assertEqual(len(result_data), 2)
        self.assertEqual(result_data[0].get('id'), 1)
        self.assertEqual(result_data[0].get('name'), 'testing1')
        self.assertEqual(result_data[1].get('id'), 2)
        self.assertEqual(result_data[1].get('name'), 'testing2')

    def test_get_by_id(self):
        # given
        response = self.__create_test_category()
        self.assertEqual(response.status_code, 201)
        category_id = json.loads(response.data).get('id')

        # when
        result = self.app.get(self.BASE_URL + str(category_id))

        # then
        self.assertEqual(result.status_code, 200)
        result_data = json.loads(result.data)
        self.assertEqual(result_data.get('id'), category_id)
        self.assertEqual(result_data.get('name'), 'testing')

    def test_create(self):
        # given
        result = self.__create_test_category()

        # when/then
        self.assertEqual(result.status_code, 201)
        result_data = json.loads(result.data)
        self.assertEqual(result_data.get('id'), 1)
        self.assertEqual(result_data.get('name'), 'testing')

    def test_update(self):
        # given
        response = self.__create_test_category()
        self.assertEqual(response.status_code, 201)
        category_id = json.loads(response.data).get('id')

        # when
        result = self.app.put(self.BASE_URL + str(category_id),
                              data=json.dumps(dict(name='Other Name')),
                              content_type='application/json',
                              headers=self.get_auth_headers())

        # then
        self.assertEqual(result.status_code, 200)
        result_data = json.loads(result.data)
        self.assertEqual(result_data.get('id'), 1)
        self.assertEqual(result_data.get('name'), 'Other Name')

    def test_delete(self):
        response = self.__create_test_category()
        self.assertEqual(response.status_code, 201)
        category_id = json.loads(response.data).get('id')

        # when
        result = self.app.delete(self.BASE_URL + str(category_id), headers=self.get_auth_headers())

        # then
        self.assertEqual(result.status_code, 204)

    def __create_test_category(self, name='testing'):
        return self.app.post(self.BASE_URL,
                             data=json.dumps(dict(name=name)),
                             content_type='application/json',
                             headers=self.get_auth_headers())


if __name__ == '__main__':
    unittest.main()
