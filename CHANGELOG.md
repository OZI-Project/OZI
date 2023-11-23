# CHANGELOG



## v0.0.211 (2023-11-23)

### :bug:

* :bug:: Sanitize ozi-fix target against directory traversal. ([`690d200`](https://github.com/rjdbcm/OZI/commit/690d200b796ae46965230410102a214149f99150))

* :bug:: Fix unsanitized path. ([`7a3d624`](https://github.com/rjdbcm/OZI/commit/7a3d624fca54405eda4fe0472403926541e07fe2))

### Other

* :rotating_light:: Fix mypy complaints. ([`d06449f`](https://github.com/rjdbcm/OZI/commit/d06449f23ecc4a53e3f9de8de6149f4ab8b4f5f6))

* :rotating_light:: Fix black and revert PKG-INFO patch bump. ([`bbea8fb`](https://github.com/rjdbcm/OZI/commit/bbea8fbe7138263d529764032dc8655733dddcb0))


## v0.0.210 (2023-11-23)

### :bug:

* :bug:: Fix email email validator install path. ([`9828d09`](https://github.com/rjdbcm/OZI/commit/9828d097103d953433d0ea814b0488bee4043ee2))


## v0.0.209 (2023-11-23)

### :bug:

* :bug:: Finish vendoring of email_validator ([`fa371f1`](https://github.com/rjdbcm/OZI/commit/fa371f178aa662bbeb4e0f3fab11fd6bb4154fa3))

* :bug:: Vendor email-validator. ([`d17acf1`](https://github.com/rjdbcm/OZI/commit/d17acf12824864d24f5493e0a3d1379632859dfa))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`c1fdcc0`](https://github.com/rjdbcm/OZI/commit/c1fdcc0e63c2114cc4e1131d626718101840115e))


## v0.0.208 (2023-11-22)

### :bug:

* :bug:: Fix circular depend on email_validator ([`30543b7`](https://github.com/rjdbcm/OZI/commit/30543b70a48b25b660030f2f032fa106359e1b26))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`5ad1bae`](https://github.com/rjdbcm/OZI/commit/5ad1bae67d7da17de21b4cc962e402fdbcb77eaa))


## v0.0.207 (2023-11-22)

### :bug:

* :bug:: Fix circular import. ([`d0fd1bd`](https://github.com/rjdbcm/OZI/commit/d0fd1bd0edcc83db54279dd182ab8e8288c2720b))


## v0.0.206 (2023-11-22)

### :bug:

* :bug:: Fix coverage with no cover of warning format. ([`05322ed`](https://github.com/rjdbcm/OZI/commit/05322ede2634de929f00915f3192c5aea7adca4c))

* :bug:: Fix linter complaints and missing import. ([`c1d68d8`](https://github.com/rjdbcm/OZI/commit/c1d68d8d20929984b04d7a104d90bca43e93818d))

* :bug:: Fix unknown import issue with email_validator. ([`d4d8b16`](https://github.com/rjdbcm/OZI/commit/d4d8b161d4e73a02e68170e64af2a48c886c8e5e))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`0605305`](https://github.com/rjdbcm/OZI/commit/0605305647598863eb5ebb8dce9e4db568ca7a17))


## v0.0.205 (2023-11-22)

### :bug:

* :bug:: No cover warning formatter. ([`5b52bfc`](https://github.com/rjdbcm/OZI/commit/5b52bfc4443e220ef23c4d612ed77cb622779722))

* :bug:: Remove test of tap warning formatting. ([`be62ac1`](https://github.com/rjdbcm/OZI/commit/be62ac1867aadf1629b77102b1e6c45ddded9b2b))

* :bug:: Fix circular assets import. ([`b8a2774`](https://github.com/rjdbcm/OZI/commit/b8a2774b5106b2e2095f4d405f88afae5a02d931))

### Other

* Fix missing ruff template and circular import. ([`323b963`](https://github.com/rjdbcm/OZI/commit/323b96375b1e1c8f083b95fdfb1bc69e3e65e911))


## v0.0.204 (2023-11-22)

### :bug:

* :bug:: Fix meson.build template pyproject.toml preprocessing. ([`e9f10da`](https://github.com/rjdbcm/OZI/commit/e9f10da28bf2a3fc9dd78766f684b72def73ee6f))

* :bug:: Fix warning output to use TAP with a contextmanager. ([`92dea85`](https://github.com/rjdbcm/OZI/commit/92dea85753c1edb4fc6bf676a1c75f4048809ac9))


## v0.0.203 (2023-11-21)

### :bug:

* :bug:: Fix ``--list-available`` to use ExactMatch API. ([`2938362`](https://github.com/rjdbcm/OZI/commit/2938362128dbcec76762648a4a11bb8839382e89))

* :bug:(ozi/__main__.py): Fix incorrect help and OZI.spec.Metadata API use. ([`67655e8`](https://github.com/rjdbcm/OZI/commit/67655e8a9ffc250b23d01e7b59e6cb7d1be025d4))


## v0.0.202 (2023-11-21)

### :bug:

* :bug:: Fix typing issue on 3.10 ([`b6722c9`](https://github.com/rjdbcm/OZI/commit/b6722c9debe222eece36d2207927c83e0b344619))

* :bug:: Fix missing Self type annotation on 3.10 builds. ([`67059e3`](https://github.com/rjdbcm/OZI/commit/67059e32d6f168b0b96570c27b282d48928b5c9b))

### :wrench:

* :hammer::wrench:: Major refactor iteration.

* Created a specification data API ``ozi/spec.py``
* Moved argument matching actions to ``ozi/actions.py``
* Moved most parsers into ``ozi/assets.py``
  * Remove ``ozi/assets/__init__.py`` and ``ozi/assets/structure.py``
* Moved most Jinja2 template setups to ``ozi/render.py``
* Moved Jinja2 compatible filter functions into ``ozi/filter.py``
* Remove spec requirement for ``__init__.pyi``
* Update spec with compatibility for ruff
  * adds single line imports specification format requirement
* Fix VCS version templating by meson to write to a preprocessed ``pyproject.toml`` (``pyproject.toml.pre``)
* Move utility requirements to top level source dir ``ozi/dist``, ``ozi/docs``, ``ozi/lint``, ``ozi/test``.
* Proper author rendering as a list. ([`0793eff`](https://github.com/rjdbcm/OZI/commit/0793eff197e991d0d87896ccfbe5dcbc4572cfbd))

### Other

* :rotating_light:: no cover type guard ([`2c4a33a`](https://github.com/rjdbcm/OZI/commit/2c4a33a27904cee4bafaa53b0be6c5d7978c1385))

* :rotating_light: Forgot to lint. ([`3bf8be5`](https://github.com/rjdbcm/OZI/commit/3bf8be525956bc427690a6d175ca9b0c799b691d))

* :rotating_light: Fix lint. ([`5a05ff0`](https://github.com/rjdbcm/OZI/commit/5a05ff088530c05f8a237caa3c09267e340a665f))


## v0.0.201 (2023-11-15)

### :bug:

* :bug:: Add missing __init__.pyi required by spec. ([`9e6ba6e`](https://github.com/rjdbcm/OZI/commit/9e6ba6efc45c8f6bbc52fe56f52fc4b7c9dd21e2))

### Other

* :rotating_light:(pyproject.toml): Clean up. ([`6c9e92c`](https://github.com/rjdbcm/OZI/commit/6c9e92c2e8d6238b4078d0b02ecad0e979d6e808))


## v0.0.200 (2023-11-14)

### :bug:

* :bug: Fix meson.build build file check to use absolute path. ([`30f8c56`](https://github.com/rjdbcm/OZI/commit/30f8c56bc611309b8ce1e59d2ed110861d764b2b))


## v0.0.199 (2023-11-14)

### :bug:

* :bug:(ozi-fix): Fix missing ``run_utility`` AttributeError

Fixes: File &#34;&lt;OZI-0.0.198&gt;/ozi/fix.py&#34;, line 667, in main
AttributeError: &#39;Namespace&#39; object has no attribute &#39;run_utility&#39; ([`6c4d52a`](https://github.com/rjdbcm/OZI/commit/6c4d52a533052006a69f645bdec79c09fde02c9f))


## v0.0.198 (2023-11-14)

### :bug:

* :bug:(ozi-new): fix missing append argparse arguments.

Revert to using standard email-validator package. ([`1f2959b`](https://github.com/rjdbcm/OZI/commit/1f2959bb9c4dfc82bf7bf64c0aa4d73709a9f42b))


## v0.0.197 (2023-11-14)

### :hammer:

* :hammer:(ozi-fix,ozi-new): Clean up

Add Author, Author-email, License to assets.required_pkg_info
Create metadata variable in __init__.py
Add meson_min_version key to ozi metadata context used in Jinja2 templates
Add check_for_update method to ``ozi`` main script
Remove verbosity requirement for ``isort``
Add ``--run-utility`` to run ``isort``, ``black``, and ``autoflake`` with ``ozi-fix``
``ozi-fix`` warns for python files missing from meson.build.
``tox`` run local ``pip install``  add ``--quiet``
:bug: Template for ``meson.build`` in root now builds ``requirements.in``
Add Author, Author-email, License, Maintainer, and Maintainer-email keys to PKG-INFO template.
:bug:(scm_version): Fix ``fallback_version`` placeholder to use VCS_TAG from ``meson`` and set ``parentdir_prefix_version`` at template render.
Add ``--check-for-update`` bool arg to ``ozi-new`` (not yet implemented) ([`ee63ffd`](https://github.com/rjdbcm/OZI/commit/ee63ffd3f78f0950a1dc080a36f816907085359e))


## v0.0.196 (2023-11-10)

### :bug:

* :bug:: Fix missing ``pip-tools`` dep. ([`1ee16cc`](https://github.com/rjdbcm/OZI/commit/1ee16ccaea5741a513982bc4681b3b8c8c838865))

* :bug: Fix release signing for sdist. ([`8295605`](https://github.com/rjdbcm/OZI/commit/829560542fab9f36f86e90e3074f10fa2814aa99))

* :bug:(CI): Fix sdist release.

Also publishes a sigstore bundle for the tarball release. ([`dcdfb20`](https://github.com/rjdbcm/OZI/commit/dcdfb204cc57fbaea6d7609928aff4ad17209145))

### :pencil2:

* :pencil2: Fix typo from clipboard. ([`fe1561c`](https://github.com/rjdbcm/OZI/commit/fe1561c213391ca697c481968cd62852b77f32b5))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`9c16b2f`](https://github.com/rjdbcm/OZI/commit/9c16b2fe8f56b55fe10b2bd1fb629851cb0f0a86))


## v0.0.195 (2023-11-10)

### :hammer:

* :hammer::construction_worker:(GitHub): Fix publish workflow to publish an sdist.

Fixes sdist builds disabled #2 ([`5a059e1`](https://github.com/rjdbcm/OZI/commit/5a059e1f3236506e28c03f44330fd3c36f72b2e9))


## v0.0.194 (2023-11-09)

### :bug:

* :bug:(ozi-new): Fix TypeError.

missing default. ([`3f8b5ff`](https://github.com/rjdbcm/OZI/commit/3f8b5ff539d54c024f1a4c89636db352b57390ed))


## v0.0.193 (2023-11-09)

### :hammer:

* :hammer:(ozi-new): Add Download-URL to PKG-INFO Template.

Adds a ``project.ci_user`` dependent on ``project.ci_provider``.
Adds a ``Download-URL`` output dependent on ``project.ci_provider``.
Adds dependency on [GitPython](https://pypi.org/project/GitPython)
Fixes Issue #5 [OZI does not support Download-URL header.](https://github.com/rjdbcm/OZI/issues/5) ([`070f033`](https://github.com/rjdbcm/OZI/commit/070f03380dae39b2e2ceb0ad63af7d9a2c38e873))


## v0.0.192 (2023-11-09)

### :hammer:

* :hammer:(ozi-new): Use ``shlex.join()`` to render argv in changelog. ([`33b5219`](https://github.com/rjdbcm/OZI/commit/33b5219bd80cf11e53de3124b779d332735a464c))

* :hammer:(PKG-INFO): Correct Download-URL. ([`f787eb8`](https://github.com/rjdbcm/OZI/commit/f787eb82bdde5c273232c1a08a4b7e7c9f5fd9b0))


## v0.0.191 (2023-11-08)

### :hammer:

* :hammer:(ozi-new): Add optional Project-URL metadata.

Fixes Issue [Project-URLs are not supported by OZI #4](https://github.com/rjdbcm/OZI/issues/4) ([`b09898b`](https://github.com/rjdbcm/OZI/commit/b09898b02edc26ba07bc223e16edc0485fa3188d))

### Other

* :rotating_light:(tests/ozi_new.py): Fix black lint failure. ([`06419d9`](https://github.com/rjdbcm/OZI/commit/06419d98e16e6f56afd5c7e48f8e7c0282b7bc56))


## v0.0.190 (2023-11-04)

### :hammer:

* :hammer:(ozi-new): Add a cache key based on compiled requirements file.

Prior to this patch caches were not checked against requirements file. ([`af72080`](https://github.com/rjdbcm/OZI/commit/af720803bfacd8944e02e2b1952bd5a160c387e4))


## v0.0.189 (2023-11-04)

### :hammer:

* :hammer:(ozi-new): Fix missing ``subprojects/ozi.wrap``. ([`97ba52a`](https://github.com/rjdbcm/OZI/commit/97ba52a0af7e15008e054956ce8a257f77e28b2e))


## v0.0.188 (2023-11-04)

### :bug:

* :bug:(ozi-new): Fix missing __init__.pyi in project initialization. ([`94eb34f`](https://github.com/rjdbcm/OZI/commit/94eb34f7b754599e2f71f660b55396ec8aa21f55))


## v0.0.187 (2023-11-04)

### :bug:

* :bug:(ozi-new): Project source ``meson.build`` options conditional removed.

This check was added in error. ([`87bf8ec`](https://github.com/rjdbcm/OZI/commit/87bf8ec6b4c9888aa582e83f8ed65cbdc2318436))


## v0.0.186 (2023-11-03)

### :hammer:

* :hammer::pencil2:(ozi-new): Fix project source directory naming in root meson.build. ([`c8eba2f`](https://github.com/rjdbcm/OZI/commit/c8eba2ff2682e4f091542970769b7732366e7fe9))


## v0.0.185 (2023-11-03)

### :hammer:

* :hammer:(ozi-new): Update templates.

Projects now initialize with a changelog.
PKG-INFO is now initialized with version ``0.0.0``.
README.rst initializes with the OZI extra package info. ([`d09381b`](https://github.com/rjdbcm/OZI/commit/d09381ba174da7046765f7ca4bae7a0905de1483))

### :pencil2:

* :pencil2: Update semantic_release CHANGELOG.md template whitespace ([`527aa60`](https://github.com/rjdbcm/OZI/commit/527aa6073ef053f1f680870c4cc01fc37126d5c5))


## v0.0.184 (2023-11-03)

### :hammer:

* :hammer:(ozi-new): Add ``--allow-file``.

Added a list of allowed files in a new project directory: ``project.allow_file``.
Currently by default ``templates/`` and ``.git/`` are allowed. ([`a9640c1`](https://github.com/rjdbcm/OZI/commit/a9640c153c0d160bb82a344528d59dcb91d57e55))

### :pencil2:

* :pencil2: Update CHANGELOG.md

Fix minor changelog format issues. ([`f53f628`](https://github.com/rjdbcm/OZI/commit/f53f62872fd5c985df753fd8f26e8f5c9603158b))

### Other

* Update CHANGELOG.md ([`dd953c8`](https://github.com/rjdbcm/OZI/commit/dd953c847a28e0936a4e94a2115319b3c920a303))


## v0.0.183 (2023-11-02)

### :bug:

* :bug:(templates): Fix author_email rendering. ([`ab78ea0`](https://github.com/rjdbcm/OZI/commit/ab78ea014c987cfde5155926a852e2ac85b08820))

### :hammer:

* :hammer:(ozi-new): Allow new project with existing ``templates/`` and ``.git/`` ([`53c5687`](https://github.com/rjdbcm/OZI/commit/53c5687821a9af76a19d3572d39b1ae13636c2c7))

### :pencil2:

* :pencil2::construction_worker: Fix workflow logging to use wildcard. ([`5fa5496`](https://github.com/rjdbcm/OZI/commit/5fa549603eb62da4ec00077c902216525dbbd980))

### Other

* Add failure logging to checkpoint workflow. ([`3c5cd27`](https://github.com/rjdbcm/OZI/commit/3c5cd2708ef3fbe027f1df31f1758c75f35c2261))

* :construction_worker:(PKG-INFO): 0.0.183 ([`db66619`](https://github.com/rjdbcm/OZI/commit/db666193bf07ee9a66b143690a5383ddd5f59c06))


## v0.0.182 (2023-11-01)

### :bug:

* :bug:(CI): Fix ozi release workflow python version string quoting. ([`b5ec332`](https://github.com/rjdbcm/OZI/commit/b5ec33265a63b91267b82fce7903c55c810a51c6))


## v0.0.181 (2023-11-01)

### :bug:

* :bug:(CI): Fix workflow job indent level. ([`b6d4587`](https://github.com/rjdbcm/OZI/commit/b6d4587a939472904af4e86d2feb598887a5d263))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`0500b78`](https://github.com/rjdbcm/OZI/commit/0500b780c80707e6f84cf715efc485734b2328e8))


## v0.0.180 (2023-11-01)

### :bug:

* :bug:(CI): Fix indentation issue in workflow template. ([`07abfd4`](https://github.com/rjdbcm/OZI/commit/07abfd40060617fdfd8ee4a775c7429ee879cd34))


## v0.0.179 (2023-11-01)

### :bug:

* :bug::construction_worker:(CI): Fix for raw jinja whitespace trimming causing broken workflow. ([`e3e4d66`](https://github.com/rjdbcm/OZI/commit/e3e4d6633e6f62a93084eee9dc1e0f74f0c0fd21))


## v0.0.178 (2023-11-01)

### :bug:

* :bug:(ozi-fix): Fix incorrect source install subdir argument. ([`77c97b2`](https://github.com/rjdbcm/OZI/commit/77c97b27c492b138dc772609a2de21b1f0bbccbd))


## v0.0.177 (2023-10-31)

### :bug:

* :bug:(tests/ozi_fix.py): Remove flaky assertion. ([`fcaf807`](https://github.com/rjdbcm/OZI/commit/fcaf8072cf3c03ebd29734b7bfe09e17ad46b5c4))

### :children_crossing:

* :children_crossing:(ozi-fix): warn for nested subdirectories. ([`8f99980`](https://github.com/rjdbcm/OZI/commit/8f99980cc219c4bf17029fdecbc49e0c0768579b))


## v0.0.176 (2023-10-31)

### :bug:

* :bug: Revert nested dir add ([`b6c0de8`](https://github.com/rjdbcm/OZI/commit/b6c0de88f59818e9a4f4ae9261fd1b817d082bf2))

* :bug:(ozi-fix): Fix unconditional output of a file add command. ([`69614ba`](https://github.com/rjdbcm/OZI/commit/69614ba5d6c0a0c2aad0ee7627c58aefc5ec962d))


## v0.0.175 (2023-10-31)

### :children_crossing:

* :children_crossing::bug:(CI): Fix retry of OZI utility checkpoint. ([`20b122d`](https://github.com/rjdbcm/OZI/commit/20b122d892dcbea1b70a59937015821e19bcfc81))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`0b8a84e`](https://github.com/rjdbcm/OZI/commit/0b8a84ecfc2c904fa90795a7a08bbe7df96a9af8))


## v0.0.174 (2023-10-31)

### :children_crossing:

* :children_crossing::construction_worker:(CI): Retry checkpoint workflow after failure. ([`3188248`](https://github.com/rjdbcm/OZI/commit/318824881d6ae0fa5a38d47ceef5b87f4767525f))


## v0.0.173 (2023-10-31)

### :bug:

* :bug:(ozi-fix): Fix incorrect path to source subdirectory __init__.py ([`b7a454c`](https://github.com/rjdbcm/OZI/commit/b7a454cc496d7252726a5be0c42b4b80433b6c02))

* :bug:(ozi-fix): FIX: Incorrect subdirectory for __init__.py when adding source directories. ([`6c295c9`](https://github.com/rjdbcm/OZI/commit/6c295c9927bb0e52a9202f145687347394a40e7a))


## v0.0.172 (2023-10-30)

### :children_crossing:

* :children_crossing::bug:(ozi-fix): Adding a source subdirectory now includes the __init__.py ([`1403d36`](https://github.com/rjdbcm/OZI/commit/1403d36b170797d676f8f36675ef83b2fb34c4bb))


## v0.0.171 (2023-10-30)

### :children_crossing:

* :children_crossing:(ozi-fix): Can now add nested subdirectories.

You can now add subdirectories that are nested like
```
ozi-fix source -a foo/bar/baz/
``` ([`5d3c15e`](https://github.com/rjdbcm/OZI/commit/5d3c15e7defcd1495ff4fc55aa24335aecdc9e25))


## v0.0.170 (2023-10-30)

### :children_crossing:

* :children_crossing:(ozi-fix): Add support for a ``templates/`` for user templates. ([`ecedb26`](https://github.com/rjdbcm/OZI/commit/ecedb26faa1015c4fba527d29b8b60919ceb5721))


## v0.0.169 (2023-10-28)

### :bug:

* :bug:(ozi-new): Fix Framework classifier output. ([`e7a7bb3`](https://github.com/rjdbcm/OZI/commit/e7a7bb36d27fd05f8ff7767584663afa5107e709))


## v0.0.168 (2023-10-28)

### :bug:

* :bug:(ozi-fix): Fix miscount in TAP output. ([`3e6b662`](https://github.com/rjdbcm/OZI/commit/3e6b66224bf24ec88f77d16b8e9e5e22f090a065))


## v0.0.167 (2023-10-27)

### :bug:

* :bug:: Fix default Multiple use args. ([`38cd3d4`](https://github.com/rjdbcm/OZI/commit/38cd3d4535a94ef8d57bc90fa108f344a3a855ca))

### :pencil2:

* :pencil2:: Fix black complaints. ([`c5b1402`](https://github.com/rjdbcm/OZI/commit/c5b1402b799b2177134d9e91d9fa21ff5b22169b))


## v0.0.166 (2023-10-27)

### :bug:

* :bug:(ozi-new): Fix keywords parsing. ([`db3f61e`](https://github.com/rjdbcm/OZI/commit/db3f61ef9080fca38d0b5e033e6031111b51faf8))


## v0.0.165 (2023-10-27)

### :bug:

* :bug:(ozi-new): Fix several improper PKG-INFO outputs ([`8db531a`](https://github.com/rjdbcm/OZI/commit/8db531a4162764f12967894f53de707386fa49e6))


## v0.0.164 (2023-10-26)

### :bug:

* :bug:: Fix missing variable in fix copyright_head. ([`1b06ddb`](https://github.com/rjdbcm/OZI/commit/1b06ddbb44e0ff3fd84b72a63033e804dc9ceed5))

### :pencil2:

* :pencil2:: Fix missing format placeholder. ([`a4c49cf`](https://github.com/rjdbcm/OZI/commit/a4c49cf0b3e09ef8068c1cc64d475ab56e665510))


## v0.0.163 (2023-10-26)

### :bug:

* :bug:: Fix missing dist_requires tests. ([`5d3c594`](https://github.com/rjdbcm/OZI/commit/5d3c594903f72d7e00168bf6f36e07697485f29c))

* :bug:: Fix default dist_requires. ([`513b932`](https://github.com/rjdbcm/OZI/commit/513b932dddcdf8890366c885f6c883445ad4cd62))


## v0.0.162 (2023-10-26)

### :bug:

* :bug:: Fix default project topic. ([`9d6e9d4`](https://github.com/rjdbcm/OZI/commit/9d6e9d4fd1330a0719fae5869da467fc4af3e9db))


## v0.0.161 (2023-10-26)

### :bug:

* :bug:(ozi/new.py): Fix EmailSyntaxError handling.

Emails with no @ sign will simply warn. ([`4e1fe3e`](https://github.com/rjdbcm/OZI/commit/4e1fe3eade42311e4cc2b7356615072d7de3fe47))


## v0.0.160 (2023-10-26)

### :children_crossing:

* :pencil2::children_crossing:: Fix flaky test deadline. ([`362c0b0`](https://github.com/rjdbcm/OZI/commit/362c0b04a31e44c4f7787c9d5601af070dda21c7))

### Other

* :rotating_light:: Re-black test file. ([`afabb83`](https://github.com/rjdbcm/OZI/commit/afabb835ee9544c83f54408f45a11dc801a349c6))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`7182937`](https://github.com/rjdbcm/OZI/commit/718293782da8391afde615bf10c607f096445ab5))


## v0.0.159 (2023-10-26)

### :hammer:

* :hammer::construction_worker:: Update templates and turn on CI dependency caching. ([`4897943`](https://github.com/rjdbcm/OZI/commit/4897943249f5375ed7ed9626e2c232b9acd13604))


## v0.0.158 (2023-10-25)

### :hammer:

* :hammer:: Add artifact upload for meson logs during checkpoint. ([`df59a74`](https://github.com/rjdbcm/OZI/commit/df59a743430fa7bc4d471c61d0621ab6aa578a8e))

### :pencil2:

* :pencil2:: Wildcard artifact upload path. ([`4a8aae1`](https://github.com/rjdbcm/OZI/commit/4a8aae1c50c8122c89fd48ddeed1ec36954db254))

* :pencil2:: Fix path name for artifact upload. ([`56fc456`](https://github.com/rjdbcm/OZI/commit/56fc4561efbf48fd1da4ab2b4f19c66141a78165))

* :pencil2:: Always upload artifact ([`3c05e6f`](https://github.com/rjdbcm/OZI/commit/3c05e6fad058cd00c617be08fcb1b3e440047503))


## v0.0.157 (2023-10-25)

### :children_crossing:

* :hammer::children_crossing:(project): Refactored for running test suite on OZI build itself. ([`1bbd6ae`](https://github.com/rjdbcm/OZI/commit/1bbd6aedcf7539d7c623991aed5bec0aed7975ec))

* :children_crossing:: Add meson-private/ to .gitignore. ([`2a4e62d`](https://github.com/rjdbcm/OZI/commit/2a4e62d30984b0334487b3691c82762640916834))

* :rotating_light::children_crossing:(tests): Fix paths for build. ([`7a8960f`](https://github.com/rjdbcm/OZI/commit/7a8960f4965edd237b8539cdf293478f8ba9048d))

* :hammer::children_crossing:(ozi/scripts): pip-compile now runs silently. ([`a1cf607`](https://github.com/rjdbcm/OZI/commit/a1cf60711aba8d8691ebab0326423faa50d42a22))

### :hammer:

* :hammer::rotating_light:(ozi): Fix py312 flake8-quotes style. ([`54f8ed7`](https://github.com/rjdbcm/OZI/commit/54f8ed7167782fc6d4da5d81d4d4ebe6eef49df6))

* :hammer:: Fix CI workflow for local checkpointing. ([`06d9107`](https://github.com/rjdbcm/OZI/commit/06d91073d1295678e3fe7c571fe891535eb76143))

* :hammer:(ozi/assets;ozi/templates): Fix missing files from build. ([`aa014bb`](https://github.com/rjdbcm/OZI/commit/aa014bbe59589d042ac5a8dbcd904d72b28d571f))

### :pencil2:

* :pencil2:: Fix missing toml-config arg. ([`c764706`](https://github.com/rjdbcm/OZI/commit/c764706ab36c054407a037e652038af941a11f29))

### Other

* :rotating_light:(ozi): Fix linting and typing. ([`7fca0c4`](https://github.com/rjdbcm/OZI/commit/7fca0c49a0d4b3f7b592d3238251f63c65bb4c30))


## v0.0.156 (2023-10-20)

### :pencil2:

* :pencil2: Emails generated from phony domains. ([`e415cc9`](https://github.com/rjdbcm/OZI/commit/e415cc97c7af5878b34334879c769450619ea49a))

### Other

* :white_check_mark:(tests/ozi_new.py): fullmatch=True for from_regex strategy. ([`c20fb56`](https://github.com/rjdbcm/OZI/commit/c20fb56cbef138ab73660e2addfa30d68b6acbe1))


## v0.0.155 (2023-10-20)

### :hammer:

* :hammer:(meson.options):Complete compliance with specification.

Flake8 is happy.
Coverage is complete. ([`5a0d991`](https://github.com/rjdbcm/OZI/commit/5a0d9910326be8e5926881f6f6b005afad0c2dae))

### Other

* Add more @settings(deadline=timedelta(milliseconds=500)) ([`c6bbe72`](https://github.com/rjdbcm/OZI/commit/c6bbe72c0d39ba2811cd683cabfc614c20487dd9))

* :white_check_mark:(tests/ozi_new.py:test_fuzz_new_project_good_namespace): suppress_health_check=[HealthCheck.too_slow] ([`1792d25`](https://github.com/rjdbcm/OZI/commit/1792d25dbee40a500e35e6a95520886b29de1ae0))

* :white_check_mark:: Fix deadline of test_fuzz_CloseMatch_nargs_None. ([`3b412c9`](https://github.com/rjdbcm/OZI/commit/3b412c9a727e2ed606d2fe92b1f386b5b3d04937))

* :white_check_mark:(tests/ozi_new.py): Reduce size of hypothesis.

Add max_size=8 to author_email and maintainer_email. ([`d75eae9`](https://github.com/rjdbcm/OZI/commit/d75eae9375390f04d6927d99c9add9f5c6a91989))


## v0.0.154 (2023-10-13)

### :bug:

* :bug:: Fix missing license templates. ([`439c426`](https://github.com/rjdbcm/OZI/commit/439c426894c4de153579be08f9b41e34ae72dff7))

### :children_crossing:

* :children_crossing:: Reduce test size to fix failed health check. ([`13bb6f3`](https://github.com/rjdbcm/OZI/commit/13bb6f339051adb1ce233cd0ae04ad86e7ca506b))

* :children_crossing:: Moved test assumptions to start of test. ([`b345516`](https://github.com/rjdbcm/OZI/commit/b3455164da0dcc64a20c773271a29327592e6b51))

### :hammer:

* :hammer:(ozi-new): Refactor of arguments. ([`69a5ace`](https://github.com/rjdbcm/OZI/commit/69a5ace417daa4d2e38d23ec3d3ea5b10ab03ff5))

* :hammer:: Change PKG-INFO template.

Add:
* keywords
* maintainer
* maintainer_email

Change:
* email -&gt; author_email ([`93b59a0`](https://github.com/rjdbcm/OZI/commit/93b59a0bcf85ca800d9898f22b8f161354cb0936))

* :hammer:: Add missing license templates.

Just LGPL-2.0-x and APSL-X.X ([`6465972`](https://github.com/rjdbcm/OZI/commit/6465972cc9ce6639d95ac99c5b57f88fe7a4f72f))


## v0.0.153 (2023-10-10)

### :hammer:

* :hammer:: add requirements.in to root_templates. ([`16f1124`](https://github.com/rjdbcm/OZI/commit/16f1124bff821a87101fad7853c5edb630f119a7))

* :hammer::construction_worker:: Update CI templates and CI build process. ([`a12607c`](https://github.com/rjdbcm/OZI/commit/a12607c954be007fd05f60a8d3da7394fcb0dba9))

* :hammer:: Add requirements.in to required file templates.

Also add metadata_version to PKG-INFO template.
Also add requirements as Requires-Dist in PKG-INFO template. ([`f18a8d8`](https://github.com/rjdbcm/OZI/commit/f18a8d8048d242f34b928509e1d6bbf9d13b8a52))

* :hammer:: Pytest entrypoint has a workflow template of its own.

This is mainly so we can document it in the specification. ([`c4fb826`](https://github.com/rjdbcm/OZI/commit/c4fb8261f1aebd7ffd74ce478d863f11b7803b50))


## v0.0.152 (2023-10-08)

### :hammer:

* :memo::hammer:(ozi-new): Add coverage and pytest templates ([`3504ee1`](https://github.com/rjdbcm/OZI/commit/3504ee1888b8b1d7a52a25db2a3b595a9561e51d))

* :hammer:: ``pytest_plugins`` option becomes ``plugin_only``. ([`72cf109`](https://github.com/rjdbcm/OZI/commit/72cf1095aa77cffaba7578978f40821743b61696))

* :hammer:: Make ``Home-page`` a REQUIRED PKG-INFO key. ([`a92191c`](https://github.com/rjdbcm/OZI/commit/a92191c98697e9957a91a4553df8b57cef90b6cc))


## v0.0.151 (2023-10-07)

### :bug:

* :bug::pencil2:: PKG-INFO template python version typo fix. ([`11ec7d9`](https://github.com/rjdbcm/OZI/commit/11ec7d9d4eee89fd74b44f2f4459c37a5972f06a))


## v0.0.150 (2023-10-06)

### :bug:

* :bug:: Fix improper import of dataclass from attr. ([`5714c66`](https://github.com/rjdbcm/OZI/commit/5714c66fc8d4a0b17419ff93b8c7aa5e27f7ac50))

### :children_crossing:

* :children_crossing:: Use Home-page header in PKG-INFO template. ([`6d4a96a`](https://github.com/rjdbcm/OZI/commit/6d4a96ac631a6b7a259d439b9c6c6ccbb558ed86))

* :children_crossing:(PKG-INFO): Use Home-page and Download-URL.

Also add requirements to PKG-INFO, including git. ([`2fda90e`](https://github.com/rjdbcm/OZI/commit/2fda90e3f1d9a405567a2a312833b481cb2ac5b4))

### Other

* :construction_worker:(PKG-INFO): Patch bump. ([`3ead502`](https://github.com/rjdbcm/OZI/commit/3ead50241c5068ff0a9137c5201b674a4b8d2f5b))


## v0.0.149 (2023-10-06)

### :bug:

* :bug:(CI): Fix Python versioning to follow an automated policy for CI templates. ([`7ae853b`](https://github.com/rjdbcm/OZI/commit/7ae853b66203f2ecf0ab4d6dacc860d5884be3ff))


## v0.0.148 (2023-10-06)

### :children_crossing:

* :children_crossing:: Add bug tracker URL. ([`957fc15`](https://github.com/rjdbcm/OZI/commit/957fc1541461d3f362f228349b0168f927edf5a1))

### :hammer:

* :hammer:: Add automation and checking of Python implementation and version metadata. ([`7315896`](https://github.com/rjdbcm/OZI/commit/7315896021a07f9cac43b003af189d22b31c0df6))


## v0.0.147 (2023-10-06)

### :bug:

* :bug::construction_worker:(tests/ozi_fix.py): Fix flaky CI due to exceeded deadline. ([`ae446ae`](https://github.com/rjdbcm/OZI/commit/ae446aeb5045e54583e27d1bee8f596b713c723e))

* :bug:(ozi/templates/project.PKG-INFO):  Fix template not specifying Python 3 Only.

```
# &lt;OZI-0.0.146&gt;/ozi/fix.py:239: RuntimeWarning
not ok - 8 - &#34;Programming Language :: Python :: 3 :: Only&#34; MISSING
``` ([`9e8b6c0`](https://github.com/rjdbcm/OZI/commit/9e8b6c0d8cfe70973ff094ff1455960dccb7334f))

### :hammer:

* :hammer::white_check_mark:(ozi-fix): Add coverage for Python version PKG-INFO. ([`39422a5`](https://github.com/rjdbcm/OZI/commit/39422a5b4052dae92c1f13c85926c32da08c237a))


## v0.0.146 (2023-10-06)

### :bug:

* :bug::construction_worker:(ozi-fix):  Fix flaky CI.

``tests/ozi_fix.py::test_fuzz_report_missing - hypothesis.errors.Flaky: Hypothesis ``
Unreliable test timings! On an initial run, this test took 359.85ms, which exceeded the deadline of 200.00ms, but on a subsequent run it took 10.32 ms, which did not. Deadline raised for this test by setting deadline=500ms. ([`7356c9a`](https://github.com/rjdbcm/OZI/commit/7356c9a697fc04279733bdeb81dec058e9f40f21))

### :hammer:

* :hammer:(ozi-fix): Coverage complete for pep-639 extra classifiers. ([`6c65619`](https://github.com/rjdbcm/OZI/commit/6c65619597f73bf7a296ccf283f6e3e653a19362))


## v0.0.145 (2023-10-05)

### :hammer:

* :hammer:(ozi-fix): Improved coverage.

Still deferring to good first issue for the extra PKG-INFO parser.
It is likely I will move it to it&#39;s own module as well. ([`a796bd3`](https://github.com/rjdbcm/OZI/commit/a796bd392e30119e2e84d33dcdad0338e6ed2071))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`d604dbc`](https://github.com/rjdbcm/OZI/commit/d604dbc357dc7a69c39ea232d9956ff46cc0cab8))


## v0.0.144 (2023-10-05)

### :hammer:

* :hammer:(ozi-fix): Add Python version checking. ([`f33d754`](https://github.com/rjdbcm/OZI/commit/f33d7542b7577288d9c4cd6e607f9d986bb5fcc9))

* :hammer:(ozi-fix): Added reporting of all PKG-INFO headers present. ([`dee27f7`](https://github.com/rjdbcm/OZI/commit/dee27f7b779d33fa8e75c4c78a4b1dda09938991))


## v0.0.143 (2023-10-04)

### :pushpin:

* :pushpin::pencil2:: Forgot to bump Python for OZI&#39;s distribution. ([`c0e07d4`](https://github.com/rjdbcm/OZI/commit/c0e07d41c8ee1c21d2f7bc395322b493cbb6c7a3))

* :pushpin:: Deprecate Python version 3.9

Add support for Python 3.12 ([`0668309`](https://github.com/rjdbcm/OZI/commit/0668309d7219029fbc0dc483ec39b9cc701076a2))

* :pushpin:: Deprecate Python version 3.9

Add support for Python 3.12 ([`706191e`](https://github.com/rjdbcm/OZI/commit/706191e80fc0ad344a0dbb66ca07b7569b4f5c91))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`eff6b85`](https://github.com/rjdbcm/OZI/commit/eff6b85697cf7c862707493293d8e7cf436da151))


## v0.0.142 (2023-10-04)

### :bug:

* :bug:: 500ms deadline for hypothesis.

Should fix:
Unreliable test timings! On an initial run, this test took 357.72ms, which exceeded the deadline of 200.00ms, but on a subsequent run it took 24.28 ms, which did not. If you expect this sort of variability in your test timings, consider turning deadlines off for this test by setting deadline=None. ([`2005bb3`](https://github.com/rjdbcm/OZI/commit/2005bb30040bc700af9d6fd857f0e69394b747b0))

### :hammer:

* :hammer:: Remove unnecessary references to NOTICE. ([`b146b78`](https://github.com/rjdbcm/OZI/commit/b146b78ee302d5d6d56ea5d1dc8248f7416e2226))

### Other

* :see_no_evil:: Update gitignore template.

Added ignored-by-default patterns for:
* Utility environments
* coverage files
* Byte-compiled / optimized / DLL files
*  C extensions ([`cfdd5d7`](https://github.com/rjdbcm/OZI/commit/cfdd5d72a660e39f923b7574efe107634e3ebc0f))


## v0.0.141 (2023-10-03)

### :bug:

* :bug:(ozi-fix): Correct warning for missing. ([`f474efd`](https://github.com/rjdbcm/OZI/commit/f474efdef3d918a423684614016bc9608612eb24))

* :bug:: Coverage fixed. ([`fe03224`](https://github.com/rjdbcm/OZI/commit/fe03224ebfdac2f99c522eeb58fc944c00abb7fe))

* :bug:: Defer some flaky tests to issues. ([`9f9fbc9`](https://github.com/rjdbcm/OZI/commit/9f9fbc98dd554c47760c6cc32d0fe430cb226a59))

* :bug:: Flaky license test. ([`1c2eba0`](https://github.com/rjdbcm/OZI/commit/1c2eba0806f0d66a5a03df1e00a217ad7ed5de01))

* :bug:: Fix flaky test caused by PEP-639 proposed keys. ([`fee17df`](https://github.com/rjdbcm/OZI/commit/fee17dfd4db81b8a3d87d9f5f4e1412b5fe01ff8))

### :hammer:

* :hammer:(ozi-new): Name test strategy changes.

```python
r&#39;^([A-Za-z]|[A-Za-z][A-Za-z0-9._-]*[A-Za-z0-9])$&#39;
``` ([`9f5d2b8`](https://github.com/rjdbcm/OZI/commit/9f5d2b840834f4b5390ffc732950470494a7756e))

### Other

* :white_check_mark:(ozi-new): Modified test draw strategy for licenses.

We mainly want to test that ``ozi-new project`` does not complain about licenses that we have templates for. ([`d99b144`](https://github.com/rjdbcm/OZI/commit/d99b144af8c975f96a0d034057b78cb9696a6795))

* :white_check_mark:(ozi-new): Coverage improved.

A handful of defer to good-first-issue like ``project.homepage.netloc`` ([`4f0339a`](https://github.com/rjdbcm/OZI/commit/4f0339a2a9a8f80b31eadc78c5ea1b54b08d004b))


## v0.0.140 (2023-10-01)

### :bug:

* :bug:(ozi-fix): Fix ``--missing`` output. ([`36fa838`](https://github.com/rjdbcm/OZI/commit/36fa838b93d36f8ffe41f787b890ed6665981b38))


## v0.0.139 (2023-10-01)

### :hammer:

* :hammer:(ozi-fix): Fix missing pretty print arg. ([`7e5a9bb`](https://github.com/rjdbcm/OZI/commit/7e5a9bb9200eac98e12a762eac3eb815c52dda60))


## v0.0.138 (2023-10-01)

### :hammer:

* :hammer:(ozi-new;ozi-fix): ``ozi-new`` just for project creation.

Decoupled utility functionality. Also corrected some output. ([`99ffe02`](https://github.com/rjdbcm/OZI/commit/99ffe022d802806559568f8da0800db9536141f7))


## v0.0.137 (2023-10-01)

### :bug:

* :bug:(ozi-new): Fix skipping of new item creation. ([`93b1e70`](https://github.com/rjdbcm/OZI/commit/93b1e701d0d3ef7dda817cd8451f80c35a51b625))


## v0.0.136 (2023-10-01)

### :hammer:

* :hammer:: Add check for missing typing arg in PKG-INFO template. ([`bb48d07`](https://github.com/rjdbcm/OZI/commit/bb48d076f073e7029630f2e943d2762eb8a9f7ab))

### Other

* :construction_worker:(PKG-INFO): Bump version. ([`1d3cf17`](https://github.com/rjdbcm/OZI/commit/1d3cf1752b78262d0a5398d9f1e3fcb86709c69b))

* :memo:: Update tempates for documentation. ([`6cb97e7`](https://github.com/rjdbcm/OZI/commit/6cb97e79d1a425e0684b5d45116766bc78fd0c76))


## v0.0.135 (2023-10-01)

### :bug:

* :bug:: Try setting PYTHONPATH to get pytest-cov working. ([`a260409`](https://github.com/rjdbcm/OZI/commit/a2604094b9646ed694ed3c5db6dc3579796e6798))

* :bug:: Get correct dist-packages coverage location. ([`054c900`](https://github.com/rjdbcm/OZI/commit/054c900b81fe8dfc1baa0b29ca207a957d35d35c))

* :bug:: Try to fix coverage path. ([`b710223`](https://github.com/rjdbcm/OZI/commit/b710223e900161e30c4567a4e4c646f701e25c98))

* :bug::pencil2:: Fix option typo. ([`348152d`](https://github.com/rjdbcm/OZI/commit/348152de6dbb61dde68594a13285e0ef08d9a95c))

* :bug:: Install requirements in addition to building clone for pytest. ([`fc79ce3`](https://github.com/rjdbcm/OZI/commit/fc79ce34f660aecf63cf0a85add55c1d5b6bf042))

* :bug:: Install from clone for pytest. ([`9f821b3`](https://github.com/rjdbcm/OZI/commit/9f821b3d4aa27cad2b3d7e8dece17bb997630027))

* :bug:: Correct tests folder path. ([`28f2f93`](https://github.com/rjdbcm/OZI/commit/28f2f936e1ebb0d0cf3a40020f0fedadd9af3e59))

* :bug:: Just do a fresh test suite environment for Pytest. ([`d0efb7c`](https://github.com/rjdbcm/OZI/commit/d0efb7cc582e51a212a52b128c24a2b163e6c086))

* :bug:: Fix call binary pytest not module. ([`35500f2`](https://github.com/rjdbcm/OZI/commit/35500f238010d64b7feee9c8a85f2462819ad88e))

* :bug:: Pytest invocation should be python version specific. ([`72cf38d`](https://github.com/rjdbcm/OZI/commit/72cf38d067b8a49d4f474ab9b6e2c2b885a18a55))

* :hammer::bug:: Fix invocation of Pytest.

It was unclear until this point where pytest would be invoked. Now it is clearly invoked during the CI checkpoint step for ``--setup=test`` only. ([`018f703`](https://github.com/rjdbcm/OZI/commit/018f70316cb5d06b6609b838ca06897c50bf3966))

### Other

* :construction_worker:: Bump PKG-INFO. ([`1dddfd7`](https://github.com/rjdbcm/OZI/commit/1dddfd72a43b343aef91b8c18f337569527a5652))

* :construction_worker:: Bump for sigstore 2.0. ([`668c389`](https://github.com/rjdbcm/OZI/commit/668c389e2d3719084167150f9e31d803eeb1249a))

* :construction_worker:: Add builtin pytest invocation. ([`88b335e`](https://github.com/rjdbcm/OZI/commit/88b335e78aa3506ddae56eb72aee5a745c618240))


## v0.0.134 (2023-10-01)

### :hammer:

* :hammer::white_check_mark:: Add a test suite.

Most nearly 100% coverage. ([`68e6dbb`](https://github.com/rjdbcm/OZI/commit/68e6dbbf6355afdf092978bc6a1a0ed6ee1fb271))

### Other

* Add basetemp for testing. ([`d92fa25`](https://github.com/rjdbcm/OZI/commit/d92fa2503dc205a664afdf25892ab2bc37cb5786))


## v0.0.133 (2023-09-28)

### :hammer:

* :hammer::test_tube:(ozi-fix,ozi-new): Add the beginning of our test suite.

Hypothesis test writing must be done from a release so failing tests are using
```
# pragma: no cover
```
This also fixes some minor UX bugs:
* Missing ``ozi-new --list`` keys
* Incorrect names ([`748b730`](https://github.com/rjdbcm/OZI/commit/748b730f393f4b7facc8060a2745dc0f31a8f638))


## v0.0.132 (2023-09-27)

### :pencil2:

* :pencil2:(ozi-fix): Remove unnecessary print statement. ([`20d509f`](https://github.com/rjdbcm/OZI/commit/20d509ff8ebbf94f03b3d67f4038bb4c1d39c943))


## v0.0.131 (2023-09-27)

### :bug:

* :bug:(ozi-fix): Fix RewriteCommand.

TypeError: Object of type RewriteCommand is not JSON serializable ([`a9344cd`](https://github.com/rjdbcm/OZI/commit/a9344cd69fcfc3671ecff8278213aaacaadfc6fb))


## v0.0.130 (2023-09-26)

### :bug:

* :bug:(ozi-fix): Fix namespace.

```
File &#34;&lt;OZI-0.0.129&gt;/ozi/fix.py&#34;, line 435, in main
File &#34;&lt;OZI-0.0.129&gt;/ozi/fix.py&#34;, line 427, in preprocess
TypeError: unhashable type: &#39;list&#39;
``` ([`5ec84bb`](https://github.com/rjdbcm/OZI/commit/5ec84bb1c4640fd3d98ba70f5f412f52452c961e))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`7254cd6`](https://github.com/rjdbcm/OZI/commit/7254cd6e9a3894c7a4c90993be881fce32d4ad91))


## v0.0.129 (2023-09-26)

### :bug:

* :bug:(ozi-fix): Fix missing args.

&#39;Namespace&#39; object has no attribute &#39;add&#39; ([`17e1d79`](https://github.com/rjdbcm/OZI/commit/17e1d794dc17a0bfb90ca4e98d7775daae1dd8d2))


## v0.0.128 (2023-09-26)

### :hammer:

* :hammer:(ozi-fix): major refactoring.

Add Rewriter class. ([`8410fcc`](https://github.com/rjdbcm/OZI/commit/8410fcc93cf507f31071abead6c7dc6504d2b4c0))

### Other

* :memo:: Add security policy. ([`ba1b1ba`](https://github.com/rjdbcm/OZI/commit/ba1b1bab2f6f4a052282a37bf5cc262e9b17a63d))


## v0.0.127 (2023-09-24)

### :children_crossing:

* :children_crossing:: Drop run of blastpipe for now.

I do plan to implement a test suite but blastpipe&#39;s invocation from OZI during continuous integration is currently suffering from broken arguments. ([`2461151`](https://github.com/rjdbcm/OZI/commit/24611518eb2fb656698532248b80c9eee3edce0d))


## v0.0.126 (2023-09-24)

### :bug:

* :bug:(ozi-fix):  &#39;Namespace&#39; object has no attribute &#39;strict&#39; ([`f7bbdaf`](https://github.com/rjdbcm/OZI/commit/f7bbdafb132be919311458487fe2834612dedc42))


## v0.0.125 (2023-09-24)

### :bug:

* :bug:(ozi-fix): Fix &#39;Namespace&#39; object has no attribute &#39;add&#39;. ([`af35c7e`](https://github.com/rjdbcm/OZI/commit/af35c7e5f8e4322a9e26b54e712540b16946db0c))


## v0.0.124 (2023-09-23)

### :bug:

* :bug:(ozi-fix): Add missing new_child template. ([`4f406ad`](https://github.com/rjdbcm/OZI/commit/4f406adc6c94fae5dddd8da59e52d04695d05772))

### Other

* :memo:(PKG-INFO): Bump version. ([`fca526b`](https://github.com/rjdbcm/OZI/commit/fca526b6aa5b59dad27b8a47c89d02e1e9f5d3e6))


## v0.0.123 (2023-09-23)

### :bug:

* :bug:(ozi-fix): proper detection of target paths. ([`09806e0`](https://github.com/rjdbcm/OZI/commit/09806e07386d7c12a40e5e6d409e8a58624f9fd4))


## v0.0.122 (2023-09-23)

### :bug:

* :bug:(ozi-fix): Fix &#39;Namespace has no attribute missing&#39;. ([`238ba81`](https://github.com/rjdbcm/OZI/commit/238ba81c18f0ad81c6b6f266639984ce8c7c5500))


## v0.0.121 (2023-09-23)

### :children_crossing:

* :children_crossing:(ozi-fix): Changed ``missing`` from a flag to a subparser. ([`526665d`](https://github.com/rjdbcm/OZI/commit/526665de9049dd4b5e897c7e509dfe7cc42f503c))

### Other

* :memo:(PKG-INFO): Bump version. ([`18c112a`](https://github.com/rjdbcm/OZI/commit/18c112ac9cb4f80851bf2fcdea5480319239c1b0))


## v0.0.120 (2023-09-23)

### :bug:

* :bug:(ozi-fix): Fix dictionary cast of RewriteCommand.

Using dataclasses.asdict(). ([`32fad26`](https://github.com/rjdbcm/OZI/commit/32fad263589ef9555f3f03fccb0ca147295e7a8d))


## v0.0.119 (2023-09-23)

### :bug:

* :bug:(ozi-fix): Fix mutable default in dataclass. ([`198bf28`](https://github.com/rjdbcm/OZI/commit/198bf287cc7f9723ce66d767d78714b54a7e6d0e))

### Other

* :memo:(PKG-INFO): Bump version. ([`ed08b45`](https://github.com/rjdbcm/OZI/commit/ed08b45eb9e3aa9b76fdd659233dff5c33fb5cff))


## v0.0.118 (2023-09-23)

### :bug:

* :bug:(ozi-fix): Fix RewriteCommand repr to dict. ([`a1dfcbb`](https://github.com/rjdbcm/OZI/commit/a1dfcbb6ef5144c5ee57ad0aa6aaf7b5c766e33c))

* :bug:(ozi-fix): Fix incorrect annotation of self. ([`d3417ae`](https://github.com/rjdbcm/OZI/commit/d3417ae6ad60d9e87e26cb7b246c225b79537a22))


## v0.0.117 (2023-09-23)

### :hammer:

* :hammer:: Improved ``ozi-fix`` implementation. ([`c4b2cf4`](https://github.com/rjdbcm/OZI/commit/c4b2cf48baf0dfd361e7729a44fb033b55f94b2f))


## v0.0.116 (2023-09-19)

### :children_crossing:

* :children_crossing:: ``ozi-fix`` arg order matches ``ozi-new`` ([`c776a0e`](https://github.com/rjdbcm/OZI/commit/c776a0e33a45adcec3fb6e351e62b8e206497c17))


## v0.0.115 (2023-09-19)

### :pencil2:

* :pencil2:: Fix copyright head between different subparsers. ([`d86bedd`](https://github.com/rjdbcm/OZI/commit/d86beddb487df36cf5ecb4bef2291846938aaac2))

* :pencil2:: Correct test count print for ``ozi-new``. ([`80eeda5`](https://github.com/rjdbcm/OZI/commit/80eeda53990dda6f7c775bda14822f5071b9a7b0))


## v0.0.114 (2023-09-18)

### :children_crossing:

* :children_crossing:: Update list functionality. ([`c681cd1`](https://github.com/rjdbcm/OZI/commit/c681cd132758cfe530b1e24791531e3d5ef97e12))


## v0.0.113 (2023-09-18)

### :pencil2:

* :pencil2:: Warning format.

Show name of Warning.
Also run isort and blacken. ([`16c948d`](https://github.com/rjdbcm/OZI/commit/16c948d48ca041e952a50c52d7b876149bd955f1))


## v0.0.112 (2023-09-18)

### :pencil2:

* :pencil2: Fix TAP output newlines. ([`cb37731`](https://github.com/rjdbcm/OZI/commit/cb377310ebb6fe75493ed83766cb58db5f21a41a))


## v0.0.111 (2023-09-18)

### :hammer:

* :hammer:: Update ``ozi-new``.

Should use TAP output throughout now. ([`1cf2cee`](https://github.com/rjdbcm/OZI/commit/1cf2cee123be53551d6b377069492be0dee13e22))


## v0.0.110 (2023-09-18)

### :ambulance:

* :ambulance::pencil2:: Fix incorrect importlib.metadata import. ([`c0cf9b9`](https://github.com/rjdbcm/OZI/commit/c0cf9b9d0ccb8cf1f258c2f4f2d396969c434789))


## v0.0.109 (2023-09-17)

### :hammer:

* :hammer:: FIX ``ozi-fix``.

```
File &#34;&lt;OZI-0.0.108&gt;/ozi/fix.py&#34;, line 250, in main
AttributeError: &#39;str&#39; object has no attribute &#39;is_dir&#39;
``` ([`8721bb0`](https://github.com/rjdbcm/OZI/commit/8721bb0235f12633352cb2afe705352c942f8323))


## v0.0.108 (2023-09-17)

### :ambulance:

* :ambulance:: FIX ``ozi-fix``

```
File &#34;&lt;OZI-0.0.107&gt;/ozi/fix.py&#34;, line 244, in main
AttributeError: &#39;Namespace&#39; object has no attribute &#39;name&#39;
``` ([`1368035`](https://github.com/rjdbcm/OZI/commit/13680352ef22520d748eab5a4a9966e63b65b2cc))

### :children_crossing:

* :pencil2::children_crossing:: Fix NoReturn annotation. ([`f5299ac`](https://github.com/rjdbcm/OZI/commit/f5299ace198182fc010ad0fd1ab42c0437daabdd))

* :children_crossing:: Add OZI_SPEC version variable. ([`4188f2d`](https://github.com/rjdbcm/OZI/commit/4188f2d529846ed97fa315761fca582040f5a677))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`fe4bf98`](https://github.com/rjdbcm/OZI/commit/fe4bf98ccedbb0c10c0ed2ac173a76f44a42a5b6))

* :memo:: Update template header. ([`f1c0f7d`](https://github.com/rjdbcm/OZI/commit/f1c0f7de109be93205affe7475f0d9f7ea5ce0dd))


## v0.0.107 (2023-09-17)

### :pencil2:

* :pencil2:: Fix README whitespace finally, hopefully. ([`4b7a27a`](https://github.com/rjdbcm/OZI/commit/4b7a27ad7b665b4be21c0174040293b93f634b3c))


## v0.0.106 (2023-09-17)

### :ambulance:

* :ambulance:: Fix incorrect OZI PKG-INFO extras. ([`ecdc241`](https://github.com/rjdbcm/OZI/commit/ecdc2419c6fdc14a9de4cd07c2f4774d0119bdfe))

### :pencil2:

* :pencil2: fix template README.rst whitespace. ([`014b862`](https://github.com/rjdbcm/OZI/commit/014b86228705ad15ffc2747ebee17649a48518dd))

* :pencil2: Fix incorrect TAP test count. ([`23a7efc`](https://github.com/rjdbcm/OZI/commit/23a7efc59cfd9ec2eb0be75fd20f319be05c09fa))

### Other

* :memo:: Bump PKG-INFO. ([`a4f6d59`](https://github.com/rjdbcm/OZI/commit/a4f6d59ea6501fcb0ab83bdfd625d59939754e91))


## v0.0.105 (2023-09-16)

### :ambulance:

* :ambulance:: Fix incorrect remote file checksumming. ([`99a3ea0`](https://github.com/rjdbcm/OZI/commit/99a3ea078e992c4fda660b19dbef5a84ae3ef39d))


## v0.0.104 (2023-09-16)

### :hammer:

* :hammer:: Use a streaming request to generate hashes for wrapfile. ([`e27546d`](https://github.com/rjdbcm/OZI/commit/e27546d17183ab85e5e8af9bd6416cac01328594))

### :pencil2:

* :pencil2:: Fix file permissions. ([`a6d033a`](https://github.com/rjdbcm/OZI/commit/a6d033afc8edb60477d9f9d7aa8e6f9e4b6575bc))

### Other

* :heavy_plus_sign:: Add ``requests`` to dependencies. ([`5e65e34`](https://github.com/rjdbcm/OZI/commit/5e65e340617f04e4b16985c6218edfa51f2a3056))


## v0.0.103 (2023-09-16)

### :ambulance:

* :ambulance:: Fix ozi.wrap hash url. ([`68af9f6`](https://github.com/rjdbcm/OZI/commit/68af9f6f856b81e63e51ab57b3a9b0c843873364))


## v0.0.102 (2023-09-16)

### :children_crossing:

* :hammer::children_crossing:: Generate sha256sum for wrapfile. ([`c9f8fd0`](https://github.com/rjdbcm/OZI/commit/c9f8fd0b6b9cc4228747fc6bcce95bc88c41727b))


## v0.0.101 (2023-09-16)

### :pencil2:

* :pencil2:: Fix variable reference in ``ozi.wrap.j2`` ([`3d7ffa1`](https://github.com/rjdbcm/OZI/commit/3d7ffa1774a8e9f0113cddd1e2df5d4f098c040a))


## v0.0.100 (2023-09-16)

### :ambulance:

* :ambulance:: Fix missing ozi.wrap template. ([`2aff6fd`](https://github.com/rjdbcm/OZI/commit/2aff6fd7f6955d07de6563b3c88cbbc8e71dcfee))

### :pencil2:

* :pencil2:: Fix wrapfile template filename. ([`46d1bd0`](https://github.com/rjdbcm/OZI/commit/46d1bd0709235417358294a1d103724b93396959))


## v0.0.99 (2023-09-16)

### :hammer:

* :hammer:: Update only need copyright_head for source generation. ([`174c1ac`](https://github.com/rjdbcm/OZI/commit/174c1acb3bad3392c0f467970b12f51f871b6ea7))


## v0.0.98 (2023-09-16)

### :pencil2:

* :pencil2:: Fix more whitespace. ([`dc2eb53`](https://github.com/rjdbcm/OZI/commit/dc2eb53d19012fa52e88725b5ebba2ff3e7a4385))

* :pencil2:: Fix missing whitespace in template. ([`58bc4f4`](https://github.com/rjdbcm/OZI/commit/58bc4f47b20c45921bdecd5e9a0138271bb82b17))

* :pencil2:: Move strict warning filter into ``ozi-new`` into project block. ([`b70ae67`](https://github.com/rjdbcm/OZI/commit/b70ae671c0211c59dde745bfe40cd98329cd4c31))


## v0.0.97 (2023-09-16)

### :children_crossing:

* :children_crossing:: add ozi.wrap creation tool. ([`64700a6`](https://github.com/rjdbcm/OZI/commit/64700a667c82eabf322f40e2986e4a370967293b))

### Other

* Updated disclaimers. ([`78f1bd0`](https://github.com/rjdbcm/OZI/commit/78f1bd09dd2152d893b3b5595a4d27b3bfed8ae2))


## v0.0.96 (2023-09-16)

### :children_crossing:

* :children_crossing:: Add ``pip-tools`` to ``pyproject.toml`` template. ([`b6346a2`](https://github.com/rjdbcm/OZI/commit/b6346a2208ef24c1cba5cc9cc07dfc73d1dddb3e))

### :hammer:

* :hammer:: Add missing ``--license-file`` arg to ``ozi-new p``. ([`ff64224`](https://github.com/rjdbcm/OZI/commit/ff64224372600ef452468c6564789956a09a5dd6))

* :hammer:: Add pip-tools to tox template. ([`5838fb7`](https://github.com/rjdbcm/OZI/commit/5838fb7d7aafd4e63bab241a7f427c08443af606))

### :pencil2:

* :pencil2:: Remove uneeded NOTICE header. ([`062e116`](https://github.com/rjdbcm/OZI/commit/062e1162152cc22f347639766a652b60e9ffecd0))


## v0.0.95 (2023-09-16)

### :ambulance:

* :ambulance:: Fix LICENSE.txt template lookup. ([`58ce5ee`](https://github.com/rjdbcm/OZI/commit/58ce5ee509bbeada0b0ad87f4b9e27530ef81c80))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`c491dbc`](https://github.com/rjdbcm/OZI/commit/c491dbc50eb716084c9d4354891ead05b951edc6))


## v0.0.94 (2023-09-16)

### :ambulance:

* :ambulance:: Fix missing pip-compile in tox. ([`d8dbfff`](https://github.com/rjdbcm/OZI/commit/d8dbfff7fc22d6ef25455a97c50c936ad2da072f))

### :children_crossing:

* :children_crossing: Restructure dependencies around pip-tools. ([`9c21588`](https://github.com/rjdbcm/OZI/commit/9c21588db1935d7c70a2f071a9d5d6b2fe8faef6))


## v0.0.93 (2023-09-15)

### :ambulance:

* :ambulance: Fix mismatched PKG-INFO. ([`3c4fd77`](https://github.com/rjdbcm/OZI/commit/3c4fd773c167041fe95cb476fa7b700d8bda20e9))

### :children_crossing:

* :memo::children_crossing:: Update README license info. ([`04811c2`](https://github.com/rjdbcm/OZI/commit/04811c2e03584c387e5a54a4cdc50e97fee24760))

### :hammer:

* :hammer:: Improved strict mode using warning filters.

Also improved license disambiguation for PEP 639 preparedness. ([`7774b02`](https://github.com/rjdbcm/OZI/commit/7774b02043fdf633ce6e5e542cd1c5324df8cc95))

* :hammer:: Add report_missing TAP fixture and SPDX expression parser. ([`4902150`](https://github.com/rjdbcm/OZI/commit/490215052385f676e216dd67b940c2a9748765c5))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`acd0eb8`](https://github.com/rjdbcm/OZI/commit/acd0eb8e545e9822b7351a54acac27e1c9084ead))

* :memo: Update licensing header format.

Loosely follows the style of LLVM. ([`f80f7eb`](https://github.com/rjdbcm/OZI/commit/f80f7eba7fb862db443494c2e01869424afdbd31))


## v0.0.92 (2023-09-14)

### :children_crossing:

* :children_crossing:: Add OZI PKG-DATA payload preamble.

PEP-639 keys:
* License-Expression
* License-File ([`19d194c`](https://github.com/rjdbcm/OZI/commit/19d194c00d861adfc23f495a6ee05a809b5d4a8a))

### Other

* :page_facing_up: Relicense codebase to LLVM-exception.

This adds the following to ``LICENSE.txt``:
---- LLVM Exceptions to the Apache 2.0 License ----

As an exception, if, as a result of your compiling your source code, portions
of this Software are embedded into an Object form of such source code, you
may redistribute such embedded portions in such Object form without complying
with the conditions of Sections 4(a), 4(b) and 4(d) of the License.

In addition, if you combine or link compiled forms of this Software with
software that is licensed under the GPLv2 (&#34;Combined Software&#34;) and if a
court of competent jurisdiction determines that the patent provision (Section
3), the indemnity provision (Section 9) or other Section of the License
conflicts with the conditions of the GPLv2, you may retroactively and
prospectively choose to deem waived or otherwise exclude such Section(s) of
the License, but only in their entirety and only with respect to the Combined
Software. ([`0ede284`](https://github.com/rjdbcm/OZI/commit/0ede284551bee0a6c6f17c0ecd27d9d43cfd2be0))


## v0.0.91 (2023-09-12)

### :bug:

* :bug:: Fix ``ozi-new`` source and test report_missing. ([`0ad2897`](https://github.com/rjdbcm/OZI/commit/0ad2897b65593c5442171c2ed793bd821925e00c))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`49c8b0d`](https://github.com/rjdbcm/OZI/commit/49c8b0d3c57cc5392402b7995400ed5ce4100e8f))


## v0.0.90 (2023-09-12)

### :children_crossing:

* :children_crossing::construction_worker:: Add OZI spec version to workflow templates for docs. ([`de50238`](https://github.com/rjdbcm/OZI/commit/de50238a74107c12043479bc4a702a96326185b0))

* :children_crossing:: Add OZI spec version comments for Documentation.

Also fixes missing [tool.setuptools_scm]. ([`faf6ddb`](https://github.com/rjdbcm/OZI/commit/faf6ddb0c397a1b1105d2594fb93c5d64398b5bd))

### :hammer:

* :hammer::pencil2:: new_module.py.j2 added to install. ([`39ac634`](https://github.com/rjdbcm/OZI/commit/39ac6342a2f9b9141f3f21451a2179957bd125d7))

* :hammer:: Source and test creation with ``ozi-new``. ([`55071ba`](https://github.com/rjdbcm/OZI/commit/55071bac9509ecfe5513881282aba0317dab076c))

* :hammer:: Add py.typed to source_templates. ([`0b2e730`](https://github.com/rjdbcm/OZI/commit/0b2e730d708cf872eb8c508f6a0e9c9f1dba1c82))


## v0.0.89 (2023-09-11)

### :hammer:

* :hammer:: Add strict flag to ``ozi-new project`` and ``ozi-fix``. ([`3f8c4db`](https://github.com/rjdbcm/OZI/commit/3f8c4db094cad91c3dfdbcce7594720c63c6b0bd))


## v0.0.88 (2023-09-11)

### :pencil2:

* :pencil2:: Fix jinja2 include directive. ([`43101e3`](https://github.com/rjdbcm/OZI/commit/43101e3a07d5838b2fd27e5b195669ebf5498732))


## v0.0.87 (2023-09-11)

### :children_crossing:

* :children_crossing: Add ``ozi.spec`` versioned header for meson templates. ([`fa27b03`](https://github.com/rjdbcm/OZI/commit/fa27b031f34b127e4a0bf3ff8e6b8bcb2bfff21a))


## v0.0.86 (2023-09-11)

### :bug:

* :bug:: Fix comment and loop whitespace trimming. ([`5c5040e`](https://github.com/rjdbcm/OZI/commit/5c5040eb1581a02e40620157b8263f871221eeaf))


## v0.0.85 (2023-09-11)

### :bug:

* :lipstick::bug:: Fix meson file header whitespace. ([`d07be48`](https://github.com/rjdbcm/OZI/commit/d07be4845bc4f83519566878367f014cc0a10319))

* :bug:: Fix PKG-INFO whitespace. ([`2ee8841`](https://github.com/rjdbcm/OZI/commit/2ee88414351a0a13e84271a00e9409cee0073fd8))


## v0.0.84 (2023-09-11)

### :bug:

* :bug:: Default topic should be a List[str]. ([`8ab11e6`](https://github.com/rjdbcm/OZI/commit/8ab11e65837720ea8c42e5cd900908887f556083))

* :bug:: Fix PKG-INFO whitespace. ([`eabd4cc`](https://github.com/rjdbcm/OZI/commit/eabd4cccdc594df90e818b48fb9f2c03b50a8496))

### Other

* :lipstick:: Fix jinja header comment rendering. ([`b5db826`](https://github.com/rjdbcm/OZI/commit/b5db826e3f56a9c17ecd906e8bc32fc2edfc500e))


## v0.0.83 (2023-09-11)

### :bug:

* :bug::pencil2:: Fix another unescaped false positive for Jinja2. ([`076cdbb`](https://github.com/rjdbcm/OZI/commit/076cdbb2ae6e43c92bfdb65f1c16e29c0555d5bb))


## v0.0.82 (2023-09-11)

### :bug:

* :bug::pencil2:: Fix template paths. ([`84363da`](https://github.com/rjdbcm/OZI/commit/84363da70e038896f02d416cd6434e5dd3f2e0b9))


## v0.0.81 (2023-09-11)

### :bug:

* :bug:: Fix unescaped jinja directive false positive. ([`2e074be`](https://github.com/rjdbcm/OZI/commit/2e074beba320179d14166e6bc9c92600b0772e62))


## v0.0.80 (2023-09-11)

### :bug:

* :bug:: Fix missing github templates. ([`78068f8`](https://github.com/rjdbcm/OZI/commit/78068f8ab5e44eeaa460d30825e5073576562061))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`0829a90`](https://github.com/rjdbcm/OZI/commit/0829a9071f73184b482417d5b1e760c8a9976eff))


## v0.0.79 (2023-09-10)

### :bug:

* :bug:: Fix missing ci workflow and test builf files. ([`0ff5d3b`](https://github.com/rjdbcm/OZI/commit/0ff5d3b2fcb0331bed338aee65f7e1d0e8bc4fc0))

* :bug:: Fix whitespace in templates. ([`d345443`](https://github.com/rjdbcm/OZI/commit/d34544374af83f0b3bc5a44ded71548d09fddbd2))


## v0.0.78 (2023-09-10)

### :bug:

* :bug:: Fix comment newlines. ([`ae54609`](https://github.com/rjdbcm/OZI/commit/ae5460982405889eac5074c6b2148b6efa2b1176))

### :children_crossing:

* :children_crossing:: Allow multiple topic classifiers. ([`4b8ef90`](https://github.com/rjdbcm/OZI/commit/4b8ef9014593c36f6aa44cf10093d59c58abfd1e))

### :hammer:

* :hammer:: add ci_provider_templates and test_templates. ([`5518bb8`](https://github.com/rjdbcm/OZI/commit/5518bb8233781682114b662e43f2a8812a75e558))


## v0.0.77 (2023-09-10)

### :bug:

* :bug:: Fix template path for tests. Fix template line trimming. ([`04ea00b`](https://github.com/rjdbcm/OZI/commit/04ea00bba9525986a0ad81c5592d2eb0692a7ae3))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`44ce220`](https://github.com/rjdbcm/OZI/commit/44ce2204f61ab92a8178aa6a10246cb2ef422d5d))


## v0.0.76 (2023-09-10)

### :bug:

* :bug:: Fix untrimmed whitespace in ``ozi-new project`` output. ([`60e0d10`](https://github.com/rjdbcm/OZI/commit/60e0d1074cbc970cecb15ace97d6c974a83d0de1))


## v0.0.75 (2023-09-10)

### :bug:

* :hammer::bug:: Fix source subdirectory naming. ([`74f7b7e`](https://github.com/rjdbcm/OZI/commit/74f7b7e46d7fba18f5fb65f74cfe756f39c15bd8))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`2309d7b`](https://github.com/rjdbcm/OZI/commit/2309d7ba2111766249164e7b0b0cb11fd6312029))


## v0.0.74 (2023-09-10)

### :bug:

* :bug:: Fix wrong subdir install location for OSI Approved licenses. ([`64d547b`](https://github.com/rjdbcm/OZI/commit/64d547bb3d4c18ec4a6b523bb16215e7a50f551a))


## v0.0.73 (2023-09-10)

### :bug:

* :bug::pencil2:: Fix trim filter should be map(&#39;trim&#39;) ([`a2a2099`](https://github.com/rjdbcm/OZI/commit/a2a2099a6c2a1ead538d905100e78001fef5a35d))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`215ae0e`](https://github.com/rjdbcm/OZI/commit/215ae0e16db795bc39612bf1bbe5d9882cb6127a))


## v0.0.72 (2023-09-10)

### :bug:

* :bug:: Fix: trim whitespace from template includes. ([`09e54dd`](https://github.com/rjdbcm/OZI/commit/09e54dd41fda430ca7edf5d1b8093939d1a2e864))


## v0.0.71 (2023-09-10)

### :pencil2:

* :pencil2:: Fix include of project.PKG-INFO. ([`332d1c1`](https://github.com/rjdbcm/OZI/commit/332d1c1b3f7ee8f431bd059476bbb426d8489c7c))


## v0.0.70 (2023-09-10)

### :pencil2:

* :pencil2:: Fix unquoted template include path. ([`3fe0d91`](https://github.com/rjdbcm/OZI/commit/3fe0d91c0a0d748cc67d716d84eaf088b0f843ab))


## v0.0.69 (2023-09-10)

### :bug:

* :bug:: Fix missing resource pyright.pyproject.toml. ([`e9f2363`](https://github.com/rjdbcm/OZI/commit/e9f236386f2f431ea8906ad478d50e0a6d3199f1))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`65fe0a7`](https://github.com/rjdbcm/OZI/commit/65fe0a75343bc2c08be310739fbf10fb90d6bdc4))


## v0.0.68 (2023-09-09)

### :bug:

* :bug:: FIX: Add missing pyright pyproject.toml template. ([`dc1b22f`](https://github.com/rjdbcm/OZI/commit/dc1b22fcdd17a657eaa6e1ddc4e16c9c95fad648))


## v0.0.67 (2023-09-09)

### :pencil2:

* :pencil2:: Fix template typo. ([`291bdf8`](https://github.com/rjdbcm/OZI/commit/291bdf889b333af2a20b8ebe2a9c0acfc073b735))


## v0.0.66 (2023-09-09)

### :bug:

* :bug::hammer:: Fix incorrect use of split function. ([`b6362b4`](https://github.com/rjdbcm/OZI/commit/b6362b454858aeb04dc2930a5c06a42088c6bc3a))


## v0.0.65 (2023-09-09)

### :bug:

* :hammer::bug:: Add split filter to template globals. ([`935c1a2`](https://github.com/rjdbcm/OZI/commit/935c1a25dad5e2502a5f25203f888e2431f82d14))


## v0.0.64 (2023-09-09)

### :bug:

* :bug::hammer:: Unite default Jinja Namespace with ours. ([`7b0d394`](https://github.com/rjdbcm/OZI/commit/7b0d394161e1f6d2eaa3d7ce30689c03cc9e04ad))


## v0.0.63 (2023-09-09)

### :bug:

* :bug:: Fix for loop over numeric range in Jinja templates. ([`940efbb`](https://github.com/rjdbcm/OZI/commit/940efbbf0464bca6fd8c60e92304e3e39ea06c78))


## v0.0.62 (2023-09-09)

### :bug:

* :hammer::bug:: Fix improper filter invocation in Jinja templates. ([`df1fe8d`](https://github.com/rjdbcm/OZI/commit/df1fe8d56f272599941de823272eeab725d9800f))


## v0.0.61 (2023-09-09)

### :hammer:

* :hammer:: ``ozi-new`` exit(1) for non-empty directory. ([`091d88e`](https://github.com/rjdbcm/OZI/commit/091d88e88ce62a35b5597eee21cc6355010f7518))

* :hammer::truck:: Move templates. ([`199bea2`](https://github.com/rjdbcm/OZI/commit/199bea2f339c98a648cb44878a0e9dfe5f1ad691))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`301e338`](https://github.com/rjdbcm/OZI/commit/301e3382cd3c69478ea76c3a60940b842c5c4f48))


## v0.0.60 (2023-09-09)

### :ambulance:

* :ambulance:: Fix Jinja includes to use a quoted string. ([`a675068`](https://github.com/rjdbcm/OZI/commit/a675068ae2dc1d985613fcfb87d2e2f7f999ba22))


## v0.0.59 (2023-09-09)

### :ambulance:

* :ambulance:: FIX: Ensure that templates are loaded properly. ([`537e2c1`](https://github.com/rjdbcm/OZI/commit/537e2c1f0f3f67267fd0fd2de502c6fa476d05c7))


## v0.0.58 (2023-09-09)

### :hammer:

* :hammer::pencil2:: Fix uneeded call to geturl(). ([`a0d6f35`](https://github.com/rjdbcm/OZI/commit/a0d6f3597740ecac4d8fd48a87cee3c4097a6f3e))


## v0.0.57 (2023-09-09)

### :hammer:

* :pencil2::hammer:: Fix geturl() call. ([`b9a770a`](https://github.com/rjdbcm/OZI/commit/b9a770af4c2c4af2812699ca4ea293fccd649956))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`3c755c8`](https://github.com/rjdbcm/OZI/commit/3c755c828d0ab741e7d552002f7960ff65c81c65))


## v0.0.56 (2023-09-09)

### :hammer:

* :hammer::pencil2:: Fix minor typo and bump the PKG-INFO. ([`165730b`](https://github.com/rjdbcm/OZI/commit/165730b5aeb4ce27be834a1a7801c23ffc4e31ad))


## v0.0.55 (2023-09-09)

### :ambulance:

* :hammer::ambulance:: Fix ``ozi-new`` bug that caused early exit. ([`f56f93b`](https://github.com/rjdbcm/OZI/commit/f56f93be9096e837fa2c3fdf9498f6bbb0f16f49))


## v0.0.54 (2023-09-08)

### :children_crossing:

* :hammer::children_crossing:: Update templates - add test and module templates. ([`3ab9892`](https://github.com/rjdbcm/OZI/commit/3ab9892b160a6f163bb9d5741b7cf7944f59e589))

### :hammer:

* :hammer:: Added LICENSE.txt template and license selection disambiguation. ([`f4e52d0`](https://github.com/rjdbcm/OZI/commit/f4e52d01a8164a5384f655529657eee69f4d461b))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`ca661f2`](https://github.com/rjdbcm/OZI/commit/ca661f2fbbf6be4335d457deebe7f3ae625e33e4))


## v0.0.53 (2023-09-06)

### :ambulance:

* :ambulance:: Fix entrypoint version arg. ([`e098e8c`](https://github.com/rjdbcm/OZI/commit/e098e8c43e8fbf07d5e76b8ac851ac4175903c27))


## v0.0.52 (2023-09-06)

### :children_crossing:

* :children_crossing::memo:: Update Topics and Clarify Python 3 Only. ([`cfbabcf`](https://github.com/rjdbcm/OZI/commit/cfbabcf008d7ec3d8e32b0e54c073d99c4147475))

* :children_crossing:: Improve help string for main script. ([`716085b`](https://github.com/rjdbcm/OZI/commit/716085b6a7c6ae94f2b10926dbba95d0f38c4613))

### :hammer:

* :hammer:: Improve main entrypoint help.

Also made ``--version`` work. ([`d804b32`](https://github.com/rjdbcm/OZI/commit/d804b320d7d074f9085b8b31631c2f614b8695c0))


## v0.0.51 (2023-09-05)

### :bento:

* :memo::bento:: Update readme for clarity. ([`172c1b5`](https://github.com/rjdbcm/OZI/commit/172c1b532613e41006a859a4b44e6aec90cc45c1))

### Other

* :memo:: Resychronize README.rst. ([`8a57e39`](https://github.com/rjdbcm/OZI/commit/8a57e3906f5456e8180ff0c7a01eeb0ee5beacf3))


## v0.0.50 (2023-09-05)

### :ambulance:

* :hammer::ambulance:: Fixed ``ozi/new.py`` PKG-INFO. |

Also added environment, framework, language and typing to PKG-INFO. ([`5e53d4d`](https://github.com/rjdbcm/OZI/commit/5e53d4dfa77dec79185cf2439728fce378f6a421))

### :hammer:

* :hammer:: Add ``--audience`` to ``ozi/new.py``.

Also fixed PKG-INFO template. ([`d9bf177`](https://github.com/rjdbcm/OZI/commit/d9bf177d22215b20356ba9ac7c7c34958cb3638a))

### :pencil2:

* :pencil2:: Remove ``__init__.pyi``from meson.build. ([`5e5e583`](https://github.com/rjdbcm/OZI/commit/5e5e583cdf323c6b1913e7d6a73311e928bcf9fb))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`35a07e2`](https://github.com/rjdbcm/OZI/commit/35a07e2006913f89d5de6323c9664e12aac1ceb2))


## v0.0.49 (2023-09-05)

### :hammer:

* :hammer:: Fix ``ozi-fix`` crash if PKG-INFO is missing. ([`79048c0`](https://github.com/rjdbcm/OZI/commit/79048c0da7af5eed72ceb595177b9078173af18d))

### Other

* :art:: Blacken and isort ``ozi/new.py``. ([`e1fabc6`](https://github.com/rjdbcm/OZI/commit/e1fabc6a6658d3536185dbb71911c93d0b5dddd9))

* :art: Add E203 to Flake8 ignore to allow for black slice style. ([`e11fef2`](https://github.com/rjdbcm/OZI/commit/e11fef2581a804bd090273e266ad24c1a571c0bc))


## v0.0.48 (2023-09-05)

### :ambulance:

* :ambulance::construction_worker:: Fix wheel versions. Was building all on 3.11. ([`0ccfa1e`](https://github.com/rjdbcm/OZI/commit/0ccfa1e2f6c2aaa6198b5d0152031f1e61ccb4fd))


## v0.0.47 (2023-09-05)

### :ambulance:

* :ambulance:: Fix release workflow. ([`476246b`](https://github.com/rjdbcm/OZI/commit/476246be55082d821669a00ffac2c9494ebf9313))

* :ambulance:: Fix release trigger checks. ([`7ac2795`](https://github.com/rjdbcm/OZI/commit/7ac2795555b353082b6c3d9fb7585935414781b9))

* :ambulance:: Fix CI Build. ([`0abe8b4`](https://github.com/rjdbcm/OZI/commit/0abe8b46ef6b80b418edcafbfa8c9220b1ef34de))

* :ambulance::construction_worker:: Fix release step outputs. ([`50c8a94`](https://github.com/rjdbcm/OZI/commit/50c8a943df4650a2ae6b63366b6f470a8d8f66c8))

* :construction_worker::ambulance:: Fix release workflow being completed for any push.

We now should only do a full release workflow if semantic-release triggers one. ([`61b1141`](https://github.com/rjdbcm/OZI/commit/61b1141d0c57e2d526fd6fd7d9128f8d9907015a))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`886ce7c`](https://github.com/rjdbcm/OZI/commit/886ce7c9a03705b58c95e0b554fc61c7ad67228f))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`c7ec522`](https://github.com/rjdbcm/OZI/commit/c7ec5225c7b30642e8e5111ae16756a7603c8309))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`fd2b5c3`](https://github.com/rjdbcm/OZI/commit/fd2b5c3c1f668c771da4ae344522f63d1ff0cb03))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`19736ab`](https://github.com/rjdbcm/OZI/commit/19736ab7e3068fb3f7d5b5f0d62e64c81b79db38))


## v0.0.46 (2023-09-04)

### :pencil2:

* :pencil2::construction_worker:: Update workflow name to OZI. ([`d59200f`](https://github.com/rjdbcm/OZI/commit/d59200f8cd64bb9727c7fe77fdd9ab7f69e81d3f))


## v0.0.45 (2023-09-04)

### :ambulance:

* :ambulance:: Move dist-info before release. ([`ca4d90d`](https://github.com/rjdbcm/OZI/commit/ca4d90d1e88944b9b8886671c64379f13206dd4d))

* :ambulance:: Fix release tag output ([`369881a`](https://github.com/rjdbcm/OZI/commit/369881a9d9d7512270999cd14dc7892ec792530f))

* :ambulance: move artifact to CWD. ([`cad344f`](https://github.com/rjdbcm/OZI/commit/cad344fdf26c21396c58798e01c7e2a9ddb7807f))

* :ambulance:: update gitignore template and gitignore. ([`6de3068`](https://github.com/rjdbcm/OZI/commit/6de306822ac4ea2740ae58157b6601c0dc8f372c))

* :ambulance::construction_worker:: Separate release and publish with artifacting. ([`e1ae4fd`](https://github.com/rjdbcm/OZI/commit/e1ae4fd56424504f3add9d7d2a30ce76276e0a3e))

* :ambulance::construction_worker:: Switch to sequential matrix action. ([`a2eb098`](https://github.com/rjdbcm/OZI/commit/a2eb098f60f5dda67e425023db152f153f8782ec))

* :ambulance::construction_worker:: Wait until builds complete to release. ([`8ac8c93`](https://github.com/rjdbcm/OZI/commit/8ac8c93d3adfca319b386f63cffc6e0573e5154b))

* :ambulance:: Fix CI workflow release versioning. ([`5b2fb2e`](https://github.com/rjdbcm/OZI/commit/5b2fb2e03b1481090333832f4816ba3487f39cb6))

* :ambulance:: Checkout released tag for publish. ([`9754cd1`](https://github.com/rjdbcm/OZI/commit/9754cd13040c61386f5f098540b78c93da82a2cc))

* :ambulance::construction_worker:: Second retry of 0.0.45, fixed some conditionals. ([`f558a13`](https://github.com/rjdbcm/OZI/commit/f558a13b34e33123d28383fd6e1d1eb815a1702f))

* :ambulance::pencil2:: Retry 0.0.45 with version as strings. ([`702e6d2`](https://github.com/rjdbcm/OZI/commit/702e6d211e5a2578aa923e81329819d297b4ff1c))

* :ambulance:: Attempt a more hermetic release with indv. versioned wheels we need. ([`7d2e4d9`](https://github.com/rjdbcm/OZI/commit/7d2e4d9d1b7af60a7cdda3b0e528b0909b89634d))

### :pencil2:

* :pencil2:: Fix version used for checkout and download. ([`2d5fdcd`](https://github.com/rjdbcm/OZI/commit/2d5fdcd9d07c0bfa6e2af4b68f499e6959b55159))

* :pencil2:: Fix PKG-INFO version overreach. ([`3a97d37`](https://github.com/rjdbcm/OZI/commit/3a97d372d1b9653e5f63ee64c954ca95f67278e5))

### Other

* :construction_worker:: Rename dist-info to match wheels. ([`81be710`](https://github.com/rjdbcm/OZI/commit/81be710209ed70c7caf0ae360374ba55a79a04a4))

* :construction_worker:: Move dist-info for all wheel releases. ([`ebc5e2f`](https://github.com/rjdbcm/OZI/commit/ebc5e2f504eaa15172644061aa499ac7bc5d59d0))

* :construction_worker:: Drop sdist for now. ([`e1a4628`](https://github.com/rjdbcm/OZI/commit/e1a46286348e11e0afa0f24883fd86f9f4663498))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/OZI ([`27dc9f6`](https://github.com/rjdbcm/OZI/commit/27dc9f630e4a0cb8fccbe9c1029113ca869d3471))

* :construction_worker:(PKG-INFO): Bump Version. ([`dbfb676`](https://github.com/rjdbcm/OZI/commit/dbfb676e6b2236dfc92124c352b60b8f0dbc3f89))

* :memo:: Remove extraneous workflow file header. ([`ba1a5af`](https://github.com/rjdbcm/OZI/commit/ba1a5af352b32313c609f121dc9c9fc2659c4a88))

* :construction_worker:: merge before pushing PKG-INFO. ([`c08266c`](https://github.com/rjdbcm/OZI/commit/c08266cbc8f3da8034373d2354d679b765563114))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`09ab46f`](https://github.com/rjdbcm/OZI/commit/09ab46fc58c726d45cb622f7df91fc00aadf8d2b))

* :construction_worker:: Merge PKG-INFO during release. ([`7df4e56`](https://github.com/rjdbcm/OZI/commit/7df4e56e128aa629e10683fd944ae28b880a3666))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`cae8bf7`](https://github.com/rjdbcm/OZI/commit/cae8bf765b2df2825d68409dc535e753cc4296b4))

* :construction_worker:: Fixing sdsist. ([`26e6c5e`](https://github.com/rjdbcm/OZI/commit/26e6c5eba95e2fea44efa66f765d039555607ea3))

* :construction_worker:: Get correct ambient credentials for sdist. ([`239f3c5`](https://github.com/rjdbcm/OZI/commit/239f3c5121465e92e5f98e690a35c0854ca95eb4))

* :construction_worker:: Add phony checkout for ambient credentials. ([`98c2670`](https://github.com/rjdbcm/OZI/commit/98c2670f1a0859673f93b9ebe13a5ccf0000bf2c))

* :construction_worker:: Fix sdist git credentials. ([`39f4259`](https://github.com/rjdbcm/OZI/commit/39f425996c4f0be8ccf3d06a0a7cc89ad9f3e66b))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`e46b6ef`](https://github.com/rjdbcm/OZI/commit/e46b6ef36e3c5f0b4bd827ad837a6bebb9b825a7))

* :construction_worker:(pyc_wheel): Only strip the built wheel not finished wheels.

Add version detection from tag. ([`44a7f05`](https://github.com/rjdbcm/OZI/commit/44a7f05be277ae280dce272f181fceda87f42962))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`7dd4bf2`](https://github.com/rjdbcm/OZI/commit/7dd4bf253827e8d409011b5a267f97436f143a80))

* :construction_worker:(pyc_wheel): strip correct wheel version. ([`9ea0c93`](https://github.com/rjdbcm/OZI/commit/9ea0c9375e1a48562933beadf1731e387bdd6711))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`1aa6744`](https://github.com/rjdbcm/OZI/commit/1aa6744a4de3f165def9476fd5ba2b57af012553))

* :construction_worker:: Only configure git repo the first time. ([`c528ac6`](https://github.com/rjdbcm/OZI/commit/c528ac645b7ccf43350d1d875c6ed1fd6761810d))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`1a156e3`](https://github.com/rjdbcm/OZI/commit/1a156e356e540c53fc1051a3402c38fbc33d154d))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`5f7dcca`](https://github.com/rjdbcm/OZI/commit/5f7dccabde45da4002a102d6b4a9179d7af45cca))

* :construction_worker:: Reverse python version build order.
sdist (py311) runs last.
this avoid commiting PKG-INFO too early. ([`14d6edc`](https://github.com/rjdbcm/OZI/commit/14d6edc658c8cd7daf802310f45411e18f6ad481))

* :construction_worker:: Use actions/download-artifact to get repo for wheel builds. ([`37ad739`](https://github.com/rjdbcm/OZI/commit/37ad739c365653ceb4f7616fe195d9578b75d50b))

* :construction_worker:(PKG-INFO): Bump Version. ([`e03b527`](https://github.com/rjdbcm/OZI/commit/e03b52768db0157d3490a5d26e0ee8aa0aa17d48))

* :construction_worker:: Only run git checkout once per release. ([`acfe7c2`](https://github.com/rjdbcm/OZI/commit/acfe7c2e832c58e3cf8dbf041de33881b2a69e40))

* :construction_worker:(PKG-INFO): Bump Version. ([`6a48956`](https://github.com/rjdbcm/OZI/commit/6a4895634585f86820b9d328d98ae92d3b61e423))

* :construction_worker:(PKG-INFO): Bump Version. ([`e556184`](https://github.com/rjdbcm/OZI/commit/e556184a8868b4a99e46fd959eb3277951bf73a4))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`7613e2e`](https://github.com/rjdbcm/OZI/commit/7613e2ec2260e5320300b02e952410ed90a0f784))

* :construction_worker:: relocate git repo setup. ([`72c648c`](https://github.com/rjdbcm/OZI/commit/72c648cd2a9292b79316c7a1381041c635510f5f))

* :construction_worker:: correctly name wheel files. ([`617c065`](https://github.com/rjdbcm/OZI/commit/617c065498d5d679d947887ff5bb2c884e6e6df6))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`7351c4a`](https://github.com/rjdbcm/OZI/commit/7351c4a3d25836bf0843a414db4b716ee1e77e79))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`f350eb3`](https://github.com/rjdbcm/OZI/commit/f350eb37576cfd47acaac9aeaef0755c45dcb68d))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`ee50603`](https://github.com/rjdbcm/OZI/commit/ee506039f97c57ab390d1130fb96399bb4156bcc))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`083af92`](https://github.com/rjdbcm/OZI/commit/083af920398f740259f51b3de915dec22b50f48c))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`3f15bec`](https://github.com/rjdbcm/OZI/commit/3f15becaea9684a2af2c34323bdeb44c50c3b428))

* :construction_worker:(PKG-INFO): Bump Version. ([`4e4cbb2`](https://github.com/rjdbcm/OZI/commit/4e4cbb2dc6a8b690dac1142b09bc6167448c9330))


## v0.0.44 (2023-09-03)

### :hammer:

* :hammer:: Update ``ozi-new`` and ``ozi-fix`` scripts. ([`2a2a131`](https://github.com/rjdbcm/OZI/commit/2a2a131b83c19d3e70a9b72147c506aaff6294cc))

### Other

* :construction_worker:(PKG-INFO): Bump Version. ([`e8897da`](https://github.com/rjdbcm/OZI/commit/e8897da27fbb1e14a4d3e33611d026937232ebfd))


## v0.0.43 (2023-09-02)

### :bento:

* :bento:: fix missing asset listing for ``structure.py``. ([`be3bc6f`](https://github.com/rjdbcm/OZI/commit/be3bc6fb2923e03ea7a06ddc4969552a86bc77c6))

### :hammer:

* :hammer:: Fix ``ozi`` entrypoint. ([`5628c02`](https://github.com/rjdbcm/OZI/commit/5628c02dc835d30b2ea66adb1cfd9c55396f38f9))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`9d247ff`](https://github.com/rjdbcm/OZI/commit/9d247ffedcb4593e428c1488f492b9e4ec5ad1fe))

* :construction_worker:(PKG-INFO): Bump Version. ([`5c10473`](https://github.com/rjdbcm/OZI/commit/5c1047327f7f673d1868bbf934e5d4f2ca2cf6c5))


## v0.0.42 (2023-09-02)

### :hammer:

* :hammer:: Fix relative import in ``ozi-fix``. ([`a23d78d`](https://github.com/rjdbcm/OZI/commit/a23d78decda22cc9b36c05905e0cbfde2d6f172d))

### Other

* :construction_worker:(PKG-INFO): Bump Version. ([`baa497e`](https://github.com/rjdbcm/OZI/commit/baa497e47225b5d51596f0f6409283f849a43b16))


## v0.0.41 (2023-09-02)

### :bento:

* :bento::memo:: Cleanup README and PKG-INFO. ([`20a2766`](https://github.com/rjdbcm/OZI/commit/20a2766b07c1d1121f3ae060e1f540292032e59e))

### :hammer:

* :hammer: update github workflow templates. ([`e7babd1`](https://github.com/rjdbcm/OZI/commit/e7babd1b78a9501808e387e25707e165fcfc388b))

* :hammer:: Add ``ozi`` script entrypoint. ([`dfc96a8`](https://github.com/rjdbcm/OZI/commit/dfc96a80a551c91867aaa6427a01b16f32931324))

* :hammer:: Add ``ozi-fix`` script for making rewrites. ([`ce4222e`](https://github.com/rjdbcm/OZI/commit/ce4222e507577dec2be8349fd5c6fde55fd82d07))

* :hammer:: Add --no-verify-email to ``ozi-new`` script. ([`4d0030a`](https://github.com/rjdbcm/OZI/commit/4d0030a586756b71065445bf076a5ef9c31a6eff))

### :pushpin:

* :pushpin:: Pin action versions with hash. ([`3fdaa02`](https://github.com/rjdbcm/OZI/commit/3fdaa02d88a6be0dde46d9bb365a8f5233f01a61))

### :wrench:

* :wrench:: Add pseudo-targets root_files and source_files. ([`e14ea88`](https://github.com/rjdbcm/OZI/commit/e14ea889aa8a1f16fb05bdb263756feb2a84b51a))

### Other

* :construction_worker:(PKG-INFO): Bump Version. ([`470d40e`](https://github.com/rjdbcm/OZI/commit/470d40e0cfd6ae82afe1f7c537cf5011e710d775))


## v0.0.40 (2023-09-01)

### :pencil2:

* :pencil2:: Add missed template from move. ([`a366872`](https://github.com/rjdbcm/OZI/commit/a366872e2120a79d19c89aa5047950b1046022de))

### Other

* :construction_worker:(PKG-INFO): Bump Version. ([`3339932`](https://github.com/rjdbcm/OZI/commit/3339932f9b5753de03f39691d9685c0ce270c302))


## v0.0.39 (2023-09-01)

### :ambulance:

* :ambulance:: Manually fix git permissions. ([`168338f`](https://github.com/rjdbcm/OZI/commit/168338f9077bc3b96456ebac771395daf2b1adf0))

* :ambulance:: Ensure that we have privileges in the .git directory during build. ([`112e7b8`](https://github.com/rjdbcm/OZI/commit/112e7b878bcd366a7ffca87464319100e0a3ac7a))

* :hammer::ambulance:: Fix relative module import. ([`d159122`](https://github.com/rjdbcm/OZI/commit/d15912294f6d52802e8fe49c0503666c040c33c6))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`bb1077c`](https://github.com/rjdbcm/OZI/commit/bb1077c6504486432d3451cb82f915194349f357))

* :construction_worker:(PKG-INFO): Bump Version. ([`4dad555`](https://github.com/rjdbcm/OZI/commit/4dad55587b5ce6ec26f6fed7d1b3f1948d2ce272))


## v0.0.38 (2023-09-01)

### :wrench:

* :pencil2::wrench:: Fix wheel build. ([`a335272`](https://github.com/rjdbcm/OZI/commit/a3352728a55f875f6cbd569b6340dac06dec8d5d))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`8a19823`](https://github.com/rjdbcm/OZI/commit/8a1982350976533437522d306266e238cadfa8c5))

* :construction_worker:(PKG-INFO): Bump Version. ([`11818bb`](https://github.com/rjdbcm/OZI/commit/11818bbedad7f7e329d34b75debdf7cc5c2c09d7))


## v0.0.37 (2023-09-01)

### :wrench:

* :wrench:: Add subdir to install_sources template. ([`105cd73`](https://github.com/rjdbcm/OZI/commit/105cd73b01eec634997b40106c8a4d9296b30776))

* :wrench:: Fix meson build for mesonpep517 wheel. ([`f6daa66`](https://github.com/rjdbcm/OZI/commit/f6daa66e00b073ff132da25a1153868cf94405b6))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`c47aebb`](https://github.com/rjdbcm/OZI/commit/c47aebb51f23f49652c651df3e925d4f14917ce8))

* :construction_worker:(PKG-INFO): Bump Version. ([`46279ac`](https://github.com/rjdbcm/OZI/commit/46279acf8a5cc1025c85a0aca0eb1054206fce7b))


## v0.0.36 (2023-09-01)

### :ambulance:

* :ambulance::hammer:: Fix meson entry point finding. ([`30c3eb0`](https://github.com/rjdbcm/OZI/commit/30c3eb09f59b80887f43cb2cede5cc66135a8d91))

### Other

* :construction_worker:(PKG-INFO): Bump Version. ([`87e5573`](https://github.com/rjdbcm/OZI/commit/87e5573ff78dbdb01b64328715dc70774c40f7b6))


## v0.0.35 (2023-09-01)

### :ambulance:

* :ambulance:: Fix python install sources for meson. ([`5c47a59`](https://github.com/rjdbcm/OZI/commit/5c47a59f1312eac75c53cb9693081920d77a95fc))

* :ambulance:(CI): Properly invoke release build with meson. ([`3ff7d07`](https://github.com/rjdbcm/OZI/commit/3ff7d0751888d102af24165ac5f1e9fd2e958828))

* :ambulance:: Fix implementation of python.install_sources(). ([`d50200b`](https://github.com/rjdbcm/OZI/commit/d50200be2ace24e5162ed5c12ce930a87617b22d))

### :fire:

* :fire:: remove duplicate workflow scripts folder. ([`239ef1a`](https://github.com/rjdbcm/OZI/commit/239ef1a110fb2766cc5b0c8ec14c203ab5edacca))

### :wrench:

* :pencil2::wrench:: Fix unquoted string in build. ([`5a9feb4`](https://github.com/rjdbcm/OZI/commit/5a9feb4842bba3b5b1efd653b833b3d9c5922ddf))

* :pencil2::wrench:: Fix missing commas in build. ([`0a5febd`](https://github.com/rjdbcm/OZI/commit/0a5febdc030eb68e7b3fb5c49020f3746f150a7b))

### Other

* :construction_worker:(PKG-INFO): Bump Version. ([`dc0e174`](https://github.com/rjdbcm/OZI/commit/dc0e174330a07b10028bba864cecf10350923509))


## v0.0.34 (2023-09-01)

### :ambulance:

* :ambulance:: Fix script location. ([`5c82b2b`](https://github.com/rjdbcm/OZI/commit/5c82b2bfa4f6fe1a8d67453ca5a00771fdf4e017))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`994435f`](https://github.com/rjdbcm/OZI/commit/994435f2fff6eabc7e157a54534784569ed988a1))

* :construction_worker:(PKG-INFO): Bump Version. ([`f426f8b`](https://github.com/rjdbcm/OZI/commit/f426f8b778ff4234213abaddcd72a4881004f3b2))


## v0.0.33 (2023-09-01)

### :children_crossing:

* :children_crossing:: Add project script ``ozi-new``. ([`5a91afc`](https://github.com/rjdbcm/OZI/commit/5a91afc310ef26eb3401c3f39280f948dfcff77a))

### Other

* 🚑️: Fix script entrypoint name. ([`7ab1b06`](https://github.com/rjdbcm/OZI/commit/7ab1b067feb58f8440955ecace0c87bd6bb87334))

* :construction_worker:(PKG-INFO): Bump Version. ([`66d1b0a`](https://github.com/rjdbcm/OZI/commit/66d1b0aa7f31c401e617164c034cf04334d5bff0))


## v0.0.32 (2023-08-31)

### :bento:

* :fire::bento:: Delete ``assets/structure`` ([`c7da0ec`](https://github.com/rjdbcm/OZI/commit/c7da0ec0c710593aa4ab14fb2cdbd5b7070a54dd))

### :wrench:

* :wrench::truck:(project): Move core templates and assets from OZI.docs. ([`959f38d`](https://github.com/rjdbcm/OZI/commit/959f38d46214c80671c0af2df252b7196b65e9cd))

### Other

* :busts_in_silhouette:: Add CODE_OF_CONDUCT.md ([`1f944ff`](https://github.com/rjdbcm/OZI/commit/1f944ff53c3be973fa6e0fcca04d398607c846ce))

* :construction_worker:(PKG-INFO): Bump Version. ([`7be3c2b`](https://github.com/rjdbcm/OZI/commit/7be3c2b672341b6226f8267cc3045e753ba4a870))


## v0.0.31 (2023-08-30)

### :children_crossing:

* :children_crossing:(semantic-release): Fix commit parsing. ([`e6d349d`](https://github.com/rjdbcm/OZI/commit/e6d349d58d8a6d8c36e3778217c8a5cf7c6f1c00))

### Other

* :construction_worker:(PKG-INFO): Bump Version. ([`b16af53`](https://github.com/rjdbcm/OZI/commit/b16af531534be46e98bb5f04ddf4ec46f9501cbf))


## v0.0.30 (2023-08-30)

### :ambulance:

* :ambulance: Fix SCM tracked version. ([`9a5a7cb`](https://github.com/rjdbcm/OZI/commit/9a5a7cbbafc8ef561e1785442c66ec1bb7c3cddf))

* :wrench::ambulance:(semantic-release): Fix args for major version bump 7 to 8. ([`501d387`](https://github.com/rjdbcm/OZI/commit/501d3873291958249ed6561688ec7ad34c55ec39))

### :wrench:

* :wrench:(meson): drop rst-lint for now. ([`7b35036`](https://github.com/rjdbcm/OZI/commit/7b35036b6d27b613b40fe8ecd30f05c21ac4d59b))

* :wrench:(tox): fix tox-gh env names. ([`81e1ebf`](https://github.com/rjdbcm/OZI/commit/81e1ebf6ba28d1acf7eab9b36d0a33b66528f186))

* :construction_worker::wrench:: Move test workflow into dist-workflow.yml ([`c2f16a1`](https://github.com/rjdbcm/OZI/commit/c2f16a14fb315e9d9225a76b93593a6863a72cbb))

### Other

* :pencil: remove trailing newline PKG-INFO template. ([`0304af0`](https://github.com/rjdbcm/OZI/commit/0304af0be29deecc8b8c0d9fa6f4200b5a11e8bd))

* :memo:: remove pytest badge. ([`1d1acde`](https://github.com/rjdbcm/OZI/commit/1d1acdedd1fefb6b1e4bd240c9ed9b9a8991a430))

* :pencil: delete symlink. ([`38076dd`](https://github.com/rjdbcm/OZI/commit/38076ddb4173b9a0261a3b0d34155facf2113dd5))

* :construction_worker:(gh-actions): Parity with blastpipe. ([`8bb5ebe`](https://github.com/rjdbcm/OZI/commit/8bb5ebe856eee7a43d01d45ea422c131d94b2777))

* 🎨: Blacken script files. ([`6b5cc15`](https://github.com/rjdbcm/OZI/commit/6b5cc15b1d14cdbe3399a59f94c874cbce1282f3))

* 🔥: remove the file setuptools_tools.py for now. ([`e66738d`](https://github.com/rjdbcm/OZI/commit/e66738d830632483a1817d59d654879835e4a9de))

* :construction_worker:: Drop docs from workflow. ([`8981a12`](https://github.com/rjdbcm/OZI/commit/8981a12650217a2f13af9cfde7db90c57d71d100))

* 👷: add all deps to tox. ([`b013818`](https://github.com/rjdbcm/OZI/commit/b013818bdfb5f155cdcba539f480944a146efb83))

* 🚑️👷(tox-gh): fix 3.11 build and delete Windows testing. ([`95c5f4f`](https://github.com/rjdbcm/OZI/commit/95c5f4fc55ffabd8e3a6a08756464d47e68230ad))

* 🐛(tox): delete --skip-pkg-install argument in CI. ([`d2d0cda`](https://github.com/rjdbcm/OZI/commit/d2d0cda2d2b729d7dc743fca980a967c07c54f2e))

* 🔨🚑️: FIX: sync_pkg_readme should use meson.source_root(). ([`ed99470`](https://github.com/rjdbcm/OZI/commit/ed994701df37ff0ceda6dca96cd501c2fcf08749))


## v0.0.29 (2023-08-29)

### :bug:

* :bug: try remove .git/COMMIT_EDITMSG during build. ([`8ea37ef`](https://github.com/rjdbcm/OZI/commit/8ea37ef48cb525675c87152a5921ea00d235d88f))

* :bug: Attempt to force a version by fixing permissions. ([`718e36d`](https://github.com/rjdbcm/OZI/commit/718e36d859019153276c2a1b239fc9dc788b2ec0))

* :bug: Attempting to force COMMIT_MSG permissions. ([`a3af65f`](https://github.com/rjdbcm/OZI/commit/a3af65ffe215d84e749281f192f58180ef3e471d))

* :bug: empty commit message during release. ([`8375f5a`](https://github.com/rjdbcm/OZI/commit/8375f5a716ce704cbafaea070619673e129532c6))

* :bug:(dist-workflow): fix permissions for commit. ([`f3e7929`](https://github.com/rjdbcm/OZI/commit/f3e79293f5882936b7d984f8fe921722cd60347a))

* :bug:(PKG-INFO): Ensure that PKG-INFO is updated at release. ([`23aa8e6`](https://github.com/rjdbcm/OZI/commit/23aa8e6367ce9d47ae130972f4a6ae563fcb6e13))

* :bug:(CI): don&#39;t stash mesons source of version info. ([`9f3d311`](https://github.com/rjdbcm/OZI/commit/9f3d3113881b5e5bd714d9ac4622cfc4ead0e486))

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`14994e0`](https://github.com/rjdbcm/OZI/commit/14994e0286f7d1c4f8af6157253272eb79a51a0d))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`fd1212e`](https://github.com/rjdbcm/OZI/commit/fd1212ef4b88d2d26b9bb8be7e383864e8f5f573))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`ae5657d`](https://github.com/rjdbcm/OZI/commit/ae5657de16cf194fc1d91550b9a0afc40e748f69))


## v0.0.28 (2023-08-29)

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`3d88d26`](https://github.com/rjdbcm/OZI/commit/3d88d2601c93c9dc30106a4ba431efce90681954))

* 🚑️(pyproject.toml:tool.semantic_release): No hardcoded version. ([`f2cad32`](https://github.com/rjdbcm/OZI/commit/f2cad323e928c8dbe12eb2f9d70dc136a11b340b))


## v0.0.27 (2023-08-29)

### :bug:

* :bug:(CI): forcing a patch. ([`799789c`](https://github.com/rjdbcm/OZI/commit/799789c805d310b4273c9c807dfbedfe1c8f8963))

* :bug:(version): Attempting direct version bump. ([`40440ed`](https://github.com/rjdbcm/OZI/commit/40440ed43b5b8951dae8097c52c005cce6913e63))

* :bug:(project): Patch release trigger. ([`0c0796d`](https://github.com/rjdbcm/OZI/commit/0c0796d329403652a3e1250b5bc71818980800b4))

### Other

* :construction_worker:(build): revert manual bump. ([`6f612c9`](https://github.com/rjdbcm/OZI/commit/6f612c9ec2f3f21db6f797fa7bd27ea34f1685d5))

* 🐛(pyproject.toml): Fix fallback version blocking release trigger. ([`75b68d4`](https://github.com/rjdbcm/OZI/commit/75b68d4f0aefd68b32dbfa6e6b2dd1b856b0b365))

* 🐛(CI/gh-actions): This should trigger a semantic-release. ([`7ea080a`](https://github.com/rjdbcm/OZI/commit/7ea080a0e35858656ff80020682673a9a6b27fdf))

* 🐛: Release should trigger. Deleted unused key. ([`e1899e9`](https://github.com/rjdbcm/OZI/commit/e1899e9f01b4230f8f63ea558c5c85d65b1ba593))

* 🚑️: Only build wheel on successful release. ([`000953f`](https://github.com/rjdbcm/OZI/commit/000953f4259a0f0d08c5487984240b4af2687ef1))

* Remove Windows Classifier. ([`92d424c`](https://github.com/rjdbcm/OZI/commit/92d424ccdc918367cd01c7865436f55c29b3ea45))


## v0.0.26 (2023-08-29)

### Other

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`4fb7a08`](https://github.com/rjdbcm/OZI/commit/4fb7a0814d501baaf539787e91f5b38888c3237d))

* 👷: remove dist-info glob. ([`8d89d33`](https://github.com/rjdbcm/OZI/commit/8d89d332e06d9f298ecb49aa824da4551dddcb45))

* 👷: move dist-info to sig. ([`78bb99e`](https://github.com/rjdbcm/OZI/commit/78bb99e61502d514bdd0ac2d3025d88997e6aaee))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`39839f3`](https://github.com/rjdbcm/OZI/commit/39839f31938642cc552eaac95778cef9b8652967))

* 👷: add hardcoded prefixes for now -py3-none-any. ([`9654dc1`](https://github.com/rjdbcm/OZI/commit/9654dc1e37e809c8f21c4fecf8db9afb025872ba))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`3f523cd`](https://github.com/rjdbcm/OZI/commit/3f523cd43b9eae54d78ca98e5a4d7a3f091b2c9c))

* :pencil: rekor should have been sigstore. ([`66d5571`](https://github.com/rjdbcm/OZI/commit/66d557191946721999a26164c6a88817d883bd92))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`4b7bdb4`](https://github.com/rjdbcm/OZI/commit/4b7bdb4212a1c3cf06fc04c23e7695d94a24ddd4))

* 🏗️: move signatures out of dist after build. ([`9310b36`](https://github.com/rjdbcm/OZI/commit/9310b369a0d673767b8bbd13b6c81fe74ba1c471))

* 🏗️: Move CI build out of dist. ([`b3d7dba`](https://github.com/rjdbcm/OZI/commit/b3d7dbaf721c414c5fe55f0913729f34815dfb48))

* 👷: Fix OZI case by hard-coding for now. ([`513612d`](https://github.com/rjdbcm/OZI/commit/513612d9d5c5e4fd2f0eae7dc400b18bb2945d96))

* 👷:update maintainer email. ([`b905956`](https://github.com/rjdbcm/OZI/commit/b905956d6acc550b0c568e05296d175731bc84d6))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`9806965`](https://github.com/rjdbcm/OZI/commit/9806965a5b5e8ea43b3679fc214ab5f20ab6f1c2))

* 👷: No longer attempting to upload signatures to PyPI. ([`c9c630e`](https://github.com/rjdbcm/OZI/commit/c9c630e5d1a2007bd29d2b59d895d5d131378161))

* 👷: May still need to stash PKG-INFO. ([`1104ff6`](https://github.com/rjdbcm/OZI/commit/1104ff65f97b813c22b2adae419790773b4a2a2b))

* 🏗️👷: remove git invocation during wheel build. ([`8b53863`](https://github.com/rjdbcm/OZI/commit/8b53863c573269760b44250e9d2c6165cb4e82d9))

* 👷: Fix gh-actions permissions. ([`750b208`](https://github.com/rjdbcm/OZI/commit/750b208903b00141fc333e0b8da6102118c2340c))

* 🏗️: release then build. ([`12b14db`](https://github.com/rjdbcm/OZI/commit/12b14db94b61b60754cc7a0b604e5a503bacc242))

* 👷: Add CI/CD user name &#34;OZI Packaging&#34;. ([`c1430b8`](https://github.com/rjdbcm/OZI/commit/c1430b86ed8de6c1352faa03f62af9ff030abcae))

* 👷: add noreply git user. ([`e960a9d`](https://github.com/rjdbcm/OZI/commit/e960a9d809ebe2af702d0054baf4e28198669424))

* :pencil: Fix unnecessary escaping. ([`b5803e4`](https://github.com/rjdbcm/OZI/commit/b5803e4f52afa5e30d41317db759d2b9f439880a))

* 🏗️: bind semantic_release.version_toml to setuptools_scm.fallback_version. ([`9f275ad`](https://github.com/rjdbcm/OZI/commit/9f275ad7378ad9553ccda638f69cc66b967625c7))

* :pencil: should have kept setuptools_scm. ([`931f1c0`](https://github.com/rjdbcm/OZI/commit/931f1c00b8a0721a4970053b0061d7b59be04059))

* 👷: pip install --user --upgrade ninja ([`9662564`](https://github.com/rjdbcm/OZI/commit/966256423aa3ddb68726c21d78b779ea77dfb0cd))

* 👷: Fix missing setuptools_scm. ([`c301871`](https://github.com/rjdbcm/OZI/commit/c3018716ceb0efa799ca20c6f30a89591d80ed3e))

* move all of CI build out of semantic-release. ([`5ff06a7`](https://github.com/rjdbcm/OZI/commit/5ff06a74c00282f507861182f169c0d59abc0328))

* 👷: move pyc_wheel out of semantic-release build cmd. ([`2715570`](https://github.com/rjdbcm/OZI/commit/2715570469c066ad1145d17e07d1b8ce2a2023f0))

* add ci build requirements. ([`69672f5`](https://github.com/rjdbcm/OZI/commit/69672f5e703a80bfbcb2e3aea9172dcdbbc76352))

* :pencil:: fix path root on build check. ([`914bb5d`](https://github.com/rjdbcm/OZI/commit/914bb5d98f831372831c65599d836423806d1692))

* :pencil:: Should have built -w (wheel) ([`d4180ea`](https://github.com/rjdbcm/OZI/commit/d4180ea1b39c01ebb40703512da6a1a3062db9ff))

* 🔧Do our own build during release CI. ([`e7c6a58`](https://github.com/rjdbcm/OZI/commit/e7c6a58ecd621901c9445f23ba8646ae28ffa4b7))

* update CI actions. ([`8f7ba72`](https://github.com/rjdbcm/OZI/commit/8f7ba72f8d0959cf6de7ef4155ee74358e91e211))

* 🔧: install build during CI. ([`b23c529`](https://github.com/rjdbcm/OZI/commit/b23c529e296fb8c2dafe5f096f65ba6b9ee10bba))

* ⬆️(python-semantic-release): Bump version to 8.0.8. ([`9c2bc45`](https://github.com/rjdbcm/OZI/commit/9c2bc45a364f76695fee4f12f42a21d3dc9f6448))

* update semantic release version. ([`4ba7161`](https://github.com/rjdbcm/OZI/commit/4ba71618fc3220ab80c3e8dbcc718b057ee901e5))

* add workflows. ([`b2802f8`](https://github.com/rjdbcm/OZI/commit/b2802f8ef0761b5b0068623ac91cf77864644598))

* Create python-publish.yml ([`c2e507d`](https://github.com/rjdbcm/OZI/commit/c2e507ddaf3c43bcd08b9b98ebdd6bdcb24b8d60))

* :pencil:(README): Fix indentation. ([`979e948`](https://github.com/rjdbcm/OZI/commit/979e948303fd32569f4fc3a4462fc42573b946be))

* 👷: HOTFIX Relative directory traversal in scripts. ([`ffd966d`](https://github.com/rjdbcm/OZI/commit/ffd966dde388677db380e6ea78e2e0b1cf70f522))

* :loud_sound: Added release changes. ([`b479657`](https://github.com/rjdbcm/OZI/commit/b479657fc6dbf60012090391551b7b38fa2f4265))

* Updated PKG-INFO Version. ([`01ba8d5`](https://github.com/rjdbcm/OZI/commit/01ba8d57ffe0927737675a57365a5860e610e9cc))

* :pencil: Revert Version. ([`8d37ca7`](https://github.com/rjdbcm/OZI/commit/8d37ca7ab25614bca8fe6f68763e1980ed07ce89))

* :pencil: commit changelog during release. ([`e646d0b`](https://github.com/rjdbcm/OZI/commit/e646d0bc8377635520eddc23bb46e4da2583c540))

* :loud_sound: Added release changes and updated PKG-INFO. ([`bbfd15a`](https://github.com/rjdbcm/OZI/commit/bbfd15a39704c2934a3ee86bd44d98866801adb0))

* :pencil: fix version. ([`7ef2a05`](https://github.com/rjdbcm/OZI/commit/7ef2a05cfd70f74d33418d706b5a1e0df518da0b))

* :pencil: remove commit ammend. ([`083284e`](https://github.com/rjdbcm/OZI/commit/083284e09ec6feabd5213b631233b0260ca93325))

* :pencil:(pyproject.toml): --noedit should be --no-verify. ([`d002a1f`](https://github.com/rjdbcm/OZI/commit/d002a1f2a312e644822b7030887d50aa819cf7c6))

* :loud_sound: Added release changes and updated PKG-INFO. ([`6a5d7bb`](https://github.com/rjdbcm/OZI/commit/6a5d7bbdef9ac149dbe3098c766d2e1d615f2b7f))

* 🚧(meson.build): Commented out migrated install summary. ([`54d31c9`](https://github.com/rjdbcm/OZI/commit/54d31c99156019b4e408587a8978b5b0a6832ad0))

* 🔧: Added mypy to optional-dependencies and requirements. ([`ba78c65`](https://github.com/rjdbcm/OZI/commit/ba78c65ae0b2b9444973d3485d6d24f53314ebc5))

* remove unecessary license header ([`4b09e8b`](https://github.com/rjdbcm/OZI/commit/4b09e8bd097c4005b07c22796e82069412ed9458))

* 🔧(ozi/scripts/meson.build): Add sync_pkg_readme.py. ([`d32bac9`](https://github.com/rjdbcm/OZI/commit/d32bac9718502e8218302a3e962ee5dae249c065))

* 🔨(meson.options): add mypy to lint utilities. ([`bee2247`](https://github.com/rjdbcm/OZI/commit/bee2247ae33974885faa57db4a10550686ff9d0f))

* 🔧🎨(meson.build): Move code out of blastpipe and format. ([`6f4a0d2`](https://github.com/rjdbcm/OZI/commit/6f4a0d2765350008882fd6fbd88935e73efd5885))

* 🔧(pyproject.toml:tool.semantic_release): Update to target standard 0.1 milestone. ([`06286da`](https://github.com/rjdbcm/OZI/commit/06286dad75f3d0c3ef0cd196acd827b50f2e4e55))

* FIX: potential CWE-23. ([`620ef68`](https://github.com/rjdbcm/OZI/commit/620ef68907b5d7a00bdcc8613e161fcc70ed9514))

* FIX: CWE-23 ([`d0036fc`](https://github.com/rjdbcm/OZI/commit/d0036fc4c91336fca41e9275e0ae1b3c6a8f7e67))

* 🔊: Add 0.0.25 changes. ([`10c0096`](https://github.com/rjdbcm/OZI/commit/10c0096d00a5743cfa036f79f94c2c8b6ead5d13))

* PKG-INFO Updated ([`e8b8e71`](https://github.com/rjdbcm/OZI/commit/e8b8e71fdb4df3c2f6c9f0cf896fc6145eb4b5e1))


## v0.0.25 (2023-08-06)

### Other

* 🍱(ozi/assets): Restructured assets folder. ([`7a09768`](https://github.com/rjdbcm/OZI/commit/7a097680f940c4190b705c590ce08125f13a1c99))

* 👷(meson.build): Check PKG-INFO synced to pyproject. ([`515d4e8`](https://github.com/rjdbcm/OZI/commit/515d4e835395695400b1d3e358502eec53d8e550))

* 🔥 Migrate docs to [OZI.docs](https://github.com/rjdbcm/ozi.docs). ([`b3ff172`](https://github.com/rjdbcm/OZI/commit/b3ff172fc79b942344c498c1a7c6bdf34b44df81))

* 🔊(v0.0.24) ([`19c20f6`](https://github.com/rjdbcm/OZI/commit/19c20f6d4e3b4f6708c1b1bd9cb7dea3d567d1a4))

* PKG-INFO Updated ([`167694d`](https://github.com/rjdbcm/OZI/commit/167694d1d78f9b40a3b65f57466e389a84c040d0))


## v0.0.24 (2023-07-13)

### Other

* 🙈: add blastpipe to gitignore ([`d0130ba`](https://github.com/rjdbcm/OZI/commit/d0130ba81d10161cb6f4e4749402b3281e0f43f5))

* 🙈: add subprojects/dev.wrap. ([`1225f5b`](https://github.com/rjdbcm/OZI/commit/1225f5b5023d1fe7ac18d34de7c35d42a55c7e74))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`2375cb4`](https://github.com/rjdbcm/OZI/commit/2375cb40d666c775c3bca411e1d75d0cb6a1b974))

* 🔧(project.optional-dependencies): add lint plugins. ([`7453005`](https://github.com/rjdbcm/OZI/commit/7453005e9732d8d8cbb201005f402b12c89e9907))

* 📝(lint): update list of flake8 plugins. ([`f27ba85`](https://github.com/rjdbcm/OZI/commit/f27ba8551f6239bc44017c16f0ac74924cac3871))

* 🔧(black): add ``-S`` to skip string normalization. ([`76d6358`](https://github.com/rjdbcm/OZI/commit/76d6358f07f221659cca7ac6b86028f168baa2bd))

* 🔧(flake8): tidy-imports ban relative beyond sibling. ([`7dbde5e`](https://github.com/rjdbcm/OZI/commit/7dbde5e2c441a37b6ba9ede37a7196aad4de2ca7))

* 📌(project): Set pins. ([`347ed85`](https://github.com/rjdbcm/OZI/commit/347ed854011570c2c0633b9564e023d964201a99))

* 🚑️(Safety): Mitigation for CVE-2022-40898. ([`380e6c0`](https://github.com/rjdbcm/OZI/commit/380e6c07ecf8efe98ae2d315d2ee9fb316292db6))

* 🚑️(Safety): mitigation for CVE-2022-40897. ([`7d3d50f`](https://github.com/rjdbcm/OZI/commit/7d3d50f54cf3e157886f813adf58c4ff38060534))

* Update README.rst

Added human-centered messaging. ([`8d7d0a6`](https://github.com/rjdbcm/OZI/commit/8d7d0a638a13e89ebfec7aefbf64a6623228188a))

* add changes. ([`991d09a`](https://github.com/rjdbcm/OZI/commit/991d09ad41e568318b4532f97e79ad83438660d2))

* PKG-INFO Updated ([`e4feee9`](https://github.com/rjdbcm/OZI/commit/e4feee97a6e7c6ce0eebd879c4770bbe9267ccaf))


## v0.0.23 (2023-07-06)

### :pencil2:

* :pencil2: blastpipe provides blastpipe. ([`68f1897`](https://github.com/rjdbcm/OZI/commit/68f1897671398b9a52ca42f3df6a15192950eba1))


## v0.0.22 (2023-07-06)

### Other

* 🔥 Remove wrap redirect. ([`e589cb6`](https://github.com/rjdbcm/OZI/commit/e589cb62d5f69e3abc71671ff349e0f5129e2cb4))

* 🔧(blastpipe): add as subproject. ([`266d128`](https://github.com/rjdbcm/OZI/commit/266d128cdd766cc5c9fa7f75bbbd749b7b289a3a))

* 🔧(project): Add blastpipe bootstrapping.
Renamed ozi-bootstrap to ozi-blastpipe. ([`216d027`](https://github.com/rjdbcm/OZI/commit/216d0277dfd94af98f14ab2d28c61290dd51dd72))

* 🔥(meson.build): install requirements individually.
This allows support of hashed version pins. ([`baaf291`](https://github.com/rjdbcm/OZI/commit/baaf291996d016debe5dae16d6ec4948aa9f0e9a))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`769a4ab`](https://github.com/rjdbcm/OZI/commit/769a4ab80f2ad8613eaa0bccfec55754c9b0f5ef))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`9603aa8`](https://github.com/rjdbcm/OZI/commit/9603aa886c6bc4bcf1e85cdd1956db23347d1c7f))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`5419ca7`](https://github.com/rjdbcm/OZI/commit/5419ca7390d06c01ccfcf867ffbad72cdc861f8c))

* Hashes in use. ([`19e481d`](https://github.com/rjdbcm/OZI/commit/19e481dd8d6d58e75942f9b425f52eecc626d702))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`271da11`](https://github.com/rjdbcm/OZI/commit/271da11683cb2cf1e904a90c7e86aa0945fd12b9))

* Not using version hashes for now. ([`5b0358b`](https://github.com/rjdbcm/OZI/commit/5b0358b181de2de0642448e9bc67825078c6801f))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`fe9fe60`](https://github.com/rjdbcm/OZI/commit/fe9fe60cc2ce10d69472e7b61676c086745a9b09))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`8b8fc3d`](https://github.com/rjdbcm/OZI/commit/8b8fc3db0c09262b272161260c62839f5e1ece47))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`42a9abb`](https://github.com/rjdbcm/OZI/commit/42a9abb844b3f6a5d1d227a06797536dc34fd694))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`29801d5`](https://github.com/rjdbcm/OZI/commit/29801d5f967b746b3896bca49cd46e7562af5e49))

* Merge branch &#39;main&#39; of https://github.com/rjdbcm/ozi ([`e0d83c0`](https://github.com/rjdbcm/OZI/commit/e0d83c0cd7edbbdad3ba312770d8f0d2ae34b1a5))

* merge ([`adaab3f`](https://github.com/rjdbcm/OZI/commit/adaab3f5c98121fc6277d91455b6b720e69e2f89))

* merge ([`2609234`](https://github.com/rjdbcm/OZI/commit/2609234be52f714a85a531d8747af8be65251d68))

* 📌(project): pin all option suite tools. ([`4d3e459`](https://github.com/rjdbcm/OZI/commit/4d3e4594b80aa3c589578590070943211dd7fd6f))

* 📌(project): pin all option suite tools. ([`73618a2`](https://github.com/rjdbcm/OZI/commit/73618a27a90a8991cdf3d8cb15a92279d6c672b9))

* 🔨(pyproject.toml): sync to README. ([`233bac5`](https://github.com/rjdbcm/OZI/commit/233bac502c5c762d5e04c9ca316961760de4b932))

* 🔨(meson.build): Implement emoji_generic. ([`e727ace`](https://github.com/rjdbcm/OZI/commit/e727acec03785869db53668b39425e64902b1375))

* 🔨(meson.options): Add generic_emoji. ([`58c4f51`](https://github.com/rjdbcm/OZI/commit/58c4f51a164bd4c34dc846989950da5a82c3f132))

* 🔊(CHANGELOG.md): Updated. ([`5aade55`](https://github.com/rjdbcm/OZI/commit/5aade551c2e25e89b18de4be2faaf9f6c2076605))

* PKG-INFO Updated ([`0877e63`](https://github.com/rjdbcm/OZI/commit/0877e63c615d2e39630dc3e0dcb08729c1854c40))


## v0.0.21 (2023-07-02)

### Other

* 🔨(meson.options): Added python version options.
Formerly these were hardcoded. ([`98dc031`](https://github.com/rjdbcm/OZI/commit/98dc03107c9ea202d92ba599a9516b58e5c76496))

* :technologist:(README.rst): Added bugfix section. ([`d522338`](https://github.com/rjdbcm/OZI/commit/d522338daf72bea127a3636a4bc61bcd13b04f49))

* 🧑‍💻: Update issue templates

Add feature request and bug report templates. ([`24a9834`](https://github.com/rjdbcm/OZI/commit/24a9834112253dbf08114d4fb71735253797a11d))

* 📝 README.rst: add OpenSSF badge. ([`334bdb9`](https://github.com/rjdbcm/OZI/commit/334bdb937133b0795cf34c9a8cf51895e3140985))

* 🧑‍💻 README.rst: Add Contributing section. ([`14b8b5a`](https://github.com/rjdbcm/OZI/commit/14b8b5a813d65d711227e8c6b44cdd7b66ff832e))

* 📝 README.rst: Remove hanging markdown. ([`e49d3a0`](https://github.com/rjdbcm/OZI/commit/e49d3a0b2462d3ba83c38397774d8e137a14489c))

* 📝 README.rst: Fix FOSSA badge. ([`08b31f7`](https://github.com/rjdbcm/OZI/commit/08b31f731306aaad06f771ea433b9738d968ec23))

* 📝README.rst: fix FOSSA badge. ([`b054f57`](https://github.com/rjdbcm/OZI/commit/b054f5757dbac829b0e5d49e4488665d5b7c9367))

* Merge pull request #1 from fossabot/add-license-scan-badge

Add license scan report and status ([`392de25`](https://github.com/rjdbcm/OZI/commit/392de25c26136925f77ddb2a9ea898f2ab085c73))

* Add license scan report and status

Signed off by: fossabot &lt;badges@fossa.com&gt; ([`3814fcb`](https://github.com/rjdbcm/OZI/commit/3814fcbcdff6622771c67f9a036b47b5c589b13c))

* 🚑️(tox): correct meson build options.
Now using ozi-bootstrap=enabled. ([`30712f5`](https://github.com/rjdbcm/OZI/commit/30712f5204cadbb5c218bccba47d44cd34af02ac))

* 👷(semantic-release): use textual changelog sections. ([`730b7ec`](https://github.com/rjdbcm/OZI/commit/730b7ec62cef8fdc7ef15391d1f15f1903244732))

* 🔨(semantic-release): git clean -dfX run pre_commit. ([`12c8de4`](https://github.com/rjdbcm/OZI/commit/12c8de45a6c36a18bc2ac2e66ef9be0ab50c081c))

* 🔊 Update CHANGELOG.md ([`1f3bf64`](https://github.com/rjdbcm/OZI/commit/1f3bf645408da6373bf12b05565fa03e0f0d2367))

* PKG-INFO Updated ([`c1c04d9`](https://github.com/rjdbcm/OZI/commit/c1c04d9bd89823b9d8c48eb422c5bc6a8360e883))


## v0.0.20 (2023-06-25)

### Other

* 🔨 drop PKG-INFO from pre_commit. ([`39a908d`](https://github.com/rjdbcm/OZI/commit/39a908d39cc747a5c33082bddf833e9fe2b9075b))

* 🔨 fix stash strategy.. ([`a20807e`](https://github.com/rjdbcm/OZI/commit/a20807e23f3555b8306523cc3da8ebf84ef575f2))

* PKG-INFO Updated ([`5de6296`](https://github.com/rjdbcm/OZI/commit/5de6296f33c58f751c97551b9b69f1f786c04409))


## v0.0.19 (2023-06-25)

### Other

* 🔨 stash after push release. ([`4169813`](https://github.com/rjdbcm/OZI/commit/4169813270f1e6783da08a914904b53776b3b49c))


## v0.0.18 (2023-06-25)

### Other

* 🔨 turn back on repo build. ([`4137e1e`](https://github.com/rjdbcm/OZI/commit/4137e1e2822dfce5eb0d47ac23519515422181db))


## v0.0.17 (2023-06-25)

### Other

* 🔊 Add changes for 0.0.16. ([`62e9641`](https://github.com/rjdbcm/OZI/commit/62e9641e4e0505e664449110d0a46b5e3a1f794f))


## v0.0.16 (2023-06-25)

### Other

* 🔊 add 0.0.16 changes. ([`c765e65`](https://github.com/rjdbcm/OZI/commit/c765e6545bbdacde2a76021e9311f3cf334e7065))

* 🔥 git rm -r --cached subprojects.dev ([`26590cc`](https://github.com/rjdbcm/OZI/commit/26590cc76e5adf543f5231d89279c8dd1c9cefb1))

* Add gitignore. ([`bf295f4`](https://github.com/rjdbcm/OZI/commit/bf295f4ad8b133cbe98a987ec09bd7bee3572428))

* 🔨 Just stash PKG-INFO. ([`40db643`](https://github.com/rjdbcm/OZI/commit/40db6433be6f26b802a4fc4b85393cf42b9c2131))

* PKG-INFO Updated ([`0916ffd`](https://github.com/rjdbcm/OZI/commit/0916ffd48343b54474bde97d77d52f32fd7b712c))


## v0.0.15 (2023-06-24)

### Other

* 🔨 just use pypi repo namespace. ([`926bce6`](https://github.com/rjdbcm/OZI/commit/926bce6f8a1ab70cb5ccb6041fbc3452dba10c17))

* PKG-INFO Updated ([`cf1df31`](https://github.com/rjdbcm/OZI/commit/cf1df31248d4cf5aae72380b928f9c3e0ddaf79f))


## v0.0.14 (2023-06-24)

### Other

* PKG-INFO Updated ([`8001504`](https://github.com/rjdbcm/OZI/commit/8001504dfe277eff8b16ea07fe5987feb0754968))


## v0.0.13 (2023-06-24)

### Other

* 🔨 fix must be a file: build/meson-dist/*.tar.gz foreals. ([`ce2e8f0`](https://github.com/rjdbcm/OZI/commit/ce2e8f0e6ccb4160e128de2759c921839ca413db))

* PKG-INFO Updated ([`382ed8a`](https://github.com/rjdbcm/OZI/commit/382ed8a40a26b47c7451b632a33ecc43b1cc1dd0))


## v0.0.12 (2023-06-24)

### Other

* 🔨 fix must be a file: build/meson-dist/*.tar.gz. ([`03de6fc`](https://github.com/rjdbcm/OZI/commit/03de6fcca53c6f0edcce3e6d3a0f44c62ab60c87))

* PKG-INFO Updated ([`7ed30a3`](https://github.com/rjdbcm/OZI/commit/7ed30a3f486f9bf1011d849b4f910dbc2d1a24fc))


## v0.0.11 (2023-06-24)

### Other

* PKG-INFO Updated ([`55f6ccb`](https://github.com/rjdbcm/OZI/commit/55f6ccb170a0c652a344a944b119ca06088bd477))


## v0.0.10 (2023-06-24)

### Other

* 🔨no initial stash clear. ([`5c9e106`](https://github.com/rjdbcm/OZI/commit/5c9e106c178d8a8fcc4555a339827fe30862fa3e))

* PKG-INFO Updated ([`79cd462`](https://github.com/rjdbcm/OZI/commit/79cd462d26dba50421267a1eaf0ebc60f2893495))


## v0.0.9 (2023-06-24)

### :pencil2:

* :pencil2: git add CHANGELOG.md. ([`6575895`](https://github.com/rjdbcm/OZI/commit/65758958a899629f680b37b930ac34377dfd0b59))


## v0.0.8 (2023-06-24)

### Other

* 👷 add summary to metadata. ([`a97a05b`](https://github.com/rjdbcm/OZI/commit/a97a05b1de54c140bde7ded8029c2a9ffa1be79c))

* 👷 use pkg-info. ([`b0cd371`](https://github.com/rjdbcm/OZI/commit/b0cd371fdbafc1ecce4274722586fa07181e351e))

* 👷 fix CI changelog commit. ([`3b8288b`](https://github.com/rjdbcm/OZI/commit/3b8288b15b9a8a46e6a9c3866942262508e98530))

* PKG-INFO Updated ([`1db763d`](https://github.com/rjdbcm/OZI/commit/1db763d5e978742e1848b0cf83b773e39a9efe98))


## v0.0.7 (2023-06-24)

### Other

* 🍱 fix readme rendering. ([`d27ffc9`](https://github.com/rjdbcm/OZI/commit/d27ffc925a80e910b6cf6d2aa3f18e51d3cdad24))

* PKG-INFO Updated ([`88d8722`](https://github.com/rjdbcm/OZI/commit/88d87224d4e8b5c734ef0791c5707df0f3441dd1))


## v0.0.6 (2023-06-24)

### :pencil2:

* :pencil2: to_lower ([`5c48087`](https://github.com/rjdbcm/OZI/commit/5c48087f08373aeeabd18b1e2899280a242f0a51))

* :pencil2: lower case folder. ([`dfaaaba`](https://github.com/rjdbcm/OZI/commit/dfaaababe369809efce86a14aba13684751bc345))

* :pencil2: fix wrap file usage. ([`b4157b1`](https://github.com/rjdbcm/OZI/commit/b4157b19fa86d2f11f1ba97cdb8799556244cbd4))

* :pencil2: fix typo in build script. ([`c0fa9c8`](https://github.com/rjdbcm/OZI/commit/c0fa9c86a37626dcb41eb2c8300339c5d82a773e))

### Other

* 📌 Add requirements to build. ([`fd83e88`](https://github.com/rjdbcm/OZI/commit/fd83e88c51a0396b91e776b64f11692ed83d96d5))

* ✏️ add config files to build. ([`f732ed1`](https://github.com/rjdbcm/OZI/commit/f732ed190d46e4c53d7c87c0f9aa2427c1479b0e))

* ⚰️ No Notice required. ([`ca50d4f`](https://github.com/rjdbcm/OZI/commit/ca50d4f89b3f6c905bae26928b0a24d5c7f7a39c))

* 📝 Add CHANGELOG. ([`bf62b43`](https://github.com/rjdbcm/OZI/commit/bf62b43d5fb3241b863177380de74dedadf8720d))

* 🔨 Add bootstrapping ozi.wrap. ([`c9a076e`](https://github.com/rjdbcm/OZI/commit/c9a076e7c0625df32bd1622a422896ff251327c2))

* 🔧 add bootstrapping script to build. ([`2215826`](https://github.com/rjdbcm/OZI/commit/221582631c5b70db905bb3e2980a61a1e86212b3))

* PKG-INFO Updated ([`c9f3a62`](https://github.com/rjdbcm/OZI/commit/c9f3a62e30f9deda448bd245ff71e6813fd84c2d))


## v0.0.5 (2023-06-24)

### :pencil2:

* :pencil2: fix typo is_enabled. ([`a966905`](https://github.com/rjdbcm/OZI/commit/a966905031826b9cfa78edcb8713831431a9676b))

### Other

* 🙈 add .gitignore!!! ([`04e2eb4`](https://github.com/rjdbcm/OZI/commit/04e2eb40a954935a251f8c65574187c013448a74))


## v0.0.4 (2023-06-24)

### Other

* 👷 PKG-INFO updated with version! ([`3a04107`](https://github.com/rjdbcm/OZI/commit/3a04107ce11622e6ba788915c5d57ad958e93c60))

* 👷 no find_program override for now. ([`a495f3d`](https://github.com/rjdbcm/OZI/commit/a495f3d8f9a7e0e9344594215c6b319091547c38))

* 🚧👷  add distrbution related build bootstrapping. ([`3fbda2a`](https://github.com/rjdbcm/OZI/commit/3fbda2aef99b4746cdd321c87c4852e11e260109))

* Create meson.build ([`51727a6`](https://github.com/rjdbcm/OZI/commit/51727a69709131eeb175d1adba4539966b211ec9))

* Update ozi.wrap ([`9b9e2cd`](https://github.com/rjdbcm/OZI/commit/9b9e2cd9ff00904636ec8f1610e52e40d40e2ab0))

* Update meson.build

add meson.override_find_program, remove todo wrap. ([`f01c0c7`](https://github.com/rjdbcm/OZI/commit/f01c0c7607d53f6ab824caa1954af2b4e58c4c6d))

* Create PKG-INFO ([`7b9ece4`](https://github.com/rjdbcm/OZI/commit/7b9ece48fd69f89d7f8849f7d0291746f2dc540a))

* Update pyproject.toml ([`5260ee9`](https://github.com/rjdbcm/OZI/commit/5260ee98ad383b1adaa9c934657c4e16375b2372))

* Create ozi.wrap ([`279ec4b`](https://github.com/rjdbcm/OZI/commit/279ec4bd2ff5247c61b8d8c6b6184be1467f18c7))

* Add files via upload ([`9fbabca`](https://github.com/rjdbcm/OZI/commit/9fbabca05a29e8350187f86d1ff4dfb4259b37be))

* Add files via upload ([`22e4055`](https://github.com/rjdbcm/OZI/commit/22e40555c85c9d36e6fef06086b81874057edf4c))

* Create tox.ini ([`2ab7c48`](https://github.com/rjdbcm/OZI/commit/2ab7c48db0529f6ba4149ba0b8df18513a813d45))

* Create workflow.yml ([`318c0c1`](https://github.com/rjdbcm/OZI/commit/318c0c19dfbbb1f3d108cb3ba4ddce6fcc14945b))

* Add files via upload ([`b2c7a93`](https://github.com/rjdbcm/OZI/commit/b2c7a93e2da6835c6dbfa07f72ace9179c5af8ce))

* Create scm_version_snip.py ([`b7ec6a7`](https://github.com/rjdbcm/OZI/commit/b7ec6a78516491a659fb48550122631b8d97070c))

* Add files via upload ([`beefc2c`](https://github.com/rjdbcm/OZI/commit/beefc2c1fbec5997af3445a3db653295bda86625))

* Create __init__.py ([`3f83f68`](https://github.com/rjdbcm/OZI/commit/3f83f68b731608d0462fb570aa8ea3a1e9915029))

* Root folder sync to blastpipe-0.4.20 ([`b05b497`](https://github.com/rjdbcm/OZI/commit/b05b4977180014aae1e5276d9588fa089ab95ae2))
