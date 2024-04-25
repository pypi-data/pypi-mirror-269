# Pailettes

Generate color palettes using artificial intelligence. The OpenAI API is used for this, so you will require an account.

![Pailettes](https://raw.githubusercontent.com/psyonara/pailettes/master/imgs/headline.jpg)

## Installation

### Pipx

```shell
pipx install pailettes
```

### Pip

```shell
pip install pailettes
```

## Configuration

To configure your OpenAI API key, create an environment variable as follows.

### Windows
TODO

### MacOS
TODO

### Linux
```shell
export OPENAI_KEY="your-key-goes-here"
```

This will set your OpenAI key for that terminal session. If you would like to permanently set the environment variable, consult the documentation of your OS/shell.

## Usage

### Quick Start

```shell
pailettes retro
```

This creates a color palette with a "retro" theme.

### Number of colors

To specify the number of colors in your palette:

```shell
pailettes retro --color-count=6
```

### Number of palettes

To specify the number of palettes to generate:

```shell
pailettes retro --palette-count=3
```
