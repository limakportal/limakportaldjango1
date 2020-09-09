from enum import IntEnum

class EnumRightTypes(IntEnum):
      Yıllık=1
      Mazeret=2
      Ücretsiz=3

class EnumRightStatus(IntEnum):
      OnayBekliyor=1
      Onaylandi=2
      Reddedildi=3
      Iptal=4

class EnumStatus(IntEnum):
      Passive=0
      Active=1
