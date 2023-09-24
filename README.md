Ansible Role: GraalVM
=====================

[![Build Status](https://github.com/arolfes/ansible-role-graalvm/workflows/molecule%20tests/badge.svg?branch=master)](https://github.com/arolfes/ansible-role-graalvm/actions?query=branch%3Amaster+workflow%3A%22molecule+tests%22)
[![Ansible Galaxy](https://img.shields.io/badge/ansible--galaxy-arolfes.graalvm-blue.svg)](https://galaxy.ansible.com/arolfes/graalvm)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/arolfes/ansible-role-graalvm/master/LICENSE)


Role to install the GraalVM CE.

Requirements
------------

* Ansible >= 5 (Ansible Core >= 2.12)

* Linux Distribution

    * Debian Family

        * Ubuntu

            * Focal (20.04)
            * jammy (22.04)

        * Debian

            * Buster (10)
            * bullseye (11)
            * bookworm (12)

    * RedHat Family

        * Fedora

            * 37
            * 38

    * SUSE Family

        * openSUSE

            * 15.0
            * 15.1
            * 15.2
            * 15.3
            * 15.4
            * 15.5

    * Note: other versions are likely to work but have not been tested.

Role Variables
--------------

The following variables will change the behavior of this role (default values
are shown below):

```yaml
# specify the underlying community jdk version
# 17.0.7, 17.0.8, 20.0.1, 20.0.2 or 21.0.0
graalvm_java_version: '21.0.0'

# Base installation directory for any GraalVM distribution
graalvm_install_dir: '/opt/graalvm'

# Directory to store files downloaded for GraalVM installation on the remote box
graalvm_download_dir: "{{ x_ansible_download_dir | default(ansible_env.HOME + '/.ansible/tmp/downloads') }}"

# If this is the default installation, profile scripts will be written to set
# the GRAALVM_HOME environment variable
graalvm_is_default_installation: true

# If the graalvm bin directory should be added to PATH environment variable
# Effect is only when this is also the default installation
graalvm_add_to_path: true

# Location GraalVM installations packages can be found on the local box
# local packages will be uses in preference to downloading new packages.
graalvm_local_archive_dir: '{{ playbook_dir }}/files'

# Wether to use installation packages in the local archive (if available)
graalvm_use_local_archive: true

# The SHA-256 for the GraalVM redistributable
graalvm_redis_sha256sum:

# location for GraalVM download (e.g. https://example.com/provisioning/files)
# specify only when NOT downloading from directly github
graalvm_redis_mirror:

# File name for the GraalVM redistributable installation file
graalvm_redis_filename: "graalvm-community-jdk-{{ graalvm_java_version }}_linux-{{ graalvm_architecture }}_bin.tar.gz"

# Name of the group of Ansible facts relating this GraalVM installation.
#
# Override if you want use this role more than once to install multiple versions
# of GraalVM.
#
# e.g. graalvm_fact_group_name: graalvm_20_0_2
# would change the GraalVM home fact to:
# ansible_local.graalvm_20_0_2.general.home
graalvm_fact_group_name: graalvm

# Timeout for GraalVM download response in seconds
graalvm_download_timeout_seconds: 600

# choose the underlying architecture, x64 (means amd64) or arch64
graalvm_architecture: 'x64'
```

Supported GraalVM Versions
--------------------------

The following versions of graalvm community jdk are supported without any additional configuration

* 17.0.7
* 17.0.8
* 20.0.1
* 20.0.2
* 21.0.0

Supported architectures
-----------------------

* x64 (means amd64)
* aarch64

Example Playbooks
-----------------

By default this role will install the latest GraalVM CE that has been tested and is known to work with this role:

```yaml
- hosts: servers
  roles:
    - role: arolfes.graalvm
# results:
# new file /etc/profile.d/graalvm.sh
# content:
# GRAALVM_HOME=/opt/graalvm/jdk-21.0.0
# PATH=${GRAALVM_HOME}/bin:${PATH}
```

install an older version

```yaml
- hosts: servers
  roles:
    - role: arolfes.graalvm
      graalvm_java_version: '17.0.7'
```

If you don't want GraalVM in your Path variable set `graalvm_add_to_path` to `false`

```yaml
- hosts: servers
  roles:
    - role: arolfes.graalvm
      graalvm_add_to_path: false
```

if you don't want an `/etc/profile.d/graalvm.sh` file

```yaml
- hosts: servers
  roles:
    - role: arolfes.graalvm
      graalvm_is_default_installation: false
```

You can install the multiple versions of the GraalVM by using this role more than once:

```yaml
- hosts: servers
  roles:
    # the first role install graalvm-community-jdk-17.0.7
    - role: arolfes.graalvm
      graalvm_java_version: '17.0.7'
      graalvm_is_default_installation: false
      graalvm_fact_group_name: 'graalvm_java_17_0_7'

    # the second role install graalvm-community-jdk-21.0.0 and is set as default GraalVM
    - role: arolfes.graalvm
```

To perform an offline install, you need to specify a bit more information (i.e. graalvm_redis_filename and graalvm_redis_sha256sum). E.g. to perform an offline install of graalvm-19.3.2-java11:

```yaml
# Before performing the offline install, download
# `graalvm-community-jdk-21.0.0_linux-x64_bin.tar.gz` to
# `{{ playbook_dir }}/files/` on the local machine.
- hosts: servers
  roles:
    - role: arolfes.graalvm
      graalvm_java_version: '21.0.0'
      graalvm_use_local_archive: true
      graalvm_redis_filename: 'graalvm-community-jdk-21.0.0_linux-x64_bin.tar.gz'
      graalvm_redis_sha256sum: '7627a40c11341f743e3d937efe4fd3115b18bb3ca39380513b31d6775512d5b0'
```

Role Facts
----------

This role exports the following Ansible facts for use by other roles:

* `ansible_local.graalvm.general.java_version`

    * e.g. `21.0.0`

* `ansible_local.graalvm.general.home`

    * e.g. `/opt/graalvm/jdk-21.0.0`

Overriding `graalvm_fact_group_name` will change the names of the facts e.g.:

```yaml
graalvm_fact_group_name: graalvm_java_21_0_0
```

Would change the name of the facts to:

* `ansible_local.graalvm_java_21_0_0.general.version`
* `ansible_local.graalvm_java_21_0_0.general.java_version`
* `ansible_local.graalvm_java_21_0_0.general.home`

Development & Testing
---------------------

This project uses [Molecule](http://molecule.readthedocs.io/) to aid in the
development and testing; the role is unit tested using
[Testinfra](http://testinfra.readthedocs.io/) and
[pytest](http://docs.pytest.org/).

To develop or test you'll need to have installed the following:

* Linux (e.g. [Ubuntu](http://www.ubuntu.com/))
* [Docker](https://www.docker.com/)
* [Python](https://www.python.org/) (including python-pip)
* [Ansible](https://www.ansible.com/)
* [Molecule](http://molecule.readthedocs.io/)

Because the above can be tricky to install, this project includes
[Molecule Wrapper](https://github.com/gantsign/molecule-wrapper). Molecule
Wrapper is a shell script that installs Molecule and it's dependencies (apart
from Linux) and then executes Molecule with the command you pass it.

To test this role using Molecule Wrapper run the following command from the
project root:

```bash
./moleculew test
```

Note: some of the dependencies need `sudo` permission to install.

License
-------

MIT

Credits
-------

**Many Thanks** to John from Gantsign for providing molecule wrapper script and awesome ansible roles which are available over ansible-galaxy.


Author Information
------------------

Alexander Rolfes
