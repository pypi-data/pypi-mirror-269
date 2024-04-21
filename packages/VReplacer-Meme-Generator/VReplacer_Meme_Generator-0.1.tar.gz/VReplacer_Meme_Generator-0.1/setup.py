import setuptools


setuptools.setup(
    name="VReplacer_Meme_Generator",
    version="0.1",
    packages=setuptools.find_packages(),
    description="Tool for replacing random word in string and generating images",
    url="https://github.com/DaSzary/vReplacer-meme-generator",
    package_data={'VReplacer_Meme_Generator': ['_Helpers.py']},
    python_requires='>=3.9'
)