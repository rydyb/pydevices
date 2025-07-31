import os
import numpy as np
import spcm
import logging


def list_devices():
    devices = []

    for devfile in os.listdir("/dev"):
        if not devfile.startswith("spcm"):
            continue

        device_identifier = f"/dev/{devfile}"
        with spcm.Card(device_identifier) as card:
            devices.append(
                {
                    "device_identifier": device_identifier,
                    "serial_number": card.sn(),
                    "family": card.family(),
                    "num_channels": card.num_channels(),
                    "product_name": card.product_name(),
                }
            )

    return devices


class SignalGenerator:
    def __init__(
        self,
        serial_number: int,
        sample_rate: float,
        output_voltage: float,
        verbose: bool = False,
    ):
        self.card = spcm.Card(serial_number=serial_number, verbose=verbose).open()
        logging.info("Opened card handle for card with serial number %s", serial_number)

        self.serial_number = serial_number
        self.sample_rate = sample_rate
        self.output_voltage = output_voltage

        try:
            self.card.timeout(10 * spcm.units.s)
            self.card.loops(0)
            logging.info("Set SPC_LOOPS to 0")

            self.channel0 = spcm.Channels(self.card, spcm.CHANNEL0)
            self.channel0.enable(True)
            self.channel0.output_load(50 * spcm.units.ohm)
            self.channel0.amp(output_voltage * spcm.units.V)
            logging.info(
                "Enabled channel 0 with output voltage %s V at 50 Ohm", output_voltage
            )

            self.clock = spcm.Clock(self.card)
            self.clock.sample_rate(sample_rate * spcm.units.Hz)
            self.clock.clock_output(False)
            logging.info("Set sample rate to %s Samples per second", sample_rate)

            self.trigger = spcm.Trigger(self.card)
        except spcm.SpcmException as error:
            logging.error("Error during initialization: %s", str(error))
            self.card.close()
            raise

    def close(self):
        self.card.close()
        self.card = None
        self.channel0 = None
        self.clock = None
        self.trigger = None
        logging.info("Closed card handle")

    def transfer_waveform(self, samples: np.ndarray):
        if len(samples) % 32 != 0:
            raise spcm.SpcmException("number of samples must be a multiple of 32")

        max_sample_value = self.card.max_sample_value()
        number_samples = len(samples) * spcm.units.S
        transfer = spcm.DataTransfer(self.card)
        transfer.memory_size(number_samples)
        transfer.allocate_buffer(number_samples)
        logging.info(
            "Allocated buffer of size %s bytes for %s samples",
            number_samples,
            len(samples),
        )

        buffer = ((samples / samples.max()) * (max_sample_value - 1)).astype(np.int16)
        transfer.buffer[:] = buffer
        transfer.start_buffer_transfer(
            spcm.M2CMD_DATA_STARTDMA, spcm.M2CMD_DATA_WAITDMA
        )
        logging.info("Started buffer transfer with %s samples", len(samples))

    def start_triggered_playback(self):
        self.trigger.termination(0)
        self.trigger.or_mask(spcm.SPC_TMASK_EXT0)
        self.trigger.ext0_mode(spcm.SPC_TM_POS)
        self.trigger.ext0_coupling(spcm.COUPLING_DC)
        self.trigger.ext0_level0(1 * spcm.units.V)
        logging.info("Configured external trigger with positive edge detection at 1 V")

        self.card.card_mode(spcm.SPC_REP_STD_SINGLERESTART)
        self.card.start(spcm.M2CMD_CARD_ENABLETRIGGER, spcm.M2CMD_CARD_FORCETRIGGER)
        logging.info("Card set to single restart mode and trigger enabled")

    def start_continuous_playback(self):
        self.trigger.or_mask(spcm.SPC_TMASK_SOFTWARE)
        logging.info("Set trigger mask for continuous playback")

        self.card.card_mode(spcm.SPC_REP_STD_CONTINUOUS)
        self.card.start(spcm.M2CMD_CARD_ENABLETRIGGER, spcm.M2CMD_CARD_FORCETRIGGER)
        logging.info("Card set to continuous mode and trigger enabled")

    def stop_playback(self):
        if self.card is None:
            raise spcm.SpcmException("Card is not initialized")

        self.card.stop(spcm.M2CMD_CARD_STOP)
        logging.info("Stopped card playback")

    def pulse(self, frequency: float, duration: float):
        num_samples = ((int(duration * self.sample_rate) + 31) // 32) * 32
        logging.info(
            "Generating pulse with %s duration %s samples", duration, num_samples
        )

        t = np.arange(num_samples) / self.sample_rate
        x = np.sin(2 * np.pi * t * frequency)
        x[int(duration * self.sample_rate) :] = 0

        self.stop_playback()
        self.transfer_waveform(x)
        self.start_triggered_playback()

    def tone(self, frequency: float):
        num_samples = 3200
        logging.info("Generating tone with %s samples", num_samples)

        t = np.arange(num_samples) / self.sample_rate
        x = np.sin(2 * np.pi * t * frequency)

        self.stop_playback()
        self.transfer_waveform(x)
        self.start_continuous_playback()

    def sweep(self, center: float, span: float, duration: float):
        f_start = center - span / 2
        f_end = center + span / 2

        num_samples = ((int(duration * self.sample_rate) + 31) // 32) * 32
        logging.info("Generating sweep with %s samples", num_samples)

        t = np.arange(num_samples) / self.sample_rate
        f = np.linspace(f_start, f_end, num_samples)
        x = np.sin(2 * np.pi * t * f)

        self.stop_playback()
        self.transfer_waveform(x)
        self.start_triggered_playback()
