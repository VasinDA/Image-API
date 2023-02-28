from django.test import TestCase
from .models import CustomUser
from plans.models import Plan

class AccountTest(TestCase):
    def setUp(self):
        Plan.objects.create(
            title='Basic', 
            original_image_link = False, 
            binary_image_link = False, 
            available_hights = '200')
        plan_user_default=CustomUser._meta.get_field('plan').get_default()
        self.default_plan = Plan.objects.get(id=plan_user_default)
        self.user = CustomUser.objects.create(
            username='test', 
            email='test@example.com', 
            password='password',
            plan = self.default_plan,
            )
        
    def test_user_default_plan(self):
        self.assertEqual(self.user.plan.id, 1)