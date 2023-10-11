import os
import datetime
import yaml

with open('update-time.yml', encoding='utf-8') as version_file:
    version_info = yaml.safe_load(version_file)

current_update = version_info['TIME']

utc_datetime = datetime.datetime.utcnow()
new_update = f'{utc_datetime.hour}:{utc_datetime.min} ngày {utc_datetime.day}/{utc_datetime.month}/{utc_datetime.year} theo giờ UTC.'
if current_update.startswith(new_update):
    current_update_list = current_update.split('.')
    current_update_list[-1] = str(int(current_update_list[-1]) + 1)
    new_update = '.'.join(current_update_list)
else:
    new_update += '1'

version_info['TIME'] = new_update

with open('update-time.yml', 'w', encoding='utf-8') as version_file:
    yaml.dump(version_info, version_file, sort_keys=False)

with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as fh:
    print(f'new_update={new_update}', file=fh)
