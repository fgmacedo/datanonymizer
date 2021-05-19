=============
datanonymizer
=============

Anonymizer tool for datasets such CSV files.

To generate fake data, you can choose between two excelent generators:

-  `Faker <https://faker.readthedocs.io/en/stable/index.html>`_  (default).
-  `mimesis <https://mimesis.name/index.html>`_ via optional install.


Install
=======

Using pip:

.. code-block:: bash

  pip install datanonymizer


Using mimesis instead of the default Faker:

.. code-block:: bash

  pip install datanonymizer[mimesis]


Or from source:

.. code-block:: bash

  git clone https://github.com/fgmacedo/datanonymizer
  cd datanonymizer
  python setup.py install


Usage
=====

Pass your data through ``stdin`` and get it back anonymized on ``stdout``.

.. note::

    In this case, the output will be equal to the input as no conversions were applied.


.. code-block:: bash

  cat input_file.csv | datanonymizer >output_file.csv

Using a config file to declare conversions and generators for the required fields:


.. code-block:: bash

  cat input_file.csv | datanonymizer --config ./dataset_anon_config.yml >output_file.csv


Optional arguments:

.. code-block::

  -h, --help            show this help message and exit
  -l LANGUAGE, --language LANGUAGE
                        Language used by the Generator
  -di DELIMITER_INPUT, --delimiter_input DELIMITER_INPUT
                        CSV delimiter
  -do DELIMITER_OUTPUT, --delimiter_output DELIMITER_OUTPUT
                        CSV delimiter
  -i, --ignore_errors   Continue on errors
  --head HEAD           Outputs only the first <HEAD> lines
  -g {faker,mimesis}, --generator {faker,mimesis}
                        Generator library to be used for fake data
  --seed SEED           Seed for the pseudo random generator providers
  --config CONFIG       Configuration file


Config file
===========

You'l need a configuration file to setup transformations for each dataset.

This file is a simple `yaml <https://yaml.org/>`_  where you can configure fields.

Field names should match the column name declared into the CSV input file.

.. code-block:: yaml

  ---
  fields:
    Task ID:
      omit: true
    Location:
      conversions:
        - fn: coords_to_h3
          kwargs:
            resolution: 8
    Client Address:
      conversions:
        - fn: has_value
      rename: has_address
    Company Name:
      generator:
        provider: business.company
      rename: company
    Invoice ID:
      generator:
        provider: person.identifier
        kwargs:
          mask: "#######"
      rename: invoice


Generators
----------

The generatos clause depends of the library you choose to provide fake data.


You can use any generator available at the generic API from
`Faker <https://faker.readthedocs.io/en/stable/providers.html>`_ or
`mimesis <https://mimesis.name/api.html>`_ .


For example, if you wanna mimic data with company names:

- Faker

  .. code-block:: yaml

    ---
    fields:
      Company Name:
        generator:
          provider: company

- Mimesis

  .. code-block:: yaml

    ---
    fields:
      Company Name:
        generator:
          provider: business.company

But you can replace the real names by names of fruits (using Mimesis) or any other provider:

.. code-block:: yaml

  ---
  fields:
    Company Name:
      generator:
        provider: food.fruit


Or generate random integers to replace real IDs:

- Faker

  .. code-block:: yaml

    ---
    fields:
      ID:
        generator:
          provider: pyint
          kwargs:
            min_value: 1
            max_value: 15_000_000

- Mimesis

  .. code-block:: yaml

    ---
    fields:
      ID:
        generator:
          provider: person.identifier
          kwargs:
            mask: "#######"


Conversions
-----------

You can apply any pre-configured conversion functions available.


- coords_to_h3
- has_value
