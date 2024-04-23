from setuptools import setup

setup(
    name='saplinkpackage',
    version='0.3',
    packages=["saplinkpackage"],
    package_data={"saplinkpackage": ["*.pyd"]},
    install_requires=[
        'wmi',
        'xlrd',
        'numpy',
        'pywin32',
        'pyautogui',
        'datetime',
    ],
    author='MaoMao',
    author_email='maomao1037386322@gmail.com',
    description='Your package description',
    license='MIT',
)

#  terminal run
#  python package_switch.py sdist bdist_wheel
