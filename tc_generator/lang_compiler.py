"""
lang_compiler.py - The list LANGS contains the languages, commands for running
and/or compiling them and links of documentation in case something goes wrong.
"""

__all__ = ['LANGS']

import os


DIRNAME = os.path.abspath(os.path.dirname(__file__)) # Absolute path of the file
CMD = os.path.join(DIRNAME, 'logic') # Command to run the logic file


LANGS = [{'req': 'gcc',
          'command': ["logicc.exe",CMD],
          'link': 'https://gcc.gnu.org/install/',
          'compile': ['gcc', f'{CMD}.c', '-o', "logicc.exe"]},
         {'req': 'g++',
          'command': ["logiccpp.exe",CMD],
          'link': 'https://www.cs.odu.edu/~zeil/cs250PreTest/latest/Public/installingACompiler/',
          'compile': ['g++', f'{CMD}.cpp', '-o', "logiccpp.exe"]},
         {'req': 'Java',
          'command': ['java', '-cp', DIRNAME, 'logic'],
          'link': 'https://introcs.cs.princeton.edu/java/15inout/windows-CMD.html',
          'compile': ['javac', f'{CMD}.java']},
         {'req': 'Python',
          'command': ['python', f'{CMD}.py'],
          'link': 'https://www.python.org/downloads/',
          'compile': ['']},
         {'req': 'C#',
          'command': ['mono', f'{CMD}'],
          'link': 'https://www.mono-project.com/docs/about-mono/languages/csharp/',
          'compile': ['msc', f'{CMD}.cs']},
         {'req': 'Golang',
          'command': ["logicgo.exe",CMD],
          'link': 'https://golang.org/doc/install',
          'compile': ['go', 'build', '-o', "logicgo.exe", f'{CMD}.go']},
         ]
