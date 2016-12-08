@echo off
REM This batch files installs a bunch of python libraries needed for a search engine
pip install lpthw.web
pip install beautifulsoup4
pip install lxml
pip install urllib3

echo Dependencies installed
PAUSE
