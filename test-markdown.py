#!/usr/bin/env python

import os, difflib, time, gc, codecs, platform, sys
from pprint import pprint
import textwrap

# Setup a logger manually for compatibility with Python 2.3
import logging
logging.getLogger('MARKDOWN').addHandler(logging.StreamHandler())
import markdown

TEST_DIR = "tests"
TMP_DIR = "./tmp/"
WRITE_BENCHMARK = True
WRITE_BENCHMARK = False
ACTUALLY_MEASURE_MEMORY = True

######################################################################

if platform.system().lower() == "darwin": # Darwin
    _proc_status = '/proc/%d/stat' % os.getpid()
else: # Linux
    _proc_status = '/proc/%d/status' % os.getpid()

_scale = {'kB': 1024.0, 'mB': 1024.0*1024.0,
          'KB': 1024.0, 'MB': 1024.0*1024.0}

def _VmB(VmKey):
    '''Private.
    '''
    global _proc_status, _scale
     # get pseudo file  /proc/<pid>/status
    try:
        t = open(_proc_status)
        v = t.read()
        t.close()
    except:
        return 0.0  # non-Linux?
     # get VmKey line e.g. 'VmRSS:  9999  kB\n ...'
    i = v.index(VmKey)
    v = v[i:].split(None, 3)  # whitespace
    if len(v) < 3:
        return 0.0  # invalid format?
     # convert Vm value to bytes
    return float(v[1]) * _scale[v[2]]


def memory(since=0.0):
    '''Return memory usage in bytes.
    '''
    if ACTUALLY_MEASURE_MEMORY :
        return _VmB('VmSize:') - since


def resident(since=0.0):
    '''Return resident memory usage in bytes.
    '''
    return _VmB('VmRSS:') - since


def stacksize(since=0.0):
    '''Return stack size in bytes.
    '''
    return _VmB('VmStk:') - since


############################################################

DIFF_FILE_TEMPLATE = """
<html>
 <head>
 <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
 <style>
   td {
     padding-left: 10px;
     padding-right: 10px;
   }
   colgroup {
     margin: 10px;
   }
   .diff_header {
      color: gray;
   }
   .ok {
      color: green;
   }
   .gray {
      color: gray;
   }
   .failed a {
      color: red;
   }
   .failed {
      color: red;
   }
 </style>
</head>
<body>
<h1>Results Summary</h1>
<table rules="groups" >
  <colgroup></colgroup>
  <colgroup></colgroup>
  <colgroup></colgroup>
  <colgroup></colgroup>
  <colgroup></colgroup>
  <th>
   <td></td>
   <td>Seconds</td>
   <td></td>
   <td>Memory</td>
  </th>
  <tbody>
 """

FOOTER = """
</body>
</html>
"""

DIFF_TABLE_TEMPLATE = """
 <table class="diff" rules="groups" >
  <colgroup></colgroup>
  <colgroup></colgroup>
  <colgroup></colgroup>
  <colgroup></colgroup>
  <colgroup></colgroup>
  <colgroup></colgroup>
  <th>
   <td></td>
   <td>Expected</td>
   <td></td>
   <td></td>
   <td>Actual</td>
  </th>
  <tbody>
        %s
  </tbody>
 </table>
"""


def smart_split(text) :
    result = []
    for x in text.splitlines() :
        for y in textwrap.wrap(textwrap.dedent(x), 40): 
            result.append(y)
    return result


differ = difflib.Differ()
try :
    htmldiff = difflib.HtmlDiff()
except: 
    htmldiff = None

class TestRunner :

    def __init__ (self) :
        self.failedTests = []
        if not os.path.exists(TMP_DIR):
            os.mkdir(TMP_DIR)

    def test_directory(self, dir, measure_time=False, safe_mode=False, encoding="utf8", output_format='xhtml1') :
        self.encoding = encoding
        benchmark_file_name = os.path.join(dir, "benchmark.dat")
        self.saved_benchmarks = {}

        if measure_time :
            if os.path.exists(benchmark_file_name) :
                file = open(benchmark_file_name)
                for line in file.readlines() :
                    test, str_time, str_mem = line.strip().split(":")
                    self.saved_benchmarks[test] = (float(str_time), float(str_mem))
            repeat = range(10)
        else :
            repeat = (0,)

        # First, determine from the name of the directory if any extensions
        # need to be loaded.

        parts = os.path.split(dir)[-1].split("-x-")
        if len(parts) > 1 :
            extensions = parts[1].split("-")
            print extensions
        else :
            extensions = []

        mem = memory()
        start = time.clock()
        self.md = markdown.Markdown(extensions=extensions, safe_mode = safe_mode, output_format=output_format)
        construction_time = time.clock() - start
        construction_mem = memory(mem)

        self.benchmark_buffer = "construction:%f:%f\n" % (construction_time,
                                                     construction_mem)

        html_diff_file_path = os.path.join(TMP_DIR, os.path.split(dir)[-1]) + ".html"
        self.html_diff_file = codecs.open(html_diff_file_path, "w", encoding=encoding)
        self.html_diff_file.write(DIFF_FILE_TEMPLATE)

        self.diffs_buffer = ""

        tests = [x.replace(".txt", "")
                      for x in os.listdir(dir) if x.endswith(".txt")]
        tests.sort()
        for test in tests :
            self.run_test(dir, test, repeat)

        self.html_diff_file.write("</table>")

        if sys.version < "3.0":
            self.html_diff_file.write(self.diffs_buffer.decode("utf8"))

        self.html_diff_file.write(FOOTER)
        self.html_diff_file.close()
        print "Diff written to %s" % html_diff_file_path

        benchmark_output_file_name = benchmark_file_name

        if not WRITE_BENCHMARK:
            benchmark_output_file_name += ".tmp"

        self.benchmark_file = open(benchmark_output_file_name, "w")
        self.benchmark_file.write(self.benchmark_buffer)
        self.benchmark_file.close()


####################


    def run_test(self, dir, test, repeat):

        print "--- %s ---" % test
        self.html_diff_file.write("<tr><td>%s</td>" % test)
        input_file = os.path.join(dir, test + ".txt")
        output_file = os.path.join(dir, test + ".html")

        expected_output = codecs.open(output_file, encoding=self.encoding).read()
        input = codecs.open(input_file, encoding=self.encoding).read()
        actual_output = ""
        actual_lines = []
        self.md.source = ""
        gc.collect()
        mem = memory()
        start = time.clock()
        for x in repeat: 
            actual_output = self.md.convert(input)
        conversion_time = time.clock() - start
        conversion_mem = memory(mem)
        self.md.reset()
        
        expected_lines = [x.encode("utf8") for x in smart_split(expected_output)]
        actual_lines = [x.encode("utf8") for x in smart_split(actual_output)]

        #diff = difflib.ndiff(expected_output.split("\n"),
        #                    actual_output.split("\n"))

        diff = [x for x in differ.compare(expected_lines,
                                     actual_lines)
                if not x.startswith("  ")]

        if not diff:
            self.html_diff_file.write("<td class='ok'>OK</td>")
        else :
            self.failedTests.append(test)
            self.html_diff_file.write("<td class='failed'>" +
                               "<a href='#diff-%s'>FAILED</a></td>" % test)
            print "MISMATCH on %s/%s.txt" % (dir, test)
            print
            for line in diff :
                print line
            if htmldiff!=None :
                htmlDiff = htmldiff.make_table(expected_lines, actual_lines,
                                        context=True)
                htmlDiff = "\n".join( [x for x in htmlDiff.splitlines()
                                       if x.strip().startswith("<tr>")] )
                self.diffs_buffer += "<a name='diff-%s'/><h2>%s</h2>" % (test, test)
                self.diffs_buffer += DIFF_TABLE_TEMPLATE % htmlDiff

        expected_time, expected_mem = self.saved_benchmarks.get(test, ("na", "na"))

        self.html_diff_file.write(get_benchmark_html(conversion_time, expected_time))
        self.html_diff_file.write(get_benchmark_html(conversion_mem, expected_mem))
        self.html_diff_file.write("</tr>\n")

        self.benchmark_buffer += "%s:%f:%f\n" % (test,
                                            conversion_time, conversion_mem)


    


def get_benchmark_html (actual, expected) :
    buffer = ""
    if not expected == "na":
        if actual > expected * 1.5:
            tdiff = "failed"
        elif actual * 1.5 < expected :
            tdiff = "ok"
        else :
            tdiff = "same"
        if ( (actual <= 0 and expected < 0.015) or
             (expected <= 0 and actual < 0.015)) :
            tdiff = "same"
    else :
        tdiff = "same"
    buffer += "<td class='%s'>%.2f</td>" % (tdiff, actual)
    if not expected == "na":
        buffer += "<td class='gray'>%.2f</td>" % (expected)
    return buffer


def run_tests() :

    tester = TestRunner()
    #test.test_directory("tests/basic")
    tester.test_directory("tests/markdown-test", measure_time=True)
    tester.test_directory("tests/misc", measure_time=True)
    tester.test_directory("tests/extensions-x-tables")
    tester.test_directory("tests/extensions-x-footnotes")
    #tester.test_directory("tests/extensions-x-ext1-ext2")
    tester.test_directory("tests/safe_mode", measure_time=True, safe_mode="escape")
    tester.test_directory("tests/extensions-x-wikilinks")
    tester.test_directory("tests/extensions-x-toc")
    tester.test_directory("tests/extensions-x-def_list")
    tester.test_directory("tests/extensions-x-abbr")
    tester.test_directory("tests/html4", output_format='html4')

    try:
        import pygments
    except ImportError:
        # Dependancy not avalable - skip test
        pass
    else:
        tester.test_directory("tests/extensions-x-codehilite")

    print "\n### Final result ###"
    if len(tester.failedTests):
        print "%d failed tests: %s" % (len(tester.failedTests), str(tester.failedTests))
    else:
        print "All tests passed, no errors!"

run_tests()




