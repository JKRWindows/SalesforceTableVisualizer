# Getting Started
This program was designed to work with `sfdx` and `sf` to retrieve the metadata required to create the graphs.
## Requirements
- [Dot](https://graphviz.org/download/) is installed and can be found on the command line. (`dot -V` should return the version)
- [Salesforce CLI](https://developer.salesforce.com/tools/salesforcecli)
- Python 3.11+ (untested on 3.10)

1. Create a directory for the metadata using `sfdx`
```sh
sfdx force source manifest create --from-org "<Your Org>" --name=allMetadata --output-dir manifest
```

2. Attempt to start downloading the data. This may error.
```sh
sf project retrieve start --manifest manifest\allMetadata.xml
```
If this errors, there's a good chance there are too many items it's trying to download. You can only download 10,000 items at a time. JKR Windows builds and stores some files in Salesforce. Go to `manifest/allMetadata` and remove the things you don't want downloaded (eg. pdf, jpg, png). Then try again.

3. Download [Grapher](https://github.com/JKRWindows/Grapher) into the Salesforce directory.

4. Move the `main.py` file from this repo outside of it's directory into the root of the one you downloaded.

3. Run `main.py` with the name of the output file as well as the name of the branch that was downloaded. It will default to `main` if not specified. If you have errors, see [Troubleshooting](#troubleshooting)
```sh
python main.py <outfile_name> [branch_name]
```

## Troubleshooting
Ensure the directory structure is correct:
./Metadata folder/
    /force-app/
        /main/
            /default/
                /...
    /[Grapher](https://github.com/JKRWindows/Grapher)/
    /SalesforceTableVisualizer/
            /__init__.py
            /SFField.py
            /SFObject.py
            /SFType.py
            /Visualizer.py
            /...
    /main.py
    /...
