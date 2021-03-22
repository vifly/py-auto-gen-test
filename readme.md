# Introduction
Generate test code/config file for Python backend Application according to your template. Now only support FastAPI framework.

# Run
Run example:
```
python3 auto_gen_test.py --domain http://127.0.0.1:8000 --define-path-code ./example/fastapi_app.py --template-file-path ./example/unittest_template.py --output-path ./test.py
```

It will generate test.py in the current dir.

You need to create your own template file to tell the script how to generate the result you want. The template will be parsed by [Jinja2](https://jinja.palletsprojects.com/). You can use these variables:     
- config.name: function name
- config.url: full url
- config.method: HTTP request method
- config.arg_num: function arguments number
- config.arg_names: function arguments name
- config.arg_types: function arguments type

Run `python3 auto_gen_test.py --help` to get help information.

*Note: In this example, the template file is a Python unittest file, but actually you can use any text file as template, not only use Python code.*

# How it works
It will use [AST](https://docs.python.org/3/library/ast.html) to analyse your code which define URL path, get path and other information from code. After parse code, it will use Jinja2 to generate result from the template.

# Todo
- support Flask
- support Django