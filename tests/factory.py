"""
Test Factory to make fake objects for testing
"""
import secrets
import factory
from factory import FuzzyChoice


class RunningFactory(factory.Factory):
    """Creates fake pets that you don't have to feed"""

    # class Meta:  # pylint: disable=too-few-public-methods
    #     """Maps factory to data model"""

    #     model = 

    id = factory.Sequence(lambda n: n)