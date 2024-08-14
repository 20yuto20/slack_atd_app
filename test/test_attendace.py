import pytest
from unittest.mock import AsyncMock, patch
from app.services import attendance
from app.constants import STATUS_WORKING, STATUS_OFF_DUTY

@pytest.mark.asyncio
async def test_record_work_start():
    mock_db = AsyncMock()
    mock_client = AsyncMock()
    
    with patch('app.services.attendance.db', mock_db), \
         patch('app.services.attendance.send_message', AsyncMock()) as mock_send_message, \
         patch('app.services.attendance.update_home_view', AsyncMock()) as mock_update_home_view, \
         patch('app.services.attendance.get_report_channel', AsyncMock(return_value='C12345')), \
         patch('app.services.attendance.get_supervisor', AsyncMock(return_value='U67890')):
        
        mock_db.put_item.return_value = True
        mock_client.users_info.return_value = {"user": {"real_name": "Test User"}}
        
        result = await attendance.record_work_start('U12345', 'W67890', mock_client)
        
        assert result == True
        mock_db.put_item.assert_called_once()
        mock_send_message.assert_called_once()
        mock_update_home_view.assert_called_once_with(mock_client, 'U12345', {"status": STATUS_WORKING, "start_time": pytest.approx(pytest.anystring())})

@pytest.mark.asyncio
async def test_record_work_end():
    mock_db = AsyncMock()
    mock_client = AsyncMock()
    
    with patch('app.services.attendance.db', mock_db), \
         patch('app.services.attendance.send_message', AsyncMock()) as mock_send_message, \
         patch('app.services.attendance.update_home_view', AsyncMock()) as mock_update_home_view:
        
        mock_db.query.return_value = [{'p_key': 'test_key', 'punch_in': '09:00'}]
        mock_db.update_item.return_value = True
        
        result = await attendance.record_work_end('U12345', 'W67890', mock_client)
        
        assert result[0] == 'test_key'
        assert isinstance(result[1], int)
        assert isinstance(result[2], int)
        mock_db.query.assert_called_once()
        mock_db.update_item.assert_called_once()
        mock_send_message.assert_called_once()
        mock_update_home_view.assert_called_once_with(mock_client, 'U12345', {"status": STATUS_OFF_DUTY})