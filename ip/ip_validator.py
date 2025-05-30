import ipaddress

class IpValidator:
    @staticmethod
    def validate(ip:str):
        try: 
            ip_address = ipaddress.ip_address(ip)
            return isinstance(ip_address, ipaddress.IPv4Address)
        except ValueError:
            return False
