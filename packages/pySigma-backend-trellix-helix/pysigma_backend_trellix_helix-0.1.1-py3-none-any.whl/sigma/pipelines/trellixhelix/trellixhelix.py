from sigma.processing.conditions import LogsourceCondition
from sigma.processing.transformations import AddConditionTransformation, FieldMappingTransformation, DetectionItemFailureTransformation, RuleFailureTransformation, SetStateTransformation, ChangeLogsourceTransformation
from sigma.processing.conditions import LogsourceCondition, IncludeFieldCondition, ExcludeFieldCondition, RuleProcessingItemAppliedCondition
from sigma.processing.pipeline import ProcessingItem, ProcessingPipeline
from sigma.rule import SigmaDetectionItem
from sigma.exceptions import SigmaTransformationError

class InvalidFieldTransformation(DetectionItemFailureTransformation):
    def apply_detection_item(self, detection_item: SigmaDetectionItem) -> None:
        fiele_name = detection_item.field
        self.message = f"Invalid fieldname encounter: {fiele_name}." + self.message
        raise SigmaTransformationError(self.message)

def _flatten(items, seqtypes=(list, tuple)):
    """Private function to flatten lists for Field mapping errors"""
    try:
        for i, x in enumerate(items):
            while isinstance(items[i], seqtypes):
                items[i:i+1] = items[i]
    except IndexError:
        pass
    return items

def trellix_helix_pipeline() -> ProcessingPipeline:
    translation_dict = {
        'windows_events':{
            "AccountDomain": "accountdomain",
            "AccountName": "accountdomain",
            "Application": "process.executable",
            "Channel": "eventlog",
            "ClientAddress": "srcipv4",
            "CommandLine":"args",
            "ComputerName": "hostname",
            "CurrentDirectory":"processpath",
            "Description": "errormessage", #helix use error message 
            "DestAddress": "dstipv4",
            "DestinationIp": "dstipv4",
            "DestinationPort": "dstport",
            "DestPort": "dstport",
            "EventID": "eventid",
            "FileName": "filename",
            "Image": "process",
            "imphash": "imphash",
            "IntegrityLevel": "integritylevel",
            "IpAddress": "srcipv4",
            "IpPort": "srcport",
            "LogonGuid": "logonguid",
            "LogonId": "logonid",
            "md5": "md5",
            "NewProcessId": "pid",
            "NewProcessName": "process",
            "OriginalFileName": "original_file_name",
            "ParentCommandLine": "pargs",
            "ParentImage": "pprocess",
            "ParentProcessGuid": "pprocessguid",
            "ParentProcessId": "ppid",
            "ParentProcessName": "process.parent.name",
            "PipeName": "filename",
            "ProcessGuid": "processguid",
            "ProcessId": "pid",
            "ProcessName": "process",
            "Product": "product",
            "Provider_Name": "source",
            "QueryName": "query",
            "QueryStatus": "statuscode",
            "sha256": "sha256",
            "SourceAddress": "srcipv4",
            "SourceHostname": "hostname",
            "SourceIp": "srcipv4",
            "SourcePort": "srcport",
            "SourceThreadId": "threadid",
            "TargetDomainName": "accountdomain",
            "TargetFilename": "filename",
            "TerminalSessionId":"sessionid",
            "User": "username"
        }
        #need to add other events
    }

    object_class_filter = [
        # Add Class = ms_windows_event
        ProcessingItem(
            identifier="trellix_class_windows",
            transformation=AddConditionTransformation({
                "metaclass": "windows"
            }),
            rule_conditions=[
                LogsourceCondition(product="windows")
            ]
        )
        # need to add other product
        # ProcessingItem(
        #     identifier="trellix_class_network",
        #     transformation=AddConditionTransformation({
        #         "metaclass": "network"
        #     }),
        #     rule_conditions=[
        #         LogsourceCondition(product="network")
        #     ]
        # ),
        # ProcessingItem(
        #     identifier="trellix_class_web",
        #     transformation=AddConditionTransformation({
        #         "metaclass": "unix"
        #     }),
        #     rule_conditions=[
        #         LogsourceCondition(product="webserver")
        #     ]
        # )
    ]

    object_eventlog_filter = [
        # Add Category = Process Create
        ProcessingItem(
            identifier="trellix_process_creation_eventtype",
            transformation=AddConditionTransformation({
                "category": ["process create (rule: processcreate)","process creation"]
            }),
            rule_conditions=[
                LogsourceCondition(category="process_creation")
            ]
        ),
        ProcessingItem(
            identifier="trellix_file_eventtype",
            transformation=AddConditionTransformation({
                "category": ["file created (rule: filecreate)","file system"]
            }),
            rule_conditions=[
                LogsourceCondition(category="file")
            ]
        ),
        # ProcessingItem(
        #     identifier="trellix_network_connection_eventtype",
        #     transformation=AddConditionTransformation({
        #         "category": "network connection detected (rule: networkconnect)"
        #     }),
        #     rule_conditions=[
        #         LogsourceCondition(category="network_connection") #initiated field not present
        #     ]
        # ),
        # ProcessingItem(
        #     identifier="trellix_powershell_eventtype",
        #     transformation=AddConditionTransformation({
        #         "source": "microsoft-windows-powershell"
        #     }),
        #     rule_conditions=[
        #         LogsourceCondition(category="powershell") #scriptblock in msg
        #     ]
        # ),
        ProcessingItem(
            identifier="trellix_dns_eventtype",
            transformation=AddConditionTransformation({
                "category": "dns query (rule: dnsquery)"
            }),
            rule_conditions=[
                LogsourceCondition(category="dns_query")
            ]
        )
        # ProcessingItem(
        #     identifier="trellix_registry_eventtype",
        #     transformation=AddConditionTransformation({
        #         "category": ["registry value set (rule: registryevent)","registry object added or deleted (rule: registryevent)"]
        #     }),
        #     rule_conditions=[
        #         LogsourceCondition(category="registry") # targetobject not present
        #     ]
        # )
    ]

    fields_mappings = [
        # Process Creation
        ProcessingItem(
            identifier="helix_process_creation_mapping",
            transformation=FieldMappingTransformation(translation_dict['windows_events']),
            rule_conditions=[
                LogsourceCondition(product="windows")
            ]
        )
    ]

    change_logsource_info = [
        # Add service to be Helix for pretty much everything
        ProcessingItem(
            identifier="helix_logsource",
            transformation=ChangeLogsourceTransformation(
                service="helix"
            ),
            rule_condition_linking=any,
            rule_conditions=[
                LogsourceCondition(category="process_creation"),
                LogsourceCondition(category="file"),
                LogsourceCondition(category="file_event"),
                LogsourceCondition(category="powershell"),
                # LogsourceCondition(category="pipe_creation"),
                LogsourceCondition(category="registry"),
                LogsourceCondition(category="dns_query"),
                LogsourceCondition(category="network_connection")
                # LogsourceCondition(category="firewall")
            ]
        ),
    ]

    unsupported_rule_types = [
        # Show error if unsupported option
        ProcessingItem(
            identifier="helix_fail_rule_not_supported",
            rule_condition_linking=any,
            transformation=RuleFailureTransformation("Rule type not yet supported by the Helix Sigma backend"),
            rule_condition_negation=True,
            rule_conditions=[
                RuleProcessingItemAppliedCondition("helix_logsource")
            ]
        )
    ]

    unsupported_field_name = [
        ProcessingItem(
            identifier='helix_fail_field_not_supported',
            transformation=InvalidFieldTransformation("This pipeline only supports the following fields:\n{" + 
            '}, {'.join(sorted(set(
                list(_flatten([[k,v] for t in translation_dict.keys() for k, v in
                            translation_dict[t].items()]))
            )))),
            field_name_conditions=[
                ExcludeFieldCondition(fields=list(set(
                    list(_flatten([[k, v] for t in translation_dict.keys() for k, v in
                                translation_dict[t].items()]))
                )))
            ]
        )
    ]

    return ProcessingPipeline(
        name="Trellix_Helix pipeline",
        priority=50,
        items = [
            *unsupported_field_name,
            *object_class_filter,
            *object_eventlog_filter,
            *fields_mappings,
            *change_logsource_info,
            *unsupported_rule_types,
        ]
    )
