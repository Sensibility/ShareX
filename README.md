<a href="https://ic.superphage.org/viewType.html?buildTypeId=ShareX_Build&guest=1"> 
<img src="https://ic.superphage.org/app/rest/builds/buildType:(ShareX_Build)/statusIcon"/>
</a>

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
