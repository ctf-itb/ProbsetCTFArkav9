from flask import Flask, request, session
import os, yaml, shlex, subprocess
import geoip2.database

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

def get_client_public_ip():
    if request.headers.getlist("X-Forwarded-For"):
        public_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        public_ip = request.remote_addr
    return public_ip

def get_country_code_by_ip(ip_address, db_path='GeoLite2-Country.mmdb'):
    try:
        reader = geoip2.database.Reader(db_path)
        response = reader.country(ip_address)
        return response.country.iso_code
    except Exception as e:
        print(f"Error fetching country code: {e}")
        return 'Unknown'

# still buggy, please be nice
@app.route("/log", methods=["POST"])
def analyze():
    if "admin" not in session or session["admin"] != True:
        return "Unauthorized access"
    if "name1" not in request.form or "name2" not in request.form or "mtch" not in request.form:
        return "Data tidak lengkap"
    name1 = request.form["name1"]
    name2 = request.form["name2"]
    mtch = request.form["mtch"]

    ip_addr = get_client_public_ip()
    cc = get_country_code_by_ip(ip_addr)
    y = f"""
    - echo
    - {ip_addr}
    - {cc}
    - {name1}
    - {name2}
    - {mtch}
    """
    try:
        arr = yaml.load(y, Loader=yaml.FullLoader)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
    try:
        for i in range(len(arr)):
            if arr[i]:
                arr[i] = shlex.quote(arr[i])
            else:
                del arr[i]
    except Exception as e:
        print(f"Error processing array: {e}")
    subprocess.run(' '.join(str(x) for x in arr if x), shell=True)
    return "Logged"

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
