from setuptools import setup, find_packages

setup(
    name='denpy',
    version='0.2.1',
    description='Simple? Fast? Easy to use? DENPY!',
    author='Discord: denflash',
    packages=find_packages(),
    install_requires=['rich', 'psutil', 'py-cord', 'mysql-connector-python', 'requests']
)
