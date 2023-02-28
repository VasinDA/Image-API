from django.test import TestCase
from io import StringIO
from io import BytesIO
from PIL import Image
from django.core.files.base import File
from .models import APIImage
from accounts.models import CustomUser
from plans.models import Plan

class ImagesTest(TestCase):
    @staticmethod
    def get_image_file_png(name='test.png', ext='png', size=(1000, 1000), color=(256, 0, 0)):
        file_obj = BytesIO
        image = APIImage.new("RGB", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)
    def get_image_file_jpg(name='test.jpg', ext='jpg', size=(1000, 1000), color=(256, 0, 0)):
        file_obj = BytesIO
        image = APIImage.new("RGB", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)
    
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
    def test_list_immage_plans(self):
        dict_json_answers = {
            1: [{"id":1,"urls":"['http://127.0.0.1:8000/image/1/thumbnail/200?format=json']"}],
            2: [{"id":1,"urls":"['http://127.0.0.1:8000/image/1/thumbnail/200?format=json', 'http://127.0.0.1:8000/image/1/thumbnail/400?format=json', 'http://127.0.0.1:8000/image/1/original?format=json']"}],
            3: [{"id":1,"urls":"['http://127.0.0.1:8000/image/1/thumbnail/200?format=json', 'http://127.0.0.1:8000/image/1/thumbnail/400?format=json', 'http://127.0.0.1:8000/image/1/original?format=json', 'http://127.0.0.1:8000/image/1/binary?format=json']"}]
        }
<<<<<<< HEAD
        #for key in dict_json_answers:
=======
        for key in dict_json_answers:
>>>>>>> 98c29e81d2f0257ad394508dabc7e9388b8eeb9c
            