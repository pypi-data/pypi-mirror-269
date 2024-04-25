from setuptools import setup, find_packages

setup(
    name='denseclus',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
    ],
    extras_require={
        'gpu-cu12': [
            'tensorflow-gpu==2.8.0; sys_platform=="linux"',  # Assuming CUDA 12 is meant for Linux platforms
            'cudatoolkit==12.0; sys_platform=="linux"'  # Specific CUDA toolkit version might be required
        ]
    },
    author='AnupamAS01 ',
    author_email='your.email@example.com',
    description='A clustering library with optional GPU support by AnupamAS01',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/anupamas01/denseclus',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
)
