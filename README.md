# SeznamAPI
Test assignment for Seznam.cz

### Install
1. Download and install python 3.5, pip and pipenv
2. Run `pipenv install`

### Run
1. Run `pipenv run deploy`

### Accessible path
You can edit accessible path in core/config.py file

### API usage
Get list of files and folders in path:
```
curl -X GET 127.0.0.1:5000/folder?path=D:\Downloads
```
Get metadata of file: 
```
curl -X GET 127.0.0.1:5000/file?path=D:\Downloads\file.txt
```
Delete empty folder
```
curl -X DELETE 127.0.0.1:5000/folder?path=D:\Downloads
```
Delete file
```
curl -X DELETE 127.0.0.1:5000/file?path=D:\Downloads\file.txt
```
Create new file
```
curl -X POST 127.0.0.1:5000/file?path=D:\Downloads\file.txt
```