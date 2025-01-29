from fastapi import FastAPI
import threading
import requests
import paramiko  # For executing code on a remote VM via SSH
import re
import json
from urllib.parse import urlparse
from codecarbon import EmissionsTracker

tracker = EmissionsTracker()

app = FastAPI(title="Orchestrator Microservice")

execution_result = {"output": None}

# Global stop event to control thread execution
stop_event = threading.Event()

def execute_encoder_code(url):
    """Function to execute code on the encoder remote VM."""
    global stop_event
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname="192.168.37.88", username="user", password="user")
        command = f"python3 /home/user/ExtractParamsURL/threadsManager.py '{url}'"
        stdin, stdout, stderr = ssh.exec_command(command)
        
        # Continuously check if we should stop
        while not stdout.channel.exit_status_ready():
            if stop_event.is_set():
                print("Stopping encoder execution early...")
                return

        raw_output = stdout.read().decode().strip()

        # Check stop event before processing further
        if stop_event.is_set():
            print("Encoder execution stopped before processing JSON.")
            return

        match = re.search(r"(\{.*\})", raw_output, re.DOTALL)
        if match:
            json_str = match.group(1)  # Extract only the JSON part
        else:
            json_str = None

        if json_str:
            try:
                encoder_output = json.loads(json_str)
            except json.JSONDecodeError as e:
                execution_result["output"] = {
                    "error": "Invalid JSON format",
                    "raw_output": raw_output
                }
                return
        else:
            execution_result["output"] = {
                "error": "No valid JSON found",
                "raw_output": raw_output
            }
            return

        json_data = json.dumps(encoder_output)
        url_predict = "http://192.168.37.14:8004/predict"
        headers = {"Content-Type": "application/json"}

        response = requests.post(url_predict, data=json_data, headers=headers, timeout=10)
        print("response: ", response.json())

        # Check stop event before saving result
        if stop_event.is_set():
            print("Encoder execution stopped before saving output.")
            return

        execution_result['output'] = response.json()
        print("Command Output:", execution_result['output'])

        # Add prediction to database table
        url_add_to_db = f"http://192.168.37.38:8010/reliability/add"
        headers = {"Content-Type": "application/json"}
        json_data = {"url": url, "prediction": execution_result['output'].get("prediction", None), "confidence": execution_result['output'].get("confidence", None)}
        response = requests.post(url_add_to_db, json=json_data, headers=headers, timeout=10)
        print("Add to database response: ", response.json())

    finally:
        ssh.close()
        print("Execution thread stopped.")


def query_database(input_url):
    """Function to query the database."""
    global stop_event
    url = f"http://192.168.37.38:8010/reliability/check/?url={input_url}"

    try:
        response = requests.get(url, timeout=10)
        
        execution_result["output"] = response.json()
        print("Database Query Output:", execution_result["output"])

    except requests.RequestException as e:
        print(f"Database request failed: {e}")

@app.get("/start_orchestration/")
def start_orchestration(url):
    tracker.start()
    global stop_event, execution_result
    stop_event.clear()  # Reset stop flag
    execution_result = {"output": None}

    # Create threads
    exec_thread = threading.Thread(target=execute_encoder_code, args=(url,))
    db_thread = threading.Thread(target=query_database, args=(url,))

    exec_thread.start()
    db_thread.start()

    db_thread.join()  # Wait for the DB thread to complete

    # If the database query was successful, return immediately
    print(execution_result["output"].get("prediction", None))
    if execution_result["output"].get('prediction', None) != "not_found":
        # If DB query finishes first, stop the encoder immediately
        stop_event.set()
        print("Database finished first. Stopping encoder...")
        tracker.stop()
        return {"status": "Orchestration complete", "execution_output": execution_result["output"]}

    print("Database result was not found or an error occurred. Awaiting encoder result...")
    
    # If database failed, wait for the encoder thread to complete
    exec_thread.join()
    tracker.stop()
    return {"status": "Orchestration complete", "execution_output": execution_result["output"]}


# start_orchestration("https://www.marmiton.org/recettes/recette_pate-a-crepes_12372.aspx")
