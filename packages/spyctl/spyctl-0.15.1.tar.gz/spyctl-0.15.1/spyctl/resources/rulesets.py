from typing import Dict, List

from tabulate import tabulate

import spyctl.spyctl_lib as lib
import spyctl.merge_lib as m_lib

SUMMARY_HEADERS = [
    "UID",
    "NAME",
    "TYPE",
    "VERSION",
    "CREATE_TIME",
    "LAST_UPDATED",
]


def rulesets_summary_output(rulesets: List[Dict]):
    data = []
    for rs in rulesets:
        data.append(
            [
                rs[lib.METADATA_FIELD][lib.METADATA_UID_FIELD],
                rs[lib.METADATA_FIELD][lib.METADATA_NAME_FIELD],
                rs[lib.METADATA_FIELD][lib.METADATA_TYPE_FIELD],
                rs[lib.METADATA_FIELD][lib.METADATA_VERSION_FIELD],
                lib.epoch_to_zulu(
                    rs[lib.METADATA_FIELD][lib.METADATA_CREATE_TIME]
                ),
                lib.epoch_to_zulu(
                    rs[lib.METADATA_FIELD][lib.METADATA_LAST_UPDATE_TIME]
                ),
            ]
        )
    data.sort(key=lambda x: x[1])
    return tabulate(data, headers=SUMMARY_HEADERS, tablefmt="plain")


RULESET_META_MERGE_SCHEMA = m_lib.MergeSchema(
    lib.METADATA_FIELD,
    merge_functions={
        lib.METADATA_NAME_FIELD: m_lib.keep_base_value_merge,
        lib.METADATA_TYPE_FIELD: m_lib.keep_base_value_merge,
        lib.METADATA_UID_FIELD: m_lib.keep_base_value_merge,
        lib.METADATA_CREATE_TIME: m_lib.keep_base_value_merge,
        lib.METADATA_CREATED_BY: m_lib.keep_base_value_merge,
        lib.METADATA_LAST_UPDATE_TIME: m_lib.keep_base_value_merge,
        lib.METADATA_LAST_UPDATED_BY: m_lib.keep_base_value_merge,
        lib.METADATA_VERSION_FIELD: m_lib.keep_base_value_merge,
    },
)

RULESET_SPEC_MERGE_SCHEMA = m_lib.MergeSchema(
    lib.SPEC_FIELD,
    merge_functions={
        lib.RULES_FIELD: m_lib.merge_rules,
    },
)

RULESET_MERGE_SCHEMAS = [RULESET_META_MERGE_SCHEMA, RULESET_SPEC_MERGE_SCHEMA]
