from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import os

package_name = 'miksi_ai_sdk'


def find_cython_extensions(package_dir):
    extensions = []
    for root, _, files in os.walk(package_dir):
        for file in files:
            if file.endswith(".pyx"):
                full_path = os.path.join(root, file)
                module_path = full_path[:-4].replace(os.path.sep, '.')
                ext = Extension(module_path, [full_path])
                extensions.append(ext)
    return extensions


extensions = cythonize(find_cython_extensions(package_name), compiler_directives={'language_level': "3"})

setup(
    name="miksiai",
    version="1.0", 
    author="RichardKaranuMbuti",
    author_email="officialforrichardk@gmail.com",
    description="Miksi-AI empowers your BI",
    long_description=open('docs.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Miksi-io/Custom-Agent",
    packages=find_packages(),
    ext_modules=extensions,
    python_requires='>=3.6',
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    zip_safe=False
)
