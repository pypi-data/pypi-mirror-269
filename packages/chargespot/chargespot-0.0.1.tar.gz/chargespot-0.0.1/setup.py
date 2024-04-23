from setuptools import setup, find_packages

setup(
    name="chargespot",
    version="0.0.1",
    keywords=("api test", "automation", "testing", "chargespot"),
    description="api test tools",
    long_description="simplify api testing",
    url="",
    author="chargespot",
    author_email="",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    platforms="any",
    install_requires=['requests', 'configobj', 'pyyaml', 'click', 'jinja2', 'pytest', 'pytest-html'],
    entry_points='''
    [console_scripts]
    chargespot=chargespot.cli:chargespot_cli
    '''
)
