title: Legacy EM Extension

# Legacy EM

## Summary

The Legacy EM extension restores Markdown's original behavior for emphasis and
strong syntax when using underscores.

By default Python-Markdown treats `_connected_words_` intelligently by
recognizing that mid-word underscores should not be used for emphasis. In other
words, by default, that input would result in this output:
`<em>connected_words</em>`.

However, that behavior is not consistent with the original rules or the behavior
of the reference implementation. Therefore, this extension can be used to better
match the reference implementation. With the extension enabled, the above input
would result in this output: `<em>connected</em>words_`.

## Usage

See [Extensions](index.md) for general extension usage. Use `legacy_em` as the
name of the extension.

This extension does not accept any special configuration options.

A trivial example:

```python
markdown.markdown(some_text, extensions=['legacy_em'])
```
