import jwt
from datetime import datetime, timedelta

def create_session_body():
    """Returns the test body for creating a running session"""
    return {
        "user_name": "Test User",
        "device_id": "test_device",
        "device_position": "PelvisBack"
    }


def create_test_token(email="test@example.com"):
    """Creates a test JWT token"""
    payload = {
        "iss": "https://accounts.google.com",
        "email": email,
        "name": "Test User",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, "dummy-secret")


def auth_headers(email="test@example.com"):
    """Returns the test headers with JWT token"""
    token = create_test_token(email)
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }



def track_session_body():
    """Returns the test body for tracking a running session"""
    return [
        {
            "time": "2024-10-03T00:00:00.200Z",
            "latitude": 12.3456,
            "longitude": 78.9012,
            "acceleration": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angular_velocity": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "magnetic_field": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angle": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            }
        },
        {
            "time": "2024-10-03T00:00:00.300Z",
            "latitude": 12.3456,
            "longitude": 78.9012,
            "acceleration": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angular_velocity": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "magnetic_field": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angle": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            }
        },
        {
            "time": "2024-10-03T00:00:00.400Z",
            "latitude": 12.3456,
            "longitude": 78.9012,
            "acceleration": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angular_velocity": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "magnetic_field": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angle": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            }
        },
        {
            "time": "2024-10-03T00:00:00.500Z",
            "latitude": 12.3456,
            "longitude": 78.9012,
            "acceleration": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angular_velocity": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "magnetic_field": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angle": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            }
        },
        {
            "time": "2024-10-03T00:00:00.600Z",
            "latitude": 12.3456,
            "longitude": 78.9012,
            "acceleration": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angular_velocity": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "magnetic_field": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angle": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            }
        },
        {
            "time": "2024-10-03T00:00:00.700Z",
            "latitude": 12.3456,
            "longitude": 78.9012,
            "acceleration": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angular_velocity": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "magnetic_field": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angle": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            }
        },
        {
            "time": "2024-10-03T00:00:00.800Z",
            "latitude": 12.3456,
            "longitude": 78.9012,
            "acceleration": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angular_velocity": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "magnetic_field": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angle": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            }
        },
        {
            "time": "2024-10-03T00:00:00.900Z",
            "latitude": 12.3456,
            "longitude": 78.9012,
            "acceleration": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angular_velocity": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "magnetic_field": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angle": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            }
        },
        {
            "time": "2024-10-03T00:00:01.603Z",
            "latitude": 12.3456,
            "longitude": 78.9012,
            "acceleration": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angular_velocity": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "magnetic_field": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angle": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            }
        }
    ]

def additional_track_session_body():
    """Returns the test body for tracking a running session"""
    return [
        {
            "time": "2024-10-03T00:00:02.603Z",
            "latitude": 12.3456,
            "longitude": 78.9012,
            "acceleration": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angular_velocity": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "magnetic_field": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angle": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            }
        },
        {
            "time": "2024-10-03T00:00:03.603Z",
            "latitude": 12.3456,
            "longitude": 78.9012,
            "acceleration": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angular_velocity": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "magnetic_field": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angle": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            }
        },
        {
            "time": "2024-10-03T00:00:04.603Z",
            "latitude": 12.3456,
            "longitude": 78.9012,
            "acceleration": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angular_velocity": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "magnetic_field": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angle": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            }
        },
        {
            "time": "2024-10-03T00:00:05.603Z",
            "latitude": 12.3456,
            "longitude": 78.9012,
            "acceleration": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angular_velocity": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "magnetic_field": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angle": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            }
        },
        {
            "time": "2024-10-03T00:00:06.603Z",
            "latitude": 12.3456,
            "longitude": 78.9012,
            "acceleration": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angular_velocity": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "magnetic_field": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angle": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            }
        },
        {
            "time": "2024-10-03T00:00:07.603Z",
            "latitude": 12.3456,
            "longitude": 78.9012,
            "acceleration": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angular_velocity": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "magnetic_field": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angle": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            }
        },
        {
            "time": "2024-10-03T00:00:08.603Z",
            "latitude": 12.3456,
            "longitude": 78.9012,
            "acceleration": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angular_velocity": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "magnetic_field": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angle": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            }
        },
        {
            "time": "2024-10-03T00:00:09.603Z",
            "latitude": 12.3456,
            "longitude": 78.9012,
            "acceleration": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angular_velocity": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "magnetic_field": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angle": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            }
        },
        {
            "time": "2024-10-03T00:00:10.603Z",
            "latitude": 12.3456,
            "longitude": 78.9012,
            "acceleration": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angular_velocity": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "magnetic_field": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            },
            "angle": {
                "x": 1.135,
                "y": 1.4312,
                "z": 3.212
            }
        }
    ]
