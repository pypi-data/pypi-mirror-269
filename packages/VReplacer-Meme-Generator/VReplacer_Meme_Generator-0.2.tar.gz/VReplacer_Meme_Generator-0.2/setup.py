import setuptools


with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="VReplacer_Meme_Generator",
    version="0.2",
    packages=setuptools.find_packages(),
    description="Tool for replacing random word in string and generating images",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/DaSzary/vReplacer-meme-generator",
    package_data={'VReplacer_Meme_Generator': ['_Helpers.py']},
    python_requires='>=3.9'
)