tshark -r tls2.pcapng '-ouat:rsa_keys:"./privkey.pem",""' -q -z follow,tls,ascii,0 | grep -o "crypto\{.+\}"
# crypto{weaknesses_of_non_ephemeral_key_exchange}
