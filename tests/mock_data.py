def create_session_body():
    """Returns the test body for creating a running session"""
    return {
        "user_name": "test_user",
        "device_id": "test_device", 
        "device_position": "PelvisBack"
    }

def auth_headers():
    """Returns the test headers for basic auth"""
    return {
        'Authorization': 'Basic YWRtaW46cGFzc3dvcmQ='
    }