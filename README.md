# rmt

Python module and command line utilities to interact with the reMarkable tablet's cloud storage

Heavily reliant on prior work by Andreas Gohr, see his API documentation over [here](https://github.com/splitbrain/ReMarkableAPI/wiki).

## Usage

```rmt``` is supposed to mimick the git work flow. 

### Initialization

You can initialize a new ```rmt``` repository using
``` BASH
mkdir Documents
rmt init Documents ONE-TIME-CODE
```
where the ONE-TIME-CODE can be obtained from reMarkable [here](https://my.remarkable.com/generator-device).

### Fetching the updates

You can fetch updated documents to your ```rmt``` repo, without overwriting the presently checked-out
files. The command is
``` BASH
rmt fetch
```

### Checking out the updates

You can check out all updates to your documents using
``` BASH
rmt checkout
```
