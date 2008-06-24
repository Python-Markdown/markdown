from __future__ import with_statement
import os

excl_tm_cases = """basic_safe_mode
basic_safe_mode_escape
auto_link_safe_mode
code_safe_emphasis
emacs_head_vars
emacs_tail_vars
footnotes
footnotes_letters
footnotes_markup
footnotes_safe_mode_escape
nested_list_safe_mode
issue2_safe_mode_borks_markup
issue3_bad_code_color_hack
link_defn_spaces_in_url
link_patterns
link_patterns_double_hit
link_patterns_edge_cases
mismatched_footnotes
nested_lists_safe_mode
pyshell
syntax_color"""


def reformat(path, dest, ex=""):
    excl = ex.split("\n")
    for fname in os.listdir(path):
        if fname.endswith(".html"):
            if fname[:-5] in excl:
                continue
            res = processFile(path + fname)
            with open(dest + fname, "w") as rfile:
                rfile.write(res)

def processFile(filePath):
    with open(filePath) as f:
        result = f.read()
    result = result.replace("</pre>\n\n<p>", "</pre><p>")
    result = result.replace("</pre>\n<", "</pre><")
    result = result.replace("</li>", "\n</li>")
    result = result.replace("<li>", "<li>\n")
    result = result.replace(">\n<p>", "><p>")
    result = result.replace("\" />", "\"/>")
    result = result.replace("</p>\n", "\n</p>\n")
    
    return result

if __name__ == "__main__":
    reformat("php-markdown-cases/", "php-markdown-cases-new/")
    reformat("tm-cases/", "tm-cases-new/", excl_tm_cases)
    
    
    