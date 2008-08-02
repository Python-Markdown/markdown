import os, difflib, time, gc, codecs
from pprint import pprint
import textwrap
        
markdown = None

TEST_DIR = "tests"
TMP_DIR = "./tmp/"
WRITE_BENCHMARK = True
WRITE_BENCHMARK = False
ACTUALLY_MEASURE_MEMORY = True

######################################################################

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



def testDirectory(dir, measure_time=False, safe_mode=False) :

    encoding = "utf8"


    benchmark_file_name = os.path.join(dir, "benchmark.dat")

    saved_benchmarks = {}

    if measure_time :

        if os.path.exists(benchmark_file_name) :

            file = open(benchmark_file_name)
            for line in file.readlines() :
                test, str_time, str_mem = line.strip().split(":")
                saved_benchmarks[test] = (float(str_time), float(str_mem))
        
    if measure_time :
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
    t = time.clock()
    md = markdown.Markdown(extensions=extensions, safe_mode = safe_mode)
    construction_time = time.clock() - t
    construction_mem = memory(mem)

    benchmark_buffer = "construction:%f:%f\n" % (construction_time,
                                                 construction_mem)

    tests = [x.replace(".txt", "")
                  for x in os.listdir(dir) if x.endswith(".txt")]
    tests.sort()

    d = difflib.Differ()
    try :
        hd = difflib.HtmlDiff()
    except: 
        hd = None

    if not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR)

    htmlDiffFilePath = os.path.join(TMP_DIR, os.path.split(dir)[-1]) + ".html"
    htmlDiffFile = codecs.open(htmlDiffFilePath, "w", encoding=encoding)
    htmlDiffFile.write(DIFF_FILE_TEMPLATE)

    diffsBuffer = ""

    for test in tests :

        print "--- %s ---" % test

        htmlDiffFile.write("<tr><td>%s</td>" % test)

        input_file = os.path.join(dir, test + ".txt")
        output_file = os.path.join(dir, test + ".html")

        expected_output = codecs.open(output_file, encoding=encoding).read()

        input = codecs.open(input_file, encoding=encoding).read()

        actual_output = ""
        actual_lines = []
        md.source = ""
        gc.collect()
        mem = memory()
        t = time.clock()
        for x in repeat: 
            actual_output = md.convert(input)
        conversion_time = time.clock() - t
        conversion_mem = memory(mem)
        md.reset()
        
        expected_lines = [x.encode("utf8") for x in smart_split(expected_output)]
        actual_lines = [x.encode("utf8") for x in smart_split(actual_output)]


        #diff = difflib.ndiff(expected_output.split("\n"),
        #                    actual_output.split("\n"))

        
        
        

        diff = [x for x in d.compare(expected_lines,
                                     actual_lines)
                if not x.startswith("  ")]

        if not diff:

            htmlDiffFile.write("<td class='ok'>OK</td>")

        else :

            htmlDiffFile.write("<td class='failed'>" +
                               "<a href='#diff-%s'>FAILED</a></td>" % test)
            
            print "MISMATCH on %s/%s.txt" % (dir, test)
            print
            for line in diff :
                print line

            if hd!=None :
                htmlDiff = hd.make_table(expected_lines, actual_lines,
                                        context=True)

                htmlDiff = "\n".join( [x for x in htmlDiff.splitlines()
                                       if x.strip().startswith("<tr>")] )

                diffsBuffer += "<a name='diff-%s'/><h2>%s</h2>" % (test, test)
                diffsBuffer += DIFF_TABLE_TEMPLATE % htmlDiff

        expected_time, expected_mem = saved_benchmarks.get(test, ("na", "na"))

        htmlDiffFile.write(get_benchmark_html(conversion_time, expected_time))
        htmlDiffFile.write(get_benchmark_html(conversion_mem, expected_mem))
        htmlDiffFile.write("</tr>\n")

            
        benchmark_buffer += "%s:%f:%f\n" % (test,
                                            conversion_time, conversion_mem)

    htmlDiffFile.write("</table>")

    htmlDiffFile.write(diffsBuffer.decode("utf8"))
    htmlDiffFile.write(FOOTER)
    htmlDiffFile.close()
    print "Diff written to %s" % htmlDiffFilePath

    benchmark_output_file_name = benchmark_file_name

    if not WRITE_BENCHMARK:
        benchmark_output_file_name += ".tmp"

    benchmark_file = open(benchmark_output_file_name, "w")
    benchmark_file.write(benchmark_buffer)
    benchmark_file.close()


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


MARKDOWN_FILE = "markdown.py"


if MARKDOWN_FILE.endswith(".py") :
    MARKDOWN_FILE = MARKDOWN_FILE[:-3]

print MARKDOWN_FILE
    

markdown = __import__(MARKDOWN_FILE)


#testDirectory("tests/basic")
testDirectory("tests/markdown-test", measure_time=True)

testDirectory("tests/misc", measure_time=True)
testDirectory("tests/extensions-x-footnotes")
#testDirectory("tests/extensions-x-tables")
# testDirectory("tests/extensions-x-ext1-ext2")
testDirectory("tests/safe_mode", measure_time=True, safe_mode="escape")

#testDirectory("tests2/php-markdown-cases-new", measure_time=True)
#testDirectory("tests2/tm-cases-new", measure_time=True) 
