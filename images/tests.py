from django.test import TestCase
from io import BytesIO
from PIL import Image
from rest_framework.reverse import reverse
from django.urls import path, include
from django.utils import timezone
from django.core.files.base import File
from .models import APIImage
from accounts.models import CustomUser
from plans.models import Plan
import base64
from django.test.client import Client


class ImagesTest(TestCase):
    @staticmethod
    def get_image_file_png(name='test.png', ext='png', size=(1000, 1000), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGB", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)
    def get_image_file_jpg(name='test.jpg', ext='jpg', size=(1000, 1000), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGB", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)
    def get_image_file_wrong_ext(name='test.gif', ext='gif', size=(1000, 1000), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGB", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
    
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
        for plan_id in list_plans_id:
            user_id = plan_id
            default_plan = Plan.objects.get(id=plan_id)
            CustomUser.objects.create(
            username='test_{0}'.format(user_id), 
            email='test@example.com', 
            password='password',
            plan = default_plan,
            )
        list_users_id = [1, 2, 3]
        for user_id in list_users_id:
            user = CustomUser.objects.get(id=user_id)
            expires_after_default = APIImage._meta.get_field('expires_after').get_default() 
            APIImage.objects.create(
                user = user,
                image = ImagesTest.get_image_file_png(),
                expires_after = expires_after_default,
                created_at = timezone.now(),
            )
        
    def test_validate_file_extetion(self):
        user = CustomUser.objects.get(id=1)
        expires_after_default = APIImage._meta.get_field('expires_after').get_default() 
        self.assertRaisesMessage(APIImage.objects.create(
            user = user,
            image = ImagesTest.get_image_file_png(),
            expires_after = expires_after_default,
            created_at = timezone.now(),
            ), 'File extension “gif” is not allowed. Allowed extensions are: jpg, jpeg, png.')
       
    def test_list_immage_plans(self):
        dict_json_answers = {
            1: [{"id":1,"urls":"['http://127.0.0.1:8000/image/1/thumbnail/200?format=json']"}],
            2: [{"id":1,"urls":"['http://127.0.0.1:8000/image/1/thumbnail/200?format=json', 'http://127.0.0.1:8000/image/1/thumbnail/400?format=json', 'http://127.0.0.1:8000/image/1/original?format=json']"}],
            3: [{"id":1,"urls":"['http://127.0.0.1:8000/image/1/thumbnail/200?format=json', 'http://127.0.0.1:8000/image/1/thumbnail/400?format=json', 'http://127.0.0.1:8000/image/1/original?format=json', 'http://127.0.0.1:8000/image/1/binary?format=json']"}]
        }
        for key in dict_json_answers:
            username = CustomUser.objects.get(id=key).username
            password = CustomUser.objects.get(id=key).password
            credentials = f"{username}:{password}".encode('utf-8')
            encoded_credentials = base64.b64encode(credentials).decode('utf-8')
            client = Client() 
            responce = client.get('image_list', HTTP_AUTHORIZATION=f'Basic {encoded_credentials}')
            print(responce)