from django.test import TestCase
from io import BytesIO
from PIL import Image
from rest_framework.reverse import reverse
from django.utils import timezone
from django.core.files.base import File
from .models import APIImage
from accounts.models import CustomUser
from plans.models import Plan
from rest_framework.test import APIClient

class ImagesTest(TestCase):
    @staticmethod
    def get_image_file(name, ext='png', size=(1000, 1000), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGB", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name + '.' + ext)
       
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
        expires_after_default = APIImage._meta.get_field('expires_after').get_default() 
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
        image_id = 1
        expected_response = {'id': 1, 'urls': "['http://testserver/image/1/thumbnail/200', 'http://testserver/image/1/thumbnail/400', 'http://testserver/image/1/original', 'http://testserver/image/1/binary']"}
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
    
    #def test_image_binary(self):

        