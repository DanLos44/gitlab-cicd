from unittest import TestCase
from bson import ObjectId
from app import app, db

class TestApp(TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.collection = db['mycollection']
        self.collection.drop()
        record = {'name': 'test', 'age': 20}
        self.collection.insert_one(record)

    def tearDown(self):
        self.collection.drop()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = response.get_data(as_text=True)
        self.assertIn('test', data)

    def test_create_record(self):
        record = {'name': 'John', 'age': 30}
        response = self.client.post('/create', data=record)
        self.assertEqual(response.status_code, 302)
        data = list(self.collection.find())
        self.assertEqual(len(data), 2)
        self.assertEqual(data[1]['name'], 'John')

    def test_update_record(self):
        data = list(self.collection.find())
        id = str(data[0]['_id'])
        record = {'name': 'updated', 'age': 25}
        response = self.client.post('/update/{}'.format(id), data=record)
        self.assertEqual(response.status_code, 302)
        updated_record = self.collection.find_one({'_id': ObjectId(id)})
        self.assertEqual(updated_record['name'], 'updated')
        self.assertEqual(int(updated_record['age']), 25)

    def test_delete_record(self):
        data = list(self.collection.find())
        id = str(data[0]['_id'])
        response = self.client.get('/delete/{}'.format(id))
        self.assertEqual(response.status_code, 302)
        data = list(self.collection.find())
        self.assertEqual(len(data), 0)


