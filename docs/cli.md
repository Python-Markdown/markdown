title: Command Line

Using Python-Markdown on the Command Line
=========================================

While Python-Markdown is primarily a python library, a command line script is
included as well. While there are many other command line implementations
of Markdown, you may not have them installed, or you may prefer to use
Python-Markdown's various extensions.

Generally, you will want to have the Markdown library fully installed on your
system to run the command line script. See the
[Installation instructions](install.md) for details.

Python-Markdown's command line script takes advantage of Python's `-m` flag.
Therefore, assuming the python executable is on your system path, use the
following format:

```bash
python -m markdown [options] [args]
```

That will run the module as a script with the options and arguments provided.

At its most basic usage, one would simply pass in a file name as the only argument:

```bash
python -m markdown input_file.txt
```

Piping input and output (on `STDIN` and `STDOUT`) is fully supported as well.
For example:

```bash
echo "Some **Markdown** text." | python -m markdown > output.html
```

Use the `--help` option for a list all available options and arguments:

```bash
python -m markdown --help
```

If you don't want to call the python executable directly (using the `-m` flag),
follow the instructions below to use a wrapper script:

Setup
-----

Upon installation, the `markdown_py` script will have been copied to
your Python "Scripts" directory. Different systems require different methods to
ensure that any files in the Python "Scripts" directory are on your system
path.

* **Windows**:

    Assuming a default install of Python on Windows, your "Scripts" directory
    is most likely something like `C:\\Python37\Scripts`. Verify the location
    of your "Scripts" directory and add it to you system path.

    Calling `markdown_py` from the command line will call the wrapper batch
    file `markdown_py.bat` in the `"Scripts"` directory created during install.

* __*nix__ (Linux, OSX, BSD, Unix, etc.):

    As each \*nix distribution is different and we can't possibly document all
    of them here, we'll provide a few helpful pointers:

    * Some systems will automatically install the script on your path. Try it
      and see if it works. Just run `markdown_py` from the command line.

    * Other systems may maintain a separate "Scripts" ("bin") directory which
      you need to add to your path. Find it (check with your distribution) and
      either add it to your path or make a symbolic link to it from your path.

    * If you are sure `markdown_py` is on your path, but it still is not being
      found, check the permissions of the file and make sure it is executable.

    As an alternative, you could just `cd` into the directory which contains
    the source distribution, and run it from there. However, remember that your
    markdown text files will not likely be in that directory, so it is much
    more convenient to have `markdown_py` on your path.

!!!Note
    Python-Markdown uses `"markdown_py"` as a script name because the Perl
    implementation has already taken the more obvious name "markdown".
    Additionally, the default Python configuration on some systems would cause a
    script named `"markdown.py"` to fail by importing itself rather than the
    markdown library. Therefore, the script has been named `"markdown_py"` as a
    compromise. If you prefer a different name for the script on your system, it
    is suggested that you create a symbolic link to `markdown_py` with your
    preferred name.

Usage
-----

To use `markdown_py` from the command line, run it as

```bash
markdown_py input_file.txt
```

or

```bash
markdown_py input_file.txt > output_file.html
```

For a complete list of options, run

```bash
markdown_py --help
```

Using Extensions
----------------

To load a Python-Markdown extension from the command line use the `-x`
(or `--extension`) option. The extension module must be on your `PYTHONPATH`
(see the [Extension API](extensions/api.md) for details). The extension can
then be invoked by the name assigned to an entry point or using Python's dot
notation to point to an extension

For example, to load an extension with the assigned entry point name `myext`,
run the following command:

```bash
python -m markdown -x myext input.txt
```

And to load an extension with Python's dot notation:

```bash
python -m markdown -x path.to.module:MyExtClass input.txt
```

To load multiple extensions, specify an `-x` option for each extension:

```bash
python -m markdown -x myext -x path.to.module:MyExtClass input.txt
```

If the extension supports configuration options (see the documentation for the
extension you are using to determine what settings it supports, if any), you
can pass them in as well:

```bash
python -m markdown -x myext -c config.yml input.txt
```

The `-c` (or `--extension_configs`) option accepts a file name. The file must be
in either the [YAML] or [JSON] format and contain YAML or JSON data that would
map to a Python Dictionary in the format required by the
[`extension_configs`][ec] keyword of the `markdown.Markdown` class. Therefore,
the file `config.yaml` referenced in the above example might look like this:

```yaml
myext:
    option1: 'value1'
    option2: True
```

Similarly, a JSON configuration file might look like this:

```json
{
  "myext":
  {
    "option1": "value1",
    "option2": "value2"
  }
}
```

Note that while the `--extension_configs` option does specify the
`myext` extension, you still need to load the extension with the `-x` option,
or the configuration for that extension will be ignored. Further, if an
extension requires a value that cannot be parsed in JSON (for example a
reference to a function), one has to use a YAML configuration file.

The `--extension_configs` option will only support YAML configuration files if
[PyYAML] is installed on your system. JSON should work with no additional
dependencies. The format of your configuration file is automatically detected.

[ec]: reference.md#extension_configs
[YAML]: https://yaml.org/
[JSON]: https://json.org/
[PyYAML]: https://pyyaml.org/
[2.5 release notes]: change_log/release-2.5.md
