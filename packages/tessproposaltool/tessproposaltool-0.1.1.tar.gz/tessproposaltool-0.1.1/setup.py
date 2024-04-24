# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tessproposaltool']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=6.0.1,<7.0.0',
 'astroquery>=0.4.7,<0.5.0',
 'asyncio>=3.4.3,<4.0.0',
 'lxml>=5.2.1,<6.0.0',
 'numpy>=1.26.4,<2.0.0',
 'pandas>=2.2.2,<3.0.0',
 'rich>=13.7.1,<14.0.0',
 'toml>=0.10.2,<0.11.0',
 'tqdm>=4.66.2,<5.0.0']

entry_points = \
{'console_scripts': ['tpt = tessproposaltool.tpt:tpt']}

setup_kwargs = {
    'name': 'tessproposaltool',
    'version': '0.1.1',
    'description': '',
    'long_description': '<a href="https://github.com/tessgi/tessproposaltool/actions/workflows/tests.yml"><img src="https://github.com/tessgi/tessproposaltool/workflows/pytest/badge.svg" alt="Test status"/></a> [!\n[![PyPI version](https://badge.fury.io/py/tessproposaltool.svg)](https://badge.fury.io/py/tessproposaltool)\n\n# TESS Proposal Tool\n\nUnder development tool to help create TESS proposals and target lists.\n\n## Use Case 1: Filling in missing TICs in a target list\n\nIf you have a list of RAs, Decs, and optionally TESS magnitudes and you would like to crossmatch them against TIC, you can do this with the `tessproposaltool`. You can do this from the command line using:\n\n```shell\ntpt radec_file.csv -o output.csv\n```\n\nWhich will result in a file `output.csv` that contains the corrected RA, Dec, TESS magnitude and TIC numbers.\n\nYour file should have a structure that contains RAs, Decs, and optionally TESS magnitudes, e.g.:\n\n```shell\nra,dec,tmag\n40.2986,56.7305,9.39\n110.093,-22.2673,13.51\n116.243,-30.0918,9.5\n152.633,-59.3549,10.05\n163.437,-58.4871,9.91\n165.091,-60.7688,12.974\n```\n\nTo do this inside Python you can use\n\n```python\nfrom tessproposaltool import fill_tics\n\n# read in your radecs, or convert them into a pandas dataframe\nRA, Dec, Tmag = ..., ..., ...\ndf = pd.DataFrame(np.asarray([RA, Dec, Tmag]).T, columns=[\'ra\', \'dec\', \'tmag\'])\nnew_df = fill_tics(df)\n```\n',
    'author': 'Christina Hedges',
    'author_email': 'christina.l.hedges@nasa.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
