from dsp_toolbox.data.database import Database


def main():
    filepath = "/home/mikhailhyde/Documents/experiments/diesel/heater_requirements/data/P3M02_1.sqlite"
    db = Database(filepath=filepath, table_name="Environmental_v3")
    db.load_database()
    print(db.database.dtypes)


if __name__ == "__main__":
    main()