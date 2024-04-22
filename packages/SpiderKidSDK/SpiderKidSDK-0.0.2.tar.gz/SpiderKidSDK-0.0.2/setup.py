import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SpiderKidSDK",
    version="0.0.2",
    author="Jyonn Liu",
    author_email="liu@qijiong.work",
    description="SpiderKid SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jyonn/SpiderKidSDK",
    packages=setuptools.find_packages(),
)
