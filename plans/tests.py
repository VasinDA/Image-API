from django.test import TestCase
from .models import Plan

class PlansTest(TestCase):
    def setUp(self):
        self.plan = Plan.objects.create(
            title='Basic', 
            original_image_link = False, 
            binary_image_link = False, 
            available_hights = '200')
        
    def test_plan_model(self):
        self.assertEqual(self.plan.title, 'Basic')
        self.assertEqual(self.plan.original_image_link, False)
        self.assertEqual(self.plan.binary_image_link, False)
        self.assertEqual(self.plan.available_hights, '200')

    def test_validate_available_hights(self):
        wrong_values_list = ['a', '!', ',', '@', '200,a', 'a,200']
        for value in wrong_values_list:
            self.assertRaisesMessage(Plan.objects.create(
                title='Basic', 
                original_image_link = False, 
                binary_image_link = False, 
                available_hights = value), "It should be integers only (e.g. '200' or '100,200')")
