from gaarf.report import GaarfReport
from gaarf.io.writer import WriterFactory, StdoutWriter, CsvWriter

report = GaarfReport(results=[[0]], column_names=["one"])
factory = WriterFactory()
console = StdoutWriter()
csv_writer = CsvWriter()
breakpoint()
