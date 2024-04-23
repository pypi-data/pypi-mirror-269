# paketoi

**Paketoi** is a command-line tool for building AWS Lambda deployment packages (zip files) for Python projects.

The goal is to provide a single command to build the deployment package for simple projects using `requirements.txt`.

## Assumptions

* The dependencies for your project are specified in a `requirements.txt` file.
* Any dependencies with native code have pre-built binary wheels for the target platform.

## Installation

Paketoi is [available on PyPI](https://pypi.org/project/paketoi/). The simplest way to install it globally is to use [pipx](https://github.com/pypa/pipx):

```sh
pipx install paketoi
```

## Usage

The tool is meant to be run in the directory that contains your project.
The source code is assumed to reside in the working directory.
The basic usage is:

```sh
paketoi -r <path to requirements.txt> <path to output file>
```

You can find all the command-line options with `paketoi --help`.

### Command-line options

```
% paketoi --help
Usage: paketoi [OPTIONS] OUTPUT

  Build AWS Lambda deployment packages (zip files) for Python projects.

Options:
  -s, --source DIRECTORY          The source root of the project.
  -I, --include PATH              Files to be included, relative to the source
                                  root.
  -E, --exclude TEXT              Files to be excluded, relative to the source
                                  root.
  -r, --requirement TEXT          Path to requirements.txt.
  --runtime [3.8|3.9|3.10|3.11|3.12]
                                  Python version to target.
  --platform [x86_64|arm64]       Architecture to target.
  --default-excludes / --no-default-excludes
                                  Enable/disable the default exclusion list.
                                  (.git, .jj, .mypy_cache, .ruff_cache)
  --help                          Show this message and exit.
```

### Python version and architecture

By default, dependencies are downloaded for Python 3.12 running on x86_64. 
You can change these options with `--platform` and `--runtime` options.

For example, to build a deployment package for Python 3.10 running on arm64, do this:

```sh
paketoi -r requirements.txt --runtime 3.10 --platform arm64 lambda.zip
```

### Simple layout

```
.
├── lambda_function.py
└── requirements.txt
```

With the project layout like above, you can build a deployment package `lambda.zip` like this:

```sh
paketoi -r requirements.txt lambda.zip
```

### `src` layout

```
.
├── requirements.txt
└── src
   └── lambda_function.py
```

When your lambda source is under the directory `src`, use `-s src` to set the source root.

```sh
paketoi -r requirements.txt -s src lambda.zip
```

## Excluding files

```
.
├── requirements.txt
├── lambda_function.py
└── tests
   └── lambda_function_test.py
```

You can exclude files you do not need by using `-E path`. For example:

```sh
paketoi -r requirements.txt -E tests lambda.zip
```

## Alternatives

* pip ([instructions](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html))
* [pex](https://docs.pex-tool.org/) ([instructions](https://quanttype.net/posts/2024-01-31-creating-aws-lambda-zip-files-with-pex.html))
* [Pants](https://www.pantsbuild.org/) ([instructions](https://www.pantsbuild.org/2.19/docs/python/integrations/aws-lambda))
* [poetry-plugin-lambda-build](https://github.com/micmurawski/poetry-plugin-lambda-build)

## Developing paketoi

This project uses [Poetry](https://python-poetry.org/) as the package manager and [just](https://github.com/casey/just) as the command runner.
Project setup:

```sh
# Create a virtualenv and install all the dependencies
poetry install

# Run all the tests and checks
just check

# Run the tool directly from the repo
poetry run paketoi
```
