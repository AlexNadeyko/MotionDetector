import sqlite3
import os

if __name__ == "__main__":
    conn = None
    scripts_path = 'Scripts/'
    db_file_name = '../Database/CerberusDatabase.db'

    try:
        print('\nOpening DB')
        conn = sqlite3.connect(db_file_name)
        cursor = conn.cursor()

        print('\nReading Scripts...')
        for script_path in os.listdir(scripts_path):

            script_file = open(f'{scripts_path}/{script_path}', 'r')
            script = script_file.read()
            script_file.close()

            print(f'Executing Script {script_path} ...')
            cursor.executescript(script)

        conn.commit()
        print('Changes successfully committed')

    except Exception as e:
        print(f'Something went wrong: {e}')
    finally:
        print('\nClosing DB')
        conn.close()