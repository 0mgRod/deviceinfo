from setuptools import setup, find_packages

setup(
    name="dvinfo",
    version="1.3",
    description="A package for getting system information on Windows and Linux",
    url="https://github.com/0mgRod/deviceinfo",
    author="OmgRod",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    keywords="system info",
    packages=find_packages(),
    install_requires=[
        "psutil",
        "netifaces",
        "wmi",
        "py-cpuinfo",
        "requests",
        "pytemperature",
        "pythonping",
        "paramiko",
        "speedtest-cli",
        "pywebview[qt]",
    ],
)
