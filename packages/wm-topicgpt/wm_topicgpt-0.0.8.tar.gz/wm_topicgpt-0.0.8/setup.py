from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    install_requires = f.read().splitlines()

with open("topicgpt/README.md", "r") as f:
    long_description = f.read()

setup(
    name='wm_topicgpt',
    version='0.0.8',
    description='This is a package to generate topics for the text corpus.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=install_requires,
    python_requires='>=3.9',
)