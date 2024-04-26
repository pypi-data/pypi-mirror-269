from setuptools import setup

setup(
   name='gameon',
   version='1.0.2',
   description='A useful game engine for beginners',
   author='Morris El Helou',
   author_email='morriselhelou816@gmail.com',
   include_package_data=True,
   packages=['gameon'], 
   package_data={"gameon": ["*.ico"]},
   install_requires=['pygame','keyboard','tymer'], #external packages as dependencies
)