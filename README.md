# Bamboo

Bamboo is a python based simple command line tool for creating regular file transfer and backups. Bamboo provides simple yet useful features to automate the file transfers as per configurations.

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


## Examples
``bamboo device`` will list down all known devices, mount points and show if they are online

```
$>bamboo device
*Camera (0.35)	: /run/media/rahul/mtp:host=Canon_m6112/
Lens	:/run/media/rahul/Lens
OnePlus6    :/run/user/1000/gvfs/mtp:host=OnePlus51201/Internal shared storage/
```

``bamboo profile`` will list down all configured profiles

```
$>bamboo profile
sample_profile   : Lens    ==> PC   
OP6_photo_sync   : OnePlus6   ==> Lens
```

``bamboo run <profile1> <profile2> ... <profileN>`` will backup as per the provided sync profiles (in the order of arguments)
```text
$>bamboo run sample_profile
Syncing:demo
Gathering info ...
7 files found 8.14 MB are to be transferred. continue ? (y) : y
device1:/home/rahul/PythonProjects/in/ -> device2:/home/rahul/PythonProjects/out/ 
Progress : 7/7 	 Transferred 8.14 MB         
complete!
Sync for profile:sample_profile completed
```

Or ``bamboo run --auto`` will automatically do backups as per available devices

## Configuration

`bamboo` configuration home needs to be created under user home directory and underlying directories for device and profile configurations
- `<user_home>/.config/bamboo`
- `<user_home>/.config/bamboo/devices`
- `<user_home>/.config/bamboo/profiles`

#### Device
To add a device a `<device_name>.json` needs to be created under `<user_home>/.config/bamboo/devices` with mount point information.

```json
{
    "mount_point" : "/run/media/rahul/Lens"
}
```
#### Profile

Profiles are a set of file types that fall under a logical  

To add a device a `<profile_name>.json` needs to be created under `<user_home>/.config/bamboo/profiles`.
Profiles contain a source and a target device (names should be as per device configuration). And it contains N number of sync entries.

sync entries take following keys,
- `name` 
- `source`
This is relative to the source device mount point
- `target`
This is relative to the target device mount point
- `filter_regex` (optional)
A list of regex to match against filenames. If none of the regex match the file will be excluded.
- `retention_period` (in days) (optional)
If mentioned files modified under the retention period will not be deleted from source location. 

```json
{
  "source_device": "device1",
  "target_device": "device2",
  "sync_entries": [
    {
      "name": "demo",
      "source": "home/rahul/demo/in/",
      "target": "home/rahul/demo/out/",
      "filter_regex": [
        ".*.jpg$"
      ],
      "retention_period": 5
    }
  ]
}
```

## Uninstallation
```commandline
python -m pip uninstall bamboo
```


## Contributing
Pull requests and suggestions are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
MIT

## Project status
This project is currently actively maintained by me. 
