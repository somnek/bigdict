import psycopg2
import dotenv
import click
import os

dotenv.load_dotenv()
OUTPUT_FILE = './output.py'

def get_conn():
  host = os.getenv('DB_HOST')
  user = os.getenv('DB_USER')
  password = os.getenv('DB_PASS')
  database = os.getenv('DB_NAME')

  if not all([host, user, password, database]):
    err = "\nMissing env var...Please check your credentials in .env file, \nmake sure you have your: \nDB_HOST, \nDB_NAME, \nDB_USER, \nDB_PASS\nvariables set."
    raise Exception(err)

  try:
    conn = psycopg2.connect(
      host=host,
      database=database,
      user=user,
      password=password
    )
  except Exception as e:
    print(e)
    raise e

  return conn


@click.command()
@click.option('--table', prompt='Tablename', help='Table name')
@click.option('--key', prompt='Key', help='The output dictionary key')
@click.option('--val', prompt='Value', help='The output dictionary value')
def do(table, key, val):
  conn = get_conn()
  cur = conn.cursor()
  query = f"SELECT {key}, {val} FROM {table};"
  print(query)
  cur.execute(query)
  rows = cur.fetchall()
  print(f'len -> {len(rows)}')

  data = {}
  for row in rows:
    data[row[0]] = row[1]

  with open(OUTPUT_FILE, 'w') as f:
    f.write('data = {\n')
    for k, v in data.items():
      # clean val
      val_str = v.replace('\n', '\\n').replace('"', '\\"')

      key_str = f'"{k}"'
      val_str = f'"{val_str}"'
      line = f'    {key_str}: {val_str},\n'
      f.write(line)
    f.write('\n}')

  # close
  cur.close()
  conn.close()
  return


if __name__ == '__main__':
  do()
