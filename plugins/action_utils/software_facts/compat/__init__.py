import sys

from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.compat.ansible.utils.vars \
    import merge_hash, isidentifier

# Attempt to use ansible native import_module, if not available, perform the same actions as ansible
try:
    from ansible.module_utils.compat.importlib import import_module
except ImportError:
    try:
        from importlib import import_module
    except ImportError:
        def import_module(name):
            __import__(name)
            return sys.modules[name]

# Attempt to use ansible native MutableMapping, if not available, expose the compat one
try:
    from ansible.module_utils.common.collections import MutableMapping
except ImportError:
    from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.compat.ansible.module_utils.common._collections_compat \
        import MutableMapping

# Attempt to use ansible native ArgumentSpecValidator, if not available, expose the compat one
try:
    from ansible.module_utils.common.arg_spec import ArgumentSpecValidator
except ImportError:
    from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.compat.ansible.module_utils.common.arg_spec \
        import ArgumentSpecValidator

# Attempt to use ansible is_sequence, if not available, expose the compat one
try:
    from ansible.module_utils.common.collections import is_sequence
except ImportError:
    from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.compat.ansible.module_utils.common.collections \
        import is_sequence

# Attempt to use ansible AnsibleFilterError, if not available, expose the compat one
try:
    from ansible.errors import AnsibleFilterError
except ImportError:
    from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.compat.ansible.errors.__init__ \
        import AnsibleFilterError

# attempt to use ansible native unicode_wrap, if not available, expose the compat one
try:
    from ansible.utils.unicode import unicode_wrap
except ImportError:
    from ansible_collections.datadope.discovery.plugins.action_utils.software_facts.compat.ansible.utils.unicode \
        import unicode_wrap

# Determine if templar has template cache (source: ansible community.general collection)
# The cache was removed for ansible-core 2.14 (https://github.com/ansible/ansible/pull/78419)
from ansible.release import __version__ as ansible_version
from ansible.module_utils.compat.version import LooseVersion

_TEMPLAR_HAS_TEMPLATE_CACHE = LooseVersion(ansible_version) < LooseVersion('2.14.0')
