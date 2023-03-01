from django.test import TestCase
from io import BytesIO
from PIL import Image
from rest_framework.reverse import reverse
from django.core.files.base import File
from .models import APIImage
from accounts.models import CustomUser
from plans.models import Plan
from rest_framework.test import APIClient
import tempfile

class ImagesTest(TestCase):
    @staticmethod
    def get_image_file(name, ext='png', size=(1000, 1000), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGB", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name + '.' + ext)
    def get_temporary_image():
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file, 'jpeg')
        tmp_file.seek(0)
        return tmp_file
       
    @classmethod
    def setUpTestData(cls):
        Plan.objects.create(
            title='Basic', 
            original_image_link = False, 
            binary_image_link = False, 
            available_hights = '200')
        Plan.objects.create(
            title='Premium', 
            original_image_link = True, 
            binary_image_link = False, 
            available_hights = '200,400')
        Plan.objects.create(
            title='Enterprise', 
            original_image_link = True, 
            binary_image_link = True, 
            available_hights = '200,400')
        
        list_plans_id = [1, 2, 3]
        for key in list_plans_id:
            user_id = key
            user_plan = Plan.objects.get(id=key)
            CustomUser.objects.create(
            username='test_{0}'.format(user_id), 
            email='test@example.com', 
            password='password',
            plan = user_plan,
            )
        list_users_ids = [1, 2, 3]
        for user_id in list_users_ids:
            user = CustomUser.objects.get(id=user_id)
            APIImage.objects.create(
                user = user,
                image = ImagesTest.get_image_file('test', 'png'),
            )
        
    def test_validate_file_invalid(self):
        user = CustomUser.objects.get(id=1)
        self.assertRaisesMessage(APIImage.objects.create(
            user = user,
            image = ImagesTest.get_image_file('test','gif'),
            ), 'File extension “gif” is not allowed. Allowed extensions are: jpg, jpeg, png.')
       
    def test_list_image_for_all_plans(self):
        expected_responses = {
            1: [{'id': 1, 'urls': "['http://testserver/image/1/thumbnail/200']"}],
            2: [{'id': 2, 'urls': "['http://testserver/image/2/thumbnail/200', 'http://testserver/image/2/thumbnail/400', 'http://testserver/image/2/original']"}],
            3: [{'id': 3, 'urls': "['http://testserver/image/3/thumbnail/200', 'http://testserver/image/3/thumbnail/400', 'http://testserver/image/3/original', 'http://testserver/image/3/binary']"}]
        }
        for user_key in expected_responses:
            user = CustomUser.objects.get(id=user_key)
            client = APIClient()
            client.force_authenticate(user=user)
            response = client.get(reverse('image_list'))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), expected_responses[user_key])

    def test_image_deteil(self):
        user_id = 3
        image_id = 3
        expected_response = {'id': 3, 'urls': "['http://testserver/image/3/thumbnail/200', 'http://testserver/image/3/thumbnail/400', 'http://testserver/image/3/original', 'http://testserver/image/3/binary']"}
        user = CustomUser.objects.get(id=user_id)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse('image_details', kwargs={'pk':image_id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)

    def test_image_original(self):
        user_id = 3
        expected_content_type_dict = {1:'image/png', 4:'image/jpeg'}
        user = CustomUser.objects.get(id=user_id)
        APIImage.objects.create(
                user = user,
                image = ImagesTest.get_image_file('test', 'jpeg'),
            )
        client = APIClient()
        client.force_authenticate(user=user)
        for id in expected_content_type_dict:
            response = client.get(reverse('image_original', kwargs={'pk':id}))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], expected_content_type_dict[id])
        APIImage.objects.get(pk=4).delete()
    
    def test_image_list_add_new(self):
        expected_response = {'id': 4}
        user = CustomUser.objects.get(id=1)
        client = APIClient()
        client.force_authenticate(user=user)
        data = {'image': ImagesTest.get_temporary_image()}
        response = client.post(reverse('image_list'), data, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), expected_response)
        APIImage.objects.get(pk=4).delete()
    
    def test_immage_details_by_another_user(self):
        user = CustomUser.objects.get(id=1)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse('image_details', kwargs={'pk':2}))
        self.assertEqual(response.status_code, 403)
    
    def test_wrong_immage(self):
        user = CustomUser.objects.get(id=1)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse('image_details', kwargs={'pk':101}))
        self.assertEqual(response.status_code, 404)