import pytest
from unittest.mock import AsyncMock, patch
from app.services import break_time
from app.constants import STATUS_BREAK, STATUS_WORKING

@pytest.mark.asyncio
async def test_start_break():
    mock_db = AsyncMock()
    mock_client = AsyncMock()
    
    with patch('app.services.break_time.db', mock_db), \
         patch('app.services.break_time.update_home_view', AsyncMock()) as mock_update_home_view:
        
        mock_db.query.return_value = [{'p_key': 'test_key'}]
        mock_db.put_item.return_value = True
        
        result = await break_time.start_break('U12345', 'W67890', mock_client)
        
        assert result == True
        mock_db.query.assert_called_once()
        mock_db.put_item.assert_called_once()
        mock_update_home_view.assert_called_once_with(mock_client, 'U12345', {"status": STATUS_BREAK, "break_start_time": pytest.approx(pytest.anystring())})

@pytest.mark.asyncio
async def test_end_break():
    mock_db = AsyncMock()
    mock_client = AsyncMock()
    
    with patch('app.services.break_time.db', mock_db), \
         patch('app.services.break_time.update_home_view', AsyncMock()) as mock_update_home_view:
        
        mock_db.query.return_value = [{'break_id': 'test_break', 'break_begin_time': '09:00'}]
        mock_db.update_item.return_value = True
        
        result = await break_time.end_break('U12345', 'W67890', mock_client)
        
        assert result == True
        mock_db.query.assert_called_once()
        mock_db.update_item.assert_called_once()
        mock_update_home_view.assert_called_once_with(mock_client, 'U12345', {"status": STATUS_WORKING})

def test_get_total_break_duration():
    mock_db = AsyncMock()
    
    with patch('app.services.break_time.db', mock_db):
        mock_db.query.return_value = [
            {'break_duration': 30},
            {'break_duration': 15},
            {'break_duration': 45}
        ]
        
        hours, minutes = break_time.get_total_break_duration('test_punch_id')
        
        assert hours == 1
        assert minutes == 30
        mock_db.query.assert_called_once()