from setuptools import setup, find_packages

setup(
    name='sysinfobj',
    version='0.1.1',
    packages=find_packages(),
    description='Linux system statistics',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Bharath',
    author_email='learnit.linux@gmail.com',
    url='https://github.com/bharathjakkani/sysinfo',
    python_requires='>=3.7',
    install_requires=[
        'psutil',  # Include any other dependencies your package needs
    ],
    entry_points={
        'console_scripts': [
            'sysinfo=sysinfo.sysinfo:get_system_stats',
        ],
    },
)

