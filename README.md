Ansible Role: GraalVM
=====================

[![Build Status](https://travis-ci.org/arolfes/ansible-role-graalvm.svg?branch=master)](https://travis-ci.org/github/arolfes/ansible-role-graalvm)
[![Ansible Galaxy](https://img.shields.io/badge/ansible--galaxy-arolfes.graalvm-blue.svg)](https://galaxy.ansible.com/arolfes/graalvm)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/arolfes/ansible-role-graalvm/master/LICENSE)


Role to install the GraalVM CE.

**Important:** This ansible role is based on [GANTSIGN ansible-role-java](https://github.com/gantsign/ansible-role-java)

**Thanks** a lot to John and Gantsign for providing molecule wrapper script and awesome ansible roles which are available over ansible-galaxy.

Requirements
------------

* Ansible >= 2.8

* Linux Distribution

    * Debian Family

        * Ubuntu

            * Focal (20.04)
            * Bionic (18.04)

        * Debian

            * Stretch (9)
            * Buster (10)

    * RedHat Family

        * CentOS

            * 7
            * 8

        * Fedora

            * 31

    * SUSE Family

        * openSUSE

            * 15.1

    * Note: other versions are likely to work but have not been tested.

Role Variables
--------------

The following variables will change the behavior of this role (default values
are shown below):

```yaml
# specify the underlying java version
# 8 or 11
graalvm_java_version: '11'

# GraalVM version number
graalvm_version: '20.1.0'

# Base installation directory for any GraalVM distribution
graalvm_install_dir: '/opt/graalvm'

# Directory to store files downloaded for GraalVM installation on the remote box
graalvm_download_dir: "{{ x_ansible_download_dir | default(ansible_env.HOME + '/.ansible/tmp/downloads') }}"

# If this is the default installation, profile scripts will be written to set
# the GRAALVM_HOME environment variable
graalvm_is_default_installation: true

# If this graalvm bin director should be add to PATH environment variable
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
graalvm_redis_filename: "graalvm-ce-java{{ graalvm_java_version }}-linux-amd64-{{ graalvm_version }}.tar.gz"

# Name of the group of Ansible facts relating this GraalVM installation.
#
# Override if you want use this role more than once to install multiple versions
# of GraalVM.
#
# e.g. graalvm_fact_group_name: graalvm_19.3
# would change the GraalVM home fact to:
# ansible_local.graalvm_19.3.general.home
graalvm_fact_group_name: graalvm

# Timeout for GraalVM download response in seconds
graalvm_download_timeout_seconds: 600
```

Supported GraalVM Versions
--------------------------

The following versions of GraalVM are supported without any additional configuration for java 8 and java 11

* 19.3.0
* 19.3.0.2
* 19.3.1
* 19.3.2
* 20.0.0
* 20.1.0


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
# GRAALVM_HOME=/opt/graalvm/graalvm-20.1.0-java11
# PATH=${GRAALVM_HOME}/bin:${PATH}
```

install an older version

```yaml
- hosts: servers
  roles:
    - role: arolfes.graalvm
      graalvm_java_version: '8'
      graalvm_version: '19.3.2'
```

install 2 GraalVMs one based on jdk8 and one based on 11 and set 11 as default

```yaml
- hosts: servers
  roles:
    - role: arolfes.graalvm
      graalvm_java_version: '8'
      graalvm_is_default_installation: false
      graalvm_fact_group_name: 'graalvm-java8'

    - role: arolfes.graalvm
```

You can install the multiple versions of the GraalVM by using this role more than once:

```yaml
- hosts: servers
  roles:
    - role: arolfes.graalvm
      graalvm_java_version: '8'
      graalvm_is_default_installation: false
      graalvm_fact_group_name: 'graalvm-java8'

    - role: arolfes.graalvm
```

To perform an offline install, you need to specify a bit more information (i.e. graalvm_redis_filename and graalvm_redis_sha256sum). E.g. to perform an offline install of graalvm-19.3.2-java8:

```yaml
# Before performing the offline install, download
# `graalvm-ce-java8-linux-amd64-19.3.2.tar.gz` to
# `{{ playbook_dir }}/files/` on the local machine.
- hosts: servers
  roles:
    - role: arolfes.graalvm
      graalvm_java_version: '8'
      graalvm_version: '19.3.2'
      graalvm_use_local_archive: true
      graalvm_redis_filename: 'graalvm-19.3.2-java8.tar.gz'
      graalvm_redis_sha256sum: '7598364ed9c4e5c0f936f37275172e84218984f25f51685ac2f501ac1a2d43bf'
```

Role Facts
----------

This role exports the following Ansible facts for use by other roles:

* `ansible_local.graalvm.general.version`

    * e.g. `20.1.0`

* `ansible_local.graalvm.general.java_version`

    * e.g. `11`

* `ansible_local.graalvm.general.home`

    * e.g. `/opt/graalvm/graalvm-20.1.0-java11`

Overriding `graalvm_fact_group_name` will change the names of the facts e.g.:

```yaml
graalvm_fact_group_name: graalvm_java8
```

Would change the name of the facts to:

* `ansible_local.graalvm_java8.general.version`
* `ansible_local.graalvm_java8.general.java_version`
* `ansible_local.graalvm_java8.general.home`

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

Author Information
------------------

Alexander Rolfes