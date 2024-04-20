from setuptools import setup, find_packages

setup(
    name='newdao-hello-tea',
    version='2.0.0',
    packages=find_packages(),
    install_requires=['numpy'],
    entry_points={
        'console_scripts': [
            'newdao-hello-tea = newdao_hello_tea.main:print_hello_tea'
        ]
    },
    author='Newdao',
    author_email='l0dx16@gmail.com',
    description='Prints "hello tea" using NumPy',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/newdao-hello-tea',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
