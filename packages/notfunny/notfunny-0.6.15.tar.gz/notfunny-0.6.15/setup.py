from setuptools import setup

setup(name='notfunny',
      version='0.6.15',
      description='Only the worst',
      long_description='Really, the worst jokes around. Actually just the one worst. This is really just a test project for packaging python projects. But as an added bonus it really isnt funny.',
      long_description_content_type='text/x-rst',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='joke',
      url='http://github.com/ohthepain/notfunny',
      author='Paul Wilkinson',
      author_email='paul@thisco.co',
      license='MIT',
      packages=['notfunny'],
      scripts=['bin/notfunny-joke'],
      # entry_points = {
      #   'console_scripts': ['funniest-joke=funniest.command_line:main'],
      # },
      install_requires=[
            # 'unittest'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
