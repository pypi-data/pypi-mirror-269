# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['arctic3d', 'arctic3d.modules']

package_data = \
{'': ['*']}

install_requires = \
['bio==1.6.2',
 'biopython==1.83',
 'defusedxml==0.7.1',
 'jsonpickle==3.0.3',
 'kaleido==0.2.1',
 'lxml==5.2.0',
 'matplotlib==3.8.2',
 'mdanalysis==2.7.0',
 'openpyxl==3.1.2',
 'pandas==2.2.1',
 'pdb-tools==2.5.0',
 'pdbecif==1.5',
 'plotly==5.19.0',
 'requests==2.31.0',
 'scipy==1.12.0']

entry_points = \
{'console_scripts': ['arctic3d = arctic3d.cli:maincli',
                     'arctic3d-localise = arctic3d.cli_localise:maincli',
                     'arctic3d-resclust = arctic3d.cli_resclust:maincli',
                     'arctic3d-restraints = arctic3d.cli_restraints:maincli']}

setup_kwargs = {
    'name': 'arctic3d',
    'version': '0.4.1',
    'description': 'Automatic Retrieval and ClusTering of Interfaces in Complexes from 3D structural information',
    'long_description': '# ARCTIC-3D\n\n[![ci](https://github.com/haddocking/arctic3d/actions/workflows/ci.yml/badge.svg)](https://github.com/haddocking/arctic3d/actions/workflows/ci.yml)\n[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/dc788367452c47928e30f2f1f481d7e4)](https://www.codacy.com/gh/haddocking/arctic3d/dashboard?utm_source=github.com&utm_medium=referral&utm_content=haddocking/arctic3d&utm_campaign=Badge_Coverage)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/dc788367452c47928e30f2f1f481d7e4)](https://www.codacy.com/gh/haddocking/arctic3d/dashboard?utm_source=github.com&utm_medium=referral&utm_content=haddocking/arctic3d&utm_campaign=Badge_Grade)\n[![SQAaaS badge shields.io](https://img.shields.io/badge/sqaaas%20software-bronze-e6ae77)](https://api.eu.badgr.io/public/assertions/oAuS52pQTWaC90qMk97hlA "SQAaaS bronze badge achieved")\n[![fair-software.eu](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B%20%20%E2%97%8B%20%20%E2%97%8F-orange)](https://fair-software.eu)\n\n[![SQAaaS badge](https://github.com/EOSC-synergy/SQAaaS/raw/master/badges/badges_150x116/badge_software_bronze.png)](https://api.eu.badgr.io/public/assertions/oAuS52pQTWaC90qMk97hlA "SQAaaS bronze badge achieved")\n\n<img src="docs/imgs/arctic3d.png" width="450">\n\n**A**utomatic **R**etrieval and **C**lus**T**ering of **I**nterfaces in Complexes from **3D** structural information\n\n## WEB SERVER\n\nARCTIC-3D is available at this webserver https://wenmr.science.uu.nl/arctic3d/\n\n## ARCTIC-3D: all you want to know about protein-specific interfaces\n\nARCTIC-3D is a software for data-mining and clustering of protein interface information. It allows you to retrieve all the existing interface information for your desired protein from the PDBE graph database (https://www.ebi.ac.uk/pdbe/pdbe-kb/), grouping similar interfaces in interacting surfaces.\n\nThe software first checks your input (a uniprot ID, a FASTA file, or a PDB file), and then retrieves the existing interaction data from the [graph API](https://www.ebi.ac.uk/pdbe/graph-api/pdbe_doc/). Such interfaces are projected on a selected PDB structure and their dissimilarity is calculated, thus allowing for the application of a hierarchical clustering algorithm.\n\nIn output you will see how your favourite protein can display different binding surfaces, each one characterised by few residues that are always present (_hotspots_) and other amino acids which are at the interface only from time to time.\n\n## Developing\n\nCheck [CONTRIBUTING.md](CONTRIBUTING.md) for more information.\n\n## Installation\n\n### With `conda`\n\nClone the repository on your computer and navigate to it\n\n```bash\ngit clone git@github.com:haddocking/arctic3d.git\ncd arctic3d\n```\n\nHere you can create the arctic3d environment:\n\n```bash\nconda create -n arctic3d python=3.10\nconda activate arctic3d\npip install .\narctic3d -h\n```\n\n## To run BLAST locally\n\n```bash\nbash install_blast_deps.sh\n```\n\nAnd put `blastp` in your `$PATH` by adding the following line to your `.bashrc` or `.bash_profile` file:\n\n```bash\nexport PATH="PATH_TO_YOUR_ARCTIC3D_INSTALLATION/src/ncbi-blast-2.15.0+/bin:$PATH"\n```\n\n## Example usage\n\nPlease refer to the [examples](docs/examples.md) documentation page.\n\n## Detailed documentation\n\nIn order to generate a detailed html documentation please execute these commands\n\n```text\npip install myst_parser\npip install chardet\nconda install sphinx\nsphinx-build -E docs ./arctic3d-docs\n```\n\nThen you can open the file `arctic3d-docs/index.html`, which contains all the necessary documentation.\n\n## Citing us\n\nIf you used ARCTIC-3D in your work please cite the following publication:\n\n**Marco Giulini, Rodrigo V. Honorato, Jesús L. Rivera, and Alexandre MJJ Bonvin**: "ARCTIC-3D: automatic retrieval and clustering of interfaces in complexes from 3D structural information." Communications Biology 7, no. 1 (2024): 49. (www.nature.com/articles/s42003-023-05718-w)\n',
    'author': 'BonvinLab',
    'author_email': 'bonvinlab.support@uu.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
