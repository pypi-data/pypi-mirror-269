# paketoi

**Paketoi** is a command-line tool for building AWS Lambda deployment packages (zip files) for Python projects.


## Assumptions

* The dependencies for your project are specified in a `requirements.txt` file.

## Installation

```sh
pipx install paketoi
```

## Usage

The basic usage is:

```
paketoi -r <path to requirements.txt> <path to output file>
```

You can find all the command-line options with `paketoi --help`.

The source code is assumed to reside in the working directory.

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
├── src
│  └── lambda_function.py
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
