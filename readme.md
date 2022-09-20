# nn 

A simple news CLI to get programming news now (nn) by common listings in Reddit, HackerNews, 
Lobste.rs, etc. This wraps a Spring Boot-powered backend aggregator that lives 
on [news.madhu.dev](https://news.madhu.dev/api/v1/articles).

![help](https://github.com/madhuravius/nn/blob/main/docs/screen2.png?raw=true) | ![listing](https://github.com/madhuravius/nn/blob/main/docs/screen1.png?raw=true)

## Quickstart

1. Download [the binary and make it an executable](https://github.com/madhuravius/nn#Installation)
2. Run it `./nn.pex all` or `./nn.pex --help` and read help text for more info

## Overview

[![GitHub release](https://img.shields.io/github/release/madhuravius/nn)](https://github.com/madhuravius/nn/)
[![Test](https://github.com/madhuravius/nn/actions/workflows/test.yaml/badge.svg)](https://github.com/madhuravius/nn/actions/workflows/test.yaml)
[![license](https://img.shields.io/github/license/madhuravius/nn.svg)](https://github.com/madhuravius/nn/blob/main/LICENSE)

For source code, see [Github repository](https://github.com/madhuravius/nn) for details.

This CLI spits out a news list based on RSS feeds and a variety of APIs.

## Installation

Releases can be found on this page for download: [Releases Github Page](https://github.com/madhuravius/nn/releases/)

It just needs to be made executable and placed in your PATH:

```bash
wget -O nn https://github.com/madhuravius/nn/releases/download/VERSION/nn.pex
chmod +x nn
./nn

# OR 
mv ./nn /usr/local/bin
```

This will require Python 3 or higher in your path to function. 

## Usage

The CLI itself is powered by components in `rich_click`. You can get detailed instruction 
on its usage with `nn --help`.

## Credits

Large parts of this repository, namely around automation via GH Actions and
also distribution used [this repository](https://github.com/aptible/aptstract)
as reference.