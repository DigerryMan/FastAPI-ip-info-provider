

class IpRegistry():
    def __init__(self):
        self.ip_dict = {}

    def check_if_already_known(self, ip):
        return ip in self.ip_dict.keys()
    
    def add_ip(self, ip, data):
        self.ip_dict[ip] = data
    
    def get_data_from_ip(self, ip):
        return self.ip_dict[ip]