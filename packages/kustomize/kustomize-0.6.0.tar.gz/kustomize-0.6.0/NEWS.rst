v0.6.0
======

Features
--------

- Adding Pydantic v2 support. (#10)


v0.5.1
======

Bugfixes
--------

- Refreshed the package metadata. (#1)
- Require Python 3.8 or later.


v0.5.0
======

* Separating generated modules by directories to avoid name clashes.

v0.4.1
======

* Fixing directory creation for dumping built YAML files.

v0.4.0
======

* Now supporting models from python-kubernetes>=11.

v0.3.6
======

* Adding logs.

v0.3.5
======

* Now supporting Kubernetes objects correctly.

v0.3.4
======

* Fixing cleanup of data before dump.

v0.3.3
======

* Cleaning up the data before dumping.

v0.3.2
======

* Preferring to_dict() to dataclasses.asdict().
  This is because objects might need to be more specific about how they
  should convert themselves to a dict.

v0.3.1
======

* Fixing the serialization of objects inside tuples.

v0.3.0
======

* Supporting tuples for multi-section YAML generation.

v0.2.0
======

Supporting other types for generating dictionaries:

* Classes with a ``to_dict`` method
* Classes from the ``attr`` library
* "Flat" classes that can be serialized through ``__dict__``

v0.1.2
======

* Supporting patchesJson6902

v0.1.1
======

* Supporting patchesStrategicMerge

v0.1.0
======

* First release!
* Supporting dictionaries and dataclasses.
