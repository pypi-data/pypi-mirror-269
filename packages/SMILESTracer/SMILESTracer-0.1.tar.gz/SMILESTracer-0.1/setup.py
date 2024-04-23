import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SMILESTracer",
    version="0.1",
    author="jnliu",
    author_email="2100011879@stu.pku.edu.cn",
    description="Labling reaction SMILES with atom-mapped SMARTS and reaction SMILES",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DMSO0408/SMILESTracer.git",
    packages=setuptools.find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'SMILESTracer = SMILESTracer:main'
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)