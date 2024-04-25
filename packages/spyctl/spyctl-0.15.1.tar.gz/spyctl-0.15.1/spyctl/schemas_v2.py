"""Contains the schemas for the various objects managed by spyctl"""

# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring,no-self-argument
# pylint: disable=raise-missing-from, too-few-public-methods


from __future__ import annotations

import ipaddress
from typing import Any, Dict, List, Optional, Union
from typing_extensions import Annotated

from pydantic import (
    field_validator,
    model_validator,
    ConfigDict,
    BaseModel,
    Field,
    IPvAnyNetwork,
    ValidationError,
)
from pydantic.functional_validators import AfterValidator
from typing_extensions import Literal

import spyctl.spyctl_lib as lib


def valid_object(
    data: Dict, verbose=True, allow_obj_list=True, interactive=False
) -> bool:
    kind = data.get(lib.KIND_FIELD)
    if kind not in KIND_TO_SCHEMA:
        if lib.ITEMS_FIELD not in data:
            lib.err_exit(
                f"Unable to validate {kind!r}, no schema exists for objects of"
                " that type."
            )
        elif not allow_obj_list:
            lib.err_exit("Nested item lists are not allowed.")
        try:
            GuardianObjectListModel(**data)
        except ValidationError as e:
            if verbose:
                if interactive:
                    return str(e)
                else:
                    lib.try_log(str(e), is_warning=True)
            return False
        for item in data[lib.ITEMS_FIELD]:
            if not valid_object(item, allow_obj_list=False):
                return False
        return True
    # Some validations depend on the type of the object in addition to the kind
    tmp_kind = (
        kind,
        data.get(lib.METADATA_FIELD, {}).get(lib.METADATA_TYPE_FIELD),
    )
    if tmp_kind in KIND_TO_SCHEMA:
        kind = tmp_kind
    try:
        KIND_TO_SCHEMA[kind](**data)
    except ValidationError as e:
        if verbose:
            if interactive:
                return str(e)
            else:
                lib.try_log(str(e), is_warning=True)
        return False
    return True


def valid_context(context_data: Dict, verbose=True):
    try:
        ContextsModel(**context_data)
    except ValidationError as e:
        if verbose:
            lib.try_log(str(e), is_warning=True)
        return False
    return True


def handle_show_schema(kind: str) -> str:
    obj = KIND_TO_SCHEMA.get(kind)
    return obj.schema_json()


def valid_notification_target(tgt_data: Dict, interactive=False):
    try:
        NotificationTargetModel(**tgt_data)
    except ValidationError as e:
        if interactive:
            return str(e)
        else:
            lib.try_log(str(e), is_warning=True)
        return False
    return True


__PROC_IDS = {}

# -----------------------------------------------------------------------------
# Selectors -------------------------------------------------------------------
# -----------------------------------------------------------------------------

EXPR_SYNTAX = (
    "{key: <key>, operator: <operator>, values: [<value1>, <value2>, ...]}"
)


class SelectorExpression(BaseModel):
    key: str = Field(alias=lib.KEY_FIELD)
    operator: Literal["In", "NotIn", "Exists", "DoesNotExist"] = Field(
        alias=lib.OPERATOR_FIELD
    )
    values: Optional[List[str]] = Field(None, alias=lib.VALUES_FIELD)

    @model_validator(mode="after")
    def ensure_values(self):
        if self.operator in ["Exists", "DoesNotExist"]:
            if self.values:
                raise ValueError(
                    f"'{self.operator}' operator does not accept"
                    f" values. Found '{self.values}'"
                )
        else:
            if not self.values:
                raise ValueError(
                    f"'{self.operator}' operator requires values."
                )
        return self


def encode_expr(key, operator, values=None) -> str:
    if operator in ["Exists", "DoesNotExist"]:
        if values:
            raise ValueError(
                f"'{operator}' operator does not accept values. Found '{values}'"  # noqa
            )
    else:
        if not values:
            raise ValueError(f"'{operator}' operator requires values.")
    values_ = "[" + ", ".join(f"{ns}" for ns in values) + "]"
    expr = (
        "{ "
        + f"key: {key}, operator: {operator}, values: {values_}"  # noqa
        + " }"
    )
    return expr


class MatchLabelsModel(BaseModel):
    match_labels: Optional[Dict[str, str]] = Field(
        None, alias=lib.MATCH_LABELS_FIELD
    )
    model_config = ConfigDict(extra="forbid")


class MatchExpressionModel(BaseModel):
    match_expressions: Optional[List[SelectorExpression]] = Field(
        None, alias=lib.MATCH_EXPRESSIONS_FIELD, min_length=1
    )
    model_config = ConfigDict(extra="forbid")


class LabelsMatchModel(MatchLabelsModel, MatchExpressionModel):

    @model_validator(mode="after")
    def ensure_one_field(self):
        values = self.model_dump(by_alias=True, exclude_unset=True)
        if not any(value for value in values.values()):
            raise ValueError("Need matchLabels or matchExpressions")
        return self

    model_config = ConfigDict(extra="forbid")


class MatchFieldsModel(BaseModel):
    match_fields: Optional[Dict[str, str]] = Field(
        None, alias=lib.MATCH_FIELDS_FIELD
    )

    @classmethod
    def get_valid_fields(cls):
        return tuple()

    @field_validator("match_fields")
    @classmethod
    def ensure_valid_fields(cls, values):
        valid_fields = cls.get_valid_fields()
        for field in values:
            if field not in valid_fields:
                raise ValueError(
                    f"Invalid field '{field}'. Valid fields are {valid_fields}"
                )
        return values

    model_config = ConfigDict(extra="forbid")


class MatchFieldsExpressionsModel(MatchFieldsModel):
    match_fields_expressions: Optional[List[SelectorExpression]] = Field(
        None, alias=lib.MATCH_FIELDS_EXPRESSIONS_FIELD, min_length=1
    )

    @field_validator("match_fields_expressions")
    @classmethod
    def ensure_valid_field_expressions(cls, values: Dict):
        valid_fields = cls.get_valid_fields()
        exprs: List[SelectorExpression] = values
        for expr in exprs:
            if expr.key not in valid_fields:
                raise ValueError(
                    f"Invalid key in expr '{expr.key}'. Valid fields are {valid_fields}"  # noqa
                )
        return values

    model_config = ConfigDict(extra="forbid")


class ContainerMatchModel(MatchFieldsExpressionsModel):

    @classmethod
    def get_valid_fields(cls):
        return (
            "image",
            "imageID",
            "containerName",
            "containerID",
        )

    model_config = ConfigDict(extra="forbid")


class ClusterMatchModel(MatchFieldsExpressionsModel):
    @classmethod
    def get_valid_fields(cls):
        return (
            "name",
            "uid",
        )


class ServiceMatchModel(MatchFieldsExpressionsModel):
    @classmethod
    def get_valid_fields(cls):
        return (
            "cgroup",
            "name",
        )


class MachineMatchModel(MatchFieldsExpressionsModel):
    @classmethod
    def get_valid_fields(cls):
        return (
            "hostname",
            "sourceName",
            "uid",
        )


class TraceMatchModel(MatchFieldsExpressionsModel):
    @classmethod
    def get_valid_fields(cls):
        return (
            "triggerClass",
            "triggerAncestors",
        )


class UserMatchModel(MatchFieldsExpressionsModel):
    @classmethod
    def get_valid_fields(cls):
        return ("user",)


class ProcessMatchModel(MatchFieldsExpressionsModel):
    @classmethod
    def get_valid_fields(cls):
        return (
            "name",
            "exe",
            "euser",
        )


class ContainerSelectorModel(ContainerMatchModel):
    image: Optional[str] = Field(None, alias=lib.IMAGE_FIELD)
    image_id: Optional[str] = Field(None, alias=lib.IMAGEID_FIELD)
    container_name: Optional[str] = Field(None, alias=lib.CONTAINER_NAME_FIELD)
    container_id: Optional[str] = Field(None, alias=lib.CONTAINER_ID_FIELD)

    model_config = ConfigDict(extra="forbid")


class ClusterSelectorModel(ClusterMatchModel):
    model_config = ConfigDict(extra="forbid")


class ServiceSelectorModel(ServiceMatchModel):
    cgroup: Optional[str] = Field(None, alias=lib.CGROUP_FIELD)
    model_config = ConfigDict(extra="forbid")


class MachineSelectorModel(MachineMatchModel):
    hostname: Optional[Union[str, List[str]]] = Field(
        None, alias=lib.HOSTNAME_FIELD
    )
    machine_uid: Optional[Union[str, List[str]]] = Field(
        None, alias=lib.MACHINE_UID_FIELD
    )

    model_config = ConfigDict(extra="forbid")


class NamespaceSelectorModel(LabelsMatchModel):
    pass


class PodSelectorModel(LabelsMatchModel):
    pass


class TraceSelectorModel(TraceMatchModel):
    trigger_class: Optional[List[str]] = Field(
        None, alias=lib.TRIGGER_CLASS_FIELD
    )
    trigger_ancestor: Optional[List[str]] = Field(
        None, alias=lib.TRIGGER_ANCESTORS_FIELD
    )
    model_config = ConfigDict(extra="forbid")


class UserSelectorModel(UserMatchModel):
    users: Optional[List[str]] = Field(None, alias=lib.USERS_FIELD)
    interactive_users: Optional[List[str]] = Field(
        None, alias=lib.INTERACTIVE_USERS_FIELD
    )
    non_interactive_users: Optional[List[str]] = Field(
        None, alias=lib.NON_INTERACTIVE_USERS_FIELD
    )
    model_config = ConfigDict(extra="forbid")


class ProcessSelectorModel(ProcessMatchModel):
    name: Optional[List[str]] = Field(None, alias=lib.NAME_FIELD, min_length=1)
    exe: Optional[List[str]] = Field(None, alias=lib.EXE_FIELD, min_length=1)
    euser: Optional[List[str]] = Field(
        None, alias=lib.EUSER_FIELD, min_length=1
    )

    @model_validator(mode="after")
    def ensure_one_field(
        self,
    ):
        values = self.model_dump(by_alias=True, exclude_unset=True)
        set_count = 0
        for v in values.values():
            if v is not None:
                set_count += 1
        if set_count == 0:
            raise ValueError("At least one key, value pair expected")
        return self

    model_config = ConfigDict(extra="forbid")


# -----------------------------------------------------------------------------
# Ruleset Models --------------------------------------------------------------
# -----------------------------------------------------------------------------


class RuleModel(BaseModel):
    verb: Literal[tuple(lib.RULE_VERBS)] = Field(  # type: ignore
        alias=lib.RULE_VERB_FIELD,
    )
    target: str = Field(alias=lib.RULE_TARGET_FIELD)  # type: ignore
    values: List[str] = Field(alias=lib.RULE_VALUES_FIELD)


class ContainerRule(RuleModel):
    cluster_selector: Optional[ClusterSelectorModel] = Field(
        None, alias=lib.CLUS_SELECTOR_FIELD
    )
    namespace_selector: Optional[NamespaceSelectorModel] = Field(
        None, alias=lib.NAMESPACE_SELECTOR_FIELD
    )
    pod_selector: Optional[PodSelectorModel] = Field(
        None, alias=lib.POD_SELECTOR_FIELD
    )
    target: Literal[tuple(lib.CONTAINER_RULE_TARGETS)] = Field(  # type: ignore
        alias=lib.RULE_TARGET_FIELD
    )


class RulesetMetadataModel(BaseModel):
    name: str = Field(alias=lib.METADATA_NAME_FIELD)
    type: Literal[tuple(lib.RULESET_TYPES)] = Field(  # type: ignore
        alias=lib.METADATA_TYPE_FIELD
    )
    create_time: Optional[Union[int, float]] = Field(
        None, alias=lib.METADATA_CREATE_TIME
    )
    created_by: Optional[str] = Field(None, alias=lib.METADATA_CREATED_BY)
    last_updated: Optional[Union[int, float]] = Field(
        None, alias=lib.METADATA_LAST_UPDATE_TIME
    )
    last_updated_by: Optional[str] = Field(
        None, alias=lib.METADATA_LAST_UPDATED_BY
    )
    version: Optional[int] = Field(None, alias=lib.METADATA_VERSION_FIELD)
    uid: Optional[str] = Field(None, alias=lib.METADATA_UID_FIELD)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if " " in v:
            raise ValueError("Name cannot contain spaces.")
        if len(v) > 64:
            raise ValueError("Name must be less than 64 characters.")
        return v


class RulesetPolicySpecModel(BaseModel):
    rules: List[ContainerRule] = Field(
        alias=lib.RULES_FIELD,
        # discriminator=lib.RULE_TARGET_FIELD,
    )


class RulesetModel(BaseModel):
    api_version: str = Field(alias=lib.API_FIELD)
    kind: Literal[lib.RULESET_KIND] = Field(alias=lib.KIND_FIELD)  # type: ignore  # noqa: E501
    metadata: RulesetMetadataModel = Field(alias=lib.METADATA_FIELD)
    spec: RulesetPolicySpecModel = Field(alias=lib.SPEC_FIELD)
    model_config = ConfigDict(extra="ignore")


# -----------------------------------------------------------------------------
# Guardian Models -------------------------------------------------------------
# -----------------------------------------------------------------------------


# This is a reused validator ensuring that the objects have a required selector
def validate_selectors(model: GuardianObjectModel):
    values = model.model_dump(by_alias=True, exclude_unset=True)
    pol_type = values["metadata"]["type"]
    if pol_type == lib.POL_TYPE_CONT:
        s_val = values["spec"].get(lib.CONT_SELECTOR_FIELD)
        if not s_val:
            raise ValueError(
                f"Type is '{lib.POL_TYPE_CONT}' and no "
                f"'{lib.CONT_SELECTOR_FIELD}' found in {lib.SPEC_FIELD}"
            )
    elif pol_type == lib.POL_TYPE_SVC:
        s_val = values["spec"].get(lib.SVC_SELECTOR_FIELD)
        if not s_val:
            raise ValueError(
                f"Type is '{lib.POL_TYPE_SVC}' and no "
                f"'{lib.SVC_SELECTOR_FIELD}' found in {lib.SPEC_FIELD}"
            )
    elif pol_type == lib.POL_TYPE_CLUS:
        s_val = values["spec"].get(lib.CLUS_SELECTOR_FIELD)
        if not s_val:
            raise ValueError(
                f"Type is '{lib.POL_TYPE_CLUS}' and no "
                f"'{lib.CLUS_SELECTOR_FIELD}' found in {lib.SPEC_FIELD}"
            )
    return model


class GuardianSelectorsModel(BaseModel):
    container_selector: Optional[ContainerSelectorModel] = Field(
        None, alias=lib.CONT_SELECTOR_FIELD
    )
    service_selector: Optional[ServiceSelectorModel] = Field(
        None, alias=lib.SVC_SELECTOR_FIELD
    )
    machine_selector: Optional[MachineSelectorModel] = Field(
        None, alias=lib.MACHINE_SELECTOR_FIELD
    )
    namespace_selector: Optional[NamespaceSelectorModel] = Field(
        None, alias=lib.NAMESPACE_SELECTOR_FIELD
    )
    pod_selector: Optional[PodSelectorModel] = Field(
        None, alias=lib.POD_SELECTOR_FIELD
    )
    model_config = ConfigDict(extra="forbid")


class ClusterPolicySelectorsModel(BaseModel):
    cluster_selector: ClusterSelectorModel = Field(
        alias=lib.CLUS_SELECTOR_FIELD
    )
    model_config = ConfigDict(extra="forbid")


class ActionSelectorsModel(BaseModel):
    cluster_selector: Optional[ClusterSelectorModel] = Field(
        None, alias=lib.CLUS_SELECTOR_FIELD
    )
    container_selector: Optional[ContainerSelectorModel] = Field(
        None, alias=lib.CONT_SELECTOR_FIELD
    )
    machine_selector: Optional[MachineSelectorModel] = Field(
        None, alias=lib.MACHINE_SELECTOR_FIELD
    )
    namespace_selector: Optional[NamespaceSelectorModel] = Field(
        None, alias=lib.NAMESPACE_SELECTOR_FIELD
    )
    pod_selector: Optional[PodSelectorModel] = Field(
        None, alias=lib.POD_SELECTOR_FIELD
    )
    process_selector: Optional[ProcessSelectorModel] = Field(
        None, alias=lib.PROCESS_SELECTOR_FIELD
    )
    model_config = ConfigDict(extra="forbid")


class GuardianSpecOptionsModel(BaseModel):
    disable_processes: Optional[
        Literal[tuple(lib.DISABLE_PROCS_STRINGS)]  # type: ignore
    ] = Field(None, alias=lib.DISABLE_PROCS_FIELD)
    disable_connections: Optional[
        Literal[tuple(lib.DISABLE_CONNS_STRINGS)]  # type: ignore
    ] = Field(None, alias=lib.DISABLE_CONNS_FIELD)
    disable_private_conns: Optional[
        Literal[tuple(lib.DISABLE_CONNS_STRINGS)]  # type: ignore
    ] = Field(None, alias=lib.DISABLE_PR_CONNS_FIELD)
    disable_public_conns: Optional[
        Literal[tuple(lib.DISABLE_CONNS_STRINGS)]  # type: ignore
    ] = Field(None, alias=lib.DISABLE_PU_CONNS_FIELD)


# Network Models --------------------------------------------------------------


class DnsBlockModel(BaseModel):
    dns_selector: List[str] = Field(alias=lib.DNS_SELECTOR_FIELD)
    model_config = ConfigDict(extra="forbid")


class CIDRModel(BaseModel):
    cidr: IPvAnyNetwork = Field(alias=lib.CIDR_FIELD)
    except_cidr: Optional[List[IPvAnyNetwork]] = Field(
        None, alias=lib.EXCEPT_FIELD, max_length=10
    )

    @model_validator(mode="after")
    def validate_except_within_cidr(self):
        values = self.model_dump(by_alias=True, exclude_unset=True)
        cidr = values["cidr"]
        try:
            cidr_net = ipaddress.IPv4Network(cidr)
        except ipaddress.AddressValueError:
            cidr_net = ipaddress.IPv6Network(cidr)
        net_type = type(cidr_net)
        if "except_cidr" in values and values["except_cidr"]:
            for e_cidr in values["except_cidr"]:
                try:
                    e_net = ipaddress.IPv4Network(e_cidr)
                except ipaddress.AddressValueError:
                    e_net = ipaddress.IPv6Network(e_cidr)
                if net_type != type(e_net):
                    raise ValueError("Network types are not the same")
                if not cidr_net.supernet_of(e_net):
                    raise ValueError(
                        f"'{e_net}' is not a subnet of '{cidr_net}'"
                    )
        return self

    model_config = ConfigDict(extra="forbid")


class IpBlockModel(BaseModel):
    ip_block: CIDRModel = Field(alias=lib.IP_BLOCK_FIELD)
    model_config = ConfigDict(extra="forbid")


class PortsModel(BaseModel):
    port: int = Field(alias=lib.PORT_FIELD, ge=0, le=65535)
    proto: Literal["UDP", "TCP"] = Field(alias=lib.PROTO_FIELD)
    endport: Optional[int] = Field(
        None, alias=lib.ENDPORT_FIELD, ge=0, le=66535
    )

    @model_validator(mode="after")
    def endport_ge_port(self):
        values = self.model_dump(by_alias=True, exclude_unset=True)
        endport = values.get("endport")
        if endport is not None and endport < values["port"]:
            raise ValueError(
                f"{lib.ENDPORT_FIELD} must be greater than or equal to"
                f" {lib.PORT_FIELD}"
            )
        return self

    model_config = ConfigDict(extra="forbid")


class IngressNodeModel(BaseModel):
    from_field: List[Union[DnsBlockModel, IpBlockModel]] = Field(
        alias=lib.FROM_FIELD, min_length=1
    )
    processes: Optional[List[str]] = Field(
        None, alias=lib.PROCESSES_FIELD, min_length=1
    )
    ports: List[PortsModel] = Field(alias=lib.PORTS_FIELD, min_length=1)

    @field_validator("processes")
    @classmethod
    def validate_proc_ids(cls, v):
        if not v:
            return v
        bad = []
        for proc_id in v:
            if not in_proc_ids(proc_id):
                bad.append(proc_id)
        if bad:
            raise ValueError(f"No process found with id(s) '{bad}'.")
        return v

    model_config = ConfigDict(extra="forbid")


class EgressNodeModel(BaseModel):
    to: List[Union[DnsBlockModel, IpBlockModel]] = Field(
        alias=lib.TO_FIELD, min_length=1
    )
    processes: Optional[List[str]] = Field(
        None, alias=lib.PROCESSES_FIELD, min_length=1
    )
    ports: List[PortsModel] = Field(alias=lib.PORTS_FIELD, min_length=1)

    @field_validator("processes")
    @classmethod
    def validate_proc_ids(cls, v):
        if not v:
            return v
        bad = []
        for proc_id in v:
            if not in_proc_ids(proc_id):
                bad.append(proc_id)
        if bad:
            raise ValueError(f"No process found with id(s) '{bad}'.")
        return v

    model_config = ConfigDict(extra="forbid")


class NetworkPolicyModel(BaseModel):
    ingress: List[IngressNodeModel] = Field(alias=lib.INGRESS_FIELD)
    egress: List[EgressNodeModel] = Field(alias=lib.EGRESS_FIELD)


class DeviationNetworkPolicyModel(BaseModel):
    ingress: Optional[List[IngressNodeModel]] = Field(
        None, alias=lib.INGRESS_FIELD
    )
    egress: Optional[List[EgressNodeModel]] = Field(
        None, alias=lib.EGRESS_FIELD
    )


# Process Models --------------------------------------------------------------


class SimpleProcessNodeModel(BaseModel):
    name: str = Field(alias=lib.NAME_FIELD)
    exe: List[str] = Field(alias=lib.EXE_FIELD)
    euser: Optional[List[str]] = Field(None, alias=lib.EUSER_FIELD)


class ProcessNodeModel(SimpleProcessNodeModel):
    id: str = Field(alias=lib.ID_FIELD)
    listening_sockets: Optional[List[PortsModel]] = Field(
        None, alias=lib.LISTENING_SOCKETS
    )
    children: Optional[List[ProcessNodeModel]] = Field(
        None, alias=lib.CHILDREN_FIELD
    )

    @field_validator("id")
    @classmethod
    def validate_no_duplicate_ids(cls, v):
        if in_proc_ids(v):
            raise ValueError(f"Duplicate id '{v}' detected.")
        add_proc_id(v)
        return v

    model_config = ConfigDict(extra="forbid")


class GuardDeviationProcessNodeModel(BaseModel):
    id: str = Field(alias=lib.ID_FIELD)
    children: Optional[List[ProcessNodeModel]] = Field(
        None, alias=lib.CHILDREN_FIELD
    )

    @field_validator("id")
    @classmethod
    def validate_no_duplicate_ids(cls, v):
        if in_proc_ids(v):
            raise ValueError(f"Duplicate id '{v}' detected.")
        add_proc_id(v)
        return v

    # class Config:
    #     extra = Extra.forbid


class GuardDeviationNodeModel(BaseModel):
    policy_node: GuardDeviationProcessNodeModel = Field(alias="policyNode")
    model_config = ConfigDict(extra="forbid")


# Actions Models --------------------------------------------------------------


class SharedDefaultActionFieldsModel(BaseModel):
    enabled: Optional[bool] = Field(None, alias=lib.ENABLED_FIELD)
    model_config = ConfigDict(extra="forbid")


class SharedActionFieldsModel(ActionSelectorsModel):
    enabled: Optional[bool] = Field(None, alias=lib.ENABLED_FIELD)

    @model_validator(mode="after")
    def validate_has_selector(self):
        values = self.model_dump(by_alias=True, exclude_unset=True)
        count = 0
        values_count = 0
        for key, value in values.items():
            if key.endswith("Selector"):
                count += 1
            if value:
                values_count += 1
        if count == 0:
            raise ValueError(
                "At least one selector required for non-default actions."
            )
        if values_count != count:
            raise ValueError("All selectors must have values.")
        return self

    model_config = ConfigDict(extra="forbid")


class DefaultMakeRedflagModel(SharedDefaultActionFieldsModel):
    content: Optional[str] = Field(
        None, alias=lib.FLAG_CONTENT, max_length=350
    )
    impact: Optional[str] = Field(None, alias=lib.FLAG_IMPACT, max_length=100)
    severity: Literal[tuple(lib.ALLOWED_SEVERITIES)] = Field(  # type: ignore
        alias=lib.FLAG_SEVERITY
    )
    model_config = ConfigDict(extra="forbid")


class MakeRedflagModel(SharedActionFieldsModel, DefaultMakeRedflagModel):
    pass


class DefaultMakeOpsflagModel(BaseModel):
    content: Optional[str] = Field(
        None, alias=lib.FLAG_CONTENT, max_length=350
    )
    description: Optional[str] = Field(
        None, alias=lib.FLAG_DESCRIPTION, max_length=350
    )
    severity: Literal[tuple(lib.ALLOWED_SEVERITIES)] = Field(  # type: ignore
        alias=lib.FLAG_SEVERITY
    )
    model_config = ConfigDict(extra="forbid")


class MakeOpsflagModel(SharedActionFieldsModel, DefaultMakeOpsflagModel):
    pass


class DefaultActionsModel(BaseModel):
    make_redflag: Optional[DefaultMakeRedflagModel] = Field(
        None, alias=lib.ACTION_MAKE_REDFLAG
    )
    make_opsflag: Optional[DefaultMakeOpsflagModel] = Field(
        None, alias=lib.ACTION_MAKE_OPSFLAG
    )
    agent_kill_pod: Optional[SharedDefaultActionFieldsModel] = Field(
        None, alias=lib.ACTION_KILL_POD
    )
    agent_kill_proc: Optional[SharedDefaultActionFieldsModel] = Field(
        None, alias=lib.ACTION_KILL_PROC
    )
    agent_kill_proc_group: Optional[SharedDefaultActionFieldsModel] = Field(
        None, alias=lib.ACTION_KILL_PROC_GRP
    )

    @model_validator(mode="after")
    def validate_only_one_action(self):
        values = self.model_dump(by_alias=True, exclude_unset=True)
        actions_count = len(values)
        if actions_count > 1:
            raise ValueError(
                "Detected multiple action definitions in one action. Each"
                " action definition must be a separate entry in the list."
            )
        return self

    model_config = ConfigDict(extra="forbid")


class ResponseActionsModel(BaseModel):
    make_redflag: Optional[MakeRedflagModel] = Field(
        None, alias=lib.ACTION_MAKE_REDFLAG
    )
    make_opsflag: Optional[MakeOpsflagModel] = Field(
        None, alias=lib.ACTION_MAKE_OPSFLAG
    )
    agent_kill_pod: Optional[SharedActionFieldsModel] = Field(
        None, alias=lib.ACTION_KILL_POD
    )
    agent_kill_proc: Optional[SharedActionFieldsModel] = Field(
        None, alias=lib.ACTION_KILL_PROC
    )
    agent_kill_proc_group: Optional[SharedActionFieldsModel] = Field(
        None, alias=lib.ACTION_KILL_PROC_GRP
    )

    @model_validator(mode="after")
    def validate_only_one_action(self):
        values = self.model_dump(by_alias=True, exclude_unset=True)
        actions_count = len(values)
        if actions_count > 1:
            raise ValueError(
                "Detected multiple action definitions in one action. Each"
                " action definition must be a separate entry in the list."
            )
        return self

    @model_validator(mode="after")
    def validated_not_none_if_set(self):
        values = self.model_dump(by_alias=True, exclude_unset=True)
        value = next(iter(values.values()))
        if value is None:
            raise ValueError("Non-default actions must have a selector")
        return self

    model_config = ConfigDict(extra="forbid")


class GuardianResponseModel(BaseModel):
    default_field: List[DefaultActionsModel] = Field(
        alias=lib.RESP_DEFAULT_FIELD
    )
    response_field: List[ResponseActionsModel] = Field(
        alias=lib.RESP_ACTIONS_FIELD
    )


# Metadata Models -------------------------------------------------------------


class GuardianMetadataModel(BaseModel):
    name: str = Field(alias=lib.METADATA_NAME_FIELD)
    type: Literal[tuple(lib.GUARDIAN_POL_TYPES)] = Field(  # type: ignore
        alias=lib.METADATA_TYPE_FIELD
    )
    create_time: Optional[Union[int, float, str]] = Field(
        None, alias=lib.METADATA_CREATE_TIME
    )
    first_timestamp: Optional[Union[int, float, str]] = Field(
        None, alias=lib.FIRST_TIMESTAMP_FIELD
    )
    latest_timestamp: Optional[Union[int, float, str]] = Field(
        None, alias=lib.LATEST_TIMESTAMP_FIELD
    )
    uid: Optional[str] = Field(None, alias=lib.METADATA_UID_FIELD)
    checksum: Optional[str] = Field(None, alias=lib.METADATA_S_CHECKSUM_FIELD)


class GuardianFingerprintGroupMetadataModel(BaseModel):
    image: Optional[str] = Field(None, alias=lib.IMAGE_FIELD)
    image_id: Optional[str] = Field(None, alias=lib.IMAGEID_FIELD)
    cgroup: Optional[str] = Field(None, alias=lib.CGROUP_FIELD)
    first_timestamp: Optional[Union[int, float]] = Field(
        None, alias=lib.FIRST_TIMESTAMP_FIELD
    )
    latest_timestamp: Optional[Union[int, float]] = Field(
        None, alias=lib.LATEST_TIMESTAMP_FIELD
    )


class GuardianDeviationMetadataModel(BaseModel):
    type: str = Field(alias=lib.METADATA_TYPE_FIELD)
    policy_uid: str = Field(alias="policy_uid")
    checksum: str = Field(alias=lib.CHECKSUM_FIELD)
    uid: str = Field(alias=lib.METADATA_UID_FIELD)


# Spec Models -----------------------------------------------------------------


class GuardianPolicySpecFieldsModel(BaseModel):
    enabled: Optional[bool] = Field(None, alias=lib.ENABLED_FIELD)
    mode: Literal[tuple(lib.POL_MODES)] = Field(  # type: ignore
        alias=lib.POL_MODE_FIELD
    )


class GuardianPolicySpecModel(
    GuardianSelectorsModel,
    GuardianSpecOptionsModel,
    GuardianPolicySpecFieldsModel,
):
    process_policy: List[ProcessNodeModel] = Field(alias=lib.PROC_POLICY_FIELD)
    network_policy: NetworkPolicyModel = Field(alias=lib.NET_POLICY_FIELD)
    response: GuardianResponseModel = Field(alias=lib.RESPONSE_FIELD)
    model_config = ConfigDict(extra="forbid")


class GuardianBaselineSpecModel(
    GuardianSelectorsModel, GuardianSpecOptionsModel
):
    process_policy: List[ProcessNodeModel] = Field(alias=lib.PROC_POLICY_FIELD)
    network_policy: NetworkPolicyModel = Field(alias=lib.NET_POLICY_FIELD)
    model_config = ConfigDict(extra="forbid")


class GuardianDeviationSpecModel(
    GuardianSelectorsModel, GuardianSpecOptionsModel
):
    process_policy: Optional[
        List[Union[ProcessNodeModel, GuardDeviationNodeModel]]
    ] = Field(None, alias=lib.PROC_POLICY_FIELD)
    network_policy: Optional[DeviationNetworkPolicyModel] = Field(
        None, alias=lib.NET_POLICY_FIELD
    )
    rules: Optional[List[ContainerRule]] = Field(
        None,
        alias=lib.RULES_FIELD,
        # discriminator=lib.RULE_TARGET_FIELD,
    )
    matches: Optional[Dict] = Field(None, alias=lib.RULE_MATCHES_FIELD)
    model_config = ConfigDict(extra="forbid")


class ClusterPolicySpecModel(
    ClusterPolicySelectorsModel, GuardianPolicySpecFieldsModel
):
    rulesets: List[str] = Field(alias=lib.RULESETS_FIELD)
    response: GuardianResponseModel = Field(alias=lib.RESPONSE_FIELD)

    @classmethod
    def get_valid_actions(cls):
        return (
            lib.ACTION_KILL_POD,
            lib.ACTION_MAKE_REDFLAG,
            lib.ACTION_MAKE_OPSFLAG,
        )

    model_config = ConfigDict(extra="forbid")


# Top-level Models ------------------------------------------------------------


class GuardianFingerprintModel(BaseModel):
    api_version: str = Field(alias=lib.API_FIELD)
    kind: Literal[lib.FPRINT_KIND] = (  # type: ignore
        Field(alias=lib.KIND_FIELD)
    )
    metadata: GuardianMetadataModel = Field(alias=lib.METADATA_FIELD)
    spec: GuardianBaselineSpecModel = Field(alias=lib.SPEC_FIELD)

    _selector_validator = model_validator(mode="after")(validate_selectors)

    def __init__(self, **data: Any):
        clear_proc_ids()
        super().__init__(**data)
        clear_proc_ids()

    model_config = ConfigDict(extra="forbid")


class FingerprintGroupDataModel(BaseModel):
    fingerprints: List[GuardianFingerprintModel] = Field(
        alias=lib.FPRINT_GRP_FINGERPRINTS_FIELD
    )
    cont_names: Optional[List[str]] = Field(
        None, alias=lib.FPRINT_GRP_CONT_NAMES_FIELD
    )
    cont_ids: Optional[List[str]] = Field(
        None, alias=lib.FPRINT_GRP_CONT_IDS_FIELD
    )
    machines: Optional[List[str]] = Field(
        None, alias=lib.FPRINT_GRP_MACHINES_FIELD
    )
    model_config = ConfigDict(extra="forbid")


class GuardianFingerprintGroupModel(BaseModel):
    api_version: str = Field(alias=lib.API_FIELD)
    kind: Literal[lib.FPRINT_GROUP_KIND] = (  # type: ignore
        Field(alias=lib.KIND_FIELD)
    )
    metadata: GuardianFingerprintGroupMetadataModel = Field(
        alias=lib.METADATA_FIELD
    )
    data: FingerprintGroupDataModel
    model_config = ConfigDict(extra="ignore")


class GuardianDeviationModel(BaseModel):
    api_version: str = Field(alias=lib.API_FIELD)
    kind: Literal[lib.DEVIATION_KIND] = (  # type: ignore
        Field(alias=lib.KIND_FIELD)
    )
    metadata: GuardianDeviationMetadataModel = Field(alias=lib.METADATA_FIELD)
    spec: GuardianDeviationSpecModel = Field(alias=lib.SPEC_FIELD)

    def __init__(self, **data: Any):
        clear_proc_ids()
        super().__init__(**data)
        clear_proc_ids()


class GuardianBaselineModel(BaseModel):
    api_version: str = Field(alias=lib.API_FIELD)
    kind: Literal[lib.BASELINE_KIND] = (  # type: ignore
        Field(alias=lib.KIND_FIELD)
    )
    metadata: GuardianMetadataModel = Field(alias=lib.METADATA_FIELD)
    spec: GuardianBaselineSpecModel = Field(alias=lib.SPEC_FIELD)

    _selector_validator = model_validator(mode="after")(validate_selectors)

    def __init__(self, **data: Any):
        clear_proc_ids()
        super().__init__(**data)
        clear_proc_ids()

    model_config = ConfigDict(extra="ignore")


class ClusterPolicyModel(BaseModel):
    api_version: str = Field(alias=lib.API_FIELD)
    kind: Literal[lib.POL_KIND] = Field(alias=lib.KIND_FIELD)  # type: ignore
    metadata: GuardianMetadataModel = Field(alias=lib.METADATA_FIELD)
    spec: ClusterPolicySpecModel = Field(alias=lib.SPEC_FIELD)

    _selector_validator = model_validator(mode="after")(validate_selectors)
    model_config = ConfigDict(extra="forbid")


class GuardianPolicyModel(BaseModel):
    api_version: str = Field(alias=lib.API_FIELD)
    kind: Literal[lib.POL_KIND] = Field(alias=lib.KIND_FIELD)  # type: ignore
    metadata: GuardianMetadataModel = Field(alias=lib.METADATA_FIELD)
    spec: GuardianPolicySpecModel = Field(alias=lib.SPEC_FIELD)

    _selector_validator = model_validator(mode="after")(validate_selectors)

    def __init__(self, **data: Any):
        clear_proc_ids()
        super().__init__(**data)
        clear_proc_ids()

    model_config = ConfigDict(extra="forbid")


class GuardianObjectModel(BaseModel):
    api_version: str = Field(alias=lib.API_FIELD)
    kind: str = Field(alias=lib.KIND_FIELD)
    metadata: Dict[str, str] = Field(alias=lib.METADATA_FIELD)
    spec: Dict = Field(alias=lib.SPEC_FIELD)
    model_config = ConfigDict(extra="ignore")


class GuardianObjectListModel(BaseModel):
    api_version: str = Field(alias=lib.API_FIELD)
    items: List[Union[GuardianObjectModel, GuardianFingerprintGroupModel]] = (
        Field(alias=lib.ITEMS_FIELD)
    )


# -----------------------------------------------------------------------------
# Notification Models ---------------------------------------------------------
# -----------------------------------------------------------------------------


class DestinationSlackModel(BaseModel):
    url: str = Field(alias=lib.DST_SLACK_URL)

    @field_validator("url")
    @classmethod
    def valid_url(cls, url):
        if not lib.is_valid_slack_url(url):
            raise ValueError(
                "Invalid url format. "
                "Example: https://hooks.slack.com/services/"
                "xxxxxxxxxxx/xxxxxxxxxxx/xxxxxxxxxxxxxxxxxxxxxxxx"
            )
        return url

    model_config = ConfigDict(extra="forbid")


class DestinationWebhookModel(BaseModel):
    url: str = Field(alias=lib.DST_WEBHOOK_URL)
    no_tls_validation: bool = Field(alias=lib.DST_WEBHOOK_TLS_VAL)

    @field_validator("url")
    @classmethod
    def valid_url(cls, url):
        if not lib.is_valid_url(url):
            raise ValueError(
                "Invalid url format. Example: https://my.url.example"
            )
        return url

    model_config = ConfigDict(extra="forbid")


class DestinationSNSModel(BaseModel):
    cross_account_iam_role: Optional[str] = Field(
        None, alias=lib.DST_SNS_CROSS_ACCOUNT_ROLE
    )
    sns_topic_arn: str = Field(alias=lib.DST_SNS_TOPIC_ARN)
    model_config = ConfigDict(extra="forbid")


def validate_email(email: str):
    if not lib.is_valid_email(email):
        raise ValueError("Email format is invalid.")
    return email


class AllDestinationsModel(BaseModel):
    org_uid: Optional[str] = Field(None, alias=lib.DST_TYPE_ORG)
    emails: Optional[List[Annotated[str, AfterValidator(validate_email)]]] = (
        Field(None, alias=lib.DST_TYPE_EMAIL)
    )
    users: Optional[List[str]] = Field(None, alias=lib.DST_TYPE_USERS)
    slack: Optional[DestinationSlackModel] = Field(
        None, alias=lib.DST_TYPE_SLACK
    )
    webhook: Optional[DestinationWebhookModel] = Field(
        None, alias=lib.DST_TYPE_WEBHOOK
    )
    sns: Optional[DestinationSNSModel] = Field(None, alias=lib.DST_TYPE_SNS)

    @model_validator(mode="after")
    def ensure_not_none(self):
        values = self.model_dump(by_alias=True, exclude_unset=True)
        for key, value in values.items():
            if value is None:
                raise ValueError(f"Field '{key}' cannot be None")
        return self

    @model_validator(mode="after")
    def one_destination(self):
        values = self.model_dump(by_alias=True, exclude_unset=True)
        count = 0
        for dst_type in lib.DST_TYPES:
            if dst_type in values:
                count += 1
        if count == 0:
            raise ValueError(
                f"One destination type is required. {lib.DST_TYPES}"
            )
        if count > 1:
            raise ValueError("Only one destination type is allowed.")
        return self

    model_config = ConfigDict(extra="forbid")


class NotificationTargetModel(AllDestinationsModel):
    data: Optional[Dict] = Field(None, alias=lib.DST_DATA)
    description: Optional[str] = Field(
        None, alias=lib.DST_DESCRIPTION, max_length=128
    )
    model_config = ConfigDict(extra="forbid")


class NotifTgtMetadataModel(BaseModel):
    name: str = Field(alias=lib.METADATA_NAME_FIELD)
    uid: str = Field(alias=lib.METADATA_UID_FIELD)
    create_time: Optional[Union[float, int]] = Field(
        None, alias=lib.METADATA_CREATE_TIME
    )
    update_time: Optional[Union[float, int]] = Field(
        None, alias=lib.NOTIF_LAST_UPDATED
    )


class NotifTgtSpecModel(AllDestinationsModel):
    pass


class NotificationTgtResourceModel(BaseModel):
    api_version: str = Field(alias=lib.API_FIELD)
    kind: Literal[lib.TARGET_KIND] = (  # type: ignore
        Field(alias=lib.KIND_FIELD)
    )
    metadata: NotifTgtMetadataModel = Field(alias=lib.METADATA_FIELD)
    spec: NotifTgtSpecModel = Field(alias=lib.SPEC_FIELD)
    model_config = ConfigDict(extra="forbid")


class NotifAnaConfigMetadataModel(BaseModel):
    name: str = Field(alias=lib.METADATA_NAME_FIELD)
    uid: str = Field(alias=lib.METADATA_UID_FIELD)
    notif_type: Literal[lib.NOTIF_TYPE_OBJECT] = Field(  # type: ignore
        lib.METADATA_TYPE_FIELD
    )
    create_time: Optional[Union[float, int]] = Field(
        None, alias=lib.METADATA_CREATE_TIME
    )
    update_time: Optional[Union[float, int]] = Field(
        None, alias=lib.NOTIF_LAST_UPDATED
    )


class NotifAnaConfigMetricsMetadataModel(NotifAnaConfigMetadataModel):
    notif_type: Literal[lib.NOTIF_TYPE_METRICS] = Field(  # type: ignore
        lib.METADATA_TYPE_FIELD
    )


class NotifAdditionalFieldsModel(BaseModel):
    details: Optional[Dict[str, str]] = None
    linkback_text: Optional[str] = None
    linkback_url: Optional[str] = None
    slack_icon: Optional[str] = None

    @model_validator(mode="after")
    def ensure_not_none(self):
        values = self.model_dump(by_alias=True, exclude_unset=True)
        for key, value in values.items():
            if value is None:
                raise ValueError(f"Field '{key}' cannot be None")
        return self


class NotifAdvancedCooldown(BaseModel):
    by_field: Union[str, List[str]] = Field(
        alias=lib.NOTIF_COOLDOWN_BY_FIELD_FIELD, min_length=1
    )
    for_seconds: int = Field(alias=lib.NOTIF_COOLDOWN_SECONDS_FIELD)


class NotifAnaConfigSpecModel(BaseModel):
    enabled: Optional[bool] = Field(None, alias=lib.ENABLED_FIELD)
    condition: str = Field(alias=lib.NOTIF_CONDITION_FIELD)
    message: str = Field(alias=lib.NOTIF_MESSAGE_FIELD)
    target: Union[str, List[str]] = Field(
        alias=lib.NOTIF_TARGET_FIELD, min_length=1
    )
    schema_type: str = Field(alias=lib.NOTIF_DEFAULT_SCHEMA)
    sub_schema: Optional[str] = Field(None, alias=lib.NOTIF_SUB_SCHEMA)
    title: str = Field(alias=lib.NOTIF_TITLE_FIELD)
    additional_fields: Dict = Field(alias=lib.NOTIF_ADDITIONAL_FIELDS)
    template: str = Field(alias=lib.NOTIF_TEMPLATE_FIELD)
    cooldown: Optional[Union[int, NotifAdvancedCooldown]] = Field(
        None, alias=lib.NOTIF_COOLDOWN_FIELD
    )

    @model_validator(mode="after")
    def validate_condition(self):
        import spyctl.api as api
        import spyctl.config.configs as cfg

        ctx = cfg.get_current_context()
        error = api.validate_search_query(
            *ctx.get_api_data(), self.schema_type, self.condition
        )
        if error and False:
            raise ValueError(error)
        return self

    model_config = ConfigDict(extra="forbid")


class NotifAnaConfigMetricsSpecModel(NotifAnaConfigSpecModel):
    for_duration: Optional[int] = Field(
        None, alias=lib.NOTIF_FOR_DURATION_FIELD
    )
    schema_type: Literal[lib.EVENT_METRICS_PREFIX] = Field(  # type: ignore
        alias=lib.NOTIF_DEFAULT_SCHEMA
    )
    model_config = ConfigDict(extra="forbid")


class NotificationConfigModel(BaseModel):
    api_version: str = Field(alias=lib.API_FIELD)
    kind: Literal[lib.NOTIFICATION_KIND] = (  # type: ignore
        Field(alias=lib.KIND_FIELD)
    )
    metadata: NotifAnaConfigMetadataModel = Field(alias=lib.METADATA_FIELD)
    spec: NotifAnaConfigSpecModel = Field(alias=lib.SPEC_FIELD)
    model_config = ConfigDict(extra="forbid")


class NotificationConfigMetricsModel(NotificationConfigModel):
    metadata: NotifAnaConfigMetricsMetadataModel = Field(
        alias=lib.METADATA_FIELD
    )
    spec: NotifAnaConfigMetricsSpecModel = Field(alias=lib.SPEC_FIELD)
    model_config = ConfigDict(extra="forbid")


class NotificationRouteDataModel(BaseModel):
    analytics_settings: Optional[NotificationConfigModel] = None


class NotificationRouteModel(BaseModel):
    targets: Optional[List[str]] = Field(None, alias=lib.ROUTE_TARGETS)
    destination: Optional[NotificationConfigModel] = Field(
        None, alias=lib.ROUTE_DESTINATION
    )
    data: Optional[Dict] = Field(None, alias=lib.ROUTE_DATA)
    description: Optional[str] = Field(None, alias=lib.ROUTE_DESCRIPTION)
    expr: Optional[Dict] = Field(None, alias=lib.ROUTE_EXPR)
    model_config = ConfigDict(extra="forbid")


class NotificationPolicyModel(BaseModel):
    targets: Optional[Dict[str, NotificationTargetModel]] = Field(
        None, alias=lib.TARGETS_FIELD
    )
    routes: Optional[List[NotificationRouteModel]] = Field(
        None, alias=lib.ROUTES_FIELD
    )

    @field_validator("targets")
    @classmethod
    def validate_target_name(cls, v):
        for name in v:
            if len(name) > 64:
                raise ValueError(
                    "Target name must be less than 64 characters."
                )
            if not lib.is_valid_tgt_name(name):
                raise ValueError(
                    "Target name must be only letters, numbers, and valid"
                    f" symbols {lib.TGT_NAME_VALID_SYMBOLS}."
                )
        return v

    model_config = ConfigDict(extra="forbid")


# -----------------------------------------------------------------------------
# Suppression Models ----------------------------------------------------------
# -----------------------------------------------------------------------------


class SuppressionPolicySelectorsModel(BaseModel):
    trace_selector: Optional[TraceSelectorModel] = Field(
        None, alias=lib.TRACE_SELECTOR_FIELD
    )
    user_selector: Optional[UserSelectorModel] = Field(
        None, alias=lib.USER_SELECTOR_FIELD
    )

    @model_validator(mode="after")
    def ensure_one_field(self):
        values = self.model_dump(by_alias=True, exclude_unset=True)
        if not any(
            value
            for field, value in values.items()
            if field.endswith("Selector")
        ):
            raise ValueError("Selectors must have values.")
        return self

    model_config = ConfigDict(extra="forbid")


# Metadata Models -------------------------------------------------------------


class SuppressionPolicyMetadataModel(BaseModel):
    name: str = Field(alias=lib.METADATA_NAME_FIELD)
    type: Literal[tuple(lib.SUPPRESSION_POL_TYPES)] = Field(  # type: ignore
        alias=lib.METADATA_TYPE_FIELD
    )
    create_time: Optional[Union[int, float, str]] = Field(
        None, alias=lib.METADATA_CREATE_TIME
    )
    first_timestamp: Optional[Union[int, float]] = Field(
        None, alias=lib.FIRST_TIMESTAMP_FIELD
    )
    latest_timestamp: Optional[Union[int, float]] = Field(
        None, alias=lib.LATEST_TIMESTAMP_FIELD
    )
    uid: Optional[str] = Field(None, alias=lib.METADATA_UID_FIELD)
    checksum: Optional[str] = Field(None, alias=lib.METADATA_S_CHECKSUM_FIELD)


# Spec Models -----------------------------------------------------------------


class AllowedFlagsModel(BaseModel):
    class_field: str = Field(alias=lib.FLAG_CLASS)


class SuppressionPolicySpecModel(SuppressionPolicySelectorsModel):
    enabled: Optional[bool] = Field(None, alias=lib.ENABLED_FIELD)
    mode: Literal[tuple(lib.POL_MODES)] = Field(  # type: ignore
        alias=lib.POL_MODE_FIELD
    )
    allowed_flags: List[AllowedFlagsModel] = Field(
        alias=lib.ALLOWED_FLAGS_FIELD
    )
    model_config = ConfigDict(extra="forbid")


# Top-level Models ------------------------------------------------------------


class SuppressionPolicyModel(BaseModel):
    api_version: str = Field(alias=lib.API_FIELD)
    kind: Literal[lib.POL_KIND] = Field(alias=lib.KIND_FIELD)  # type: ignore
    metadata: SuppressionPolicyMetadataModel = Field(alias=lib.METADATA_FIELD)
    spec: SuppressionPolicySpecModel = Field(alias=lib.SPEC_FIELD)
    model_config = ConfigDict(extra="forbid")


# -----------------------------------------------------------------------------
# Config Models ----------------------------------------------------------
# -----------------------------------------------------------------------------


class ContextModel(BaseModel):
    org: str = Field(alias=lib.ORG_FIELD)
    cgroups: Optional[Union[str, List[str]]] = Field(
        None, alias=lib.CGROUP_FIELD
    )
    cluster: Optional[Union[str, List[str]]] = Field(
        None, alias=lib.CLUSTER_FIELD
    )
    container_ids: Optional[Union[str, List[str]]] = Field(
        None, alias=lib.CONTAINER_ID_FIELD
    )
    container_names: Optional[Union[str, List[str]]] = Field(
        None, alias=lib.CONTAINER_NAME_FIELD
    )
    image_ids: Optional[Union[str, List[str]]] = Field(
        None, alias=lib.IMAGEID_FIELD
    )
    images: Optional[Union[str, List[str]]] = Field(
        None, alias=lib.IMAGE_FIELD
    )
    machines: Optional[Union[str, List[str]]] = Field(
        None, alias=lib.MACHINES_FIELD
    )
    namespace: Optional[Union[str, List[str]]] = Field(
        None, alias=lib.NAMESPACE_FIELD
    )
    pods: Optional[Union[str, List[str]]] = Field(None, alias=lib.POD_FIELD)
    model_config = ConfigDict(extra="forbid")


# Metadata Models -------------------------------------------------------------


class SecretMetadataModel(BaseModel):
    name: str = Field(alias=lib.METADATA_NAME_FIELD)
    create_time: Optional[Union[float, int]] = Field(
        None, alias=lib.METADATA_CREATE_TIME
    )


# Top-level Models ------------------------------------------------------------


class SecretModel(BaseModel):
    api_version: str = Field(alias=lib.API_FIELD)
    kind: Literal[lib.SECRET_KIND] = (  # type: ignore
        Field(alias=lib.KIND_FIELD)
    )
    metadata: SecretMetadataModel = Field(alias=lib.METADATA_FIELD)
    data: Optional[Dict[str, str]] = Field(None, alias=lib.DATA_FIELD)
    string_data: Optional[Dict[str, str]] = Field(
        None, alias=lib.STRING_DATA_FIELD
    )
    model_config = ConfigDict(extra="forbid")


class ContextsModel(BaseModel):
    context_name: str = Field(alias=lib.CONTEXT_NAME_FIELD)
    secret: str = Field(alias=lib.SECRET_FIELD)
    context: ContextModel = Field(alias=lib.CONTEXT_FIELD)
    model_config = ConfigDict(extra="forbid")


class ConfigModel(BaseModel):
    api_version: str = Field(alias=lib.API_FIELD)
    kind: Literal[lib.CONFIG_KIND] = (  # type: ignore
        Field(alias=lib.KIND_FIELD)
    )
    contexts: List[ContextsModel] = Field(alias=lib.CONTEXTS_FIELD)
    current_context: str = Field(alias=lib.CURR_CONTEXT_FIELD)
    model_config = ConfigDict(extra="forbid")


# -----------------------------------------------------------------------------
# Misc Models -----------------------------------------------------------------
# -----------------------------------------------------------------------------


class UidListMetadataModel(BaseModel):
    start_time: Union[int, float] = Field(alias=lib.METADATA_START_TIME_FIELD)
    end_time: Union[int, float] = Field(alias=lib.METADATA_END_TIME_FIELD)

    @model_validator(mode="after")
    def valid_end_time(self):
        if self.end_time <= self.start_time:
            raise ValueError(
                f"'{lib.METADATA_END_TIME_FIELD}' must be greater than"
                f" '{lib.METADATA_START_TIME_FIELD}'"
            )
        return self


class UidListDataModel(BaseModel):
    uids: List[str] = Field(alias=lib.UIDS_FIELD)
    model_config = ConfigDict(extra="forbid")


class UidListModel(BaseModel):
    api_version: str = Field(alias=lib.API_FIELD)
    kind: Literal[lib.UID_LIST_KIND] = (  # type: ignore
        Field(alias=lib.KIND_FIELD)
    )
    metadata: UidListMetadataModel = Field(alias=lib.METADATA_FIELD)
    data: UidListDataModel = Field(alias=lib.DATA_FIELD)
    model_config = ConfigDict(extra="forbid")


class SpyderbatObject(BaseModel):
    api_version: Literal[lib.API_VERSION] = (  # type: ignore
        Field(alias=lib.API_FIELD)
    )
    kind: str = Field(alias=lib.KIND_FIELD)

    @field_validator("kind")
    @classmethod
    def valid_kind(cls, v):
        if v not in KIND_TO_SCHEMA:
            raise ValueError(f"Kind '{v}' not in {list(KIND_TO_SCHEMA)}")
        return v

    model_config = ConfigDict(extra="allow")


KIND_TO_SCHEMA: Dict[str, BaseModel] = {
    lib.BASELINE_KIND: GuardianBaselineModel,
    lib.CONFIG_KIND: ConfigModel,
    lib.FPRINT_GROUP_KIND: GuardianFingerprintGroupModel,
    lib.FPRINT_KIND: GuardianFingerprintModel,
    lib.POL_KIND: GuardianPolicyModel,
    (lib.POL_KIND, lib.POL_TYPE_TRACE): SuppressionPolicyModel,
    (lib.POL_KIND, lib.POL_TYPE_CLUS): ClusterPolicyModel,
    lib.SECRET_KIND: SecretModel,
    lib.UID_LIST_KIND: UidListModel,
    lib.DEVIATION_KIND: GuardianDeviationModel,
    lib.NOTIFICATION_KIND: NotificationConfigModel,
    (
        lib.NOTIFICATION_KIND,
        lib.NOTIF_TYPE_METRICS,
    ): NotificationConfigMetricsModel,
    lib.TARGET_KIND: NotificationTgtResourceModel,
    lib.CLUSTER_RULESET_RESOURCE.kind: RulesetModel,
}


def clear_proc_ids():
    __PROC_IDS.clear()


def in_proc_ids(proc_id: str) -> bool:
    return proc_id in __PROC_IDS


def add_proc_id(proc_id: str):
    __PROC_IDS[proc_id] = True
