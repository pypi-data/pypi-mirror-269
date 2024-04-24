from setuptools import setup, find_packages

setup(
    name='copilot4office',
    version='0.1',
    # packages=find_packages(exclude=["tests*", "docs*"]),
    packages=find_packages(where='presentation'),
    description='ChatGPT copilot for office files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Faisal Rehman',
    author_email='fslurrehman@gmail.com',
    license='MIT',
    install_requires=[
        'python-pptx',  # dependency
    ],
    #  entry_points={
    #      'console_scripts': [
    #         'PresentationCreator=copilot4office.ex',
    #         'PresentationProcessor=copilot4office.presentation_processor:PresentationProcessor'
    #     ]
    #  },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
