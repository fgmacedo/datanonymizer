=============
datanonymizer
=============

Anonymizer tool for datasets such CSV files.

Uses the excelent library `mimesis <https://mimesis.name/index.html>`_ to generate fake data.

Install
=======

Using pip:

```
pip install datanonymizer
```

Or from source:

```
git clone https://github.com/fgmacedo/datanonymizer
cd datanonymizer
python setup.py install
```


Usage
=====

Pass your data through ``stdin`` and get it back anonymized on ``stdout``.

.. note:

    In this case, the output will be equal to the input as no conversions were applied.


``` bash
cat input_file.csv | datanonymizer >output_file.csv
```

Using a config file to declare conversions and generators for the required fields:

``` bash
cat input_file.csv | datanonymizer --config ./dataset_anon_config.yml >output_file.csv
```

Optional arguments:

```
  -h, --help            show this help message and exit
  -l LANGUAGE, --language LANGUAGE
                        Language used by the Generator
  -di DELIMITER_INPUT, --delimiter_input DELIMITER_INPUT
                        CSV delimiter
  -do DELIMITER_OUTPUT, --delimiter_output DELIMITER_OUTPUT
                        CSV delimiter
  --head HEAD           Outputs only the first <head> lines
  --seed SEED           Seed for the pseudo random generator providers
  --config CONFIG       Configuration file
```

Config file
===========

You'l need a configuration file to setup transformations for each dataset.

This file is a simple `yaml <https://yaml.org/>`_  where you can configure fields.

Field names should match the column name declared into the CSV input file.

``` yaml
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
```


Generators
----------

You can use `any generator <https://mimesis.name/api.html>`_ available at the
generic API from mimesis.

For example, if you wanna mimic data with company names:

``` yml
---
fields:
  Company Name:
    generator:
      provider: business.company
```

But you can replace the real names by names of fruits:


``` yml
---
fields:
  Company Name:
    generator:
      provider: food.fruit
```


Conversions
-----------

You can apply any pre-configured conversion functions available.


- coords_to_h3
- has_value
