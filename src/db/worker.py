import random
from typing import List
from typing import Optional
from typing import Any
import json

from src.settings.logging import logger
from src.db.query import DatabaseQuery
from src.db.scopes import TableName


def serialize(input_object: Any) -> str:
    return json.dumps(input_object)


def de_serialize(input_object: Any) -> Any:
    return json.loads(input_object)


class DatabaseHandler:
    """
    Database handler.
    """

    def __init__(self,
                 uri: str = 'db.sqlite') -> None:
        self._uri = uri
        self._query: Optional[DatabaseQuery] = None
        self.TABLE_NAME = TableName()

    def __str__(self) -> str:
        return f"Connected to database from={self._uri}"

    def __repr__(self) -> str:
        return f"Connected to database from={self._uri}"

    @property
    def uri(self) -> str:
        """
        View and set database file name.

        Returns:
            (str)
        """

        return self._uri

    @uri.setter
    def uri(self,
            uri: str) -> None:
        self._uri = uri
        self._query = DatabaseQuery(uri=self._uri)
        self._query.connect()

    def connect(self) -> None:
        try:
            self._query.is_connected
        except AttributeError:
            self._query = DatabaseQuery(uri=self._uri)
            self._query.connect()
            self._query.create_all()
        else:
            self._query.reconnect()

    def delete_all_table(self):
        self._query.delete_all()

    def _check_object(self,
                      current_row: Properties,
                      new_row: Properties) -> Properties:

        if new_row.device is None:
            device = current_row.device
        else:
            device = new_row.device

        if new_row.type is None:
            _type = current_row.type
        else:
            _type = new_row.type

        if new_row.index is None:
            index = current_row.index
        else:
            index = new_row.index

        if new_row.gateway is None:
            gateway = current_row.gateway
        else:
            gateway = new_row.gateway

        if new_row.state.event is None:
            event = current_row.state.event
        else:
            event = new_row.state.event

        if new_row.state.value is None:
            value = current_row.state.value
        else:
            value = new_row.state.value

        if new_row.state.locked is None:
            locked = current_row.state.locked
        else:
            locked = new_row.state.locked

        if new_row.state.home is None:
            home = current_row.state.home
        else:
            home = new_row.state.home

        if new_row.state.back is None:
            back = current_row.state.back
        else:
            back = new_row.state.back

        if new_row.state.unconfigured is None:
            unconfigured = current_row.state.unconfigured
        else:
            unconfigured = new_row.state.unconfigured

        state = State(event=event,
                      value=value,
                      locked=locked,
                      home=home,
                      back=back,
                      unconfigured=unconfigured)
        return Properties(ouid=current_row.ouid,
                          topic_name=current_row.topic_name,
                          device=device,
                          type=_type,
                          index=index,
                          gateway=gateway,
                          state=state)

    def _check_config(self,
                      current_row: Config,
                      new_row: Properties) -> Properties:
        if new_row.config.output[0].offset is None:
            offset = current_row.output[0].offset
        else:
            offset = new_row.config.output[0].offset

        if new_row.config.output[0].raise_time is None:
            raise_time = current_row.output[0].raise_time
        else:
            raise_time = new_row.config.output[0].raise_time

        if new_row.config.output[0].fall_time is None:
            fall_time = current_row.output[0].fall_time
        else:
            fall_time = new_row.config.output[0].fall_time

        if new_row.config.output[0].type is None:
            _type = current_row.output[0].type
        else:
            _type = new_row.config.output[0].type

        if new_row.config.output[0].mode is None:
            _mode = current_row.output[0].mode
        else:
            _mode = new_row.config.output[0].mode

        if new_row.config.output[0].order is None:
            _order = current_row.output[0].order
        else:
            _order = new_row.config.output[0].order

        if new_row.config.output[0].universe is None:
            sacn_universe = current_row.output[0].universe
        else:
            sacn_universe = new_row.config.output[0].universe

        if new_row.config.sacn.priority is None:
            sacn_priority = current_row.sacn.priority
        else:
            sacn_priority = new_row.config.sacn.priority

        if new_row.config.sacn.name is None:
            sacn_name = current_row.sacn.name
        else:
            sacn_name = new_row.config.sacn.name

        if new_row.config.sacn.pps is None:
            sacn_pps = current_row.sacn.pps
        else:
            sacn_pps = new_row.config.sacn.pps

        if new_row.config.address is None:
            address = current_row.address
        else:
            address = new_row.config.address

        config_dmx = ConfigDmx(offset=offset,
                               raise_time=raise_time,
                               fall_time=fall_time,
                               type=_type,
                               universe=sacn_universe,
                               order=_order,
                               mode=_mode)
        config_sacn = ConfigSacn(name=sacn_name,
                                 priority=sacn_priority,
                                 pps=sacn_pps)
        config = Config(output=[config_dmx],
                        sacn=config_sacn,
                        address=address)
        return Properties(ouid=new_row.ouid,
                          config=config)

    def get_object_by_ouid(self,
                           ouid: str) -> Optional[Properties]:
        dbquery = self._query.select(ouid=ouid,
                                     table=self.TABLE_NAME.OBJECT)

        if dbquery is None:
            logger.debug(f"No object with OUID={ouid}"
                         f" in table={self.TABLE_NAME.OBJECT}")
            return None

        state = State(event=dbquery[6],
                      value=dbquery[7],
                      locked=bool(dbquery[8]),
                      unconfigured=bool(dbquery[9]))
        result = Properties(ouid=dbquery[1],
                            device=dbquery[2],
                            type=dbquery[3],
                            index=dbquery[4],
                            gateway=dbquery[5],
                            state=state)
        logger.debug(f"Object {result} find in MainObject table")
        return result

    def get_config_by_ouid(self,
                           ouid: str) -> Optional[Config]:
        dbquery = self._query.select(ouid=ouid,
                                     table=self.TABLE_NAME.CONFIG)
        if dbquery is None:
            logger.debug(f"No object with OUID={ouid}"
                         f" in table={self.TABLE_NAME.CONFIG}")
            return None

        output: List[ConfigDmx] = []
        config_dmx = ConfigDmx(offset=dbquery[2],
                               raise_time=dbquery[3],
                               fall_time=dbquery[4],
                               type=dbquery[5],
                               universe=dbquery[8],
                               mode=dbquery[6],
                               order=dbquery[7])
        config_sacn = ConfigSacn(priority=dbquery[9],
                                 name=dbquery[10],
                                 pps=dbquery[11])
        output.append(config_dmx)
        config = Config(output=output,
                        sacn=config_sacn,
                        address=dbquery[12])

        logger.debug(f"Object {config} find in MainConfig table")
        return config

    def get_page_by_ouid(self,
                         ouid: str) -> Optional[Page]:
        dbquery = self._query.select(ouid=ouid,
                                     table=self.TABLE_NAME.PAGE)
        if dbquery is None:
            logger.debug(f"No object with OUID={ouid}"
                         f" in table={self.TABLE_NAME.PAGE}")
            return None

        page = Page(page=de_serialize(dbquery[1]))

        logger.debug(f"Object {page} find in Page table")
        return page

    def add_object(self,
                   entry: Properties) -> None:
        """
        Обновляет или добавляет запись в таблицу Object.

        Args:
            entry (Properties): распарсеный payload и topic в виде датакласса.
        """

        current_row = self.get_object_by_ouid(entry.ouid)
        if current_row is None:
            self._query.insert_main_object(entry)
        else:
            row = self._check_object(current_row=current_row,
                                     new_row=entry)
            self._query.update_main_object(row)

    def add_config(self,
                   entry: Properties) -> None:
        """
        Обновляет или добавляет запись в таблицу Config.

        Args:
            entry (Properties): распарсеный payload и topic в виде датакласса.
        """

        current_row = self.get_config_by_ouid(entry.ouid)

        if current_row is None:
            self._query.insert_main_config(entry)
        else:
            row = self._check_config(current_row=current_row,
                                     new_row=entry)
            self._query.update_main_config(row)

    def add_page(self,
                 entry: Properties) -> None:
        """
        Обновляет или добавляет запись в таблицу Page.

        Args:
            entry (Properties): распарсеный payload и topic в виде датакласса.
        """

        current_row = self.get_page_by_ouid(entry.ouid)
        if current_row is None:
            self._query.insert_page(ouid=entry.ouid,
                                    page=serialize(entry.control.page.page))
        else:
            self._query.update_page(ouid=entry.ouid,
                                    page=serialize(entry.control.page.page))

    def add_config_page(self,
                        entry: Optional[dict]) -> None:
        """
        Временный метода для добавления конфига в БД.

        Args:
            entry: конфиг
        """

        self._query.insert_page(ouid=str(random.randint(1, 1000)),
                                page=serialize(entry))
