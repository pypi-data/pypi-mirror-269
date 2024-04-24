from setuptools import setup

setup(
    name='SilverStreamingApplicationPoC',
    version='1.26',
    packages=['com.phida.main', 'com.phida.tests'],
    url='',
    license='',
    author='',
    author_email='',
    description='For Demo'
)

#roll back to version 1.3 for unmodified code(nearly)
#1.6 trying with show and count statements - once added df.show(), the heavy files(afvc)works good
#1.7 validating arguments from Spark Application. sparkAppName in sparksession.py
#1.8 fixing error due to comment after line: .appName(sparkAppName) \ - SyntaxError: unexpected character after line continuation character
#1.9 'Fix: NameError: name "sparkAppName" is not defined' in sparksession.py
#1.10 Added config.py to dynamically change appName in sparksession.py
#1.11 FOr Demo
#1.21 fixing k8s env secret in sparksession.py