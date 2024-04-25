from setuptools import setup, find_packages

setup(
    name='pygame-magics',
    version='0.2.0',
    author='MCtop4ik',
    author_email='senyaza@mail.ru',
    description='Magic survival funcs',
    long_description='Hyper grest library for magic survival',
    long_description_content_type='text/markdown',
    url='https://github.com/MCtop4ik/pygame-magics',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',

    install_requires=[
        'pygame',
    ],
)
