SuperTester
===========
Home page: https://github.com/alberthrocks/SuperTester

Introduction
-------------
SuperTester is a mini testing suite suited for testing programs that create
standard output from standard input. It also works great for testing student
programs that require input and produce output!

Files
------
You can download a release of SuperTester at:
https://github.com/alberthrocks/SuperTester/releases

Otherwise, you can simply run the Python source directly. You can
download the source code directly from git:

```
git clone https://github.com/alberthrocks/SuperTester.git
```

Requirements
-------------
SuperTester requires at least Python 2.4. (And yes, it is tested on an actual
installation of Python 2.4!)

Got Python? That's it! SuperTester does NOT use any external modules!

SuperTester is compatible with Linux, Mac OS X, BSD, and any other Unix system
that has a standard installation of Python. It can run on Windows, but the
output may look junky due to ANSI colors not being compatible with Windows.

Using SuperTester
------------------
Before using this really fun (and colorful) debugging tool, you MUST put
this line at the very beginning of C main() function:
```
setvbuf(stdout, NULL, _IONBF, 0);
```
This forces your C program to buffer output!
Finally, make sure to remove any extraneous debug statements before running
this program! The valid output will not match any extra debug statements!

This little script assumes that your program is `./myprog`.
If it isn't, you can do either of the following:

  1. Compile it to `./myprog`:  
     `gcc coolcode.c cool2.c cool3.c -o myprog`
  2. Alternatively, you can modify this script to use a different file name.
     Really easy - just open this script in your favorite editor (vi, emacs,
     nano, or any other CLI/GUI text editor), scroll to the bottom, and follow
     the instructions there.

You will also need to provide input files and valid output files to compare
to. Note that valid output does NOT contain program input. Currently, the
input and output files are named `test1.in` and `test1.out`, respectively.
You can also modify these file names at the bottom of this script.
 
Once you are sure you have done all of the above (AND recompiled your
program), you can go ahead and run SuperTester. All you need to do is run:
```
python SuperTester.py
```

Once done, if you are successful, it will finish without any error. If not,
SuperTester will halt at the point where your program's output stops matching
the valid output, and will create the following three files:

  * `progout.txt` - your program's output, stopped at the error.
  * `progdiff.txt` - a diff of the valid output versus your program's output.
  * `progunified.txt` - program input and output merged, just as if you were
    running this program by yourself and manually providing input!

Continue to fix bugs and re-run SuperTester until there are no more errors.

And that's it! Good luck and have fun debugging!

TODO
-----
  * Fix dirty error handling in code
  * Make `progunified.txt` include initial output, which is left out.
  * Add error checking to see if files exist
  * Add error checking for write permissions
  * Add error checking on *nix systems to see if the program is executable
  * Add Windows support by including colorama

License
--------
SuperTester is licensed under the GPL, v3. The usual notice header:
```
SuperTester v1.4 - a mini testing suite for programs using standard I/O!
Copyright (C) 2014 Albert Huang.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
```

You can find the full license in LICENSE.

A non-legalese version can be found here:
http://www.tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)
