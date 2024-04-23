from setuptools import setup, find_packages
 
setup(
  name='mapal',
  version='1.0',
  description='MAPping ALloys - A Python library for mapping features and properties of alloys over compositional spaces.',
  url='https://sites.google.com/view/mapal-pylib',
  author='Dishant Beniwal; Pratik K. Ray',
  author_email='dishant.beniwal@gmail.com; ',
  license='MIT',
  keywords='mapal; mapping alloys; alloy features; multi-principal element alloys', 
  packages=find_packages(),
  include_package_data=True,
  package_data={
      'mapal': ["element_data/mapal_EL1/*",
      "preTrained_ML_mods/*",
      "preTrained_ML_mods/M1-trained-model/*",
      "preTrained_ML_mods/M1-trained-model/min_max_feat_values/*",
      "preTrained_ML_mods/M1-trained-model/mod_files/*",
      "preTrained_ML_mods/M2-trained-model/min_max_feat_values/*",
      "preTrained_ML_mods/M2-trained-model/mod_files/*"]
   },
  install_requires=[
    'numpy',
    'pandas',
    'tensorflow',
    'matplotlib',
    'plotly',
    'scikit-image'
  ]
)