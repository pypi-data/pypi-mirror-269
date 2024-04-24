# Hubstaff

## Overview
Library for Hubstaff. Perform actions such as list projects detail. 
Request Feature/Suggestion: https://forms.gle/efGD5DuTpWsX96GG7

[//]: # (## Download stats)

[//]: # ([![Downloads]&#40;https://static.pepy.tech/badge/ActiveCollab&#41;]&#40;https://pepy.tech/project/ActiveCollab&#41;)

## Installation
```console
pip install Hubstaff
```
Hubstaff supports Python 3+.

## Usage

### Default
```python
import Hubstaff

personal_access_tokens = "your_personal_access_tokens" #can be generated from https://developer.hubstaff.com/personal_access_tokens


hb = Hubstaff.Connect(personal_access_tokens)  # Login to Hubstaff

print(hb.get_projects_data())
```

### List all projects
```python
hb.get_projects_data()  # List out all project assigned to logged in user
```
