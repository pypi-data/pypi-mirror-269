from setuptools import setup
setup(
	name="whole",
	version="1.0.0.0.0.6",
	packages=["whole"],
    install_requires=[
    "mysql-connector",
    "xlrd == 1.2.0",
    ],
    entry_points="""
    [console_scripts]
    t = whole.TCP_UDP:TU
    """,
)