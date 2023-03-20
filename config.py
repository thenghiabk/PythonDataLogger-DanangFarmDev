import configparser


# config_param : dictionary
def create_new_config(config_param):
    current_config = configparser.ConfigParser()
    current_config.read('config.ini')
    if current_config.has_section(config_param['controller_name']):
        print('This controller does not exist.')
        return
    else:
        current_config.add_section(config_param['controller_name'])
        current_config.set(config_param['controller_name'], 'house_name', config_param['house_name'])
        current_config.set(config_param['controller_name'], 'house_number', config_param['house_number'])
        current_config.set(config_param['controller_name'], 'flock_number', config_param['flock_number'])
        current_config.set(config_param['controller_name'], 'last_update', config_param['last_update'])
        with open('config.ini', 'a') as config_file:
            current_config.write(config_file)
        print('Finished adding new configuration.')


# config_param : dictionary
def update_config(config_param):
    current_config = configparser.ConfigParser()
    current_config.read('config.ini')
    if not current_config.has_section(config_param['controller_name']):
        print('This controller does not exist. Please add it first.')
        return
    else:
        current_config.set(config_param['controller_name'], 'house_name', config_param['house_name'])
        current_config.set(config_param['controller_name'], 'house_number', config_param['house_number'])
        current_config.set(config_param['controller_name'], 'flock_number', config_param['flock_number'])
        current_config.set(config_param['controller_name'], 'last_update', config_param['last_update'])
        with open('config.ini', 'w') as config_file:
            current_config.write(config_file)
        print('Finished updating configuration.')


# controller_name : string
# collect_time: string
def save_last_update_time_to_config(controller_name, collect_time):
    current_config = configparser.ConfigParser()
    current_config.read('config.ini')

    new_config_param = {
        'controller_name': controller_name,
    }

    current_config[controller_name]['last_update'] = collect_time
    new_config_param.update(current_config[controller_name])
    update_config(new_config_param)
