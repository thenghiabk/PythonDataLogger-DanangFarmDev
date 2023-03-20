import time
from datetime import datetime
import config
import configparser
import json
import csv
import requests

# history_folder = 'E:\\DanangFarmDev\\PythonDataLogger\\history\\'
history_folder = 'E:\\DanangFarmDev\\DanangFarmLiveUpdate\\'


def check_update():
    current_config = configparser.ConfigParser()
    current_config.read('config.ini')
    print("Number of Controllers: ", end="")
    print(len(current_config.sections()))

    for section in current_config.sections():
        print("Controller name: ", end="")
        print(section)

        # section: controller_name
        last_update = datetime.strptime(current_config[section]['last_update'], "%Y-%m-%d %H:%M:%S") if \
            current_config[section]['last_update'] else ''
        print("Last update: ", end="")
        print(last_update)
        print("History file: ", end="")
        print(current_config[section]['history_file_name'])

        data_file = current_config[section]['history_file_name'] + '.csv'

        with open(history_folder + data_file, 'r') as f:
            reader = csv.DictReader(f)
            # next(reader, None)  # skip csv header
            new_data = []
            last_update_time = ''
            for row in reader:
                collect_time = datetime.strptime("{} {}".format(row['Collect Date'], row['Collect Time']),
                                                 "%m/%d/%Y %I:%M:%S %p")
                last_update_time = collect_time

                # search new data
                if (collect_time > last_update) if last_update else True:
                    new_data.append(row)
            if new_data:
                print("# of update: ", end="")
                print(len(new_data))
                i = 0
                uploading_data = []

                # if new data is too large, it should be split into many small parts before submitting
                if len(new_data) > 20:
                    for item in new_data:
                        uploading_data.append(item)
                        i += 1
                        if i > 10:
                            json_data = json.dumps(uploading_data)
                            print(json_data)
                            submit_new_data(json_data)
                            i = 0
                            uploading_data = []
                else:
                    json_data = json.dumps(new_data)
                    print(json_data)
                    submit_new_data(json_data)
                print("Last update: ", end="")
                print(last_update_time)
                config.save_last_update_time_to_config(section, str(last_update_time))

                # TODO: backup the log according to date
                # shutil.copy2('./history/' + data_file, './backup/' + data_file, )
            else:
                print("No updates from last run.")
        print("##----------------------------")


# TODO: need to check connection to server before sending data
def submit_new_data(json_data):
    url = "http://localhost:3000/companies"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json_data)

    if response.status_code == 200:
        print("Data submitted successfully")
    else:
        print("Failed to submit data")
    time.sleep(1)


def main():
    while True:
        check_update()
        time.sleep(30) # should be smaller than 60 secs


if __name__ == '__main__':
    main()
