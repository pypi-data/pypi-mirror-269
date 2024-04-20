# al-helper

A simple library to help you fetch data from AniList

## Description

Welcome to my first python project!
This library is aimed at people who might be interested in automatizing their anime library.

## Getting Started

### Dependencies

* Python(tested on the latest ver.)
* An AniList account
* An AniList developer app
* Javascript enabled during the set-up process (for sending the access token back to Python)

### Installing

* Clone this repo
```
git clone https://github.com/ProchyGaming/al-helper /path/to/desired/folder
```
* Install it using pip
```
pip install al-helper
```
* Install it using pip locally
```
cd /path/to/desired/folder
pip install .
```
* If you want to make modifications to the library install it in the edit mode:
```
cd /path/to/desired/folder
pip install -e .
```

### Using the library

* To import the library into your code use:
```
import alhelper
```
* When importing this library for the first time, you will be taken through the setup process

### Setting up the AniList developer app

* When the setup process starts, you will be automatically taken to required pages. This process is really simple.
* When asked for the Client ID, you will be taken to the account developer page.
* If not logged in, log in first.
* Then create a new client
* Choose whatever name you fancy, and for the redirect URL use http://localhost:8888/auth
* After you save the client, copy the ID and paste it into the terminal
* After entering the ID you will be taken to an auth page, where you need to allow the app to access your account.
* Afterwards you will be taken to a redirect page that is momentarily hosted using gevent. (If you have any worries, please see the token_getter.html source code.)
* After that the library is successfully set-up and ready for use.

## Help

If you encounter any issues, feel free to open a new issue. If you have any new ideas or fixes, please open a pull request, they are more than welcome!

## Version History
* [1.0.0](https://github.com/prochy-exe/al-helper/releases/tag/v1.0.0)
    * [Initial Release](https://github.com/prochy-exe/al-helper/commit/8abffc852728cecb580282a0749c8051b95e3d10)

## Acknowledgments

Huge thanks to AniList team for their great page and database:
* [AniList](https://anilist.co/home)
* [AniList GraphQL](https://anilist.co/graphiql)
