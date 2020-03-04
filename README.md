# Bruvio tools

This project started as a tool designed to help me getting, wrangling and plotting e2d data.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

1) You will need to be sure you can use a few Python packages used at JET to download and read data:

```
import ppf
import getdat
import eproc
```
the code at the time of writing this README file cannot work offile. So those  packages are mandatory.

If you can skip to  )


2) You will need to install a few Python packages
```
pip install -r requirements.txt --user
```

3) 
to install JET Python packages please follow these web pages:
 for the ppf package:
https://users.euro-fusion.org/pages/data-ppf-jpf/ppfuserguide/python/PPF.html#_converters
end of the page tells you what to do in case of errors

for getdat

https://data.jet.uk/guides/jpf/getdat.html

for eproc
https://users.euro-fusion.org/tfwiki/index.php/EPROC_Python_module

### Installing

to install the tool clone the repository to a convenient location
```
git clone  https://github.com/bruvio/multitool.git

```

After this you should edit the file user_installation_data.json

This file will contain info on where the code is located 

if you cloned the repository in 


```
/home/username/foldername1/subfolder/repository
```
then you should edit the file as follow

And repeat

```
base folder = home

installation folder =  foldername1/subfolder/repository
```

Once this is done you should be able to run the code.

## Running the tests

The code has a few tests inside the folder
```
./tests
```

these tests allow the user to verify that the MainWindow and the Widgets can be launched.
More tests will be created in the future



## Authors

* **Bruno Viola** - *Initial work* - [PurpleBooth](https://github.com/bruvio)



## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

