from setuptools import setup

setup(
   name='GameOn',
   version='1.0.0',
   description='A useful game engine for beginners',
   author='Morris El Helou',
   author_email='morriselhelou816@gmail.com',
   include_package_data=True,
   packages=['GameOn'], 
   package_data={"GameOn": ["*.ico"]},
   install_requires=['pygame','keyboard','tymer'], #external packages as dependencies
)