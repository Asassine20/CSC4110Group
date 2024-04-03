#Revision 1 4/2/2024
#Beging CS NJA 4/2/2024
"""
G1 CSC Bug Tracker
"""
import datetime as d
import pickle

#First time run assignment is below:
#tracker = [{'Name': 'Julian','Bug':'Crash on Startup',
#'Application':'Calculator', 'Dev Assigned':'Dave','Timestamp':'03/28/24, #16:37:10'}]
# dev_data = {'Phillip': True, 'Dave': False, 'James': True}

with open('ForestviewBugTracker.pkl', 'rb') as f:
    tracker = pickle.load(f)
with open('ForestviewSoftwareDevs.pkl', 'rb') as g:
    dev_data = pickle.load(g)


def load():
    """
    Loads/Updates database
    """
    with open('ForestviewBugTracker.pkl', 'wb') as f:
        pickle.dump(tracker,f)
    with open('ForestviewSoftwareDevs.pkl', 'wb') as g:
        pickle.dump(dev_data,g)
    with open('ForestviewBugTracker.pkl', 'rb') as f:
        tracker_e = pickle.load(f)
    with open('ForestviewSoftwareDevs.pkl', 'rb') as g:
        dev_data_e = pickle.load(g)
    #below print statements can be split
    print(tracker_e)
    print(dev_data_e)

def check_dev(x, data):
    """
    Checks if dev is available
    """
    if data[x] is True:
        data[x] = False
        return True
    else:
        return False

def _filter(x):
    """
    Filters for special characters
    """
    #special characters can be added as condition to allow
    #allowed_char = [] , along those lines
    temp = ''
    for i in x:
        if (i.isalpha() or i.isdigit() or i == ' ' or i == ','):
            temp += i
    return temp

def _create_data(entry_log):
    """
    Bug tracking data creation
    """
    #entry_log can be used inside if accessing the input directly from UI
    #entry_log = enter_info.get() or something along those lines
    storage = {}
    entry_log = _filter(entry_log)
    #filter characters before input into storage
    entry_log = entry_log.split(',')
    #splitting up the input, if UI entry is changed, change as well
    if check_dev(entry_log[3], dev_data) is True:
        storage['Name'] = entry_log[0]
        storage['Bug'] = entry_log[1]
        storage['Application'] = entry_log[2]
        storage['Dev Assigned'] = entry_log[3]
        storage['Timestamp'] = d.datetime.now().strftime("%x, %X")
        tracker.append(storage)
    else:
        print("Dev is not available")

def query(x):
    """
    Function to query database
    """
    #q_entry is just the entry for type of infromation to find
    #q_entry = enter_info.get(), possible UI replacement for input
    #q_entry = _filter(q_entry)
    #q_entry = q_entry.split(',')
    #below is a temp logic for logs
    #if q_entry[0]=='logs':
        #print("Log event " + q_entry[1] + logs[int(q_entry[1])])
    #else:
    out = next((i for i in tracker if i['Name'] == x), None)
    print(out)

load()
#query('Julian') use to find out logic before UI is put in
#load() use on first run, can be swapped out when UI is added

#Revision 1 4/2/2024
#Beging CS NJA 4/2/2024
