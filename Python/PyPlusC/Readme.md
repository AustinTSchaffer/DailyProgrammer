# C-Extension for Python

Example of a C extension for Python, allowing Python to natively call C code for
fun or profit or serious performance gains.

```bash
python example_usage.py 
cat some_file_name.txt 
# Some text!
```

## VSCode IDE Setup

In order to get good intellisense on the C code in VSCode, you need to set the
workspace settings so the compiler can find `Python.h`. This is my setup
(Linux, Python 3.8):

```json
/* ./vscode/settings.json */
{
    "C_Cpp.default.includePath": [
        "/usr/include/python3.8"
    ]
}
```
