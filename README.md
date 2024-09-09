# Bulk Genome Assembly Downloader

A terminal tool to download multiple genome assemblies from NCBI FTP server.

The terminal tool is written in `Python3` it uses:
* `requests` library to download files from the NCBI FTP server.
* `wget` to download files from the NCBI FTP server (in `full` mode)
* `curl` to download some filess from the NCBI DATASET server (in `lite` mode)

## Installation

Just download repisitory and unzip it in some folder.

Command to use:

`python ./ncbi_downloader.py -h`

It will open mannual in terminal and show avalable options.
