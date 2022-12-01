# AS1-CENG-Tester
 A script that will compile and run C++ test cases against your code to test against the given set of expected outputs

## Demo


## How to Use
### Install
 - Clone this repository.
 - Pre-requisites: ```icdiff```  
  ```python3 -m pip install -r requirements.txt```

### Prepare
 - Some test cases pair, each of them contains test code and a corresponding output.
 - Code you are going to test.

Then put them as the following:

```
AS1-CENG-Tester
│   AS1_tester.py
│
└───your_code
│   │   (all your code files)
│   
└───cases (code for test cases goes here)
|    └───program1
|    └───program2
|    
└───expected_output (expected outputs)
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
  python3 tester2.py -p program1 -d
  ```
