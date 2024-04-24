from aura.config_repository import CLIConfig
from aura.format import format_text_output
import pytest
from click.testing import CliRunner
from unittest.mock import MagicMock

from aura.credentials import list as list_credentials

def test_list_credentials():
    runner = CliRunner()

    mock_config = MagicMock(spec=CLIConfig)
    mock_config.list_credentials.return_value = [{"Name": "prod", "ClientId": "e3jso20fnak29sk"}, {"Name": "dev", "ClientId": "j3n3dmksd03isi8"}]
    mock_config.current_credentials.return_value = "prod", {}

    result = runner.invoke(list_credentials, [], obj=mock_config)
    
    assert result.exit_code == 0
    assert result.output == format_text_output([{"Name": "prod", "ClientId": "e3jso20fnak29sk", "Current": "   X   "}, {"Name": "dev", "ClientId": "j3n3dmksd03isi8", "Current": ""}], printing=False) + "\n"

    mock_config.list_credentials.assert_called_once_with()