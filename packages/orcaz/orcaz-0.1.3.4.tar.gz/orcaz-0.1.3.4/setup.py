from setuptools import setup

setup(
    name='orcaz',
    version='0.1.3.4',
    packages=['orcaz'],
    url='',
    license='GNU General Public License v3.0',
    author='Zacharias Chalampalakis, PhD, Lalith Kumar Shiyam Sundar, PhD',
    author_email='zacharias.chalampalakis@meduniwien.ac.at, lalith.shiyamsundar@meduniwien.ac.at',
    description='ORCA (Optimized Registration through Conditional Adversarial networks) ',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    install_requires=['pyfiglet~=0.8.post1',
                      'setuptools~=65.5.1',
                      'nibabel',
                      'tqdm',
                      'torch>=0.4.1',
                      'torchvision>=0.2.1',
                      'matplotlib',
                      'tensorboard',
                      'scipy',
                      'SimpleITK',
                      'scikit-learn',
                      'emoji',
                      'pydicom',
                      'dicom2nifti',
                      'moosez',
                      'falconz',
                      'nifti2dicom',
                      'rich',
                      'pathlib'],
    entry_points={
        'console_scripts': [
            'orcaz = orcaz.orcaz:main',
        ],
    },
)

