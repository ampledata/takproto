## Install on Debian, Ubuntu or Raspberry Pi

TAKProto is distributed as a Debian package (``.deb``). takproto should be compatible 
with most contemporary system-Python versions from Python 3.6 onward. 

To install takproto, download the takproto package and install using apt:

```sh linenums="1"
sudo apt update -qq
wget https://github.com/snstac/takproto/releases/latest/download/takproto_latest_all.deb
sudo apt install -f ./takproto_latest_all.deb
```

## Install from Python Package Index (PyPI)

```sh linenums="1"
python3 -m pip install takproto
```

## Install from Source

```sh linenums="1"
git clone https://github.com/snstac/takproto.git
cd takproto/
python3 -m pip install .
```
