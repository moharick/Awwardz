from django.test import TestCase
from .models import Project, Profile, Review

# Create your tests here.
class ProjectTestClass(TestCase):
    def setUp(self):
        self.git= Project(title = 'git',home = 'photos/photos/blog.png',description ='personal blogsite',live_link ='https://github.com ',design ='9',usability='8',content = '9', overall = '8', posted= '2019-08-05 16:05:47.026576+03',user = '1')

    def test_instance(self):
        self.assertTrue(isinstance(self.git,Project))

    def test_save_method(self):
        self.git.save_project()
        projects = Project.objects.all()
        self.assertTrue(len(projects)>0)

    def test_delete_method(self):
        self.git.save_project()
        projects = Project.objects.all()
        self.assertFalse(len(projects) == 0)

    def test_get_project(self):
        projects = Project.objects.all()
        self.assertFalse(len(projects)>0)

    def tearDown(self):
        Project.objects.all().delete()
        Review.objects.all().delete()
        Profile.objects.all().delete()


class ProfileTestClass(TestCase):
    def setUp(self):
        self.moharick = Profile(user = '1', profile_photo = '', bio = 'the guy who knows a guy',contact ='moharick@yahoo.com')

    def test_instance(self):
        self.assertTrue(isinstance(self.moharick, Profile))

    def test_save_method(self):
        self.moharick.save_profile()
        profiles = Profile.objects.all()
        self.assertFalse(len(profiles) > 0)

    def test_delete_method(self):
        self.moharick.save_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) == 0)





