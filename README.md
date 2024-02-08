<br/>
<p align="center">
  <a href="https://github.com/derkalle4/python3-palworld-rcon">
    <img src="images/logo.webp" alt="Logo" width="250" height="250">
  </a>

  <h3 align="center">Palworld RCON</h3>

  <p align="center">
    Automate your Palworld server the easy way
    <br/>
    <br/>
    <a href="https://github.com/derkalle4/python3-palworld-rcon"><strong>Explore the docs »</strong></a>
    <br/>
    <br/>
    <a href="https://github.com/derkalle4/python3-palworld-rcon/issues">Report Bug</a>
    .
    <a href="https://github.com/derkalle4/python3-palworld-rcon/issues">Request Feature</a>
  </p>
</p>

![Downloads](https://img.shields.io/github/downloads/derkalle4/python3-palworld-rcon/total) ![Contributors](https://img.shields.io/github/contributors/derkalle4/python3-palworld-rcon?color=dark-green) ![Forks](https://img.shields.io/github/forks/derkalle4/python3-palworld-rcon?style=social) ![Stargazers](https://img.shields.io/github/stars/derkalle4/python3-palworld-rcon?style=social) ![Issues](https://img.shields.io/github/issues/derkalle4/python3-palworld-rcon) ![License](https://img.shields.io/github/license/derkalle4/python3-palworld-rcon) 

## Table Of Contents

* [About the Project](#about-the-project)
* [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Authors](#authors)
* [Acknowledgements](#acknowledgements)

## About The Project

This repository aims to be an automated solution for your Palworld server. You can design your own plug-ins and schedules as you like.

## Built With

* [Python 3](https://www.python.org/downloads/)
* [mccron](https://github.com/Tiiffi/mcrcon)
* [schedule](https://schedule.readthedocs.io/en/stable/)

## Getting Started

To get a local copy up and running follow these simple example steps:

### Prerequisites

Please install the following for your distribution (Windows may work but it is untested):

* latest Python3
* Python3 Virtual Env

### Installation

1. Clone the repo

```sh
git clone https://github.com/derkalle4/python3-palworld-rcon.git
```

2. Create virtual environment and install all dependencies

```sh
./create_venv.sh
```

## Usage

If you used the ./create_venv.sh you should use this command to run the app:

```sh
./run_in_venv.sh
```
If you do not use a virtual environment the command will look like this:

```sh
python3 .\app.py
```

## Roadmap

Feel free to contribute following the roadmap

* [ ] use types in every function
* [ ] better source code documentation
* [ ] split to multiple classes to make everything smaller and give a better overview
* [ ] re-implement mccron to avoid using a third-party library for the small percentage we need from it
* [ ] document how to properly use this rcon tool

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.
* If you have suggestions for adding or removing projects, feel free to [open an issue](https://github.com/derkalle4/python3-palworld-rcon/issues/new) to discuss it, or directly create a pull request after you edit the *README.md* file with necessary changes.
* Please make sure you check your spelling and grammar.
* Create individual PR for each suggestion.
* Please also read through the [Code Of Conduct](https://github.com/derkalle4/python3-palworld-rcon/blob/main/CODE_OF_CONDUCT.md) before posting your first idea as well.

### Creating A Pull Request

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the GNU GENERAL PUBLIC License. See [LICENSE](https://github.com/derkalle4/python3-palworld-rcon/blob/main/LICENSE) for more information.

## Authors

* [Kalle Minkner](https://github.com/derkalle4) - *Project Founder*

## Acknowledgements

None so far
