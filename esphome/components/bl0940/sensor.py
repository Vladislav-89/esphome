import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, uart
from esphome.const import (
    CONF_CURRENT,
    CONF_ENERGY,
    CONF_EXTERNAL_TEMPERATURE,
    CONF_ID,
    CONF_INTERNAL_TEMPERATURE,
    CONF_POWER,
    CONF_VOLTAGE,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_VOLTAGE,
    DEVICE_CLASS_TEMPERATURE,
    STATE_CLASS_MEASUREMENT,
    UNIT_AMPERE,
    UNIT_CELSIUS,
    UNIT_KILOWATT_HOURS,
    UNIT_VOLT,
    UNIT_WATT,
    STATE_CLASS_TOTAL_INCREASING,
)

CONF_VOLTAGE_DIVIDER_R1 = "voltage_divider_r1"
CONF_VOLTAGE_DIVIDER_R2 = "voltage_divider_r2"
CONF_CURRENT_SENSOR = "current_sensor"
CONF_SHUNT_RESISTOR = "shunt_resistance_mOhm"
CONF_CT_LOAD_RESISTOR = "CT_load_resistor"
CONF_CT_TURNS_RATIO = "CT_turns_ratio"


DEPENDENCIES = ["uart"]


bl0940_ns = cg.esphome_ns.namespace("bl0940")
BL0940 = bl0940_ns.class_("BL0940", cg.PollingComponent, uart.UARTDevice)

sensor_t = bl0940_ns.enum("sensor_t")
SENSOR = {
    "CT": sensor_t.CT,
    "SHUNT": sensor_t.SHUNT,
}




CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(BL0940),
            cv.Optional(CONF_VOLTAGE): sensor.sensor_schema(
                unit_of_measurement=UNIT_VOLT,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_VOLTAGE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_CURRENT): sensor.sensor_schema(
                unit_of_measurement=UNIT_AMPERE,
                accuracy_decimals=5,
                device_class=DEVICE_CLASS_CURRENT,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_POWER): sensor.sensor_schema(
                unit_of_measurement=UNIT_WATT,
                accuracy_decimals=3,
                device_class=DEVICE_CLASS_POWER,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_ENERGY): sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOWATT_HOURS,
                accuracy_decimals=3,
                device_class=DEVICE_CLASS_ENERGY,
                state_class=STATE_CLASS_TOTAL_INCREASING,
            ),
            cv.Optional(CONF_INTERNAL_TEMPERATURE): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_EXTERNAL_TEMPERATURE): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_CURRENT_SENSOR, default="CT"): cv.All(
                cv.enum(
                    SENSOR,
                    upper=True,
                ),
            ),
            
            cv.Optional(CONF_VOLTAGE_DIVIDER_R1): cv.float_,
            cv.Optional(CONF_VOLTAGE_DIVIDER_R2): cv.float_,
            cv.Optional(CONF_SHUNT_RESISTOR): cv.float_,
            cv.Optional(CONF_CT_LOAD_RESISTOR): cv.float_,
            cv.Optional(CONF_CT_TURNS_RATIO): cv.float_, 
        }
    )
    .extend(cv.polling_component_schema("60s"))
    .extend(uart.UART_DEVICE_SCHEMA)
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    if voltage_config := config.get(CONF_VOLTAGE):
        sens = await sensor.new_sensor(voltage_config)
        cg.add(var.set_voltage_sensor(sens))
    if current_config := config.get(CONF_CURRENT):
        sens = await sensor.new_sensor(current_config)
        cg.add(var.set_current_sensor(sens))
    if power_config := config.get(CONF_POWER):
        sens = await sensor.new_sensor(power_config)
        cg.add(var.set_power_sensor(sens))
    if energy_config := config.get(CONF_ENERGY):
        sens = await sensor.new_sensor(energy_config)
        cg.add(var.set_energy_sensor(sens))
    if internal_temperature_config := config.get(CONF_INTERNAL_TEMPERATURE):
        sens = await sensor.new_sensor(internal_temperature_config)
        cg.add(var.set_internal_temperature_sensor(sens))
    if external_temperature_config := config.get(CONF_EXTERNAL_TEMPERATURE):
        sens = await sensor.new_sensor(external_temperature_config)
        cg.add(var.set_external_temperature_sensor(sens))
        
    if (voltage_divider_r1 := config.get(CONF_VOLTAGE_DIVIDER_R1, None)) is not None:
        cg.add(var.set_voltage_divider_r1(voltage_divider_r1))
    if (voltage_divider_r2 := config.get(CONF_VOLTAGE_DIVIDER_R2, None)) is not None:
        cg.add(var.set_voltage_divider_r2(voltage_divider_r2))
    if (shunt_resistor_mOhm := config.get(CONF_SHUNT_RESISTOR, None)) is not None:
        cg.add(var.set_shunt_resistor(shunt_resistor_mOhm))
    if (CT_load_resistor := config.get(CONF_CT_LOAD_RESISTOR, None)) is not None:
        cg.add(var.set_CT_load_resistor(CT_load_resistor))
    if (CT_turns_ratio := config.get(CONF_CT_TURNS_RATIO, None)) is not None:
        cg.add(var.set_CT_turns_ratio(CT_turns_ratio))
    
    cg.add(var.set_current_sensor(config[CONF_CURRENT_SENSOR]))
