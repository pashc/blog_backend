import json
import unittest

from blog_app.tests.test_basic import BasicTest


class ArticleTests(BasicTest):
    BASE_URL = '/api/blog/articles/'

    def test_get_all_articles(self):
        # given
        category_response = self.__create_test_category()
        category_id = json.loads(category_response.data).get('id')
        self.__create_test_article(category_id=category_id,
                                   title='testing1',
                                   content='content1')
        self.__create_test_article(category_id=category_id,
                                   title='testing2',
                                   content='content2')

        # when
        result = self.app.get(self.BASE_URL + 'list')

        # then
        self.assertEqual(result.status_code, 200)
        result_data = json.loads(result.data)
        self.assertEqual(len(result_data), 2)

        self.assertEqual(result_data[0].get('id'), 1)
        self.assertEqual(result_data[0].get('title'), 'testing1')
        self.assertEqual(result_data[0].get('content'), 'content1')
        self.assertEqual(result_data[0].get('category_id'), category_id)
        self.assertIsNotNone(result_data[0].get('pub_date'))

        self.assertEqual(result_data[1].get('id'), 2)
        self.assertEqual(result_data[1].get('title'), 'testing2')
        self.assertEqual(result_data[1].get('content'), 'content2')
        self.assertIsNotNone(result_data[1].get('pub_date'))
        self.assertEqual(result_data[1].get('category_id'), category_id)

    def test_create_article(self):
        # given
        category_response = self.__create_test_category()
        category_id = json.loads(category_response.data).get('id')

        # when
        result = self.__create_test_article(category_id=category_id,
                                            title='testing',
                                            content='content')

        # then
        self.assertEqual(result.status_code, 201)
        result_data = json.loads(result.data)
        self.assertEqual(result_data.get('id'), 1)
        self.assertEqual(result_data.get('title'), 'testing')
        self.assertEqual(result_data.get('content'), 'content')
        self.assertEqual(result_data.get('category_id'), category_id)
        self.assertIsNotNone(result_data.get('pub_date'))

    def test_get_by_id(self):
        # given
        category_response = self.__create_test_category()
        category_id = json.loads(category_response.data).get('id')
        article_response = self.__create_test_article(category_id=category_id,
                                                      title='testing',
                                                      content='content')
        article_id = json.loads(article_response.data).get('id')

        # when
        result = self.app.get(self.BASE_URL + str(article_id))

        # then
        self.assertEqual(result.status_code, 200)
        result_data = json.loads(result.data)
        self.assertEqual(result_data.get('id'), article_id)
        self.assertEqual(result_data.get('title'), 'testing')
        self.assertEqual(result_data.get('content'), 'content')
        self.assertEqual(result_data.get('category_id'), category_id)
        self.assertIsNotNone(result_data.get('pub_date'))

    def test_update_article(self):
        # given
        category1_response = self.__create_test_category(name='category 1')
        category1_id = json.loads(category1_response.data).get('id')
        category2_response = self.__create_test_category(name='category 2')
        category2_id = json.loads(category2_response.data).get('id')

        article_response = self.__create_test_article(category_id=category1_id,
                                                      title='testing',
                                                      content='content')
        article_id = json.loads(article_response.data).get('id')

        # when
        result = self.app.put(self.BASE_URL + str(article_id),
                              data=json.dumps(dict(title='updated title',
                                                   content='updated content',
                                                   category_id=category2_id)),
                              content_type='application/json',
                              headers=self.get_auth_headers())

        # then
        self.assertEqual(result.status_code, 204)

        updated_article = self.app.get(self.BASE_URL + str(article_id))
        updated_data = json.loads(updated_article.data)

        self.assertEqual(updated_data.get('id'), article_id)
        self.assertEqual(updated_data.get('title'), 'updated title')
        self.assertEqual(updated_data.get('content'), 'updated content')
        self.assertEqual(updated_data.get('category_id'), category2_id)
        self.assertIsNotNone(updated_data.get('pub_date'))

    def test_delete_article(self):
        # given
        category_response = self.__create_test_category()
        category_id = json.loads(category_response.data).get('id')
        article_response = self.__create_test_article(category_id=category_id)
        article_id = json.loads(article_response.data).get('id')

        # when
        result = self.app.delete(self.BASE_URL + str(article_id),
                                 headers=self.get_auth_headers())

        # then
        self.assertEqual(result.status_code, 204)

    def __create_test_article(self, category_id, title='testing', content='content'):
        return self.app.post(self.BASE_URL,
                             data=json.dumps(dict(category_id=category_id,
                                                  title=title,
                                                  content=content)),
                             content_type='application/json',
                             headers=self.get_auth_headers())

    def __create_test_category(self, name='testing'):
        return self.app.post('/api/blog/categories/',
                             data=json.dumps(dict(name=name)),
                             content_type='application/json',
                             headers=self.get_auth_headers())


if __name__ == '__main__':
    unittest.main()
