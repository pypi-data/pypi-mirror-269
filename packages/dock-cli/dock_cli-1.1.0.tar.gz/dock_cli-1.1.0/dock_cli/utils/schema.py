import enum

@enum.unique
class ChartConfigOptions(str, enum.Enum):
    REGISTRY = 'oci-registry'
    TYPE = 'type'
    def __str__(self):
        return self.value

@enum.unique
class ImageConfigOptions(str, enum.Enum):
    REGISTRY = 'registry'
    FILE = 'image-file'
    NAME = 'image-name'
    DEPENDS_ON = 'depends-on'
    TYPE = 'type'
    def __str__(self):
        return self.value

@enum.unique
class SectionType(str, enum.Enum):
    CHART = 'chart'
    IMAGE = 'image'
    def __str__(self):
        return self.value
