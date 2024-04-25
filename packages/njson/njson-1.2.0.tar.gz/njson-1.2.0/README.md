# njson: efficient JSON-like data transformation tool

## What is it?
Provide fast JSON-like data transformation to and from nested
parent-child and flat label-value data items, such as Pandas `Series`
with MultiIndex index.

## Features

* Transformation are optimized for speed, to allow parsing deeply 
  nested json-like data with millions of data points in seconds.
* Transformation are lazily computed properties only calculated when
  accessed for the first time. Initializing NestedJson object does not
  require parsing the source data.
* NestedJson is Pure-Python package that runs on JupyterLite, Pyodide,
  PyScript, Cloudflare Workers in Python, etc.
* Itegrates with pandas for quick data transformation to and from
  pandas `Series` and `DataFrame`.
* Provides easy access to nested data at any level using parent keys.
* Provides easy way to pipe data manipulation methods for editing nested
  json-like data. 

## Example usage
### Flatten and unflatten nested json-like or flat-dict-like data.
```python
>>> import njson as nj
>>> d = {'a': 1, 'b': [{}, {'d': 2}]}
>>> njd = nj.NestedJson(d)
>>> print(njd.data) # source data
>>> print(njd.flat_dict) # data as flat-dict with parent key tuples
>>> print(njd.data_series) # with event length parent key tuples
>>> print(njd.data_series_bfill) # even length key tuples aligned rigth
>>> print(njd.get('b')) # get data
>>> print(njd.get('b', 0)) # get nested data
>>> print(njd.get('b', 1)) # get data at any nesting level
>>> njd.parsed.nfd.str # json str of `.data` parsed as nested flat-dict
{'a': 1, 'b': [{}, {'d': 2}]}
{('a',): 1, ('b', 0): {}, ('b', 1, 'd'): 2}
{('a', '', ''): 1, ('b', 0, ''): {}, ('b', 1, 'd'): 2}
{('', '', 'a'): 1, ('', 'b', 0): {}, ('b', 1, 'd'): 2}
[{}, {'d': 2}]
{}
{'d': 2}
'{"a": 1, "b": [{}, {"d": 2}]}'
```

**Note**
* Flat-dict keys are parent key tuples of nested json-like data values.
* List value parent key labels in flat-dict are integer values.
* Empty dict and list values are not "flattened", as they have no
  nested values or parent keys for nested values.
* The `.data_series` - a flat-dict with even length key tuples - has 
  similar data structure to pandas `Series` with `MultiIndex`. As such, 
  key tuple length normalization prepares data for efficient creation
  of Pandas `Series` objects from deeply nested JSON object data.

### Transforming Pandas `Series`, `DataFrame` to and from JSON-like data
```python
>>> import pandas as pd
>>> import njson as nj
>>> d = {'a': 1, 'b': [{}, {'d': 2}]}
>>> njd = nj.NestedJson(d)
>>> ds = njd.to_data_series(into = pd.Series)
>>> print(ds) # pandas Series from NestedJson
>>> print(ds.unstack(level = [0])) # to DataFrame from Series
>>> print(ds.to_dict(into = NestedJson).parsed.nds.data)
<class 'pandas.core.series.Series'>
a           1
b  0       {}
   1  d     2
dtype: object
            d
a      1  NaN
b 0   {}  NaN
  1  NaN    2
a           1
b  0       {}
   1  d     2
dtype: object
{'a': 1, 'b': [{}, {'d': 2}]}
```

**Note**
* Pass pandas `Series` to `NestedJson`'s `.to_data_series` method to
  directly derive Pandas `Series` data. Then access `.parsed.nds.data`
  attribute to derive nested JSON-like data.
* Pass `NestedJson` to pandas `Series.to_dict(into = NestedJson)` to
  directly derive `NestedJson` from Pandas `Series` data.
* Stacking and unstacking Pandas `Series` with `.unstack()` and
  `.stack()` allows to tranform the nested JSON-like data to and from
  convenient tabular-like Pandas `DataFrame` data structure. Note that
  (un)stacking by default sorts the level(s) in the resulting index or
  columns and therefore can alter the order of elements.

### Manipulate nested json-like data.
```python
>>> import njson as nj
>>> d = {'a': 1, 'b': [{}, {'d': 2}]}
>>> njd = nj.NestedJson(d)
>>> # source data
>>> print(njd.data)
>>> # add new nested data
>>> print(njd.setdefault([{'k1': 'v', 'k2': 'v', 'k3': 'v'}], 'c').data)
>>> # clear single key,value pair from nested dict
>>> print(njd.clear('c', 0, 'k1').data)
>>> # clear all values from nested dict
>>> print(njd.clear('c', 0).data)
>>> # remove existing sub-element
>>> print(njd.remove('b', 1).data)
>>> # add new or update existing sub-element or value
>>> print(njd.update({'d': 2}, 'b', 1).data)
>>> # replace existing sub-element or value
>>> print(njd.replace('replaced', 'b', 1).data)
>>> # if key does not exist, replace doesn't add new data
>>> print(njd.replace('notreplaced', 'b', 2).data)
>>> # add new list value value at start position index
>>> print(njd.setdefault('new list value at start', 'b', -3).data)
{'a': 1, 'b': [{}, {'d': 2}]}
{'a': 1, 'b': [{}, {'d': 2}], 'c': [{'k1': 'v', 'k2': 'v', 'k3': 'v'}]}
{'a': 1, 'b': [{}, {'d': 2}], 'c': [{'k2': 'v', 'k3': 'v'}]}
{'a': 1, 'b': [{}, {'d': 2}], 'c': [{}]}
{'a': 1, 'b': [{}], 'c': [{}]}
{'a': 1, 'b': [{}, {'d': 2}], 'c': [{}]}
{'a': 1, 'b': [{}, 'replaced'], 'c': [{}]}
{'a': 1, 'b': [{}, 'replaced'], 'c': [{}]}
{'a': 1, 'b': ['new list value at start', {}, 'replaced'], 'c': [{}]}
```

**Note**
* Data manipulation methods `.clear()`, `.remove()`, `.update()`, 
  `.replace()`, and `.setdefault()` return `NestedJson` object. Such
  that it is possible to pipe mutiple data manpiluation operations.

### Read JSON files

```python
>>> import njson as nj
>>> njd_from_file = nj.read_json('path-to.json')
>>> njd_from_str = nj.read_json_str('{"a": 1, "b": [{}, {"d": 2}]}')
>>> njd_from_str.flat_dict
{('a',): 1, ('b', 0): {}, ('b', 1, 'd'): 2}
```

## Changelog

### v1.2
#### Features
* Add data manipulation methods `.clear()`, `.remove()`, `.update()`, 
  `.replace()`, and `.setdefault()`.

#### Bug Fixes
* Do not flatten `tuple` and `set` objects, to avoid non-reversable data
  transformations via implicit data converstions from tuples to lists.

### v1.1
#### Features
* Add methods `.pipe_flat_dict()`, `.pipe_data_series()`, 
  `.pipe_mapping()` to pipe flat-dict, data-series, mapping, in addition
  to `.pipe_data()`.
* Add optimzied `NestedJsonKeysView`, `NestedJsonValuesView`,
  `NestedJsonItemsView` for `.keys()`, `.values()`, and `.items()`
  methods.

### v1.0
#### Features
* Initial implementation of fast JSON-like data transformation to and 
  from nested parent-child and flat label-value data items.
* Flat-dict keys are parent key tuples of nested json-like data values.
* List value parent key labels in flat-dict are integer values.
* Empty dict and list values are not "flattened", as they have
  no nested values or parent keys for nested values.
* The `.data_series()` - a flat-dict with even length key tuples - has 
  similar data structure to pandas `Series` with `MultiIndex`. As such, 
  key tuple length normalization prepares data for efficient creation
  of Pandas `Series` objects from deeply nested JSON object data.
* Pass pandas `Series` to `NestedJson`'s `.to_data_series` method to
  directly derive Pandas `Series` data. Then access `.parsed.nds.data`
  attribute to derive nested JSON-like data.
* Pass `NestedJson` to pandas `Series.to_dict(into = NestedJson)` to
  directly derive `NestedJson` from Pandas `Series` data.
* Stacking and unstacking Pandas `Series` with `.unstack()` and
  `.stack()` allows to tranform the nested JSON-like data to and from
  convenient tabular-like Pandas `DataFrame` data structure. Note that
  (un)stacking by default sorts the level(s) in the resulting index or
  columns and therefore can alter the order of elements.
