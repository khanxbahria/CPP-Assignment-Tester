# Generic CPP Assignment Tester - Template
 A script that will compile and run C++ test cases against your code to test against the given set of expected outputs
#### Note: 
To be used as a template.

## Demo
TBD

# How to Use
## Try online
 - TBD. Github codespaces instructions
 - Sign in to Github.
 - Open the repository in Github Codespaces.  
  [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=REPO_ID)
 - Upload your code files to ```your_code``` folder.
 - ```Ctrl```+``` ` ``` to toggle terminal.
 - ```  python3 tester.py -p program1 -d```
 
 

## Local
### Install
 - Clone this repository.
 - Pre-requisites: ```python3``` ```icdiff```  
  ```python3 -m pip install -r requirements.txt```

### Prepare
 - Some test cases pair, each of them contains test code and a corresponding output.
 - Test cases and output pairs should be located in the program folders having same filenames but with different extensions (```.cpp``` and ```.txt``` respectively).
 - Code you are going to test.

Then put them as the following:

```
AS1-CENG-Tester
│   AS1_tester.py
│
└───your_code
│   │   (all your code files)
│   
└───cases (code for test cases goes inside the program folders)
|    └───program1
|    └───program2
|    
└───expected_output (expected outputs inside the program folders)
|    └───program1
|    └───program2
```


### Usage
```
 python3 tester.py -h
usage: C++ Assignment Tester [-h] -p PROGRAM [-cc COMPILER_COMMAND] [-d]

A script that will compile and run C++ test cases and test against the given set of
expected outputs

options:
  -h, --help            show this help message and exit
  -p PROGRAM, --program PROGRAM
                        The program to be tested
  -cc COMPILER_COMMAND, --compiler-command COMPILER_COMMAND
  -d, --show-diff       Display diff between Given Output and Expected Output.
  ```
  
  Test cases for program1 and show diff
  ```
  python3 tester.py -p program1 -d
  ```
