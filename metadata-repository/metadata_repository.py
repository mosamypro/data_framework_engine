# pylint: disable=import-error
from flask import Flask, request, jsonify
from threading import Thread, Lock
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add thread safety with locks
metadata_lock = Lock()
metadata_store = {}
schema_change_events = []

@app.route('/metadata', methods=['POST'])
def save_metadata():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        if 'source_id' not in data or 'metadata' not in data:
            return jsonify({"error": "Missing required fields: source_id or metadata"}), 400
        
        source_id = data['source_id']
        
        with metadata_lock:
            metadata_store[source_id] = data['metadata']
            schema_change_events.append({'source_id': source_id, 'event': 'schema_changed'})
        
        logger.info(f"Saved metadata for source_id: {source_id}")
        return jsonify({"status": "success"}), 201
    
    except Exception as e:
        logger.error(f"Error saving metadata: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/events', methods=['GET'])
def get_events():
    with metadata_lock:
        events = list(schema_change_events)  # Create a copy to avoid race conditions
    return jsonify(events)

def start_metadata_service():
    # Bind to all interfaces (0.0.0.0) to make it accessible from outside the container
    app.run(host='0.0.0.0', port=5000)

def init():
    # Start the metadata repository as a background thread
    metadata_service_thread = Thread(target=start_metadata_service)
    metadata_service_thread.daemon = True
    metadata_service_thread.start()
    logger.info("Metadata repository service started")

# Only start the service if this file is run directly
if __name__ == "__main__":
    init()
else:
    # If imported as a module, provide a function to start the service
    logger.info("Metadata repository module loaded")
