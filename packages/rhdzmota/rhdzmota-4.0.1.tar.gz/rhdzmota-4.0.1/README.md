# RHDZMOTA Package

[Rodrigo H. Mota](https://rhdzmota.com)'s personal python package that contains general tooling for facilitating the development of software engineering, data engineering, and machine learning projects.

**Aren't toolbox packages usually heavy?** One main concern of designing toolbox packages shared across projects is that the dependency set often becomes too heavy. This is specially true for data-related projects (e.g., installing pandas, request, tensorflow, sklearn, etc). To solve this issue, the `rhdzmota` package offers "package extensions" that can be installed by specifying their corresponding tags. This allows us to "split" the dependency set and functionality in sub-python packages; resulting in a lightweight and modular toolbox!

**How can I install a package extension?** You just need to specify their corresponing "extras-require" tag. Example:

```commandline
$ pip install 'rhdzmota[ext.hello_world]'
```

All the package extensions tag will follow the pattern: `ext.*`

**Are there any import patterns to consider?** Yes, both the core package and the extensions share a common namespace: `rhdzmota`. The core package contains their modules directly at the first level (e.g., `rhdzmota.*`) and the extensions share an inner namespace (i.e., `rhdzmota.ext`) resulting in the following pattern: `rhdzmota.ext.{{ext-slug}}`).

The following example imports the `Env` enum from the `settings` module in the core package and the `hello` function from the `hello_world` extension.

```python
from rhdzmota.settings import Env
from rhdzmota.ext.hello_world.functions import hello

...
```
