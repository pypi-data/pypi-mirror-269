from setuptools import setup, find_packages
import os

def parse_requirements(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

# Function to find all files in the 'models/' directory
def find_model_files(directory):
    model_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            model_files.append(os.path.relpath(os.path.join(root, file), directory))
    return model_files

setup(
    name='anprs',
    version='0.0.5',
    author='Aditya Upadhye',
    author_email='adityasu12@gmail.com',
    description='Automatic Number Plate Recognition System',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Adityaupadhye/package_anprs',
    packages=find_packages(exclude=['.vscode/*', 'local_env/*']),
    package_data={
        '': ['../media/*', '../models/*', '../results/*']
    },
    include_package_data=True,
    # data_files=[('models', find_model_files('./models'))],
    install_requires=[
        'opencv-python-headless',
        'keras',
        'tensorflow-cpu'
    ],
    python_requires='>=3.6',
)
