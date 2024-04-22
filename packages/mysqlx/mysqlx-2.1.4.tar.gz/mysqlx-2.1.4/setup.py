import os
from setuptools import setup

# INSTALL_PACKAGES = open(path.join(DIR, 'requirements.txt')).read().splitlines()
def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path), 'r', encoding='UTF-8') as fp:
        return fp.read()

long_description = read("README.rst")

setup(
    name='mysqlx',
    packages=['mysqlx'],
    description="A thread safe sql executor for MySQL like MyBatis with connection pool. It helps you automatically manage database connections and transactions. It also provides ORM operations for single tables.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'Jinja2>=2.7.0',
        'sqlx-exec>=2.3.6',
    ],
    version='2.1.4',
    url='https://gitee.com/summry/mysqlx',
    author='summy',
    author_email='xiazhongbiao@126.com',
    keywords=['sql', 'MySQL', 'MyBatis', 'python'],
    package_data={
        # include json and txt files
        '': ['*.rst', '*.dtd', '*.tpl'],
    },
    include_package_data=True,
    python_requires='>=3.5',
    zip_safe=False
)

