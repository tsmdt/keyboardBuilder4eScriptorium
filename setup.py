from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Keyboard Builder for eScriptorium",
    author="Thomas Schmidt",
    version='0.1',
    packages=find_packages(),
    package_data={
        '': ['templates/*.html', 'static/fonts/*', 'static/img/*'],
    },
    license="MIT License",
    description="Build virtual keyboards for eScriptorium with ease...",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tsmdt/keyboardBuilder4eScriptorium",
    install_requires=[
        'Flask==3.0.3',
        'click==8.1.7'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    entry_points={
        'console_scripts': [
            'keybuilder=src.keyboard_builder:main',
        ],
    },
)
