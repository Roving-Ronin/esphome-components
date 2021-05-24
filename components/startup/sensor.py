import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, time
from esphome.const import (
    CONF_ID,
    CONF_TIME_ID,
    DEVICE_CLASS_TIMESTAMP,
    UNIT_EMPTY,
)

ICON_CLOCK_START = "mdi:clock-start"

CODEOWNERS = ["@dentra"]

DEPENDENCIES = ["time"]

startup_ns = cg.esphome_ns.namespace("startup")
StartupSensor = startup_ns.class_("StartupSensor", sensor.Sensor, cg.PollingComponent)

CONFIG_SCHEMA = (
    sensor.sensor_schema(UNIT_EMPTY, ICON_CLOCK_START, 0, DEVICE_CLASS_TIMESTAMP)
    .extend(
        {
            cv.GenerateID(): cv.declare_id(StartupSensor),
            cv.GenerateID(CONF_TIME_ID): cv.use_id(time.RealTimeClock),
        }
    )
    .extend(cv.polling_component_schema("60s"))
)


def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    yield sensor.register_sensor(var, config)
    tm = yield cg.get_variable(config[CONF_TIME_ID])
    cg.add(var.set_time(tm))
