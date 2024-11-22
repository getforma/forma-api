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


'''

'''


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
