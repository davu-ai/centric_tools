# Centric Internal Tool 

A collection of internal tools shared among all Centric Microservices.

## Features
- **Logging**: Custom logger for structured logs.
- **Permission Checking**: Utility functions to verify user permissions.
- **Decorators**: Easily enforce permissions on API endpoints.

## Installation

You can install this package directly from GitHub:

```bash
pip install git+https://github.com/davu-ai/centric_tools.git.git@main
```

## Usage

### 1. Import the permission decorator
```python
from centric_tools.permission.decorators import validate_permission
from centric_tools.permission.table import PermissionTable

@validate_permission([PermissionTable.can_manage_project])
async def protected_route():
    return {"message": "You have access"}
```
### **2. Control Permission Check Using an Environment Variable**
You can enable or disable permission checks by setting an environment variable:  

```bash
export PERMISSION_CHECK="False"
```
- To disable permission checks, explicitly set PERMISSION_CHECK to the string "False".

- If the variable is not set or set to any other value (including "True"), permission checks will remain enabled for all endpoints decorated with validate_permission.





## Development

Clone the repository:

```bash
git clone git@github.com:davu-ai/centric_tools.git
cd centric_tools
pip install -r requirements.txt
```

## License
This project is licensed under the MIT License.

---

⭐ **Contributions are welcome!** Feel free to open issues or submit pull requests.

