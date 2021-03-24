from setuptools import setup

with open("README.MD", 'r') as fp:
    long_description = fp.read()

setup(
   name='Andrew Wong Backend Engineering Intern Coding Challenge',
   version='1.0',
   description='Backend Engineering Intern Coding Challenge',
   long_description=long_description,
   author='Andrew Wong',
   author_email='wong.816@osu.edu',
   scripts=['notifications.py', 'test_notifications.py', 'load_json.py'],
   data_files = ['notifications_old.json']
)