# `mirofile` - Your buddy for dealing with raw MIROSLAV data

#### What is it?

**MIROSLAV (Multicage InfraRed Open Source Locomotor Activity eValuator)** is a platform for non-invasive monitoring of circadian locomotor activity in laboratory rodents. All of its hardware and software components are described in the paper: #url

This `mirofile` library, acting as a file-like object, loads raw MIROSLAV files containing experimental data and parses them into a sequence of lists, each containing appropriately-typed timestamps and sensor readings, which can then be turned into a `pandas` data frame by the user.

A script which exemplifies the use of this library can also be found in the MIROSLAV paper's data repository: #url.

#### How to install?

`mirofile` is [available on PyPi](https://pypi.org/project/mirofile/) can be installed with `pip`:

```bash
pip install mirofile
```

##### Dependencies

 * [`tqdm`](https://pypi.org/project/tqdm/) - can be also be installed with `pip`

#### License

The code is distributed under GPLv3.
