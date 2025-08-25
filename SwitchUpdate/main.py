import telnetlib
import csv
import getpass
import os
import time


# Pulls data out of CSV and converts to list
def csv_data(csv_name, csv_row):
    with open(csv_name, 'r') as file:
        reader = csv.reader(file)
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


# Use built Ips to see which
def test_ip_active(ipinfo):
    response_list = []
    i = 0

    # Pings WAN IPs to see which devices are active
    while i < 5:
        hostname = ipinfo[i]
        response = os.system("ping -n 1 " + hostname)
        response_list.append(response)
        i = i + 1

    return response_list


# Builds commands for router prior to connection
def build_cmd(ip, ip_response):
    # WAN Info
    # rw = ip[0]   # Router IP
    # c1w = ip[1]  # Camera 1 Wan IP
    # c2w = ip[2]  # Camera 2 Wan IP
    # pw = ip[3]   # PLC Wan IP
    # hw = ip[4]   # HMI Wan IP

    # LAN Info
    # c1l = ip[5]  # Camera 1 Lan IP
    # c2l = ip[6]  # Camera 2 Lan IP
    # pl = ip[7]   # PLC Lan IP
    # hl = ip[8]   # HMI Lan IP

    # Misc Info
    st = ip[9]  # Switch Type
    # dep = ip[10]      # Department
    # ln = ip[11]       # Line number

    # IP Responses
    rwr = ip_response[0]  # Router IP response
    # c1wr = ip_response[1]  # Cam 1 IP response
    # c2wr = ip_response[2]  # Cam 2 IP response
    # pwr = ip_response[3]   # PLC IP response
    # hwr = ip_response[4]   # HMI IP response

    # Function variables
    command_list = []
    x = 1

    if rwr != 0:
        command_list.append("No router response")
        return command_list

    if st == "Moxa":
        command_list.append("configure terminal")
        while x < 5:
            if ip_response[x] != 0:
                next_command = "ip nat static inside " + ip[x + 4] + " outside wan " + ip[x]
                command_list.append(next_command)
            x = x + 1
        command_list.append("exit")
        command_list.append("save")
        command_list.append("reload")

    if st == "Cisco":
        command_list.append("configure terminal")
        while x < 5:
            if ip_response[x] != 0:
                next_command = "ip nat inside source static " + ip[x + 4] + " " + ip[x]
                command_list.append(next_command)
            x = x + 1
        command_list.append("exit")
        command_list.append("write")

    return command_list


# Opens telnet and runs commands
def run_telnet(cmds, router_address, user, p_word, router_brand):
    # hold variables to clear faults
    port = 23
    timeout = 3

    # Open telnet and connect to switch
    tn = telnetlib.Telnet()
    tn.open(router_address, port, timeout)

    # Login with Username
    if router_brand == "Moxa":
        tn.read_until(b"login as: ")
    if router_brand == "Cisco":
        tn.read_until(b"Username: ")
    tn.write(user.encode("ascii") + b"\n")

    # Login with Password
    tn.read_until(b"Password: ")
    tn.write(p_word.encode("ascii") + b"\n")
    time.sleep(1)

    for command in cmds:
        tn.write(command.encode("ascii"))
        time.sleep(1)
        tn.write(b"\n")
        time.sleep(1)
    # print(tn.read_until(b"ffa").decode('ascii'))

    # exit telnet
    tn.close()


# Broken down IP Location
FILE = "venv/PFS_Update_Info.csv"

# Populate user and password for routers - all must have same user/pass
username = input("Username: ")
password = getpass.getpass()

# Function run location
# Row starts at 2
row = 2
row_tot = 54  # 58 total rows
while row < row_tot:
    # Modify variables to ensure correct outputs
    router_ip = ""
    switch_type = ""
    department = ""
    line = ""
    Cam1 = ""
    Cam2 = ""
    PLC = ""
    HMI = ""
    commands = []

    # Pull one row of data (one router) from csv
    csv_info = csv_data(FILE, row)

    # Organize data pull into ip addresses and other info
    info_prep = prep_info(csv_info)

    # Variables to run telnet later and print updates
    router_ip = info_prep[0]
    switch_type = info_prep[9]
    department = info_prep[10]
    line = info_prep[11]

    # Ping devices on OT net to determine what needs to be updated - no ping implies not device not translated
    ip_test = test_ip_active(info_prep)

    # Report what devices are added to the router NAT
    if ip_test[1] != 0:
        Cam1 = " Cam1,"
    if ip_test[2] != 0:
        Cam2 = " Cam2,"
    if ip_test[3] != 0:
        PLC = " PLC,"
    if ip_test[4] != 0:
        HMI = " HMI"

    # Build command list based on switch type and unreachable devices
    commands = build_cmd(info_prep, ip_test)

    # Check to make sure router is active before trying to connect, otherwise don't telnet
    if commands[0] != "No router response":
        # Connect to router via telnet and input commands
        run_telnet(commands, router_ip, username, password, switch_type)
        update_text = (department + " line " + line + " updated" + Cam1 + Cam2 + PLC + HMI)
    else:
        update_text = ("No response from: " + department + " line " + line + " - " + router_ip)

    # Logs updates made to router
    with open('PFS_router_update_log.txt', 'a') as log_file:
        log_file.write(update_text)
        log_file.write("\n")

    row = row + 1
