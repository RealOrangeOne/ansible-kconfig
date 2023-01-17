from ansible.module_utils.basic import AnsibleModule


class KConfigWrapper:
    def __init__(self, module: AnsibleModule):
        self.module = module
        self.check_mode = module.check_mode

        self.write_config_bin = self.module.get_bin_path('kwriteconfig5', required=True)
        self.read_config_bin = self.module.get_bin_path('kreadconfig5', required=True)

    def read(self, file, group, key):
        command = [self.read_config_bin, "--group", group, "--key", key]

        if file is not None:
            command.extend([
                "--file", file
            ])

        rc, out, err = self.module.run_command(command)

        if rc != 0:
            self.module.fail_json(
                msg='kreadconfig5 failed while reading the value with error: %s' % err,
                out=out,
                err=err
            )

        if out == '':
            value = None
        else:
            value = out.rstrip('\n')

        return value


def main():
    module = AnsibleModule(
        argument_spec={
            "state": {
                "default": "read",
                "choices": [
                    "read"
                ]
            },
            "key": {
                "required": True,
                "type": "str",
            },
            "group": {
                "required": True,
                "type": "str",
            },
            "value": {
                "required": False,
                "type": "str",
                "default": None
            },
            "file": {
                "required": False,
                "type": "str",
                "default": None
            }
        },
        supports_check_mode=True
    )

    kconfig = KConfigWrapper(module)

    params = module.params

    if params["state"] == "read":
        value = kconfig.read(params["file"], params["group"], params["key"])
        module.exit_json(changed=False, value=value)


if __name__ == "__main__":
    main()
