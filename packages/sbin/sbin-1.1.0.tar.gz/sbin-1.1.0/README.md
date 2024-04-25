# sbin

[![versions](https://img.shields.io/pypi/pyversions/sbin.svg)](https://gitlab.com/mazmrini/bin)
[![license](https://img.shields.io/gitlab/license/mazmrini/bin)](https://gitlab.com/mazmrini/bin/-/blob/main/LICENSE)

Automate your project setup with a simple `bin.yml` file.

## Help
See [documentation](https://google.com) for more details.

## Installation
We recommend installing `sbin` globally through `pip install sbin`.
`sbin` and its alias `bin` executables will be available from the command line.

Please note that the documentation will refer to `sbin` as `bin`.

## Quick start
Start by creating an example `bin.yaml` file at the root of your project with
```
bin init
```

You can explore bin commands through `bin <help|h|-h|--help>`. Here
are some built-in ones:
```
bin req   # makes sure you have the requirements to run the projet 
bin up    # sets up whatever is needed to run the project
bin down  # tear down whatever was up
```

## Examples
Here are few project [examples](https://gitlab.com/mazmrini/bin/-/blob/main/examples) utilizing `bin`.

## Contributing
See the [contributing](https://gitlab.com/mazmrini/bin/-/blob/main/CONTRIBUTING.md) doc.
