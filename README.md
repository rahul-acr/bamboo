# Bamboo

Bamboo is a python based simple command line tool for creating regular backups

## Description

Bamboo is simple command line tool 


## Build

```commandline
python setup.py bdist_wheel
```

## Installation
Grab the wheel from the release or build from source
```commandline
python -m pip install dist/bamboo-0.1-py3-none-any.whl
```

And bamboo should be available from the terminal

## Uninstallation
```commandline
python -m pip uninstall bamboo
```

## Usage

```commandline
bamboo profile
bamboo device
bamboo backup --auto
```

## Examples
``bamboo device`` will list down all known devices, mount points and if they are online

```text
$>bamboo device
*Camera (0.35)	: /run/media/rahul/mtp:host=Canon_m6112/
Lens	:/run/media/rahul/Lens
OnePlus6    :/run/user/1000/gvfs/mtp:host=OnePlus51201/Internal shared storage/
```

``bamboo profile`` will list down all configured profiles

```text
$>bamboo profile
sample_profile   : Lens    ==> PC   
OP6_photo_sync   : OnePlus6   ==> Lens
```

``bamboo backup <profile>`` will backup as per the provided sync profile
```text
$>bamboo backup sample_profile
device1 usage : 60.79 GB / 101.27 GB (34.85 %)
device2 usage : 60.79 GB / 101.27 GB (34.85 %)
Syncing:demo
Gathering info ...
No file found for backup. Skipping.
Sync for profile:sample_profile completed
```

Or ``bamboo backup --auto`` will automatically do backups as per available devices

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)

##Project status
This project is currently actively maintained by me. 