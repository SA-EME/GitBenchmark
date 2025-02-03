"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""

def create_file(file, content):
    """
    Create a file with the given name.

    Args:
        file (str): The name of the file to create.
    """
    with open(file, 'w') as f:
        f.write(content)