import codecs
from setuptools import setup


with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="shadowsocks-alexforks",
    version="3.0.10",
    license='http://www.apache.org/licenses/LICENSE-2.0',
    description="A fast tunnel proxy that help you get through firewalls. FALL in forks.",
    author='clowwindy',
    author_email='clowwindy42@gmail.com',
    url='https://github.com/alexforks/shadowsocks',
    packages=['shadowsocks', 'shadowsocks.crypto'],
    package_data={
        'shadowsocks': ['README.rst', 'LICENSE']
    },
    install_requires=[],
    setup_requires=['wheel'],
    requires_python='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*',
    entry_points="""
    [console_scripts]
    sslocal = shadowsocks.local:main
    ssserver = shadowsocks.server:main
    """,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: Proxy Servers',
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
