from aiovemmio import addon_pb2 as _addon_pb2
from aiovemmio import admin_pb2 as _admin_pb2
from aiovemmio import battery_pb2 as _battery_pb2
from aiovemmio import ble_pb2 as _ble_pb2
from aiovemmio import carbon_monoxide_pb2 as _carbon_monoxide_pb2
from aiovemmio import color_pb2 as _color_pb2
from aiovemmio import configuration_pb2 as _configuration_pb2
from aiovemmio import devices_pb2 as _devices_pb2
from aiovemmio import firmware_pb2 as _firmware_pb2
from aiovemmio import gate_pb2 as _gate_pb2
from aiovemmio import gateway_pb2 as _gateway_pb2
from aiovemmio import info_pb2 as _info_pb2
from aiovemmio import level_pb2 as _level_pb2
from aiovemmio import lock_pb2 as _lock_pb2
from aiovemmio import messaging_pb2 as _messaging_pb2
from aiovemmio import meter_pb2 as _meter_pb2
from aiovemmio import remote_pb2 as _remote_pb2
from aiovemmio import roller_shutter_pb2 as _roller_shutter_pb2
from aiovemmio import siren_pb2 as _siren_pb2
from aiovemmio import status_pb2 as _status_pb2
from aiovemmio import structure_pb2 as _structure_pb2
from aiovemmio import switch_pb2 as _switch_pb2
from aiovemmio import temperature_pb2 as _temperature_pb2
from aiovemmio import thermostat_pb2 as _thermostat_pb2
from aiovemmio import ultraviolet_pb2 as _ultraviolet_pb2
from aiovemmio import wifi_pb2 as _wifi_pb2
from aiovemmio import zigbee_pb2 as _zigbee_pb2
from aiovemmio import zwave_pb2 as _zwave_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
REPLY_TYPE_ACK: CommandReplyType
REPLY_TYPE_DATA: CommandReplyType
REPLY_TYPE_EOF: CommandReplyType
REPLY_TYPE_ERROR: CommandReplyType
REPLY_TYPE_UNSPECIFIED: CommandReplyType
REQUEST_OPTION_NOACK: CommandRequestOption
REQUEST_OPTION_NORESPONSE: CommandRequestOption
REQUEST_OPTION_UNSPECIFIED: CommandRequestOption
REQUEST_TYPE_DATA: CommandRequestType
REQUEST_TYPE_EOF: CommandRequestType
REQUEST_TYPE_UNSPECIFIED: CommandRequestType

class CommandReply(_message.Message):
    __slots__ = ["data", "error", "payload", "type"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    data: CommandReplyData
    error: CommandReplyError
    payload: bytes
    type: CommandReplyType
    def __init__(self, type: _Optional[_Union[CommandReplyType, str]] = ..., error: _Optional[_Union[CommandReplyError, _Mapping]] = ..., data: _Optional[_Union[CommandReplyData, _Mapping]] = ..., payload: _Optional[bytes] = ...) -> None: ...

class CommandReplyData(_message.Message):
    __slots__ = ["AddonAddThermostat", "AddonList", "BatteryGet", "CarbonMonoxideGet", "ColorSet", "ConfigurationGet", "ConfigurationList", "ConfigurationSet", "DevicesList", "DisableAdvertising", "EnableAdvertising", "FirmwareLatestVersion", "FirmwareUpdate", "FirmwareUpgrade", "FirmwareUpload", "FollowLogs", "GateClose", "GateCycle", "GateOpen", "GetStructure", "Info", "KeyDown", "KeyUp", "LevelDecrease", "LevelDown", "LevelGet", "LevelGetStep", "LevelIncrease", "LevelSet", "LevelUp", "LockSet", "MeterGet", "MeterReset", "ReadLogs", "Reboot", "Restart", "RollerShutterClose", "RollerShutterOpen", "RollerShutterSet", "SirenGetDefaultTone", "SirenGetTones", "SirenGetVolume", "SirenPlayDefaultTone", "SirenPlayTone", "SirenSetDefaultTone", "SirenSetVolume", "StartSupport", "StatusCheck", "StopSupport", "SwitchOff", "SwitchOn", "TemperatureGet", "ThermostatFanModeSet", "ThermostatModeSet", "ThermostatModeSupGet", "ThermostatSetpointSet", "UltravioletGet", "WalkNodes", "WiFiConnect", "WiFiQuery", "WiFiScan", "ZWaveAbort", "ZWaveAddEntry", "ZWaveExclude", "ZWaveHeal", "ZWaveHealthCheck", "ZWaveInclude", "ZWaveListEntries", "ZWaveNotificationItems", "ZWaveReadNode", "ZWaveReadNodes", "ZWaveRemoveEntry", "ZWaveRemoveFailed", "ZWaveReplaceFailed", "ZWaveReset", "ZWaveTest", "ZWaveUpdate", "ZWaveUpdateNode", "ZigbeeExclude", "ZigbeeGetNodes", "ZigbeeInclude"]
    ADDONADDTHERMOSTAT_FIELD_NUMBER: _ClassVar[int]
    ADDONLIST_FIELD_NUMBER: _ClassVar[int]
    AddonAddThermostat: _addon_pb2.AddonAddResponse
    AddonList: _addon_pb2.AddonListResponse
    BATTERYGET_FIELD_NUMBER: _ClassVar[int]
    BatteryGet: _battery_pb2.BatteryGetResponse
    CARBONMONOXIDEGET_FIELD_NUMBER: _ClassVar[int]
    COLORSET_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATIONGET_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATIONLIST_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATIONSET_FIELD_NUMBER: _ClassVar[int]
    CarbonMonoxideGet: _carbon_monoxide_pb2.CarbonMonoxideGetResponse
    ColorSet: _color_pb2.ColorResponse
    ConfigurationGet: _configuration_pb2.ConfigurationGetResponse
    ConfigurationList: _configuration_pb2.ConfigurationListResponse
    ConfigurationSet: _configuration_pb2.ConfigurationSetResponse
    DEVICESLIST_FIELD_NUMBER: _ClassVar[int]
    DISABLEADVERTISING_FIELD_NUMBER: _ClassVar[int]
    DevicesList: _devices_pb2.DevicesListResponse
    DisableAdvertising: _ble_pb2.AdvertisingResponse
    ENABLEADVERTISING_FIELD_NUMBER: _ClassVar[int]
    EnableAdvertising: _ble_pb2.AdvertisingResponse
    FIRMWARELATESTVERSION_FIELD_NUMBER: _ClassVar[int]
    FIRMWAREUPDATE_FIELD_NUMBER: _ClassVar[int]
    FIRMWAREUPGRADE_FIELD_NUMBER: _ClassVar[int]
    FIRMWAREUPLOAD_FIELD_NUMBER: _ClassVar[int]
    FOLLOWLOGS_FIELD_NUMBER: _ClassVar[int]
    FirmwareLatestVersion: _firmware_pb2.FirmwareLatestVersionResponse
    FirmwareUpdate: _firmware_pb2.FirmwareUpdateResponse
    FirmwareUpgrade: _firmware_pb2.FirmwareUpgradeAck
    FirmwareUpload: _firmware_pb2.FirmwareChunkAck
    FollowLogs: _admin_pb2.LogsChunk
    GATECLOSE_FIELD_NUMBER: _ClassVar[int]
    GATECYCLE_FIELD_NUMBER: _ClassVar[int]
    GATEOPEN_FIELD_NUMBER: _ClassVar[int]
    GETSTRUCTURE_FIELD_NUMBER: _ClassVar[int]
    GateClose: _gate_pb2.GateResponse
    GateCycle: _gate_pb2.GateResponse
    GateOpen: _gate_pb2.GateResponse
    GetStructure: _structure_pb2.StructureResponse
    INFO_FIELD_NUMBER: _ClassVar[int]
    Info: _info_pb2.InfoResponse
    KEYDOWN_FIELD_NUMBER: _ClassVar[int]
    KEYUP_FIELD_NUMBER: _ClassVar[int]
    KeyDown: _remote_pb2.RemoteResponse
    KeyUp: _remote_pb2.RemoteResponse
    LEVELDECREASE_FIELD_NUMBER: _ClassVar[int]
    LEVELDOWN_FIELD_NUMBER: _ClassVar[int]
    LEVELGETSTEP_FIELD_NUMBER: _ClassVar[int]
    LEVELGET_FIELD_NUMBER: _ClassVar[int]
    LEVELINCREASE_FIELD_NUMBER: _ClassVar[int]
    LEVELSET_FIELD_NUMBER: _ClassVar[int]
    LEVELUP_FIELD_NUMBER: _ClassVar[int]
    LOCKSET_FIELD_NUMBER: _ClassVar[int]
    LevelDecrease: _level_pb2.LevelResponse
    LevelDown: _level_pb2.LevelResponse
    LevelGet: _level_pb2.LevelGetResponse
    LevelGetStep: _level_pb2.LevelGetResponse
    LevelIncrease: _level_pb2.LevelResponse
    LevelSet: _level_pb2.LevelResponse
    LevelUp: _level_pb2.LevelResponse
    LockSet: _lock_pb2.LockResponse
    METERGET_FIELD_NUMBER: _ClassVar[int]
    METERRESET_FIELD_NUMBER: _ClassVar[int]
    MeterGet: _meter_pb2.MeterGetResponse
    MeterReset: _meter_pb2.MeterResetResponse
    READLOGS_FIELD_NUMBER: _ClassVar[int]
    REBOOT_FIELD_NUMBER: _ClassVar[int]
    RESTART_FIELD_NUMBER: _ClassVar[int]
    ROLLERSHUTTERCLOSE_FIELD_NUMBER: _ClassVar[int]
    ROLLERSHUTTEROPEN_FIELD_NUMBER: _ClassVar[int]
    ROLLERSHUTTERSET_FIELD_NUMBER: _ClassVar[int]
    ReadLogs: _admin_pb2.LogsChunk
    Reboot: _gateway_pb2.RebootResponse
    Restart: _gateway_pb2.RestartResponse
    RollerShutterClose: _roller_shutter_pb2.RollerShutterResponse
    RollerShutterOpen: _roller_shutter_pb2.RollerShutterResponse
    RollerShutterSet: _roller_shutter_pb2.RollerShutterResponse
    SIRENGETDEFAULTTONE_FIELD_NUMBER: _ClassVar[int]
    SIRENGETTONES_FIELD_NUMBER: _ClassVar[int]
    SIRENGETVOLUME_FIELD_NUMBER: _ClassVar[int]
    SIRENPLAYDEFAULTTONE_FIELD_NUMBER: _ClassVar[int]
    SIRENPLAYTONE_FIELD_NUMBER: _ClassVar[int]
    SIRENSETDEFAULTTONE_FIELD_NUMBER: _ClassVar[int]
    SIRENSETVOLUME_FIELD_NUMBER: _ClassVar[int]
    STARTSUPPORT_FIELD_NUMBER: _ClassVar[int]
    STATUSCHECK_FIELD_NUMBER: _ClassVar[int]
    STOPSUPPORT_FIELD_NUMBER: _ClassVar[int]
    SWITCHOFF_FIELD_NUMBER: _ClassVar[int]
    SWITCHON_FIELD_NUMBER: _ClassVar[int]
    SirenGetDefaultTone: _siren_pb2.SirenGetDefaultToneResponse
    SirenGetTones: _siren_pb2.SirenGetTonesResponse
    SirenGetVolume: _siren_pb2.SirenGetVolumeResponse
    SirenPlayDefaultTone: _siren_pb2.SirenPlayDefaultToneResponse
    SirenPlayTone: _siren_pb2.SirenPlayToneResponse
    SirenSetDefaultTone: _siren_pb2.SirenSetDefaultToneResponse
    SirenSetVolume: _siren_pb2.SirenSetVolumeResponse
    StartSupport: _gateway_pb2.SupportResponse
    StatusCheck: _status_pb2.StatusCheckResponse
    StopSupport: _gateway_pb2.SupportResponse
    SwitchOff: _switch_pb2.SwitchResponse
    SwitchOn: _switch_pb2.SwitchResponse
    TEMPERATUREGET_FIELD_NUMBER: _ClassVar[int]
    THERMOSTATFANMODESET_FIELD_NUMBER: _ClassVar[int]
    THERMOSTATMODESET_FIELD_NUMBER: _ClassVar[int]
    THERMOSTATMODESUPGET_FIELD_NUMBER: _ClassVar[int]
    THERMOSTATSETPOINTSET_FIELD_NUMBER: _ClassVar[int]
    TemperatureGet: _temperature_pb2.TemperatureGetResponse
    ThermostatFanModeSet: _thermostat_pb2.ThermostatResponse
    ThermostatModeSet: _thermostat_pb2.ThermostatResponse
    ThermostatModeSupGet: _thermostat_pb2.ThermostatModeSupGetResponse
    ThermostatSetpointSet: _thermostat_pb2.ThermostatResponse
    ULTRAVIOLETGET_FIELD_NUMBER: _ClassVar[int]
    UltravioletGet: _ultraviolet_pb2.UltravioletGetResponse
    WALKNODES_FIELD_NUMBER: _ClassVar[int]
    WIFICONNECT_FIELD_NUMBER: _ClassVar[int]
    WIFIQUERY_FIELD_NUMBER: _ClassVar[int]
    WIFISCAN_FIELD_NUMBER: _ClassVar[int]
    WalkNodes: _admin_pb2.WalkNodesResponse
    WiFiConnect: _wifi_pb2.WiFiConnectResponse
    WiFiQuery: _wifi_pb2.WiFiQueryResponse
    WiFiScan: _wifi_pb2.WiFiScanResponse
    ZIGBEEEXCLUDE_FIELD_NUMBER: _ClassVar[int]
    ZIGBEEGETNODES_FIELD_NUMBER: _ClassVar[int]
    ZIGBEEINCLUDE_FIELD_NUMBER: _ClassVar[int]
    ZWAVEABORT_FIELD_NUMBER: _ClassVar[int]
    ZWAVEADDENTRY_FIELD_NUMBER: _ClassVar[int]
    ZWAVEEXCLUDE_FIELD_NUMBER: _ClassVar[int]
    ZWAVEHEALTHCHECK_FIELD_NUMBER: _ClassVar[int]
    ZWAVEHEAL_FIELD_NUMBER: _ClassVar[int]
    ZWAVEINCLUDE_FIELD_NUMBER: _ClassVar[int]
    ZWAVELISTENTRIES_FIELD_NUMBER: _ClassVar[int]
    ZWAVENOTIFICATIONITEMS_FIELD_NUMBER: _ClassVar[int]
    ZWAVEREADNODES_FIELD_NUMBER: _ClassVar[int]
    ZWAVEREADNODE_FIELD_NUMBER: _ClassVar[int]
    ZWAVEREMOVEENTRY_FIELD_NUMBER: _ClassVar[int]
    ZWAVEREMOVEFAILED_FIELD_NUMBER: _ClassVar[int]
    ZWAVEREPLACEFAILED_FIELD_NUMBER: _ClassVar[int]
    ZWAVERESET_FIELD_NUMBER: _ClassVar[int]
    ZWAVETEST_FIELD_NUMBER: _ClassVar[int]
    ZWAVEUPDATENODE_FIELD_NUMBER: _ClassVar[int]
    ZWAVEUPDATE_FIELD_NUMBER: _ClassVar[int]
    ZWaveAbort: _zwave_pb2.ZWaveAbortResponse
    ZWaveAddEntry: _zwave_pb2.ZWaveAddEntryResponse
    ZWaveExclude: _zwave_pb2.ZWaveExcludeStatus
    ZWaveHeal: _zwave_pb2.ZWaveHealResponse
    ZWaveHealthCheck: _zwave_pb2.ZWaveHealthCheckStatus
    ZWaveInclude: _zwave_pb2.ZWaveIncludeStatus
    ZWaveListEntries: _zwave_pb2.ZWaveListEntriesResponse
    ZWaveNotificationItems: _zwave_pb2.ZWaveNotificationItemsResponse
    ZWaveReadNode: _zwave_pb2.ZWaveNodeResponse
    ZWaveReadNodes: _zwave_pb2.ZWaveNodesResponse
    ZWaveRemoveEntry: _zwave_pb2.ZWaveRemoveEntryResponse
    ZWaveRemoveFailed: _zwave_pb2.ZWaveRemoveFailedResponse
    ZWaveReplaceFailed: _zwave_pb2.ZWaveReplaceFailedResponse
    ZWaveReset: _zwave_pb2.ZWaveResetResponse
    ZWaveTest: _zwave_pb2.ZWaveTestResponse
    ZWaveUpdate: _zwave_pb2.ZWaveUpdateStatus
    ZWaveUpdateNode: _zwave_pb2.ZWaveUpdateNodeResponse
    ZigbeeExclude: _zigbee_pb2.ZigbeeExcludeResponse
    ZigbeeGetNodes: _zigbee_pb2.ZigbeeNodesResponse
    ZigbeeInclude: _zigbee_pb2.ZigbeeIncludeResponse
    def __init__(self, AddonList: _Optional[_Union[_addon_pb2.AddonListResponse, _Mapping]] = ..., AddonAddThermostat: _Optional[_Union[_addon_pb2.AddonAddResponse, _Mapping]] = ..., WalkNodes: _Optional[_Union[_admin_pb2.WalkNodesResponse, _Mapping]] = ..., ReadLogs: _Optional[_Union[_admin_pb2.LogsChunk, _Mapping]] = ..., FollowLogs: _Optional[_Union[_admin_pb2.LogsChunk, _Mapping]] = ..., BatteryGet: _Optional[_Union[_battery_pb2.BatteryGetResponse, _Mapping]] = ..., ColorSet: _Optional[_Union[_color_pb2.ColorResponse, _Mapping]] = ..., ConfigurationList: _Optional[_Union[_configuration_pb2.ConfigurationListResponse, _Mapping]] = ..., ConfigurationGet: _Optional[_Union[_configuration_pb2.ConfigurationGetResponse, _Mapping]] = ..., ConfigurationSet: _Optional[_Union[_configuration_pb2.ConfigurationSetResponse, _Mapping]] = ..., ThermostatModeSet: _Optional[_Union[_thermostat_pb2.ThermostatResponse, _Mapping]] = ..., ThermostatModeSupGet: _Optional[_Union[_thermostat_pb2.ThermostatModeSupGetResponse, _Mapping]] = ..., ThermostatSetpointSet: _Optional[_Union[_thermostat_pb2.ThermostatResponse, _Mapping]] = ..., ThermostatFanModeSet: _Optional[_Union[_thermostat_pb2.ThermostatResponse, _Mapping]] = ..., DevicesList: _Optional[_Union[_devices_pb2.DevicesListResponse, _Mapping]] = ..., FirmwareUpload: _Optional[_Union[_firmware_pb2.FirmwareChunkAck, _Mapping]] = ..., FirmwareUpgrade: _Optional[_Union[_firmware_pb2.FirmwareUpgradeAck, _Mapping]] = ..., FirmwareUpdate: _Optional[_Union[_firmware_pb2.FirmwareUpdateResponse, _Mapping]] = ..., FirmwareLatestVersion: _Optional[_Union[_firmware_pb2.FirmwareLatestVersionResponse, _Mapping]] = ..., Reboot: _Optional[_Union[_gateway_pb2.RebootResponse, _Mapping]] = ..., Restart: _Optional[_Union[_gateway_pb2.RestartResponse, _Mapping]] = ..., StartSupport: _Optional[_Union[_gateway_pb2.SupportResponse, _Mapping]] = ..., StopSupport: _Optional[_Union[_gateway_pb2.SupportResponse, _Mapping]] = ..., Info: _Optional[_Union[_info_pb2.InfoResponse, _Mapping]] = ..., LevelGet: _Optional[_Union[_level_pb2.LevelGetResponse, _Mapping]] = ..., LevelGetStep: _Optional[_Union[_level_pb2.LevelGetResponse, _Mapping]] = ..., LevelSet: _Optional[_Union[_level_pb2.LevelResponse, _Mapping]] = ..., LevelUp: _Optional[_Union[_level_pb2.LevelResponse, _Mapping]] = ..., LevelDown: _Optional[_Union[_level_pb2.LevelResponse, _Mapping]] = ..., LevelIncrease: _Optional[_Union[_level_pb2.LevelResponse, _Mapping]] = ..., LevelDecrease: _Optional[_Union[_level_pb2.LevelResponse, _Mapping]] = ..., LockSet: _Optional[_Union[_lock_pb2.LockResponse, _Mapping]] = ..., MeterGet: _Optional[_Union[_meter_pb2.MeterGetResponse, _Mapping]] = ..., MeterReset: _Optional[_Union[_meter_pb2.MeterResetResponse, _Mapping]] = ..., RollerShutterOpen: _Optional[_Union[_roller_shutter_pb2.RollerShutterResponse, _Mapping]] = ..., RollerShutterClose: _Optional[_Union[_roller_shutter_pb2.RollerShutterResponse, _Mapping]] = ..., RollerShutterSet: _Optional[_Union[_roller_shutter_pb2.RollerShutterResponse, _Mapping]] = ..., SirenGetTones: _Optional[_Union[_siren_pb2.SirenGetTonesResponse, _Mapping]] = ..., SirenPlayTone: _Optional[_Union[_siren_pb2.SirenPlayToneResponse, _Mapping]] = ..., SirenPlayDefaultTone: _Optional[_Union[_siren_pb2.SirenPlayDefaultToneResponse, _Mapping]] = ..., SirenGetDefaultTone: _Optional[_Union[_siren_pb2.SirenGetDefaultToneResponse, _Mapping]] = ..., SirenSetDefaultTone: _Optional[_Union[_siren_pb2.SirenSetDefaultToneResponse, _Mapping]] = ..., SirenGetVolume: _Optional[_Union[_siren_pb2.SirenGetVolumeResponse, _Mapping]] = ..., SirenSetVolume: _Optional[_Union[_siren_pb2.SirenSetVolumeResponse, _Mapping]] = ..., SwitchOn: _Optional[_Union[_switch_pb2.SwitchResponse, _Mapping]] = ..., SwitchOff: _Optional[_Union[_switch_pb2.SwitchResponse, _Mapping]] = ..., TemperatureGet: _Optional[_Union[_temperature_pb2.TemperatureGetResponse, _Mapping]] = ..., WiFiQuery: _Optional[_Union[_wifi_pb2.WiFiQueryResponse, _Mapping]] = ..., WiFiScan: _Optional[_Union[_wifi_pb2.WiFiScanResponse, _Mapping]] = ..., WiFiConnect: _Optional[_Union[_wifi_pb2.WiFiConnectResponse, _Mapping]] = ..., ZigbeeInclude: _Optional[_Union[_zigbee_pb2.ZigbeeIncludeResponse, _Mapping]] = ..., ZigbeeExclude: _Optional[_Union[_zigbee_pb2.ZigbeeExcludeResponse, _Mapping]] = ..., ZigbeeGetNodes: _Optional[_Union[_zigbee_pb2.ZigbeeNodesResponse, _Mapping]] = ..., ZWaveInclude: _Optional[_Union[_zwave_pb2.ZWaveIncludeStatus, _Mapping]] = ..., ZWaveExclude: _Optional[_Union[_zwave_pb2.ZWaveExcludeStatus, _Mapping]] = ..., ZWaveAbort: _Optional[_Union[_zwave_pb2.ZWaveAbortResponse, _Mapping]] = ..., ZWaveReadNodes: _Optional[_Union[_zwave_pb2.ZWaveNodesResponse, _Mapping]] = ..., ZWaveUpdate: _Optional[_Union[_zwave_pb2.ZWaveUpdateStatus, _Mapping]] = ..., ZWaveUpdateNode: _Optional[_Union[_zwave_pb2.ZWaveUpdateNodeResponse, _Mapping]] = ..., ZWaveReset: _Optional[_Union[_zwave_pb2.ZWaveResetResponse, _Mapping]] = ..., ZWaveListEntries: _Optional[_Union[_zwave_pb2.ZWaveListEntriesResponse, _Mapping]] = ..., ZWaveAddEntry: _Optional[_Union[_zwave_pb2.ZWaveAddEntryResponse, _Mapping]] = ..., ZWaveRemoveEntry: _Optional[_Union[_zwave_pb2.ZWaveRemoveEntryResponse, _Mapping]] = ..., ZWaveNotificationItems: _Optional[_Union[_zwave_pb2.ZWaveNotificationItemsResponse, _Mapping]] = ..., ZWaveTest: _Optional[_Union[_zwave_pb2.ZWaveTestResponse, _Mapping]] = ..., ZWaveHeal: _Optional[_Union[_zwave_pb2.ZWaveHealResponse, _Mapping]] = ..., ZWaveReplaceFailed: _Optional[_Union[_zwave_pb2.ZWaveReplaceFailedResponse, _Mapping]] = ..., ZWaveRemoveFailed: _Optional[_Union[_zwave_pb2.ZWaveRemoveFailedResponse, _Mapping]] = ..., ZWaveHealthCheck: _Optional[_Union[_zwave_pb2.ZWaveHealthCheckStatus, _Mapping]] = ..., ZWaveReadNode: _Optional[_Union[_zwave_pb2.ZWaveNodeResponse, _Mapping]] = ..., CarbonMonoxideGet: _Optional[_Union[_carbon_monoxide_pb2.CarbonMonoxideGetResponse, _Mapping]] = ..., EnableAdvertising: _Optional[_Union[_ble_pb2.AdvertisingResponse, _Mapping]] = ..., DisableAdvertising: _Optional[_Union[_ble_pb2.AdvertisingResponse, _Mapping]] = ..., UltravioletGet: _Optional[_Union[_ultraviolet_pb2.UltravioletGetResponse, _Mapping]] = ..., KeyUp: _Optional[_Union[_remote_pb2.RemoteResponse, _Mapping]] = ..., KeyDown: _Optional[_Union[_remote_pb2.RemoteResponse, _Mapping]] = ..., GateOpen: _Optional[_Union[_gate_pb2.GateResponse, _Mapping]] = ..., GateClose: _Optional[_Union[_gate_pb2.GateResponse, _Mapping]] = ..., GateCycle: _Optional[_Union[_gate_pb2.GateResponse, _Mapping]] = ..., StatusCheck: _Optional[_Union[_status_pb2.StatusCheckResponse, _Mapping]] = ..., GetStructure: _Optional[_Union[_structure_pb2.StructureResponse, _Mapping]] = ...) -> None: ...

class CommandReplyError(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class CommandRequest(_message.Message):
    __slots__ = ["data", "method", "options", "payload", "type"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    data: CommandRequestData
    method: str
    options: _containers.RepeatedScalarFieldContainer[CommandRequestOption]
    payload: bytes
    type: CommandRequestType
    def __init__(self, method: _Optional[str] = ..., type: _Optional[_Union[CommandRequestType, str]] = ..., data: _Optional[_Union[CommandRequestData, _Mapping]] = ..., payload: _Optional[bytes] = ..., options: _Optional[_Iterable[_Union[CommandRequestOption, str]]] = ...) -> None: ...

class CommandRequestData(_message.Message):
    __slots__ = ["AddonAddThermostat", "AddonList", "BatteryGet", "CarbonMonoxideGet", "ColorSet", "ConfigurationGet", "ConfigurationList", "ConfigurationSet", "DevicesList", "DisableAdvertising", "EnableAdvertising", "FirmwareLatestVersion", "FirmwareUpdate", "FirmwareUpgrade", "FirmwareUpload", "FollowLogs", "GateClose", "GateCycle", "GateOpen", "GetStructure", "Info", "KeyDown", "KeyUp", "LevelDecrease", "LevelDown", "LevelGet", "LevelGetStep", "LevelIncrease", "LevelSet", "LevelUp", "LockSet", "MeterGet", "MeterReset", "ReadLogs", "Reboot", "Restart", "RollerShutterClose", "RollerShutterOpen", "RollerShutterSet", "SirenGetDefaultTone", "SirenGetTones", "SirenGetVolume", "SirenPlayDefaultTone", "SirenPlayTone", "SirenSetDefaultTone", "SirenSetVolume", "StartSupport", "StatusCheck", "StopSupport", "SwitchOff", "SwitchOn", "TemperatureGet", "ThermostatFanModeSet", "ThermostatModeSet", "ThermostatModeSupGet", "ThermostatSetpointSet", "UltravioletGet", "WalkNodes", "WiFiConnect", "WiFiQuery", "WiFiScan", "ZWaveAbort", "ZWaveAddEntry", "ZWaveExclude", "ZWaveHeal", "ZWaveHealthCheck", "ZWaveInclude", "ZWaveListEntries", "ZWaveNotificationItems", "ZWaveReadNode", "ZWaveReadNodes", "ZWaveRemoveEntry", "ZWaveRemoveFailed", "ZWaveReplaceFailed", "ZWaveReset", "ZWaveTest", "ZWaveUpdate", "ZWaveUpdateNode", "ZigbeeExclude", "ZigbeeGetNodes", "ZigbeeInclude"]
    ADDONADDTHERMOSTAT_FIELD_NUMBER: _ClassVar[int]
    ADDONLIST_FIELD_NUMBER: _ClassVar[int]
    AddonAddThermostat: _addon_pb2.AddonAddThermostatRequest
    AddonList: _addon_pb2.AddonListRequest
    BATTERYGET_FIELD_NUMBER: _ClassVar[int]
    BatteryGet: _battery_pb2.BatteryGetRequest
    CARBONMONOXIDEGET_FIELD_NUMBER: _ClassVar[int]
    COLORSET_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATIONGET_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATIONLIST_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATIONSET_FIELD_NUMBER: _ClassVar[int]
    CarbonMonoxideGet: _carbon_monoxide_pb2.CarbonMonoxideGetRequest
    ColorSet: _color_pb2.ColorSetRequest
    ConfigurationGet: _configuration_pb2.ConfigurationGetRequest
    ConfigurationList: _configuration_pb2.ConfigurationListRequest
    ConfigurationSet: _configuration_pb2.ConfigurationSetRequest
    DEVICESLIST_FIELD_NUMBER: _ClassVar[int]
    DISABLEADVERTISING_FIELD_NUMBER: _ClassVar[int]
    DevicesList: _devices_pb2.DevicesListRequest
    DisableAdvertising: _ble_pb2.AdvertisingRequest
    ENABLEADVERTISING_FIELD_NUMBER: _ClassVar[int]
    EnableAdvertising: _ble_pb2.AdvertisingRequest
    FIRMWARELATESTVERSION_FIELD_NUMBER: _ClassVar[int]
    FIRMWAREUPDATE_FIELD_NUMBER: _ClassVar[int]
    FIRMWAREUPGRADE_FIELD_NUMBER: _ClassVar[int]
    FIRMWAREUPLOAD_FIELD_NUMBER: _ClassVar[int]
    FOLLOWLOGS_FIELD_NUMBER: _ClassVar[int]
    FirmwareLatestVersion: _firmware_pb2.FirmwareLatestVersionRequest
    FirmwareUpdate: _firmware_pb2.FirmwareUpdateRequest
    FirmwareUpgrade: _firmware_pb2.FirmwareUpgradeRequest
    FirmwareUpload: _firmware_pb2.FirmwareChunk
    FollowLogs: _admin_pb2.LogsRequest
    GATECLOSE_FIELD_NUMBER: _ClassVar[int]
    GATECYCLE_FIELD_NUMBER: _ClassVar[int]
    GATEOPEN_FIELD_NUMBER: _ClassVar[int]
    GETSTRUCTURE_FIELD_NUMBER: _ClassVar[int]
    GateClose: _gate_pb2.GateRequest
    GateCycle: _gate_pb2.GateRequest
    GateOpen: _gate_pb2.GateRequest
    GetStructure: _structure_pb2.StructureRequest
    INFO_FIELD_NUMBER: _ClassVar[int]
    Info: _info_pb2.InfoRequest
    KEYDOWN_FIELD_NUMBER: _ClassVar[int]
    KEYUP_FIELD_NUMBER: _ClassVar[int]
    KeyDown: _remote_pb2.RemoteRequest
    KeyUp: _remote_pb2.RemoteRequest
    LEVELDECREASE_FIELD_NUMBER: _ClassVar[int]
    LEVELDOWN_FIELD_NUMBER: _ClassVar[int]
    LEVELGETSTEP_FIELD_NUMBER: _ClassVar[int]
    LEVELGET_FIELD_NUMBER: _ClassVar[int]
    LEVELINCREASE_FIELD_NUMBER: _ClassVar[int]
    LEVELSET_FIELD_NUMBER: _ClassVar[int]
    LEVELUP_FIELD_NUMBER: _ClassVar[int]
    LOCKSET_FIELD_NUMBER: _ClassVar[int]
    LevelDecrease: _level_pb2.LevelStepRequest
    LevelDown: _level_pb2.LevelStepRequest
    LevelGet: _level_pb2.LevelRequest
    LevelGetStep: _level_pb2.LevelRequest
    LevelIncrease: _level_pb2.LevelStepRequest
    LevelSet: _level_pb2.LevelSetRequest
    LevelUp: _level_pb2.LevelStepRequest
    LockSet: _lock_pb2.LockSetRequest
    METERGET_FIELD_NUMBER: _ClassVar[int]
    METERRESET_FIELD_NUMBER: _ClassVar[int]
    MeterGet: _meter_pb2.MeterGetRequest
    MeterReset: _meter_pb2.MeterResetRequest
    READLOGS_FIELD_NUMBER: _ClassVar[int]
    REBOOT_FIELD_NUMBER: _ClassVar[int]
    RESTART_FIELD_NUMBER: _ClassVar[int]
    ROLLERSHUTTERCLOSE_FIELD_NUMBER: _ClassVar[int]
    ROLLERSHUTTEROPEN_FIELD_NUMBER: _ClassVar[int]
    ROLLERSHUTTERSET_FIELD_NUMBER: _ClassVar[int]
    ReadLogs: _admin_pb2.LogsRequest
    Reboot: _gateway_pb2.RebootRequest
    Restart: _gateway_pb2.RestartRequest
    RollerShutterClose: _roller_shutter_pb2.RollerShutterRequest
    RollerShutterOpen: _roller_shutter_pb2.RollerShutterRequest
    RollerShutterSet: _roller_shutter_pb2.RollerShutterSetRequest
    SIRENGETDEFAULTTONE_FIELD_NUMBER: _ClassVar[int]
    SIRENGETTONES_FIELD_NUMBER: _ClassVar[int]
    SIRENGETVOLUME_FIELD_NUMBER: _ClassVar[int]
    SIRENPLAYDEFAULTTONE_FIELD_NUMBER: _ClassVar[int]
    SIRENPLAYTONE_FIELD_NUMBER: _ClassVar[int]
    SIRENSETDEFAULTTONE_FIELD_NUMBER: _ClassVar[int]
    SIRENSETVOLUME_FIELD_NUMBER: _ClassVar[int]
    STARTSUPPORT_FIELD_NUMBER: _ClassVar[int]
    STATUSCHECK_FIELD_NUMBER: _ClassVar[int]
    STOPSUPPORT_FIELD_NUMBER: _ClassVar[int]
    SWITCHOFF_FIELD_NUMBER: _ClassVar[int]
    SWITCHON_FIELD_NUMBER: _ClassVar[int]
    SirenGetDefaultTone: _siren_pb2.SirenGetDefaultToneRequest
    SirenGetTones: _siren_pb2.SirenGetTonesRequest
    SirenGetVolume: _siren_pb2.SirenGetVolumeRequest
    SirenPlayDefaultTone: _siren_pb2.SirenPlayDefaultToneRequest
    SirenPlayTone: _siren_pb2.SirenPlayToneRequest
    SirenSetDefaultTone: _siren_pb2.SirenSetDefaultToneRequest
    SirenSetVolume: _siren_pb2.SirenSetVolumeRequest
    StartSupport: _gateway_pb2.SupportRequest
    StatusCheck: _status_pb2.StatusCheckRequest
    StopSupport: _gateway_pb2.SupportRequest
    SwitchOff: _switch_pb2.SwitchRequest
    SwitchOn: _switch_pb2.SwitchRequest
    TEMPERATUREGET_FIELD_NUMBER: _ClassVar[int]
    THERMOSTATFANMODESET_FIELD_NUMBER: _ClassVar[int]
    THERMOSTATMODESET_FIELD_NUMBER: _ClassVar[int]
    THERMOSTATMODESUPGET_FIELD_NUMBER: _ClassVar[int]
    THERMOSTATSETPOINTSET_FIELD_NUMBER: _ClassVar[int]
    TemperatureGet: _temperature_pb2.TemperatureGetRequest
    ThermostatFanModeSet: _thermostat_pb2.ThermostatFanModeSetRequest
    ThermostatModeSet: _thermostat_pb2.ThermostatModeSetRequest
    ThermostatModeSupGet: _thermostat_pb2.ThermostatModeSupGetRequest
    ThermostatSetpointSet: _thermostat_pb2.ThermostatSetpointSetRequest
    ULTRAVIOLETGET_FIELD_NUMBER: _ClassVar[int]
    UltravioletGet: _ultraviolet_pb2.UltravioletGetRequest
    WALKNODES_FIELD_NUMBER: _ClassVar[int]
    WIFICONNECT_FIELD_NUMBER: _ClassVar[int]
    WIFIQUERY_FIELD_NUMBER: _ClassVar[int]
    WIFISCAN_FIELD_NUMBER: _ClassVar[int]
    WalkNodes: _admin_pb2.WalkNodesRequest
    WiFiConnect: _wifi_pb2.WiFiConnectRequest
    WiFiQuery: _wifi_pb2.WiFiQueryRequest
    WiFiScan: _wifi_pb2.WiFiScanRequest
    ZIGBEEEXCLUDE_FIELD_NUMBER: _ClassVar[int]
    ZIGBEEGETNODES_FIELD_NUMBER: _ClassVar[int]
    ZIGBEEINCLUDE_FIELD_NUMBER: _ClassVar[int]
    ZWAVEABORT_FIELD_NUMBER: _ClassVar[int]
    ZWAVEADDENTRY_FIELD_NUMBER: _ClassVar[int]
    ZWAVEEXCLUDE_FIELD_NUMBER: _ClassVar[int]
    ZWAVEHEALTHCHECK_FIELD_NUMBER: _ClassVar[int]
    ZWAVEHEAL_FIELD_NUMBER: _ClassVar[int]
    ZWAVEINCLUDE_FIELD_NUMBER: _ClassVar[int]
    ZWAVELISTENTRIES_FIELD_NUMBER: _ClassVar[int]
    ZWAVENOTIFICATIONITEMS_FIELD_NUMBER: _ClassVar[int]
    ZWAVEREADNODES_FIELD_NUMBER: _ClassVar[int]
    ZWAVEREADNODE_FIELD_NUMBER: _ClassVar[int]
    ZWAVEREMOVEENTRY_FIELD_NUMBER: _ClassVar[int]
    ZWAVEREMOVEFAILED_FIELD_NUMBER: _ClassVar[int]
    ZWAVEREPLACEFAILED_FIELD_NUMBER: _ClassVar[int]
    ZWAVERESET_FIELD_NUMBER: _ClassVar[int]
    ZWAVETEST_FIELD_NUMBER: _ClassVar[int]
    ZWAVEUPDATENODE_FIELD_NUMBER: _ClassVar[int]
    ZWAVEUPDATE_FIELD_NUMBER: _ClassVar[int]
    ZWaveAbort: _zwave_pb2.ZWaveAbortRequest
    ZWaveAddEntry: _zwave_pb2.ZWaveAddEntryRequest
    ZWaveExclude: _zwave_pb2.ZWaveExcludeRequest
    ZWaveHeal: _zwave_pb2.ZWaveHealRequest
    ZWaveHealthCheck: _zwave_pb2.ZWaveHealthCheckRequest
    ZWaveInclude: _zwave_pb2.ZWaveIncludeRequest
    ZWaveListEntries: _zwave_pb2.ZWaveListEntriesRequest
    ZWaveNotificationItems: _zwave_pb2.ZWaveNotificationItemsRequest
    ZWaveReadNode: _zwave_pb2.ZWaveNodeRequest
    ZWaveReadNodes: _zwave_pb2.ZWaveNodesRequest
    ZWaveRemoveEntry: _zwave_pb2.ZWaveRemoveEntryRequest
    ZWaveRemoveFailed: _zwave_pb2.ZWaveRemoveFailedRequest
    ZWaveReplaceFailed: _zwave_pb2.ZWaveReplaceFailedRequest
    ZWaveReset: _zwave_pb2.ZWaveResetRequest
    ZWaveTest: _zwave_pb2.ZWaveTestRequest
    ZWaveUpdate: _zwave_pb2.ZWaveUpdateRequest
    ZWaveUpdateNode: _zwave_pb2.ZWaveUpdateNodeRequest
    ZigbeeExclude: _zigbee_pb2.ZigbeeExcludeRequest
    ZigbeeGetNodes: _zigbee_pb2.ZigbeeNodesRequest
    ZigbeeInclude: _zigbee_pb2.ZigbeeIncludeRequest
    def __init__(self, AddonList: _Optional[_Union[_addon_pb2.AddonListRequest, _Mapping]] = ..., AddonAddThermostat: _Optional[_Union[_addon_pb2.AddonAddThermostatRequest, _Mapping]] = ..., WalkNodes: _Optional[_Union[_admin_pb2.WalkNodesRequest, _Mapping]] = ..., ReadLogs: _Optional[_Union[_admin_pb2.LogsRequest, _Mapping]] = ..., FollowLogs: _Optional[_Union[_admin_pb2.LogsRequest, _Mapping]] = ..., BatteryGet: _Optional[_Union[_battery_pb2.BatteryGetRequest, _Mapping]] = ..., ColorSet: _Optional[_Union[_color_pb2.ColorSetRequest, _Mapping]] = ..., ConfigurationList: _Optional[_Union[_configuration_pb2.ConfigurationListRequest, _Mapping]] = ..., ConfigurationGet: _Optional[_Union[_configuration_pb2.ConfigurationGetRequest, _Mapping]] = ..., ConfigurationSet: _Optional[_Union[_configuration_pb2.ConfigurationSetRequest, _Mapping]] = ..., ThermostatModeSet: _Optional[_Union[_thermostat_pb2.ThermostatModeSetRequest, _Mapping]] = ..., ThermostatModeSupGet: _Optional[_Union[_thermostat_pb2.ThermostatModeSupGetRequest, _Mapping]] = ..., ThermostatSetpointSet: _Optional[_Union[_thermostat_pb2.ThermostatSetpointSetRequest, _Mapping]] = ..., ThermostatFanModeSet: _Optional[_Union[_thermostat_pb2.ThermostatFanModeSetRequest, _Mapping]] = ..., DevicesList: _Optional[_Union[_devices_pb2.DevicesListRequest, _Mapping]] = ..., FirmwareUpload: _Optional[_Union[_firmware_pb2.FirmwareChunk, _Mapping]] = ..., FirmwareUpgrade: _Optional[_Union[_firmware_pb2.FirmwareUpgradeRequest, _Mapping]] = ..., FirmwareUpdate: _Optional[_Union[_firmware_pb2.FirmwareUpdateRequest, _Mapping]] = ..., FirmwareLatestVersion: _Optional[_Union[_firmware_pb2.FirmwareLatestVersionRequest, _Mapping]] = ..., Reboot: _Optional[_Union[_gateway_pb2.RebootRequest, _Mapping]] = ..., Restart: _Optional[_Union[_gateway_pb2.RestartRequest, _Mapping]] = ..., StartSupport: _Optional[_Union[_gateway_pb2.SupportRequest, _Mapping]] = ..., StopSupport: _Optional[_Union[_gateway_pb2.SupportRequest, _Mapping]] = ..., Info: _Optional[_Union[_info_pb2.InfoRequest, _Mapping]] = ..., LevelGet: _Optional[_Union[_level_pb2.LevelRequest, _Mapping]] = ..., LevelGetStep: _Optional[_Union[_level_pb2.LevelRequest, _Mapping]] = ..., LevelSet: _Optional[_Union[_level_pb2.LevelSetRequest, _Mapping]] = ..., LevelUp: _Optional[_Union[_level_pb2.LevelStepRequest, _Mapping]] = ..., LevelDown: _Optional[_Union[_level_pb2.LevelStepRequest, _Mapping]] = ..., LevelIncrease: _Optional[_Union[_level_pb2.LevelStepRequest, _Mapping]] = ..., LevelDecrease: _Optional[_Union[_level_pb2.LevelStepRequest, _Mapping]] = ..., LockSet: _Optional[_Union[_lock_pb2.LockSetRequest, _Mapping]] = ..., MeterGet: _Optional[_Union[_meter_pb2.MeterGetRequest, _Mapping]] = ..., MeterReset: _Optional[_Union[_meter_pb2.MeterResetRequest, _Mapping]] = ..., RollerShutterOpen: _Optional[_Union[_roller_shutter_pb2.RollerShutterRequest, _Mapping]] = ..., RollerShutterClose: _Optional[_Union[_roller_shutter_pb2.RollerShutterRequest, _Mapping]] = ..., RollerShutterSet: _Optional[_Union[_roller_shutter_pb2.RollerShutterSetRequest, _Mapping]] = ..., SirenGetTones: _Optional[_Union[_siren_pb2.SirenGetTonesRequest, _Mapping]] = ..., SirenPlayTone: _Optional[_Union[_siren_pb2.SirenPlayToneRequest, _Mapping]] = ..., SirenPlayDefaultTone: _Optional[_Union[_siren_pb2.SirenPlayDefaultToneRequest, _Mapping]] = ..., SirenGetDefaultTone: _Optional[_Union[_siren_pb2.SirenGetDefaultToneRequest, _Mapping]] = ..., SirenSetDefaultTone: _Optional[_Union[_siren_pb2.SirenSetDefaultToneRequest, _Mapping]] = ..., SirenGetVolume: _Optional[_Union[_siren_pb2.SirenGetVolumeRequest, _Mapping]] = ..., SirenSetVolume: _Optional[_Union[_siren_pb2.SirenSetVolumeRequest, _Mapping]] = ..., SwitchOn: _Optional[_Union[_switch_pb2.SwitchRequest, _Mapping]] = ..., SwitchOff: _Optional[_Union[_switch_pb2.SwitchRequest, _Mapping]] = ..., TemperatureGet: _Optional[_Union[_temperature_pb2.TemperatureGetRequest, _Mapping]] = ..., WiFiQuery: _Optional[_Union[_wifi_pb2.WiFiQueryRequest, _Mapping]] = ..., WiFiScan: _Optional[_Union[_wifi_pb2.WiFiScanRequest, _Mapping]] = ..., WiFiConnect: _Optional[_Union[_wifi_pb2.WiFiConnectRequest, _Mapping]] = ..., ZigbeeInclude: _Optional[_Union[_zigbee_pb2.ZigbeeIncludeRequest, _Mapping]] = ..., ZigbeeExclude: _Optional[_Union[_zigbee_pb2.ZigbeeExcludeRequest, _Mapping]] = ..., ZigbeeGetNodes: _Optional[_Union[_zigbee_pb2.ZigbeeNodesRequest, _Mapping]] = ..., ZWaveInclude: _Optional[_Union[_zwave_pb2.ZWaveIncludeRequest, _Mapping]] = ..., ZWaveExclude: _Optional[_Union[_zwave_pb2.ZWaveExcludeRequest, _Mapping]] = ..., ZWaveAbort: _Optional[_Union[_zwave_pb2.ZWaveAbortRequest, _Mapping]] = ..., ZWaveReadNodes: _Optional[_Union[_zwave_pb2.ZWaveNodesRequest, _Mapping]] = ..., ZWaveUpdate: _Optional[_Union[_zwave_pb2.ZWaveUpdateRequest, _Mapping]] = ..., ZWaveUpdateNode: _Optional[_Union[_zwave_pb2.ZWaveUpdateNodeRequest, _Mapping]] = ..., ZWaveReset: _Optional[_Union[_zwave_pb2.ZWaveResetRequest, _Mapping]] = ..., ZWaveListEntries: _Optional[_Union[_zwave_pb2.ZWaveListEntriesRequest, _Mapping]] = ..., ZWaveAddEntry: _Optional[_Union[_zwave_pb2.ZWaveAddEntryRequest, _Mapping]] = ..., ZWaveRemoveEntry: _Optional[_Union[_zwave_pb2.ZWaveRemoveEntryRequest, _Mapping]] = ..., ZWaveNotificationItems: _Optional[_Union[_zwave_pb2.ZWaveNotificationItemsRequest, _Mapping]] = ..., ZWaveTest: _Optional[_Union[_zwave_pb2.ZWaveTestRequest, _Mapping]] = ..., ZWaveHeal: _Optional[_Union[_zwave_pb2.ZWaveHealRequest, _Mapping]] = ..., ZWaveReplaceFailed: _Optional[_Union[_zwave_pb2.ZWaveReplaceFailedRequest, _Mapping]] = ..., ZWaveRemoveFailed: _Optional[_Union[_zwave_pb2.ZWaveRemoveFailedRequest, _Mapping]] = ..., ZWaveHealthCheck: _Optional[_Union[_zwave_pb2.ZWaveHealthCheckRequest, _Mapping]] = ..., ZWaveReadNode: _Optional[_Union[_zwave_pb2.ZWaveNodeRequest, _Mapping]] = ..., CarbonMonoxideGet: _Optional[_Union[_carbon_monoxide_pb2.CarbonMonoxideGetRequest, _Mapping]] = ..., EnableAdvertising: _Optional[_Union[_ble_pb2.AdvertisingRequest, _Mapping]] = ..., DisableAdvertising: _Optional[_Union[_ble_pb2.AdvertisingRequest, _Mapping]] = ..., UltravioletGet: _Optional[_Union[_ultraviolet_pb2.UltravioletGetRequest, _Mapping]] = ..., KeyUp: _Optional[_Union[_remote_pb2.RemoteRequest, _Mapping]] = ..., KeyDown: _Optional[_Union[_remote_pb2.RemoteRequest, _Mapping]] = ..., GateOpen: _Optional[_Union[_gate_pb2.GateRequest, _Mapping]] = ..., GateClose: _Optional[_Union[_gate_pb2.GateRequest, _Mapping]] = ..., GateCycle: _Optional[_Union[_gate_pb2.GateRequest, _Mapping]] = ..., StatusCheck: _Optional[_Union[_status_pb2.StatusCheckRequest, _Mapping]] = ..., GetStructure: _Optional[_Union[_structure_pb2.StructureRequest, _Mapping]] = ...) -> None: ...

class MessagingRequest(_message.Message):
    __slots__ = ["email", "push"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PUSH_FIELD_NUMBER: _ClassVar[int]
    email: _messaging_pb2.EmailMessage
    push: _messaging_pb2.PushMessage
    def __init__(self, email: _Optional[_Union[_messaging_pb2.EmailMessage, _Mapping]] = ..., push: _Optional[_Union[_messaging_pb2.PushMessage, _Mapping]] = ...) -> None: ...

class MetricsNotification(_message.Message):
    __slots__ = ["data", "mac"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    MAC_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedScalarFieldContainer[bytes]
    mac: str
    def __init__(self, mac: _Optional[str] = ..., data: _Optional[_Iterable[bytes]] = ...) -> None: ...

class PresenceNotification(_message.Message):
    __slots__ = ["build_time", "firmware_version", "git_commit", "mac", "version"]
    BUILD_TIME_FIELD_NUMBER: _ClassVar[int]
    FIRMWARE_VERSION_FIELD_NUMBER: _ClassVar[int]
    GIT_COMMIT_FIELD_NUMBER: _ClassVar[int]
    MAC_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    build_time: str
    firmware_version: str
    git_commit: str
    mac: str
    version: str
    def __init__(self, mac: _Optional[str] = ..., version: _Optional[str] = ..., git_commit: _Optional[str] = ..., build_time: _Optional[str] = ..., firmware_version: _Optional[str] = ...) -> None: ...

class CommandRequestType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class CommandRequestOption(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class CommandReplyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
