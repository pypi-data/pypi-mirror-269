Create documentation from python modules and other objects.

*Latest release 20240422*:
module_doc: only list things in __all__ if provided.

## Function `is_dunder(name)`

Test whether a name is a dunder name (`__`*foo*`__`).

## Function `module_doc(module, *, sort_key=<function <lambda> at 0x102b29000>, filter_key=<function <lambda> at 0x102b29090>, method_names=None)`

Fetch the docstrings from a module and assemble a MarkDown document.

Parameters:
* `module`: the module or module name to inspect
* `sort_key`: optional key for sorting names in the documentation;
  default: `name`
* filter_key`: optional test for a key used to select or reject keys
  to appear in the documentation
* `method_names`: optional list of method names to document;
  the default is to document `__init__`, then CONSTANTS, the
  dunders, then other public names

## Function `obj_docstring(obj)`

Return a docstring for `obj` which has been passed through `stripped_dedent`.

This function uses `obj.__doc__` if it is not `None`,
otherwise `getcomments(obj)` if that is not `None`,
otherwise `''`.
The chosen string is passed through `stripped_dedent` before return.

# Release Log



*Release 20240422*:
module_doc: only list things in __all__ if provided.

*Release 20240412*:
module_doc: classes: MRO: suppress classes which are not immediate superclasses.

*Release 20220311*:
module_doc: class members no longer rendered as headings, too verbose.

*Release 20210306*:
Drop noise leaked into output.

*Release 20210123*:
* module_doc: include properties/descriptors.
* DISTINFO: this is not Python 2 compatible, drop tag.

*Release 20200718*:
* New is_dunder(name) function to test whether name is a dunder name.
* module_doc: new method_names parameter to report only specific attributes from a class - default is all public names and most dunder methods - things without docs are not reported.
* Assorted small changes.

*Release 20200521*:
Initial PyPI release.
