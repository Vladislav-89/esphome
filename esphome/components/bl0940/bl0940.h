#pragma once

#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/sensor/sensor.h"

namespace esphome {
namespace bl0940 {


static const float VOLTAGE_DIVIDER_R2 = 1950.0; // VOLTAGE DIVIDER, R2 390kOhm*5
static const float VOLTAGE_DIVIDER_R1 = 0.51; // VOLTAGE DIVIDER, R1 0.51kOhm
static const float SHUNT_RESISTOR_mOHhm = 1.0; // SHUNT RESISTOR, RL 1mOhm
static const float CT_LOAD_RESISTOR = 3.0; // CT LOAD RESISTOR, R 3Ohm
static const float CT_TURNS_RATIO = 2000.0; // CT TURNS RATIO, 2000
static const float Vref = 1.218; //[V]


struct ube24_t {  // NOLINT(readability-identifier-naming,altera-struct-pack-align)
  uint8_t l;
  uint8_t m;
  uint8_t h;
} __attribute__((packed));

struct ube16_t {  // NOLINT(readability-identifier-naming,altera-struct-pack-align)
  uint8_t l;
  uint8_t h;
} __attribute__((packed));

struct sbe24_t {  // NOLINT(readability-identifier-naming,altera-struct-pack-align)
  uint8_t l;
  uint8_t m;
  int8_t h;
} __attribute__((packed));

// Caveat: All these values are big endian (low - middle - high)

union DataPacket {  // NOLINT(altera-struct-pack-align)
  uint8_t raw[35];
  struct {
    uint8_t frame_header;  // value of 0x58 according to docs. 0x55 according to Tasmota real world tests. Reality wins.
    ube24_t i_fast_rms;    // 0x00
    ube24_t i_rms;         // 0x04
    ube24_t RESERVED0;     // reserved
    ube24_t v_rms;         // 0x06
    ube24_t RESERVED1;     // reserved
    sbe24_t watt;          // 0x08
    ube24_t RESERVED2;     // reserved
    ube24_t cf_cnt;        // 0x0A
    ube24_t RESERVED3;     // reserved
    ube16_t tps1;          // 0x0c
    uint8_t RESERVED4;     // value of 0x00
    ube16_t tps2;          // 0x0c
    uint8_t RESERVED5;     // value of 0x00
    uint8_t checksum;      // checksum
  };
} __attribute__((packed));



enum sensor_t {
  CT,
  SHUNT,
};




class BL0940 : public PollingComponent, public uart::UARTDevice {
 public:
  void set_current_sensor(sensor_t sensor) { this->sensor_type_ = sensor; }
  void set_voltage_sensor(sensor::Sensor *voltage_sensor) { voltage_sensor_ = voltage_sensor; }
  void set_current_sensor(sensor::Sensor *current_sensor) { current_sensor_ = current_sensor; }
  void set_power_sensor(sensor::Sensor *power_sensor) { power_sensor_ = power_sensor; }
  void set_energy_sensor(sensor::Sensor *energy_sensor) { energy_sensor_ = energy_sensor; }
  void set_internal_temperature_sensor(sensor::Sensor *internal_temperature_sensor) {
    internal_temperature_sensor_ = internal_temperature_sensor;
  }
  void set_external_temperature_sensor(sensor::Sensor *external_temperature_sensor) {
    external_temperature_sensor_ = external_temperature_sensor;
  }
  void set_voltage_divider_r1(float R1_ref) {
    this->voltage_divider_r1_ = R1_ref;
    this->voltage_divider_r1_set_ = true;
  }
  void set_voltage_divider_r2(float R2_ref) {
    this->voltage_divider_r2_ = R2_ref;
    this->voltage_divider_r2_set_ = true;
  }
  void set_shunt_resistor(float shunt_r) {
    this->shunt_resistor_ = shunt_r;
    this->shunt_resistor_set_ = true;
  }
  void set_CT_load_resistor(float CT_r) {
    this->CT_load_resistor_ = CT_r;
    this->CT_load_resistor_set_ = true;
  }
  void set_CT_turns_ratio(float CT_tr) {
    this->CT_turns_ratio_ = CT_tr;
    this->CT_turns_ratio_set_ = true;
  }






  void loop() override;

  void update() override;
  void setup() override;
  void dump_config() override;

 protected:
  sensor::Sensor *voltage_sensor_{nullptr};
  sensor::Sensor *current_sensor_{nullptr};
  // NB This may be negative as the circuits is seemingly able to measure
  // power in both directions
  sensor::Sensor *power_sensor_{nullptr};
  sensor::Sensor *energy_sensor_{nullptr};
  sensor::Sensor *internal_temperature_sensor_{nullptr};
  sensor::Sensor *external_temperature_sensor_{nullptr};





  float voltage_divider_r1_ = VOLTAGE_DIVIDER_R1;
  bool voltage_divider_r1_set_ = false;
  float voltage_divider_r2_ = VOLTAGE_DIVIDER_R2;
  bool voltage_divider_r2_set_ = false;
  float shunt_resistor_ = SHUNT_RESISTOR_mOHhm;
  bool shunt_resistor_set_ = false;
  float CT_load_resistor_ = CT_LOAD_RESISTOR;
  bool CT_load_resistor_set_ = false;
  float CT_turns_ratio_ = CT_TURNS_RATIO;
  bool CT_turns_ratio_set_ = false;

  sensor_t sensor_type_{CT};


  // Max difference between two measurements of the temperature. Used to avoid noise.
  float max_temperature_diff_{0};


  float update_temp_(sensor::Sensor *sensor, ube16_t packed_temperature) const;

  static uint32_t to_uint32_t(ube24_t input);
  static int32_t to_int32_t(sbe24_t input);
  static bool validate_checksum(const DataPacket *data);

  void received_package_(const DataPacket *data) const;
};
}  // namespace bl0940
}  // namespace esphome
