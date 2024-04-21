from pyModbusTCP.client import ModbusClient
from loguru import logger as log

from . import constants as c

class Victron():
    def __init__(self, host:str, port:int=502, unit_id:int=100, config:dict={}) -> None:
        self.host = host
        self.port = port
        self.unit_id = unit_id
        self.client = None

        self.gridLimit = config.get(c.CFG_GRID_LIMIT)
        self.essFeedLimit = config.get(c.CFG_ESS_FEED_LIMIT)
        self.essChargeLimit = config.get(c.CFG_ESS_CHARGE_LIMIT)
        self.socLimit = config.get(c.CFG_SOC_LIMIT)
        self.batteryCapacity = config.get(c.CFG_BATTERY_CAPACITY)

        self.connect()

    def connect(self):
        self.client = ModbusClient(
            host=self.host,
            port=self.port,
            auto_open=True,
            auto_close=True,
            unit_id=self.unit_id,
        )

    def parseValue(self, value:int) -> int:
        if value is not None:
            if value >= 32768:
                value = value - 65536
            return value

    def parseSetPoint(self, value:float) -> int:
        if value is not None:
            if value < 0:
                value = 65536 + value
            return int(value)

    def readSingleHoldingRegisters(self, address:int, parse:bool=True):
        if parse:
            return self.parseValue(self.client.read_holding_registers(address, 1)[0])
        return self.client.read_holding_registers(address, 1)[0]

    def writeSingleHoldingRegisters(self, address:int, value:float):
        return self.client.write_single_register(address, int(value))

    def getSoc(self, address:int=843) -> float:
        return self.readSingleHoldingRegisters(address, 1)
    
    def isSocLimitReached(self, soc:float|None=None, socLimit:float|None=None) -> bool:
        if soc is None:
            soc = self.getSoc()
        if socLimit is None:
            if self.socLimit is None:
                log.error("SOC limit not set.")
                return False
            socLimit = self.socLimit
        return soc <= socLimit

    def getPower(self, address:int=820):
        return self.readSingleHoldingRegisters(address, 1)

    def getEssSetPoint(self, address:int=2700):
        return self.readSingleHoldingRegisters(address, 1)

    def applyLimit(self, value:int, limit:int) -> int:
        if value < 0:
            if value < (limit * -1):
                log.debug(f"Limit reached: {value} of {limit * -1}.")
                value = limit * -1
        else:
            if value > limit:
                log.debug(f"Limit reached: {value} of {limit}.")
                value = limit
        return value

    def applyGridLimit(self, value:int) -> int:
        if self.gridLimit is not None:
            value = self.applyLimit(value, self.gridLimit)
        return value

    def applyFeedLimit(self, value:int) -> int:
        if self.essFeedLimit is not None:
            value = self.applyLimit(value, self.essFeedLimit)
        return value

    def applyChargeLimit(self, value:int) -> int:
        if self.essChargeLimit is not None:
            value = self.applyLimit(value, self.essChargeLimit)
        return value

    def setEssSetPoint(self, value:int, address:int=2700, soc:float|None=None, socLimit:float|None=None) -> int:
        value = self.applyGridLimit(value)
        if value < 0: # only apply feed limit if value is negative
            value = self.applyFeedLimit(value)
            if socLimit is not None and soc is not None:
                if self.isSocLimitReached(soc=soc, socLimit=socLimit):
                    log.debug(f"SOC limit reached. Setting ESS feed limit to 0.")
                    value = 0
        else:
            value = self.applyChargeLimit(value)
        value = self.parseSetPoint(value)
        self.writeSingleHoldingRegisters(address, value)
        return self.parseValue(value)