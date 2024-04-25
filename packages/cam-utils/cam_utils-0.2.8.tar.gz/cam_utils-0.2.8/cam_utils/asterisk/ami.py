import logging
import socket
import time
from abc import ABC, abstractmethod
from typing import Any, Optional

from . import exceptions
from .actions import actions_asterisk_13

logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - [ %(levelname)s ] - %(message)s"
)


class AMI(ABC):
    def __init__(
        self, server: str, username: str, password: str, port: int = 5038, timeout=5
    ):
        self.__server = server
        self.__username = username
        self.__password = password
        self.__port = port
        self.__timeout = timeout
        self.__connection: Optional[socket.socket] = None

    def connect(self):
        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connection.settimeout(self.__timeout)
        self.__connection.connect((self.__server, self.__port))

    def disconnect(self) -> None:
        if self.__connection:
            self.__connection.close()
            self.__connection = None

    @abstractmethod
    def parse_command(self, command: dict[str, str]) -> bytes:
        pass

    def __parse_login_response(self, connection: socket.socket) -> dict:
        raw_response = ""
        while True:
            data = connection.recv(4096)
            raw_response += data.decode()
            if "Response:" in raw_response:
                break

        response = {}
        lines = raw_response.splitlines()
        for line in lines:
            splitted = line.split(":", 1)
            if len(splitted) == 1 and splitted[0].startswith("Asterisk"):
                response["AMI"] = splitted[0]
            if len(splitted) == 2:
                key, value = splitted
                key = key.strip()
                if key == "Response":
                    response[key] = value.strip()
                if key == "Message":
                    response[key] = value.strip()
        return response

    def login(self):
        login_command = {
            "Action": "Login",
            "Username": self.__username,
            "Secret": self.__password,
            "Events": "Off",
        }
        if not self.__connection:
            self.connect()

        if self.__connection:
            self.__connection.sendall(self.parse_command(login_command))
        else:
            raise exceptions.ConnectionError(
                f"Not connected to the server {self.__server}"
            )

        response = self.__parse_login_response(self.__connection)

        if response.get("Response") == "Error":
            raise exceptions.AuthenticationError(response.get("Message"))

    def logout(self) -> None:
        logout_command = {
            "Action": "Logoff",
        }
        if self.__connection:
            self.__connection.sendall(self.parse_command(logout_command))
            self.disconnect()

    def read_until(self, end_of_command: str) -> str:
        response = ""
        timeout = time.time() + self.__timeout
        if self.__connection:
            self.__connection.setblocking(False)  # Para evitar deadlock
        else:
            raise exceptions.ConnectionError(
                f"Not connected to the server {self.__server}"
            )

        while True:
            if time.time() > timeout:
                raise TimeoutError("Timeout enquanto esperava resposta do comando.")
            try:
                data = self.__connection.recv(4096)
                if data:
                    response += data.decode()
                    if end_of_command in response:
                        break
            except BlockingIOError:
                time.sleep(0.1)
            except Exception as e:
                logging.error(e)
                raise e
        self.__connection.setblocking(True)  # Reabilitar para uso do sendall
        return response

    def send_command(self, command: dict[str, str], end_of_command: str) -> str:
        parsed_command = self.parse_command(command)

        if not self.__connection:
            self.connect()
            if not self.__connection:
                raise ConnectionError(f"Not connected to the server {self.__server}")

        self.login()
        self.__connection.sendall(parsed_command)  ## error is here
        result = self.read_until(end_of_command)
        self.logout()
        self.disconnect()

        return result


class AMI13(AMI):
    def __init__(
        self, server: str, username: str, password: str, port: int = 5038, timeout=5
    ):
        super().__init__(server, username, password, port, timeout)

    def parse_command(self, command: dict[str, str]) -> bytes:
        """Build the command to be sent as bytes

        Args:
            command (dict[str, str]): the action and the parameters

        Raises:
            exceptions.WrongAMIAction: If a wrong action is sent

        Returns:
            bytes: The command to be sent as bytes
        """
        if command.get("Action") not in actions_asterisk_13:
            raise exceptions.WrongAMIAction(
                f"The action {command.get('Action')} is not supported"
            )

        parsed_command = ""
        for key, value in command.items():
            parsed_command += f"{key}: {value}\r\n"
        parsed_command += "\r\n"

        return parsed_command.encode("utf-8")


class _ModuleMessages:
    @staticmethod
    def error_response(error: str, data: dict = {}) -> dict[str, Any]:
        logging.error(error)

        return {
            "success": False,
            "message": str(error),
            "data": data,
        }

    @staticmethod
    def success_response(message: str, data: dict = {}) -> dict[str, Any]:
        logging.info(message)
        return {
            "success": True,
            "message": str(message),
            "data": data,
        }


class _Module:
    def __init__(self, ami: AMI) -> None:
        self._ami = ami

    def __parse_ping_response(self, data: str) -> dict[str, Any]:
        response = {}
        for line in data.splitlines():
            if not line:
                continue
            key, value = line.split(":")
            response[key] = value.strip()

        return response

    def ping(self):
        """Send ping to AMI

        Returns:
            dict: a dict with response of the command
        ----
        Response Example::
            {
                "success": True,
                "message": "Ping",
                "data": {
                    "Response": "Success",
                    "Ping": "Pong",
                    "Timestamp": "1713985155.928151",
                },
            }

        """
        command = {
            "Action": "Ping",
        }
        end_of_command = "Timestamp: "
        try:
            response = self._ami.send_command(command, end_of_command)
            data = self.__parse_ping_response(response)
            return _ModuleMessages.success_response("Ping", data)
        except Exception as e:
            return _ModuleMessages.error_response(str(e))


class SipModule(_Module):
    def __build_sip_peers(self, data: str) -> dict[str, Any]:
        fields = (
            "Channeltype"
            "ObjectName"
            "ChanObjectType"
            "IPaddress"
            "IPport"
            "Dynamic"
            "AutoForcerport"
            "Forcerport"
            "AutoComedia"
            "Comedia"
            "VideoSupport"
            "TextSupport"
            "ACL"
            "Status"
            "RealtimeDevice"
            "Description"
            "Accountcode"
        )

        item = {}
        _data = {}
        lines = data.splitlines()
        for line in lines:
            splitted = line.split(":", 1)
            if len(splitted) == 2:
                key, value = splitted
                key = key.strip()
                if key in fields:
                    item[key] = value.strip()
                    if key == "Accountcode":
                        _data[item["ObjectName"]] = item
                        item = {}
        return _data

    def sip_peers(self) -> dict:
        try:
            cmd = {
                "Action": "SIPpeers",
            }

            response = self._ami.send_command(cmd, "PeerlistComplete")
            data = self.__build_sip_peers(response)
            return _ModuleMessages.success_response("SIP Peers", data)
        except Exception as e:
            return _ModuleMessages.error_response(str(e))

    def __parse_sip_peer(self, data: str) -> dict[str, str]:
        fields = (
            "Channeltype",
            "ObjectName",
            "ChanObjectType",
            "SecretExist",
            "RemoteSecretExist",
            "MD5SecretExist",
            "Context",
            "Language",
            "ToneZone",
            "AMAflags",
            "CID-CallingPres",
            "Callgroup",
            "Pickupgroup",
            "Named Callgroup",
            "Named Pickupgroup",
            "MOHSuggest",
            "VoiceMailbox",
            "TransferMode",
            "LastMsgsSent",
            "Maxforwards",
            "Call-limit",
            "Busy-level",
            "MaxCallBR",
            "Dynamic",
            "Callerid",
            "RegExpire",
            "SIP-AuthInsecure",
            "SIP-Forcerport",
            "SIP-Comedia",
            "ACL",
            "SIP-CanReinvite",
            "SIP-DirectMedia",
            "SIP-PromiscRedir",
            "SIP-UserPhone",
            "SIP-VideoSupport",
            "SIP-TextSupport",
            "SIP-T.38Support",
            "SIP-T.38EC",
            "SIP-T.38MaxDtgrm",
            "SIP-Sess-Timers",
            "SIP-Sess-Refresh",
            "SIP-Sess-Expires",
            "SIP-Sess-Min",
            "SIP-RTP-Engine",
            "SIP-Encryption",
            "SIP-RTCP-Mux",
            "SIP-DTMFmode",
            "ToHost",
            "Address-IP",
            "Address-Port",
            "Default-addr-IP",
            "Default-addr-port",
            "Default-Username",
            "Codecs",
            "Status",
            "SIP-Useragent",
            "Reg-Contact",
            "QualifyFreq",
            "Parkinglot",
            "SIP-Use-Reason-Header",
            "Description",
            "Response",
            "Message",
        )

        _data = {"AMIStatus": "Success"}
        lines = data.splitlines()
        for line in lines:
            splitted = line.split(":", 1)
            if len(splitted) == 2:
                key, value = splitted
                key = key.strip()
                if key in fields:
                    _data[key] = value.strip()
        if _data.get("Response") == "Error":
            raise exceptions.AMIResponseError(_data.get("Message"))
        return _data

    def sip_peer(self, peer: str) -> dict[str, str]:
        try:
            cmd = {
                "Action": "SIPshowpeer",
                "Peer": peer,
            }

            response = self._ami.send_command(cmd, "\r\n\r\n")
            data = self.__parse_sip_peer(response)

            return _ModuleMessages.success_response(f"SIP Peer {peer}", data)
        except Exception as e:
            return _ModuleMessages.error_response(str(e))


class CommandModule(_Module):
    def execute(self, command: str) -> dict[str, Any]:
        _command = {
            "Action": "Command",
            "Command": command,
        }

        try:
            response = self._ami.send_command(_command, "--END COMMAND--")
            return _ModuleMessages.success_response(
                f"Command: {command}", {"response": response}
            )
        except Exception as e:
            return _ModuleMessages.error_response(str(e))


class PJSIPModule(_Module):
    def __build_pjsip_endpoints(self, data: str) -> dict[str, Any]:
        fields = [
            "ActiveChannels",
            "Aor",
            "Auths",
            "Contacts",
            "DeviceState",
            "Event",
            "ObjectName",
            "ObjectType",
            "OutboundAuths",
            "Transport",
        ]

        item = {}
        _data = {}
        lines = data.splitlines()
        for line in lines:
            splitted = line.split(":", 1)
            if len(splitted) == 2:
                key, value = splitted
                key = key.strip()
                if key in fields:
                    item[key] = value.strip()
                    if key == "ActiveChannels":
                        _data[item["ObjectName"]] = item
                        item = {}
        return _data

    def pjsip_endpoints(self) -> dict:
        """Request endpoints to ami

        Returns:
            dict: with status of the response and the data
        ---
        Example response::
            {
                "success": True,
                "message": "PJSIP Endpoints",
                "data": {
                    "8146": {
                        "Event": "EndpointList",
                        "ObjectType": "endpoint",
                        "ObjectName": "8146",
                        "Transport": "transport-tcp",
                        "Aor": "8146",
                        "Auths": "auth8146",
                        "OutboundAuths": "",
                        "Contacts": "8146/sip:8146@10.0.0.123:44684;transport=tcp,",
                        "DeviceState": "Not in use",
                        "ActiveChannels": "",
                    },
                },
            }
        """
        try:
            cmd = {
                "Action": "PJSIPShowEndpoints",
            }

            response = self._ami.send_command(cmd, "EndpointListComplete")
            data = self.__build_pjsip_endpoints(response)
            return _ModuleMessages.success_response("PJSIP Endpoints", data)
        except Exception as e:
            return _ModuleMessages.error_response(str(e))

    def __build_pjsip_endpoint(self, data: str) -> dict[str, Any]:
        result = {}
        current_event = ""
        for line in data.splitlines():
            if not line:
                continue
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key == "Event":
                current_event = value
                if current_event not in result:
                    result[current_event] = {}
            elif key == "Event" and value == "EndpointDetailComplete":
                break
            elif not current_event:
                continue
            else:
                if current_event in result:
                    result[current_event][key] = value
        return result

    def pjsip_endpoint(self, endpoint: str) -> dict[str, Any]:
        try:
            cmd = {
                "Action": "PJSIPShowEndpoint",
                "Endpoint": endpoint,
            }

            response = self._ami.send_command(cmd, "EndpointDetailComplete")
            data = self.__build_pjsip_endpoint(response)
            return _ModuleMessages.success_response(f"PJSIP Endpoint {endpoint}", data)
        except Exception as e:
            return _ModuleMessages.error_response(str(e))
