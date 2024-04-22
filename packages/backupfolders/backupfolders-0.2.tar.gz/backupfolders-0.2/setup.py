import setuptools

with open("README.md","r") as f:
    long_description = f.read()

setuptools.setup(
  name = 'backupfolders',
  version = '0.2',
  license='MIT',
  long_description = long_description,
  long_description_content_type = "text/markdown",
  description = 'Backup your folders from one location to another with ease.',
  author = 'Fahad Devnikar',
  author_email = 'devnikarfahad@gmail.com',
  url = 'https://github.com/Fahad-codecraft',
  keywords = ['backup', 'folders', 'files'],
  install_requires=[
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)
