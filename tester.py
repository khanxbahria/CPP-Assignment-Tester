import argparse
import sys
from pathlib import Path
import subprocess
import os
from icdiff_helper import custom_diff

class CompileException(Exception):
    pass

class RunException(Exception):
    pass

class CengTester:
    def __init__(self):
        self.compiler_command = ""
        self.expected_output_dir : Path
        self.your_output_dir : Path
        self.test_cases_dir : Path
        self.test_cases_names = []
        self.program = ""
        self.total = 0
        self.passed = 0
        self.failed = 0

    def run(self):
        args = self.get_args()
        self.is_show_diff = args.show_diff
        self.init_compiler(args.compiler_command)
        self.check_code_exists()
        self.init_program(args.program)
        self.test_program()

    def init_compiler(self, cc):
        """Check and set if compiler exists"""
        try:
            r = self.run_command(cc.split()[0] + " --version")
        except Exception as e:
            print(e)
            print(f"Compiler {cc.split()[0]} not found!")
            sys.exit()
        if r.stderr:
            print(f"Compiler {cc.split()[0]} not found!")
            sys.exit()

        self.compiler_command = cc

    def check_code_exists(self):
        your_code_files = Path("your_code").glob("*.h")
        if not len(list(your_code_files)):
            print("Please copy your C++ files to 'your_code' folder")
            sys.exit()

    def init_program(self, prog):
        """Check and set if program files exist"""
        self.test_cases_dir = Path("cases") / prog
        self.expected_output_dir = Path("expected_output") / prog 
        if not (self.test_cases_dir.is_dir() and self.expected_output_dir.is_dir()):
            print(f"Cases or output not found for {prog}")
            sys.exit()
        self.your_output_dir = Path("your_output") / prog
        self.your_output_dir.mkdir(parents=True, exist_ok=True)
        [f.unlink() for f in self.your_output_dir.glob("*.txt") if f.is_file()]          


        # Count files
        test_cases_names = {x.name[:-4]
                                for x in self.test_cases_dir.glob("*.cpp")}
        expected_output_names = {x.name[:-4]
                            for x in self.expected_output_dir.glob("*.txt")}
        if test_cases_names!=expected_output_names:
            print("Missing test_case expected_output pairs:", 
                test_cases_names.symmetric_difference(expected_output_names))
            sys.exit()

        self.test_cases_names = list(test_cases_names)
        try:
            self.test_cases_names = sorted([int(x) for x in self.test_cases_names])
            self.test_cases_names = [str(x) for x in self.test_cases_names]
        except:
            self.test_cases_names = sorted(self.test_cases_names)


        self.total = len(self.test_cases_names)
        if self.total == 0:
            print("No test cases found")
            sys.exit()
        self.program = prog

    def compile(self, c):
        inputf = str(self.test_cases_dir / f"{c}.cpp")
        command = str(self.compiler_command + f" {inputf} -o {c}")

        try:
            r = self.run_command(command)
        except Exception as e:
            raise CompileException(e)
        if r.stderr:
            raise CompileException(str(r.stderr))

    def delete_exec(self, c):
        if os.name == "nt":
            Path(f"{c}.exe").unlink(missing_ok=True)
        else:
            Path(c).unlink(missing_ok=True)

    def run_test_case(self, c):
        command = f"./{c}"
        r = self.run_command(command)
        if r.stderr:
            raise RunException(str(r.stderr))
        return r.stdout
        
    def ask_stop(self, msg):
        r = input(f"{msg} [Y/n] ")
        if r.lower() == "n":
            return True
        else:
            return False

    def show_diff(self, yourf, expectedf):
        custom_diff(yourf, expectedf)
        print()
        print("[Q] to terminate")
        print("[V] to view whole file")
        print("[Enter] to continue")
        r = input("").upper()
        if r == "Q":
            print("Terminating...")
            return -1
        elif r == "V":
            custom_diff(yourf, expectedf)
            print()
            print("[Q] to terminate")
            print("[Enter] to continue")
            r = input("").upper()
            if r == "Q":
                print("Terminating...")
                return -1

    def test_program(self):
        for c in self.test_cases_names:
            yourf = self.your_output_dir / f"{c}.txt"
            expectedf = self.expected_output_dir / f"{c}.txt"
            expected_output = expectedf.read_text()

            try:
                self.compile(c)
                your_output = str(self.run_test_case(c))
            except Exception as e:
                your_output = str(e)
            self.delete_exec(c)


            if your_output != expected_output:
                self.failed += 1
                yourf.write_text(your_output)
                print(f"Test Case: {c} FAILED")
                if(self.is_show_diff):
                    if(self.show_diff(yourf, expectedf) == -1):
                        break

            else:
                self.passed += 1
                print(f"Test Case: {c} PASSED")
        
        print()
        print("#-----------------------------------------#")
        print("#                  Result                 #")
        print("#-----------------------------------------#")
        print("Passed:", self.passed, end = " | ")
        print("Failed:", self.failed, end = " | ")
        print("Remaining:", self.total-(self.passed+self.failed))
        print()
        print(f"Score: {self.passed}/{self.total}")

    def run_command(self, command):
        r = subprocess.run(command.split(), capture_output=True, text=True)
        return r

    def get_args(self):
        parser = argparse.ArgumentParser(
                        prog =        'C++ Assignment Tester',
                        description = 'A script that will compile and run C++ test'
                                      ' cases and test against the given set of'
                                      ' expected outputs',
                                      )
        parser.add_argument('-p', '--program', required=True, 
                            help = 'The program to be tested')
        parser.add_argument('-cc', '--compiler-command', default='g++')
        parser.add_argument('-d', '--show-diff', action='store_true', default=True,
                            help = 'Display diff between Given Output and Expected Output.'
                                   )
        return parser.parse_args()

if __name__ == "__main__":
    app = CengTester()
    app.run()
