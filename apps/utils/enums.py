from enum import IntEnum

class EnumRightTypes(IntEnum):
      Yillik=1
      Mazeret=2
      Ucretsiz=3

class EnumRightStatus(IntEnum):
      OnayBekliyor=1
      Onaylandi=2
      IKOnayladi=3
      Iptal=4

class EnumStatus(IntEnum):
      Passive=0
      Active=1
