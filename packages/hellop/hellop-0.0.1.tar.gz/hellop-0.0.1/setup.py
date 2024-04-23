from setuptools import setup, find_packages
setup(
    name='hellop',
    version='0.0.1',
    packages=find_packages(),
    install_requires= [
        # Add dependencies here.
        # e.g. 'numpy>=1.11.1'
    ],
    entry_points={
        "console_scripts": [
            "hellop = hellop:hello"
        ]
    },
    author="rehmet",
    description="A hello world girly",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown"
)