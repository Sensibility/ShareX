[![Build Status](https://superphage.us:8443/app/rest/builds/buildType\(id:ShareX_Build\)/statusIcon)](https://superphage.us:8443/viewType.html?buildTypeId=ShareX_Build&guest=1)

# ShareX
Python ShareX Server.

## Dependencies
* [Python 3](https://www.python.org)


## Setup
Run the following
```
git clone --depth 1 https://github.com/Sensibility/ShareX.git
cd ShareX/bin/
chmod +x *.sh
./install.sh
```

## Structure
All .sh files in the root directory contain different tasks.<br />
* `install.sh` - This will install all required dependencies to run this app (excluding python)
* `compile.sh` - Self explanatory, used by build agent
* `test.sh` - Runs all of the tests for the project