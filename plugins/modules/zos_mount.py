#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2020, 2021
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

__metaclass__ = type


DOCUMENTATION = r"""
---
module: zos_mount
author:
    - "Rich Parker (@richp405)"
short_description: Mount a z/OS Unix System Services (USS) file system data set.
description:
  - The module M(zos_mount) can mount a z/OS Unix System Services (USS) file system data set.
  - The I(src) data set must be unique and a Fully Qualified Name (FQN).
  - The I(path) will be created if needed.
options:
    path:
        description:
            - The absolute path name onto which the file system is to be mounted.
            - The I(path) is case sensitive and must be less than or equal 1023 characters long.
        type: str
        required: True
    src:
        description:
            - The zFS aggregate data set to be mounted.
        type: str
        required: True
    fs_type:
        description:
            - The type of file system that will be mounted.
            - The physical file systems data set format to perform the logical mount.
            - The I(fs_type) is required to be uppercase, any lower case characters will be converted to uppercase.
        type: str
        choices:
            - HFS
            - ZFS
            - NFS
            - TFS
        required: True
    state:
        description:
            - The desired status of the described mount (choice).
            - >
                If I(state=mounted) and I(src) is not in use, the module will add the file system entry to
                I(persistent/data_set_name) parmlib member if not present. The I(path) will be updated and the module
                will complete successfully with I(changed=True).
            - >
                If I(state=mounted) and I(src) is in use, the module will add the file system entry to
                I(persistent/data_set_name) parmlib member if not present. The I(path) will not be updated and the module
                will complete successfully with I(changed=False).
            - >
                If I(state=unmounted) and I(src) is in use, device will be unmounted.
                I(persistent/data_set_name) is not altered, even when provided.
                Module completes successfully with I(changed=True).
            - >
                If I(state=unmounted) and I(src) is not in use, no action taken.
                I(persistent/data_set_name) is not altered, even when provided.
                Module completes successfully with I(changed=False).
            - >
                If I(state=present), if makes sure device is in I(persistent/data_set_name), if provided.
                Returns I(changed=True) if I(persistent/data_set_name).
            - >
                If I(state=absent), this will un-mount and alse remove from I(persistent/data_set_name) if provided.
            - >
                If I(state=remounted) the device is unmounted and mounted again.
                I(persistent/data_set_name) is not altered, even when provided.
                Always returns I(changed=True).
        type: str
        choices:
            - absent
            - mounted
            - unmounted
            - present
            - remounted
        required: False
        default: mounted
    persistent:
        description:
            - Add/remove mount command entries to or from I(data_set_name)
        required: False
        type: dict
        suboptions:
            data_set_name:
                description:
                    - The data set name used for persisting a mount command.
                        Usually a BPXPRMxx file, or a copy.
                required: True
                type: str
            backup:
                description:
                    - Creates a backup file or backup data set for I(data_set_name), including the
                        timestamp information to ensure that you retrieve the original APF list
                        defined in I(data_set_name)".
                    - I(backup_name) can be used to specify a backup file name if I(backup=true).
                    - The backup file name will be return on either success or failure
                        of module execution such that data can be retrieved.
                required: false
                type: bool
                default: false
            backup_name:
                description:
                    - Specify the USS file name or data set name for the destination backup.
                    - If the source I(data_set_name) is a USS file or path, the backup_name name must be a
                        file or path name, and the USS file or path must be an absolute path name.
                    - If the source is an MVS data set, the backup_name must be
                        an MVS data set name.
                    - If the backup_name is not provided, the default backup_name
                        will be used. If the source is a USS file or path, the name of
                        the backup file will be the source file or path name appended
                        with a timestamp.
                        For example, C(/path/file_name.2020-04-23-08-32-29-bak.tar).
                    - If the source is an MVS data set, it will be a data set with a
                        random name generated by calling the ZOAU API. The MVS backup
                        data set recovery can be done by renaming it.
                required: false
                type: str
    tabcomment:
        description:
        - If provided, this is used in markers that surround the command in the I(persistent/data_set_name).
        - Markers are used to encapsulate the I(persistent/data_set_name) entry such that they can
            easily be understood and located.
        type: list
        required: False
    unmount_opts:
        description:
            - Describes how the unmount is to be performed.
        type: str
        choices:
            - DRAIN
            - FORCE
            - IMMEDIATE
            - NORMAL
            - REMOUNT
            - RESET
        required: False
        default: NORMAL
    mount_opts:
        description:
            - Options available to the mount.
            - If I(mount_opts=ro) on a mounted/remount, mount is performed read-only.
            - If I(mount_opts=same) and (unmount_opts=REMOUNT), mount is opened is same mode as previously.
            - If I(mount_opts=nowait), mount is performed asynchronously.
            - If I(mount_opts=nosecurity), Security checks are not enforced for files in this file system.
        type: str
        choices:
            - ro
            - rw
            - same
            - nowait
            - nosecurity
        required: False
        default: rw
    src_params:
        description:
            - Specifies a parameter string to be passed to the file system type.
            - The parameter format and content are specified by the file system type.
        type: str
        required: False
    tag_untagged:
        description:
            - If present, tags get written to any untagged file
            - When the file system is unmounted, the tags are lost.
            - If I(tag_untagged=NOTEXT) none of the untagged files in the file system are
                  automatically converted during file reading and writing.
            - If I(tag_untagged=TEXT) each untagged file is implicitly marked as
                  containing pure text data that can be converted.
            - If this flag is used, use of tag_ccsid is encouraged.
        type: str
        choices:
            - ''
            - TEXT
            - NOTEXT
        required: False
    tag_ccsid:
        description:
            - Coded Character Set Identifier to be used on untagged files.
            - https://www.ibm.com/support/knowledgecenter/SSLTBW_2.2.0/com.ibm.zos.v2r2.idad400/ccsids.htm
            - only required it I(tag_untagged=TEXT).
            - ccsid
                - Identifies the coded character set identifier to be implicitly
                  set for the untagged file. ccsid is specified as a decimal value
                  from 0 to 65535. However, when TEXT is specified, the value must
                  be between 0 and 65535. Other than this, the value is not
                  checked as being valid and the corresponding code page is not
                  checked as being installed.
        type: int
        required: False
    allow_uid:
        description:
            - >
              Specifies whether the SETUID and SETGID mode bits on executables in
              this file system are considered. Also determines whether the APF
              extended attribute or the Program Control extended attribute is
              honored.
            - >
              If I(allow_uid=True) the SETUID and SETGID mode bits are considered when a
              program in this file system is run. SETUID is the default.
            - >
              If I(allow_uid=False) the SETUID and SETGID mode bits are ignored when a
              program in this file system is run. The program runs as though the
              SETUID and SETGID mode bits were not set. Also, if you specify the
              NOSETUID option on MOUNT, the APF extended attribute and the Program Control
              Bit values are ignored.
        type: bool
        required: False
        default: True
    sysname:
        description:
            - >
              For systems participating in shared file system, I(sysname) specifies
              the particular system on which a mount should be performed. This
              system will then become the owner of the file system mounted. This
              system must be IPLed with SYSPLEX(YES).
            - >
              I(sysname) is a 1–8 alphanumeric name of a system participating in shared file system.
        type: str
        required: False
    automove:
        description:
            - >
              These parameters apply only in a sysplex where systems are exploiting
              the shared file system capability. They specify what happens to
              the ownership of a file system when a shutdown, PFS termination, dead
              system takeover, or file system move occurs. The default setting is
              AUTOMOVE where the file system will be randomly moved to another system
              (no system list used).
            - >
              I(automove=AUTOMOVE) indicates that ownership of the file system can be
              automatically moved to another system participating in a shared file system.
            - >
              I(automove=NOAUTOMOVE) prevents movement of the file system's ownership in some situations.
            - >
              I(automove=UNMOUNT) allows the file system to be unmounted in some situations.
        type: str
        choices:
            - AUTOMOVE
            - NOAUTOMOVE
            - UNMOUNT
        required: False
        default: AUTOMOVE
    automove_list:
        description:
            - >
              If(automove=AUTOMOVE), this option will be checked.
            - >
              This specifies the list of servers to include or exclude as destinations.
            - >
              None is a valid value, meaning 'move anywhere'.
            - >
              Indicator is either INCLUDE or EXCLUDE, which can also be abbreviated as I or E.
        type: str
        required: False
"""

EXAMPLES = r"""
- name: Mount a filesystem.
  zos_mount:
    src: SOMEUSER.VVV.ZFS
    path: /u/omvsadm/core
    fs_type: ZFS
    state: mounted

- name: Unmount a filesystem.
  zos_mount:
    src: SOMEUSER.VVV.ZFS
    path: /dontcare
    fs_type: ZFS
    state: unmounted
    unmount_opts: REMOUNT
    opts: same

- name: Mount a filesystem readonly.
  zos_mount:
    src: SOMEUSER.VVV.ZFS
    path: /u/omvsadm/core
    fs_type: ZFS
    state: mounted
    mount_opts: ro

- name: Mount a filesystem and record change in BPXPRMAA.
  zos_mount:
    src: SOMEUSER.VVV.ZFS
    path: /u/omvsadm/core
    fs_type: ZFS
    state: mounted
    persistent:
        data_set_name: SYS1.PARMLIB(BPXPRMAA)
    tabcomment: For Tape2 project

- name: Mount a filesystem and record change in BPXPRMAA after backing up to BPXPRMAB.
  zos_mount:
    src: SOMEUSER.VVV.ZFS
    path: /u/omvsadm/core
    fs_type: ZFS
    state: mounted
    persistent:
        data_set_name: SYS1.PARMLIB(BPXPRMAA)
        backup: Yes
        backup_name: SYS1.PARMLIB(BPXPRMAB)
    tabcomment: For Tape2 project

- name: Mount a filesystem ignoring uid/gid values.
  zos_mount:
    src: SOMEUSER.VVV.ZFS
    path: /u/omvsadm/core
    fs_type: ZFS
    state: mounted
    allow_uid: no

- name: Mount a filesystem asynchronously (don't wait for completion).
  zos_mount:
    src: SOMEUSER.VVV.ZFS
    path: /u/omvsadm/core
    fs_type: ZFS
    state: mounted
    opts: nowait

- name: Mount a filesystem with no security checks.
  zos_mount:
    src: SOMEUSER.VVV.ZFS
    path: /u/omvsadm/core
    fs_type: ZFS
    state: mounted
    mount_opts: nosecurity

- name: Mount a filesystem, limiting automove to 4 devices.
  zos_mount:
    src: SOMEUSER.VVV.ZFS
    path: /u/omvsadm/core
    fs_type: ZFS
    state: mounted
    automove: AUTOMOVE
    automove_list: I,DEV1,DEV2,DEV3,DEV9

- name: Mount a filesystem, limiting automove to all except 4 devices.
  zos_mount:
    src: SOMEUSER.VVV.ZFS
    path: /u/omvsadm/core
    fs_type: ZFS
    state: mounted
    automove: AUTOMOVE
    automove_list: EXCLUDE,DEV4,DEV5,DEV6,DEV7

"""

RETURN = r"""
path:
    description: The absolute path name onto which the file system is to be mounted.
    returned: always
    type: str
    sample: /u/omvsadm/core
src:
    description: The file in zos that is to be mounted.
    returned: always
    type: str
    sample: SOMEUSER.VVV.ZFS
fs_type:
    description: The type of file system that will perform the logical mount request.
    returned: always
    type: str
    sample: ZFS
state:
    description: The desired status of the described mount.
    returned: always
    type: str
    sample: mounted
persistent:
    description: Values the user provided as input.
    returned: always
    type: dict
    contains:
        data_set_name:
            description: This is the full qualified name of the dataset member to change.
            returned: always
            type: str
            sample: SYS1.FILESYS(BPXPRMAA)
        backup:
            description: Specifies whether a backup of destination should be created.
            returned: always
            type: bool
            sample: True
        backup_name:
            description: Specify a unique data set name for the destination backup.
            returned: always
            type: str
            sample: SYS1.FILESYS(PRMAABAK)
tabcomment:
    description: The text that was used in markers around the Persistent/data_set_name entry.
    returned: always
    type: list
    sample:
        - [u'I did this because..']
unmount_opts:
    description: Describes how the unmount it to be performed.
    returned: changed and if state=unmounted
    type: str
    sample: DRAIN
mount_opts:
    description: Options available to the mount.
    returned: whenever non-None
    type: str
    sample: rw,nosecurity
src_params:
    description: Specifies a parameter string to be passed to the file system type.
    returned: whenever non-None
    type: str
    sample: D(101)
tag_untagged:
    description: Indicates if tags should be written to untagged files.
    returned: whenever Non-None
    type: str
    sample: TEXT
tag_ccsid:
    description: CCSID for untagged files in the mounted file system.
    returned: when tag_untagged is defined
    type: int
    sample: 819
allow_uid:
    description: Whether the SETUID and SETGID mode bits on executables in this file system are considered.
    returned: always
    type: bool
    sample: yes
sysname:
    description: I(sysname) specifies the particular system on which a mount should be performed.
    returned: if Non-None
    type: str
    sample: MVSSYS01
automove:
    description:
        - >
          Specifies what is to happens to the ownership of a file system during
          a shutdown, PFS termination, dead system takeover, or file system move occurs.
    returned: if Non-None
    type: str
    sample: AUTOMOVE
automove_list:
    description: This specifies the list of servers to include or exclude as destinations.
    returned: if Non-None
    type: str
    sample: I,SERV01,SERV02,SERV03,SERV04
msg:
    description: Failure message returned by the module.
    returned: failure
    type: str
    sample: Error while gathering information
stdout:
    description: The stdout from the tso mount command.
    returned: always
    type: str
    sample: Copying local file /tmp/foo/src to remote path /tmp/foo/dest.
stderr:
    description: The stderr from the tso mount command.
    returned: failure
    type: str
    sample: No such file or directory "/tmp/foo"
stdout_lines:
    description: List of strings containing individual lines from stdout.
    returned: failure
    type: list
    sample: [u"Copying local file /tmp/foo/src to remote path /tmp/foo/dest.."]
stderr_lines:
    description: List of strings containing individual lines from stderr.
    returned: failure
    type: list
    sample: [u"FileNotFoundError: No such file or directory '/tmp/foo'"]
cmd:
    description: The actual tso command that was attempted.
    returned: failure
    type: str
    sample: MOUNT EXAMPLE.DATA.SET /u/omvsadm/sample 3380
rc:
    description: The return code of the mount command, if applicable.
    returned: failure
    type: int
    sample: 8

"""

import os
import re
import tempfile

from datetime import datetime
from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.ansible_module import (
    AnsibleModuleHelper,
)

from ansible_collections.ibm.ibm_zos_core.plugins.module_utils import (
    better_arg_parser,
    data_set,
    backup as Backup,
)

from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.import_handler import (
    MissingZOAUImport,
)

from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.copy import (
    copy_ps2uss,
    copy_mvs2mvs,
    copy_uss2mvs,
)

try:
    from zoautil_py import Datasets, MVSCmd, types
except Exception:
    Datasets = MissingZOAUImport()
    MVSCmd = MissingZOAUImport()
    types = MissingZOAUImport()


# This is a duplicate of backupOper found in zos_apf.py of this collection
# Ansible doesn't want to import things not in the module_utils folder,
# necessitating this
# supported data set types
mt_DS_TYPE = ["PS", "PO"]


def mt_backupOper(module, src, backup):
    # analysis the file type
    ds_utils = data_set.DataSetUtils(src)
    file_type = ds_utils.ds_type()
    if file_type != "USS" and file_type not in mt_DS_TYPE:
        message = "{0} data set type is NOT supported".format(str(file_type))
        module.fail_json(msg=message)

    # backup can be True(bool) or none-zero length string. string indicates that backup_name was provided.
    # setting backup to None if backup_name wasn't provided. if backup=None, Backup module will use
    # pre-defined naming scheme and return the created destination name.
    if isinstance(backup, bool):
        backup = None
    try:
        if file_type == "USS":
            backup_name = Backup.uss_file_backup(
                src, backup_name=backup, compress=False
            )
        else:
            backup_name = Backup.mvs_file_backup(dsn=src, bk_dsn=backup)
    except Exception:
        module.fail_json(msg="creating backup has failed")

    return backup_name


def swap_text(original, adding, removing):
    """
    swap_text returns original after removing blocks matching removing,
    and adding the adding param
    original now should be a list of lines without newlines
    return is the consolidated file value
    """
    content_lines = original

    remove_starting_at_index = None
    remove_ending_at_index = None

    ms = re.compile(r"^\s*MOUNT\s+FILESYSTEM\(\s*'" + removing.upper() + r"'\s*\)")
    print(ms)
    boneyard = dict()

    for index, line in enumerate(content_lines):
        if remove_starting_at_index is None:
            if ms.match(line) is not None:
                remove_starting_at_index = index
                # Check for comments above the match line
                if index > 0:
                    for tmpindex in range(index - 1, 0, -1):
                        tmpline = content_lines[tmpindex]
                        if len(tmpline) > 0:
                            # Added the second test to handle adjacent entries
                            if tmpline[0:2] != "/*" or tmpline[0:6] == "/* BEG":
                                remove_starting_at_index = tmpindex
                                break
                        else:
                            remove_starting_at_index = tmpindex
                            break
                remove_ending_at_index = index
                continue
        if remove_starting_at_index is not None:
            remove_ending_at_index = index
            doit = False
            if len(line) > 0:
                if line[0] != " " and line[0] != "\t" and line[0:2] != "/*":
                    doit = True
                elif line[0:6] == "/* END":
                    doit = True
            else:
                doit = True
            if doit:
                boneyard[remove_starting_at_index] = remove_ending_at_index
                remove_starting_at_index = None
                remove_ending_at_index = None

    if remove_starting_at_index is not None:
        if remove_ending_at_index is not None:
            if remove_starting_at_index != remove_ending_at_index:
                boneyard[remove_starting_at_index] = remove_ending_at_index

    for startidx in reversed(boneyard.keys()):
        endidx = boneyard[startidx]
        del content_lines[startidx: endidx + 1]

    if len(adding) > 0:
        content_lines.extend(adding.split("\n"))

    return "\n".join(content_lines)


# #############################################################################
# ############## run_module: code for zos_mount module ########################
# #############################################################################


def run_module(module, arg_def):
    # ********************************************************************
    # Verify the validity of module args. BetterArgParser raises ValueError
    # when a parameter fails its validation check
    # ********************************************************************

    try:
        parser = better_arg_parser.BetterArgParser(arg_def)
        parsed_args = parser.parse_args(module.params)
    except ValueError as err:
        module.fail_json(msg="Parameter verification failed", stderr=str(err))
    changed = False
    res_args = dict()

    src = parsed_args.get("src")
    path = parsed_args.get("path")
    fs_type = parsed_args.get("fs_type").upper()
    state = parsed_args.get("state")
    persistent = parsed_args.get("persistent")
    backup = None
    backup_name = None
    tabcomment = parsed_args.get("tabcomment")
    unmount_opts = parsed_args.get("unmount_opts")
    mount_opts = parsed_args.get("mount_opts")
    src_params = parsed_args.get("src_params")
    tag_untagged = parsed_args.get("tag_untagged")
    tag_ccsid = parsed_args.get("tag_ccsid")
    allow_uid = parsed_args.get("allow_uid")
    sysname = parsed_args.get("sysname")
    automove = parsed_args.get("automove")
    automove_list = parsed_args.get("automove_list")

    if persistent:
        data_set_name = persistent.get("data_set_name").upper()
        backup = persistent.get("backup")
        if backup:
            if persistent.get("backup_name"):
                backup_name = persistent.get("backup_name").upper()
                del persistent["backup_name"]
            res_args["backup_name"] = mt_backupOper(module, data_set_name, backup)
            del persistent["backup"]
        if state == "present":
            persistent["addDataset"] = data_set_name
        else:
            persistent["delDataset"] = data_set_name
        del persistent["data_set_name"]

    write_persistent = False
    if "mounted" in state or "present" in state or "absent" in state:
        if persistent:
            if data_set_name:
                if len(data_set_name) > 0:
                    write_persistent = True

    gonna_mount = True
    if "unmounted" in state or "absent" in state:
        gonna_mount = False

    gonna_unmount = False
    if "unmounted" in state or "remounted" in state or "absent" in state:
        gonna_unmount = True

    comment = "starting"

    res_args.update(
        dict(
            src=src,
            path=path,
            fs_type=fs_type,
            state=state,
            persistent=parsed_args.get("persistent"),
            tabcomment=tabcomment,
            unmount_opts=unmount_opts,
            mount_opts=mount_opts,
            src_params=src_params,
            tag_untagged=tag_untagged,
            tag_ccsid=tag_ccsid,
            allow_uid=allow_uid,
            sysname=sysname,
            automove=automove,
            automove_list=automove_list,
            cmd="not built",
            changed=changed,
            comment=comment,
            rc=0,
            stdout="",
            stderr="",
        )
    )

    # data set to be mounted/unmounted must exist
    fs_du = data_set.DataSetUtils(src)
    fs_exists = fs_du.exists()
    if fs_exists is False:
        module.fail_json(
            msg="Mount source (" + src + ") doesn't exist", stderr=str(res_args)
        )

    # Validate mountpoint exists if mounting
    if gonna_mount:
        mp_exists = os.path.exists(path)
        if mp_exists is False:
            try:
                os.mkdir(path)
            except Exception as err:
                module.fail_json(msg=str(err), stderr=str(res_args))

        comment += "ran unmount command\n"
        currently_mounted = False
        mp_exists = os.path.exists(path)
        if mp_exists is False:
            module.fail_json(
                msg="Mount destination (" + path + ") doesn't exist",
                stderr=str(res_args),
            )

    # Need to see if mountpoint is in use for idempotence
    currently_mounted = False

    rc, stdout, stderr = module.run_command("df", use_unsafe_shell=False)

    if rc != 0:
        module.fail_json(
            msg="Checking filesystem list failed with error", stderr=str(res_args)
        )
    sttest = stdout.splitlines()
    for line in sttest:
        if src in line:
            currently_mounted = True
            # reminder: we can space-split the string and find out mount destination
            break

    # can type be validated?

    # ##########################################
    # Assemble the mount command

    d = datetime.today()
    dtstr = d.strftime("%Y%m%d-%H%M%S")
    parmtext = "/* BEGIN ANSIBLE MANAGED BLOCK " + dtstr + " */\n"
    parmtail = "\n" + parmtext.replace("BEGIN", "END")

    if tabcomment is not None:
        extra = ""
        ctr = 1
        for tabline in tabcomment:
            if len(extra) > 0:
                extra += " "
            extra += tabline.strip()
            if len(extra) > 60:
                stopper = 60
                for i in range(59, 48, -1):
                    if extra[i] == " ":
                        stopper = i
                        break
                tmpx = extra[0:stopper]
                parmtext += "/* C{0}:{1}".format(ctr, tmpx)
                extra = extra[stopper:].strip()
            else:
                parmtext += "/* C{0}:{1}".format(ctr, extra)
                extra = ""
            parmtext += " */\n"
            ctr += 1
        # This is to handle the possibility of cumulative, multi-line overflow
        while len(extra) > 0:
            if len(extra) > 60:
                stopper = 60
                for i in range(59, 48, -1):
                    if extra[i] == " ":
                        stopper = i
                        break
                tmpx = extra[0:stopper]
                parmtext += "/* C{0}:{1}".format(ctr, tmpx)
                extra = extra[stopper:].strip()
            else:
                parmtext += "/* C{0}:{1}".format(ctr, extra)
                extra = ""
            parmtext += " */\n"
            ctr += 1

    fullcmd = ""
    fullumcmd = ""

    if gonna_mount:
        # @asifmahmud asifmahmud 4 days ago Collaborator
        #
        # I would suggest not using tsocmd as that command may not be available on some systems our customers use.
        # Instead I would suggest using ikjeft01 to execute any TSO commands that you want to execute.
        # There is a module util called mvs_cmd that has an API for ikjeft01.

        fullcmd = "tsocmd MOUNT FILESYSTEM\\( \\'{0}\\' \\) MOUNTPOINT\\( \\'{1}\\' \\) TYPE\\( '{2}' \\)".format(
            src, path, fs_type
        )
        parmtext = (
            parmtext
            + "MOUNT FILESYSTEM('{0}')\n      MOUNTPOINT('{1}')\n      TYPE('{2}')".format(
                src, path, fs_type
            )
        )
        if "ro" in mount_opts or "RO" in mount_opts:
            subcmd = "READ"
        else:
            subcmd = "RDWR"
        fullcmd = "{0} MODE\\({1}\\)".format(fullcmd, subcmd)
        parmtext = "{0}\n      MODE({1})".format(parmtext, subcmd)

        if src_params is not None:
            if len(src_params) > 1:
                fullcmd = "{0} PARM\\(\\'{1}\\'\\)".format(fullcmd, src_params)
                parmtext = "{0}\n      PARM('{1}')".format(parmtext, src_params)

        if tag_untagged is not None:
            if len(tag_untagged) > 0:
                fullcmd = "{0} TAG\\({1},{2}\\)".format(
                    fullcmd, tag_untagged, tag_ccsid
                )
                parmtext = "{0}\n      TAG({1},{2})".format(
                    parmtext, tag_untagged, tag_ccsid
                )

        if allow_uid:
            fullcmd = fullcmd + " SETUID"
            parmtext = parmtext + "\n      SETUID"
        else:
            fullcmd = fullcmd + " NOSETUID"
            parmtext = parmtext + "\n      NOSETUID"

        if "NOWAIT" in mount_opts or "nowait" in mount_opts:
            fullcmd = fullcmd + " NOWAIT"
            parmtext = parmtext + "\n      NOWAIT"
        else:
            fullcmd = fullcmd + " WAIT"
            parmtext = parmtext + "\n      WAIT"

        if "NOSECURITY" in mount_opts or "nosecurity" in mount_opts:
            fullcmd = fullcmd + " NOSECURITY"
            parmtext = parmtext + "\n      NOSECURITY"
        else:
            fullcmd = fullcmd + " SECURITY"
            parmtext = parmtext + "\n      SECURITY"

        if sysname is not None:
            if len(sysname) > 0 and len(sysname) < 9:
                fullcmd = "{0} SYSNAME\\({1}\\)".format(fullcmd, sysname)
                parmtext = "{0}\n      SYSNAME({1})".format(parmtext, sysname)

        if automove is not None:
            if len(automove) > 1:
                fullcmd = fullcmd + " " + automove
                parmtext = parmtext + "\n      " + automove
                if automove_list is not None:
                    if len(automove_list) > 1:
                        fullcmd = fullcmd + "(" + automove_list + ")"
                        parmtext = parmtext + "(" + automove_list + ")"
        parmtext = parmtext + parmtail
    else:
        parmtext = ""

    if gonna_unmount:  # unmount/remount
        fullumcmd = "tsocmd UNMOUNT FILESYSTEM\\( '{0}' \\)".format(src)
        if unmount_opts is None:
            unmount_opts = "NORMAL"
            fullumcmd = fullcmd + " " + unmount_opts
        elif len(unmount_opts) < 2:
            unmount_opts = "NORMAL"
            fullumcmd = fullcmd + " " + unmount_opts

    if gonna_unmount:
        if currently_mounted:
            changed = True
            if module.check_mode is False:
                try:
                    (rc, stdout, stderr) = module.run_command(
                        fullumcmd, use_unsafe_shell=False
                    )
                    comment += "ran unmount command\n"
                    currently_mounted = False
                except Exception as err:
                    module.fail_json(msg=str(err), stderr=str(res_args))
            else:
                comment += "(unmount) NO Action taken: ANSIBLE CHECK MODE\n"
                stdout = "ANSIBLE CHECK MODE"
        else:
            comment += "Unmount called on data set that is not mounted.\n"

    if gonna_mount:
        if currently_mounted is False:
            changed = True
            if module.check_mode is False:
                try:
                    (rc, stdout, stderr) = module.run_command(
                        fullcmd, use_unsafe_shell=False
                    )
                    comment = "ran command\n"
                except Exception as err:
                    module.fail_json(msg=str(err), stderr=str(res_args))
            else:
                comment += "(mount) NO Action taken: ANSIBLE CHECK MODE\n"
                stdout = "ANSIBLE CHECK MODE"
        else:
            comment += "Mount called on data set that is already mounted.\n"

    rc = 0
    stdout = stderr = None

    if write_persistent and module.check_mode is False:
        fst_du = data_set.DataSetUtils(data_set_name)
        fst_exists = fst_du.exists()
        if fst_exists is False:
            module.fail_json(
                msg="persistent ds set member (" + data_set_name + ") doesn't exist",
                stderr=str(res_args),
            )

        tmp_file = tempfile.NamedTemporaryFile(delete=True)
        tmp_file_filename = tmp_file.name
        tmp_file.close()

        # look at using zos_copy here
        copy_ps2uss(data_set_name, tmp_file_filename, False)

        # zos_copy could obviate the need for the backup call here
        if backup:
            copy_mvs2mvs(data_set_name, backup_name, False)
            comment += "Wrote backup to " + backup_name + "\n"

        with open(tmp_file_filename, "r") as fh:
            content = fh.read().splitlines()

        newtext = swap_text(content, parmtext, src)
        if newtext != content:
            fh = open(tmp_file_filename, "w")
            fh.write(newtext)
            fh.close()
            # look at using zos_copy here
            # fullcmd = "cp " + tmp_file_filename + " \"//'" + persistds + "'\""
            # try:
            #    (rc, stdout, stderr) = module.run_command(
            #        fullcmd, use_unsafe_shell=False)
            # except Exception as err:
            #    module.fail_json(msg=str(err), stderr=str(res_args))
            copy_uss2mvs(tmp_file_filename, data_set_name, "PO", False)
            comment += "Modified " + data_set_name + " in place\n"

        if os.path.isfile(tmp_file_filename):
            os.unlink(tmp_file_filename)

    res_args.update(
        dict(
            changed=changed,
            comment=comment,
            cmd=fullcmd,
            rc=rc,
            stdout=stdout,
            stderr=stderr,
        )
    )

    return res_args


# #############################################################################
# ####################### Main                     ############################
# #############################################################################


def main():
    global module

    module = AnsibleModule(
        argument_spec=dict(
            src=dict(type="str", required=True),
            path=dict(type="str", required=True),
            fs_type=dict(
                type="str",
                choices=[
                    "HFS",
                    "ZFS",
                    "NFS",
                    "TFS",
                ],
                required=True,
            ),
            state=dict(
                type="str",
                default="mounted",
                choices=["absent", "mounted", "unmounted", "present", "remounted"],
                required=False,
            ),
            persistent=dict(
                type="dict",
                required=False,
                options=dict(
                    data_set_name=dict(
                        type="str",
                        required=True,
                    ),
                    backup=dict(type="bool", default=False),
                    backup_name=dict(type="str", required=False, default=None),
                ),
            ),
            tabcomment=dict(type="list", required=False),
            unmount_opts=dict(
                type="str",
                default="NORMAL",
                choices=["DRAIN", "FORCE", "IMMEDIATE", "NORMAL", "REMOUNT", "RESET"],
                required=False,
            ),
            mount_opts=dict(
                type="str",
                default="rw",
                choices=["ro", "rw", "same", "nowait", "nosecurity"],
                required=False,
            ),
            src_params=dict(type="str", required=False),
            tag_untagged=dict(
                type="str", default="", choices=["", "TEXT", "NOTEXT"], required=False
            ),
            tag_ccsid=dict(type="int", required=False),
            allow_uid=dict(type="bool", default=True, required=False),
            sysname=dict(type="str", required=False),
            automove=dict(
                type="str",
                default="AUTOMOVE",
                choices=["AUTOMOVE", "NOAUTOMOVE", "UNMOUNT"],
                required=False,
            ),
            automove_list=dict(type="str", required=False),
        ),
        add_file_common_args=True,
        supports_check_mode=True,
    )

    arg_def = dict(
        src=dict(arg_type="data_set", required=True),
        path=dict(arg_type="path", required=True),
        fs_type=dict(
            arg_type="str",
            choices=[
                "HFS",
                "ZFS",
                "NFS",
                "TFS",
            ],
            required=True,
        ),
        state=dict(
            arg_type="str",
            default="mounted",
            choices=["absent", "mounted", "unmounted", "present", "remounted"],
            required=False,
        ),
        persistent=dict(
            arg_type="dict",
            required=False,
            options=dict(
                data_set_name=dict(arg_type="str", required=True),
                backup=dict(arg_type="bool", default=False),
                backup_name=dict(arg_type="str", required=False, default=None),
            ),
        ),
        tabcomment=dict(arg_type="list", elements="str", required=False),
        unmount_opts=dict(
            arg_type="str",
            default="NORMAL",
            choices=["DRAIN", "FORCE", "IMMEDIATE", "NORMAL", "REMOUNT", "RESET"],
            required=False,
        ),
        mount_opts=dict(
            arg_type="str",
            default="rw",
            choices=["ro", "rw", "same", "nowait", "nosecurity"],
            required=False,
        ),
        src_params=dict(arg_type="str", default="", required=False),
        tag_untagged=dict(
            arg_type="str", default="", choices=["", "TEXT", "NOTEXT"], required=False
        ),
        tag_ccsid=dict(arg_type="str", required=False),
        allow_uid=dict(arg_type="bool", default=True, required=False),
        sysname=dict(arg_type="str", default="", required=False),
        automove=dict(
            arg_type="str",
            default="AUTOMOVE",
            choices=["AUTOMOVE", "NOAUTOMOVE", "UNMOUNT"],
            required=False,
        ),
        automove_list=dict(arg_type="str", default="", required=False),
    )

    res_args = None
    res_args = run_module(module, arg_def)
    module.exit_json(**res_args)


if __name__ == "__main__":
    main()
