# syncrm

Python module and command line utilities to interact with the reMarkable tablet's cloud storage

Heavily reliant on prior works:

 - by Andreas Gohr (@splitbrain), see his API documentation over [here](https://github.com/splitbrain/ReMarkableAPI/wiki);
 - by @edupont, see his rM2svg code over [here](https://github.com/reHackable/maxio/blob/master/tools/rM2svg).

## Usage

```syncrm``` is supposed to mimick the git work flow. 

### Initialization

You can initialize a new ```syncrm``` repository using
``` BASH
mkdir Documents
syncrm init Documents ONE-TIME-CODE
```
where the ONE-TIME-CODE can be obtained from reMarkable [here](https://my.remarkable.com/generator-device).

### Fetching the updates

You can fetch updated documents to your ```syncrm``` repo, without overwriting the presently checked-out
files. The command is
``` BASH
syncrm fetch
```

### Checking out the updates

You can check out all updates to your documents using
``` BASH
syncrm checkout
```
