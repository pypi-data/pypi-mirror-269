VST Compile utility
===================

Lib for quick formatting `setup.py` in projects. Moved from `vstutils` projects for easyer integration.

Quick start
-----------

1. Install package via `pip install vstcompile`

2. Create `requirements.txt` and `setup.py` in your project:

   .. sourcecode:: python

      import os
      from vstcompile import load_requirements, make_setup, find_packages


      # allow setup.py to be run from any path
      os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

      ext_list = [
        ... some extentions import paths with `*.py, *.c or *.pyx` extentions ...
      ]
      
      make_setup(
        packages=find_packages(exclude=['tests']+ext_list),
        ext_modules_list=ext_list,
        include_package_data=True,
        install_requires=load_requirements('requirements.txt')
      )

3. Run `python setup.py compile` to compile and pack dist-package.

4. Add requirement to `pyproject.toml` and enjoy!

Requirements
------------

If you want to use Sphinx in projects, you should install package with sphinx packages.

If you want to use github release, install it with extra `release` and use command `githubrelease`:

   .. sourcecode:: bash

      pip install vstcompile[release]
      python setup.py githubrelease


License
-------

VST Compile is licensed under the terms of the Apache License 2.0.
See the file "LICENSE" for more information.

Copyright 2018-2023 VST Consulting
