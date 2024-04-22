from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()

from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as f:
    long_desc = f.read()


setup(name='FunPayPython',
      version="1.1.1",
      description='Прослойка между FunPayAPI и клиентом. [Исправленная версия]',
      long_description=long_desc,
      long_description_content_type="text/markdown",
      author='ArttekPublic',
      author_email='arttekpublic@mail.ru',
      url='https://discord.gg/HNhrWJKz3T',
      packages=find_packages("."),
      license='GPL3',
      keywords='funpay bot api tools',
      install_requires=['requests==2.28.1', 'beautifulsoup4', 'requests_toolbelt==0.10.1'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Programming Language :: Python :: 3',
          'Environment :: Console',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      ]
)
