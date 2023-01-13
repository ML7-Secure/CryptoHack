import pyshark

cap = pyshark.FileCapture(
    input_file="tls3.pcapng",
    custom_parameters={"-o": "ssl.keylog_file:keylogfile.txt"}, # learned about the custom_parameters option from @maple3142's solution for Authenticated Handshake
    display_filter="http2.data.data",
)

for packet in cap:
    print(bytes.fromhex(packet.layers[-1].data))