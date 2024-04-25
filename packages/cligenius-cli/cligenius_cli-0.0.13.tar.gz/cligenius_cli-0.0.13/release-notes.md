# Release Notes

## Latest Changes

* 👷 Update tokens for tmate and latest changes. PR [#127](https://github.com/khulnasoft/cligenius-cli/pull/127) by [@khulnasoft](https://github.com/khulnasoft).
* 👷 Update token for latest changes. PR [#126](https://github.com/khulnasoft/cligenius-cli/pull/126) by [@khulnasoft](https://github.com/khulnasoft).
* ⬆️ Update pytest-cov requirement from ^2.8.1 to ^4.0.0. PR [#76](https://github.com/khulnasoft/cligenius-cli/pull/76) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Update mypy requirement from ^0.910 to ^1.0. PR [#83](https://github.com/khulnasoft/cligenius-cli/pull/83) by [@dependabot[bot]](https://github.com/apps/dependabot).

### Internal

* 👷 No longer publish cligenius-cli, as it's published by the cligenius repo. PR [#135](https://github.com/khulnasoft/cligenius-cli/pull/135) by [@khulnasoft](https://github.com/khulnasoft).
* 🔧 Add GitHub templates for discussions and issues, and security policy. PR [#133](https://github.com/khulnasoft/cligenius-cli/pull/133) by [@alejsdev](https://github.com/alejsdev).
* 👷 Update latest-changes GitHub Action. PR [#130](https://github.com/khulnasoft/cligenius-cli/pull/130) by [@khulnasoft](https://github.com/khulnasoft).

## 0.0.13

### Upgrades

* ✨ Refactor to make Cligenius CLI compatible with (and require) Cligenius `>=0.4.0` and Click `8.x.x`. Initial PRs [#67](https://github.com/khulnasoft/cligenius-cli/pull/67) by [@cdcadman](https://github.com/cdcadman) and [#82](https://github.com/khulnasoft/cligenius-cli/pull/82) by [@omBratteng](https://github.com/omBratteng).

### Internal

* 💚 Fix latest-changes GitHub Action, strike two ⚾. PR [#97](https://github.com/khulnasoft/cligenius-cli/pull/97) by [@khulnasoft](https://github.com/khulnasoft).
* 💚 Fix latest-changes release notes GitHub Action. PR [#96](https://github.com/khulnasoft/cligenius-cli/pull/96) by [@khulnasoft](https://github.com/khulnasoft).
* 📝 Update badges on README. PR [#94](https://github.com/khulnasoft/cligenius-cli/pull/94) by [@khulnasoft](https://github.com/khulnasoft).
* 👷 Tweak latest-changes GitHub Action when running as a workflow dispatch. PR [#98](https://github.com/khulnasoft/cligenius-cli/pull/98) by [@khulnasoft](https://github.com/khulnasoft).
* ⬆️ Enable tests and classifiers for Python 3.11. PR [#95](https://github.com/khulnasoft/cligenius-cli/pull/95) by [@khulnasoft](https://github.com/khulnasoft).
* 👷 Migrate CI coverage to Smokeshow and include alls-green. PR [#93](https://github.com/khulnasoft/cligenius-cli/pull/93) by [@khulnasoft](https://github.com/khulnasoft).
* 👷 Upgrade GitHub Actions, add funding config. PR [#92](https://github.com/khulnasoft/cligenius-cli/pull/92) by [@khulnasoft](https://github.com/khulnasoft).
* 👷 Upgrade Dependabot, include GitHub Actions. PR [#86](https://github.com/khulnasoft/cligenius-cli/pull/86) by [@khulnasoft](https://github.com/khulnasoft).
* ♻️ Refactor build system to use Hatch instead of Poetry. PR [#85](https://github.com/khulnasoft/cligenius-cli/pull/85) by [@khulnasoft](https://github.com/khulnasoft).
* ⬆️ Update flake8 requirement from ^3.7.9 to ^4.0.1. PR [#52](https://github.com/khulnasoft/cligenius-cli/pull/52) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Update pytest requirement from ^6.0.1 to ^7.0.1. PR [#62](https://github.com/khulnasoft/cligenius-cli/pull/62) by [@dependabot[bot]](https://github.com/apps/dependabot).

## 0.0.12

* ✨ Move CI to GitHub Actions, remove dependency on `importlib-metadata`. This would fix use cases that also depend on `importlib-metadata` and could have conflicts, like installing `mkdocs`, as now `cligenius-cli` no longer depends on `importlib-metadata`. PR [#48](https://github.com/khulnasoft/cligenius-cli/pull/48) by [@khulnasoft](https://github.com/khulnasoft).

## 0.0.11

* 🐛 Fix latest changes GitHub Action. PR [#34](https://github.com/khulnasoft/cligenius-cli/pull/34) by [@khulnasoft](https://github.com/khulnasoft).
* ⬆️ Update importlib-metadata requirement from ^1.5 to >=1.5,<3.0. PR [#29](https://github.com/khulnasoft/cligenius-cli/pull/29).
* 👷 Add Latest Changes GitHub Action. PR [#30](https://github.com/khulnasoft/cligenius-cli/pull/30) by [@khulnasoft](https://github.com/khulnasoft).
* ⬆️ Update black requirement from ^19.10b0 to ^20.8b1. PR [#28](https://github.com/khulnasoft/cligenius-cli/pull/28).
* ⬆️ Update pytest-xdist requirement from ^1.31.0 to ^2.1.0. PR [#27](https://github.com/khulnasoft/cligenius-cli/pull/27).

## 0.0.10

* ⬆️ Update pytest requirement from ^5.4.3 to ^6.0.1. PR [#22](https://github.com/khulnasoft/cligenius-cli/pull/22).
* Update tests with defaults. PR [#24](https://github.com/khulnasoft/cligenius-cli/pull/24).
* Add support for *CLI Arguments* with `help`. PR [#20](https://github.com/khulnasoft/cligenius-cli/pull/20) by [@ovezovs](https://github.com/ovezovs).
* ⬆ Upgrade Cligenius version to 0.3.0. PR [#13](https://github.com/khulnasoft/cligenius-cli/pull/13).
* ⬆️ Update mypy requirement from ^0.761 to ^0.782. PR [#18](https://github.com/khulnasoft/cligenius-cli/pull/18).
* ⬆️ Update pytest requirement from ^4.4.0 to ^5.4.3. PR [#16](https://github.com/khulnasoft/cligenius-cli/pull/16).
* ⬆️ Update isort requirement from ^4.3.21 to ^5.0.6. PR [#15](https://github.com/khulnasoft/cligenius-cli/pull/15).
* Update GitHub action issue-manager and add Dependabot. PR [#14](https://github.com/khulnasoft/cligenius-cli/pull/14).

## 0.0.9

* Upgrade Cligenius to `0.2.1`. PR [#9](https://github.com/khulnasoft/cligenius-cli/pull/9).

## 0.0.8

* Upgrade Cligenius to `0.1.1`. PR [#8](https://github.com/khulnasoft/cligenius-cli/pull/8).

## 0.0.7

* Upgrade Cligenius to version 0.1.0. PR [#7](https://github.com/khulnasoft/cligenius-cli/pull/7).

## 0.0.6

* Synchronize README with docs in [Cligenius - Cligenius CLI](https://cligenius.khulnasoft.com/cligenius-cli/) and update links. PR [#5](https://github.com/khulnasoft/cligenius-cli/pull/5).
* Upgrade **Cligenius** after re-implementing completion:
    * Add support for PowerShell in modern versions (e.g. Windows 10).
    * Fix support for user-provided completions.
    * Fix creation of sub-command `run` in each internal case.
    * PR [#4](https://github.com/khulnasoft/cligenius-cli/pull/4).

## 0.0.5

* Add support for [generating Markdown docs](https://github.com/khulnasoft/cligenius-cli#generate-docs) for **Cligenius** apps. PR [#3](https://github.com/khulnasoft/cligenius-cli/pull/3).

## 0.0.4

* Handle default Cligenius to extract and run in this priority:
    * App object from `--app` *CLI Option*.
    * Function to convert to a **Cligenius** app from `--func` *CLI Option*.
    * **Cligenius** app in a variable with a name of `app`, `cli`, or `main`.
    * The first **Cligenius** app available in the file, with any name.
    * A function in a variable with a name of `main`, `cli`, or `app`.
    * The first function in the file, with any name.
    * PR [#2](https://github.com/khulnasoft/cligenius-cli/pull/2).

## 0.0.3

* Add Travis CI. PR [#1](https://github.com/khulnasoft/cligenius-cli/pull/1).