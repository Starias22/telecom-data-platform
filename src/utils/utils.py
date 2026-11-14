import re
fmt_datetime = lambda  dt:dt.replace("-", "").replace(":", "").replace(" ", "")

def get_num_records(psql_copy_cmd_output=str):
      numbers = re.findall(r'COPY (\d+)', psql_copy_cmd_output)
      return [int(n) for n in numbers]

if __name__ == "__main__":
      num_records = get_num_records("COPY 100 COPY 10000")
      print(num_records)
     