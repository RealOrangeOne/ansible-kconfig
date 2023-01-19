from typing import Optional

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r"""
module: kconfig
author:
    - Jake Howard
short_description: Manage KDE's configuration through kconfig
description:
  - This module allows modification and reading of KDE's C(kconfig) configuration.
  - This module works by wrapping the C(kreadconfig5) and C(kwriteconfig5) CLI tools,
    which need to be on your C($PATH). These should come with any KDE install.
notes:
  - KDE sadly doesn't easily expose which keys and groups respond to which settings,
    so it will require some work to diff the C(~/config) directory yourself.
options:
  file:
    type: str
    required: false
    description:
      - The filename to read / write configuration from.
  group:
    type: str
    required: true
    description:
      - The group in the given I(file) to write into.
  key:
    type: str
    required: true
    description:
      - The key in the I(group) which is modified or read.
  value:
    type: str
    required: false
    description:
      - The value to set for the specified key.
      - Required for I(state=present).
  state:
    type: str
    required: false
    default: present
    choices: [ 'read', 'present' ]
    description:
      - The action to take upon the key/value.
"""

RETURN = r"""
value:
    description: value associated with the requested key
    returned: success, state was "read"
    type: str
"""


class KConfigWrapper:
    def __init__(self, module: AnsibleModule):
        self.module = module
        self.check_mode = module.check_mode

        self.write_config_bin = self.module.get_bin_path("kwriteconfig5", required=True)
        self.read_config_bin = self.module.get_bin_path("kreadconfig5", required=True)

    def read(self, file: Optional[str], group: str, key: str) -> Optional[str]:
        command = [self.read_config_bin, "--group", group, "--key", key]

        if file is not None:
            command.extend(["--file", file])

        rc, out, err = self.module.run_command(command)

        if rc != 0:
            self.module.fail_json(
                msg="kreadconfig5 failed while reading the value with error: %s" % err,
                out=out,
                err=err,
            )

        if out == "":
            value = None
        else:
            value = out.rstrip("\n")

        return value

    def write(self, file: Optional[str], group: str, key: str, value: str) -> bool:
        # If no change is needed (or won't be done due to check_mode), notify
        # caller straight away.
        if value == self.read(file, group, key):
            return False
        elif self.check_mode:
            return True

        command = [self.write_config_bin, "--group", group, "--key", key]

        if file is not None:
            command.extend(["--file", file])

        # The value must always be the last argument
        command.append(value)

        # Run the command and fetch standard return code, stdout, and stderr.
        rc, out, err = self.module.run_command(command)

        if rc != 0:
            self.module.fail_json(
                msg="kwriteconfig5 failed while write the value with error: %s" % err,
                out=out,
                err=err,
            )

        return True


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "state": {"default": "present", "choices": ["present", "read"]},
            "key": {
                "required": True,
                "type": "str",
            },
            "group": {
                "required": True,
                "type": "str",
            },
            "value": {"required": False, "type": "str", "default": None},
            "file": {"required": False, "type": "str", "default": None},
        },
        supports_check_mode=True,
    )

    params = module.params

    # If present state was specified, value must be provided.
    if params["state"] == "present" and params["value"] is None:
        module.fail_json(msg='State "present" requires "value" to be set.')

    kconfig = KConfigWrapper(module)

    if params["state"] == "read":
        value = kconfig.read(params["file"], params["group"], params["key"])
        module.exit_json(changed=False, value=value)
    elif params["state"] == "present":
        changed = kconfig.write(
            params["file"], params["group"], params["key"], params["value"]
        )
        module.exit_json(changed=changed)


if __name__ == "__main__":
    main()
