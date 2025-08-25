import csv
import telnetlib


# Pulls data out of CSV and converts to list
def csv_data(csv_name, csv_row):
    with open(csv_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for single_line in range(csv_row - 1):
            next(reader)
        return next(reader)


# Converts CSV list to complete info for telnet update
def prep_info(info):
    # Combining information for simplicity later
    router_wan = info[2] + info[3]
    cam1_wan = info[2] + info[4]
    cam2_wan = info[2] + info[5]
    plc_wan = info[2] + info[6]
    hmi_wan = info[2] + info[7]
    cam1_lan = info[8] + info[9]
    cam2_lan = info[8] + info[10]
    plc_lan = info[11] + info[12]
    hmi_lan = info[11] + info[13]
    switch_model = info[14]
    dept_name = info[0]
    line_number = info[1]

    # Ordered by WAN group, LAN group, and Misc Info
    ret_info = [router_wan, cam1_wan, cam2_wan, plc_wan, hmi_wan,
                cam1_lan, cam2_lan, plc_lan, hmi_lan,
                switch_model, dept_name, line_number]

    return ret_info


# Format structure for ping view
def format_ping(ip):
    # Formatting for ping view variables
    rtr = ip[0]
    cam1 = ip[1]
    cam2 = ip[2]
    plc = ip[3]
    hmi = ip[4]
    swb = ip[9]
    dep = ip[10]
    lin = ip[11]

    # Build ping list
    rtr_str = rtr + " " + dep + " " + lin + " Router - " + swb
    cam1_str = cam1 + " " + dep + " " + lin + " CAM1"
    cam2_str = cam2 + " " + dep + " " + lin + " CAM2"
    plc_str = plc + " " + dep + " " + lin + " PLC"
    hmi_str = hmi + " " + dep + " " + lin + " HMI"

    # Combine ping list for later breakdown
    ping = [rtr_str, cam1_str, cam2_str, plc_str, hmi_str]

    return ping


# Perform test of telnet - not in use
def test_tn(router_address, router_brand, user, p_word):
    # base variables
    port = 23
    timeout = 3
    login_status = ""

    # Open telnet and connect to switch
    tn = telnetlib.Telnet()
    tn.open(router_address, port, timeout)

    print("Open telnet for " + router_address + " " + router_brand)

    # Login Moxa and check failure
    if router_brand == "Moxa":
        tn.read_until(b"login as: ")
        tn.write(user.encode("ascii") + b"\n")
        tn.read_until(b"Password: ")
        tn.write(p_word.encode("ascii") + b"\n")
        login_status = tn.read_until(b"Login incorrect").decode('ascii')[:-15]
        tn.close()

    # Login Cisco
    if router_brand == "Cisco":
        tn.read_until(b"Username: ")
        tn.write(user.encode("ascii") + b"\n")
        tn.read_until(b"Password: ")
        tn.write(p_word.encode("ascii") + b"\n")
        login_status = tn.read_until(b"Login invalid").decode('ascii')[:-13]
        tn.close()

    print("Closed telnet for " + router_address + " " + router_brand)

    return login_status


# Function run location
FILE = "PFS_Update_Info.csv"
update_log = []

# Populate user and password for routers - all must have same user/pass
# username = input("Username: ")
# password = getpass.getpass()
# username = "admin"
# password = "private"

# Row starts at 2
row = 2
row_tot = 58  # 58 total rows
while row < row_tot:
    # Pull one row of data (one router) from csv
    csv_info = csv_data(FILE, row)

    # Organize data pull into ip addresses and other info
    info_prep = prep_info(csv_info)

    # Format text for ping view
    update_text = format_ping(info_prep)

    # Logs updates made to router
    with open('PFSPing.txt', 'a') as file:
        file.write('\n'.join(update_text))
        file.write('\n')

    # Need to reset update text to prevent accidental overlap
    update_text = []

    row = row + 1
