from kklib import NativeLib, ErrorCode, KK_ReportType

CMD_FREQ_AVG = bytes([0x43])
CMD_RATE_1S = bytes([0x29])

class FrequencyCounter:
    def __init__(self, connection: str, channels: int):
        self.connection = connection
        self.channels = channels
        self.lib = NativeLib()
        self.source_id = self.lib.get_source_id()

        result = self.lib.open_connection(self.source_id, self.connection, True)
        if result.result_code != ErrorCode.KK_NO_ERR:
            raise RuntimeError(f"Error opening connection: {result.data}")

        self.lib.send_command(self.source_id, CMD_FREQ_AVG)
        self.lib.send_command(self.source_id, CMD_RATE_1S)
        self.lib.send_command(self.source_id, str(self.channels).encode('ascii'))

    def report(self) -> list[float] | None:
        report = self.lib.get_kk_report(self.source_id)
        if report.get_report_type() == KK_ReportType.RT_DOUBLE:
            return report._floats
        return None

    def close(self):
        self.lib.close_connection(self.source_id)
