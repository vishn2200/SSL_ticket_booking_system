import os
from OpenSSL import crypto

# Create the "certs" folder if it doesn't exist
if not os.path.exists("certs"):
    os.makedirs("certs")

# Generate a new private key
key = crypto.PKey()
key.generate_key(crypto.TYPE_RSA, 2048)

# Generate a self-signed certificate
cert = crypto.X509()
cert.get_subject().CN = "Vishnu Prakash"
cert.set_serial_number(1)
cert.gmtime_adj_notBefore(0)
cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)  # 1 year validity
cert.set_issuer(cert.get_subject())
cert.set_pubkey(key)
cert.sign(key, "sha256")

# Save the private key and certificate to files
key_file_path = os.path.join("certs", "server.key")
cert_file_path = os.path.join("certs", "server.crt")

with open(key_file_path, "wb") as key_file:
    key_file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

with open(cert_file_path, "wb") as cert_file:
    cert_file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

print("Private key and certificate files created in the 'certs' folder.")
