from fastapi import FastAPI
import threading
import time
import paramiko  # For executing code on a remote VM via SSH
# import psycopg2  # Replace with your database client library

app = FastAPI()

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
        command = f"python3 /home/user/ExtractParamsURL/threadManager.py '{url}'"
        stdin, stdout, stderr = ssh.exec_command(command)
        
        output = []
        while not stop_event.is_set():
            if stdout.channel.exit_status_ready():  # Check if the process is done
                output.extend(stdout.readlines())
                break
            time.sleep(1)  # Check status every second

        execution_result["output"] = "".join(output).strip()  # Convert list to string and remove extra spaces
        print(f"Execution Output: {execution_result['output']}")

        # TODO: Call the AI microservice with the results above as input 
        # and return the result of the AI microservice 
            
    finally:
        ssh.close()
        print("Execution thread stopped.")
        return result

def query_database():
    """Function to query the database."""
    global stop_event
    conn = None
    try:
        conn = psycopg2.connect(
            dbname="your_db",
            user="your_user",
            password="your_password",
            host="db-vm-ip",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM your_table WHERE condition=True;")
        result = cursor.fetchall()

        print(f"Database result: {result}")
        stop_event.set()  # Signal the execution thread to stop if DB query finishes first

    except Exception as e:
        print(f"Database error: {e}")
    
    finally:
        if conn:
            conn.close()

@app.post("/start_orchestration/")
def start_orchestration(url):
    global stop_event, execution_result
    stop_event.clear()  # Reset stop flag
    execution_result["output"] = None

    # Create threads
    exec_thread = threading.Thread(target=execute_encoder_code, args=(url,))
    # db_thread = threading.Thread(target=query_database)

    exec_thread.start()
    # db_thread.start()

    # db_thread.join()  # Wait for the DB thread to complete

    #if exec_thread.is_alive():
    #    print("Database finished first. Stopping execution thread...")
    #    stop_event.set()  # Request execution thread to stop
    
    exec_thread.join()  # Ensure execution thread stops before returning

    return {"status": "Orchestration complete", "execution_output": execution_result["output"]}


# start_orchestration("https://www.marmiton.org/recettes/recette_pate-a-crepes_12372.aspx")