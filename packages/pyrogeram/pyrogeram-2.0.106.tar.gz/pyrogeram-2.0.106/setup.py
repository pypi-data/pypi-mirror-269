from setuptools import setup, find_packages

# Membaca isi dari requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="pyrogeram",
    version="2.0.106",
    packages=find_packages(),
    description='Seratus Persen Clone Pyrofork',
    author="rizaldevs",
    author_email="rizaldaitona@gmail.com",
    url="https://t.me/pyrogram",
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=requirements,
)

