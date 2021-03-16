# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2020
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import, division, print_function

import os
import sys
import pytest

from pprint import pprint
__metaclass__ = type


# Facts will be gathered once and the result will be checked for accuracy and completeness throughout the test. It does not make sense to repeatedly gather facts on the same target per test. This is why there's one very large test instead of many small ones.

# the following values are defined in the module and could be changed later.
ZOS_ANSIBLE_FACTS_DICT = 'zos_ansible_facts'
FACTS_PREFIX = 'ansible_'


def test_fact_gather(ansible_zos_module):
    # assert 1 == 0
    hosts = ansible_zos_module
    # params = dict(gather_subset=all)
    # try:

    results = hosts.all.zos_gather_facts()
    for result in results.contacted.values():
        print(result)
        # something was returned -- most basic test case.
        assert len(result.get(ZOS_ANSIBLE_FACTS_DICT)) > 0

        # base collectors:

        # PlatformFactCollector
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX+'architecture') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'domain') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'fqdn') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'hostname') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'kernel') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'kernel_version') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'machine') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'nodename') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'python_version') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'system') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'userspace_bits') is not None

        # DistributionFactCollector
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'distribution') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'distribution_release') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'distribution_version') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'os_family') is not None

        # general collectors:

        # PythonFactCollector
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'python') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'python').get('executable') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'python').get('has_sslcontext') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'python').get('type') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'python').get('version') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'python').get('version').get('major') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'python').get('version').get('micro') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'python').get('version').get('minor') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'python').get('version').get('releaselevel') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'python').get('version').get('serial') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'python').get('version_info') is not None

        # ServiceMgrFactCollector
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'service_mgr') is not None

        # DateTimeFactCollector
        assert len(result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'date_time')) > 0

        # checking a few select ones here instead of ALL fields of datetime
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'date_time').get('date') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'date_time').get('day') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'date_time').get('epoch') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'date_time').get('time') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'date_time').get('weekday_number') is not None

        # EnvFactCollector
        assert len(result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'env')) > 0

        # checking a few select ones here instead of ALL fields of datetime
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'env').get('PATH') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'env').get('PYTHONPATH') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'env').get('SHELL') is not None

        # SshPubKeyFactCollector
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'ssh_host_key_dsa_public') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'ssh_host_key_ecdsa_public') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'ssh_host_key_rsa_public') is not None

        # UserFactCollector
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'effective_group_id') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'effective_user_id') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'real_group_id') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'real_user_id') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'user_dir') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'user_gecos') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'user_gid') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'user_id') is not None
        assert result.get(ZOS_ANSIBLE_FACTS_DICT).get(FACTS_PREFIX + 'user_shell') is not None


        # assert result.get("zos_ansible_facts").get("ansible_os_family") is not None
        # # a specific value was returned at a specific key
        # assert result.get("zos_ansible_facts").get("ansible_hostname") == 'EC33018A'

        # zos collected facts
        # assert result.get("zos_ansible_facts").get("ansible_z_symbols").get('rc') == 0