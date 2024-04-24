from setuptools import setup

setup(
    name='easybloom',
    version='0.1.0',
    description='Simplifies using bloom ai. Brings it down to only 1 line of code.',
    url='https://github.com/shuds13/pyexample',
    author='Abbott Broughton',
    author_email='abbottbroughton@icloud.com',
    license='The Unlicense',
    packages=['ezbloom'],
    install_requires=['requests'],
    long_description='Use bloom_ans() to ask bloom questions like a chatbot.\nFor example, to ask bloom "Whats a '
                     'unicorn?" you would do this: bloom_ans("Whats a unicorn?") and you can use bloom_gen() to '
                     'generate the rest of a story you give it. It uses the same syntax as bloom_ans().',

    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)