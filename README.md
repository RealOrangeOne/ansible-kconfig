# Ansible kconfig

Ansible module to manage KDE's configuration through [kconfig](https://develop.kde.org/docs/use/configuration/introduction/).

## Requirements

This module works by wrapping `kreadconfig5` and `kwriteconfig5`. These need to be installed and on your `$PATH`. THey should come with any KDE install.


## Installation

Install the `realorangeone.kconfig` collection from Ansible Galaxy:

```
ansible-galaxy collection install realorangeone.kconfig
```

## Use

This collection defines a single module `kconfig` which can be used to read or write config:

### Writing configuration parameters

```yaml
- name: Set animation duration
  kconfig:
    group: KDE
    key: AnimationDurationFactor
    value: 0.5
```

### Reading configuration parameters

```yaml
- name: Get keyboard shortcuts for krunner
  kconfig:
    state: read
    file: kglobalshortcutsrc
    group: org.kde.krunner.desktop
    key: _launch
```

### Parameters

See the `DOCUMENTATION` parameter in [`kconfig.py`](./plugins/modules/kconfig.py) for full documentation.
