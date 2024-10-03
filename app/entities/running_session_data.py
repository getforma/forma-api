from app.config import Config
from app.entities.base_entity import BaseEntity
from decimal import Decimal

class RunningSessionData(BaseEntity):
    def __init__(self, running_session_id: str, time: str, lat: float, long: float, acceleration: dict, angular_velocity: dict, magnetic_field: dict, angle: dict):
        super().__init__(Config.RUNNING_SESSIONS_DATA_TABLE)
        self.running_session_id = running_session_id
        self.time = time
        self.latitude = Decimal(str(lat))
        self.longitude = Decimal(str(long))
        self.x_acceleration = Decimal(str(acceleration['x']))
        self.y_acceleration = Decimal(str(acceleration['y']))
        self.z_acceleration = Decimal(str(acceleration['z']))
        self.x_angular_velocity = Decimal(str(angular_velocity['x']))
        self.y_angular_velocity = Decimal(str(angular_velocity['y']))
        self.z_angular_velocity = Decimal(str(angular_velocity['z']))
        self.x_magnetic_field = Decimal(str(magnetic_field['x']))
        self.y_magnetic_field = Decimal(str(magnetic_field['y']))
        self.z_magnetic_field = Decimal(str(magnetic_field['z']))
        self.x_angle = Decimal(str(angle['x']))
        self.y_angle = Decimal(str(angle['y']))
        self.z_angle = Decimal(str(angle['z']))
        self.save()


    def to_dict(self):
        return {
            'id': self.id,
            'running_session_id': self.running_session_id,
            'created_at': self.created_at,
            'time': self.time,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'x_acceleration': self.x_acceleration,
            'y_acceleration': self.y_acceleration,
            'z_acceleration': self.z_acceleration,
            'x_angular_velocity': self.x_angular_velocity,
            'y_angular_velocity': self.y_angular_velocity,
            'z_angular_velocity': self.z_angular_velocity,
            'x_magnetic_field': self.x_magnetic_field,
            'y_magnetic_field': self.y_magnetic_field,
            'z_magnetic_field': self.z_magnetic_field,
            'x_angle': self.x_angle,
            'y_angle': self.y_angle,
            'z_angle': self.z_angle
        }