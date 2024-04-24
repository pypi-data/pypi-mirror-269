# Commitizen Lightroom Plug-in Version Provider

A commitizen version provider for Lua Lightroom plug-ins, which store the version in a Lua table, stating major, minor, and revision explicitly.

## Requirements

Your Lightroom plug-in contains a file `Info.lua` in the format:

    return {
        VERSION = { major = 1, minor = 1, revision = 0, },
        LrSdkVersion = 9.0,
        ...
    }

## Installation

    pip install commitizen-lrplugin

## Usage

### Configuration

There are several ways to configure commitizen.
This example setup uses a local installation of commitizen via python and works  with `yaml` configuration files, but any other format as stated in the commitizen documentation works as well.

In your Lightroom plug-in source folder, create a `.cz.yaml`:

    ---
    commitizen:
      name: cz_conventional_commits
      tag_format: $version
      update_changelog_on_bump: true
      version_provider: "commitizen-lrplugin"
      version_scheme: semver

Note: it's not necessary to include a `version` key inside the config file. Best practice is to keep the version in a single source of truth, which is the `Info.lua`.

### Bumping versions

Now

    cz bump

will read the current version from `Info.lua`, increase it accordingly and write it back to the same file.

## Contribution

Contributions, issues and feature requests are welcome.
For major changes, please open an issue first to discuss what you would like to change.

- Fork the project
- Clone the fork
- Add your changes and update tests as appropriate.
- Create a pull request

## License

This project is [MIT](LICENSE) licensed.
