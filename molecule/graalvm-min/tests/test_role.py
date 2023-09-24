import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('command', [
    'java',
    'javac'
])
def test_java_tools(host, command):

    graalvmsh_file = host.file("/etc/profile.d/graalvm.sh")
    assert graalvmsh_file.exists
    assert oct(graalvmsh_file.mode) == '0o644'

    cmd = host.run('. /etc/profile && ' + command + ' -version')
    assert cmd.rc == 0

    if command == 'javac':
        assert ' 17.0.' in cmd.stdout
    if command == 'java':
        assert ' 17.0.' in cmd.stderr
        assert 'OpenJDK Runtime Environment GraalVM CE' in cmd.stderr


@pytest.mark.parametrize('version_dir_pattern', [
    'jdk-[0-9]+.[0-9]+.[0-9]+$'
])
def test_graalvm_installed(host, version_dir_pattern):

    graalvm_home = host.check_output('find %s | grep --color=never -E %s',
                                     '/opt/graalvm/',
                                     version_dir_pattern)

    java_exe = host.file(graalvm_home + '/bin/java')

    assert java_exe.exists
    assert java_exe.is_file
    assert java_exe.user == 'root'
    assert java_exe.group == 'root'
    assert oct(java_exe.mode) == '0o755'

    gu_file = host.file(graalvm_home + '/bin/gu')
    assert gu_file.exists
    assert oct(gu_file.mode) == '0o777'


def test_gu(host):

    cmd = host.run('. /etc/profile && gu --help')
    assert cmd.rc == 0
    assert 'GraalVM Component Updater v2.0.0' in cmd.stdout
    assert '' in cmd.stderr


@pytest.mark.parametrize('fact_group_name', [
    'graalvm'
])
def test_facts_installed(host, fact_group_name):
    fact_file = host.file('/etc/ansible/facts.d/' + fact_group_name + '.fact')

    assert fact_file.exists
    assert fact_file.is_file
    assert fact_file.user == 'root'
    assert fact_file.group == 'root'
    assert oct(fact_file.mode) == '0o644'
