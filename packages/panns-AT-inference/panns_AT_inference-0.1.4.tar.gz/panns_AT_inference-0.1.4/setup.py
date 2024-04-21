import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="panns_AT_inference",
    version="0.1.4",
    author="Qiuqiang Kong, Stefano Giacomelli (Ph.D. student UnivAQ)",
    author_email="qiuqiangkong@gmail.com, stefano.giacomelli@graduate.univaq.it",
    description="panns_AT_inference: audio tagging inference toolbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/StefanoGiacomelli/panns_AT_inference",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy', 'torch', 'matplotlib', 'librosa', 'torchlibrosa'],
    python_requires='>=3.6',
)
