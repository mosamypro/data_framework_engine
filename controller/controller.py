# pylint: disable=E0401  # Disable "import-error" by error code
import requests
import time

class Controller:
    def __init__(self, metadata_repo_url):
        self.metadata_repo_url = metadata_repo_url

    def listen_for_events(self):
        last_event_index = 0
        while True:
            try:
                response = requests.get(f"{self.metadata_repo_url}/events", timeout=10)
                response.raise_for_status()  # Raise an exception for HTTP errors
                events = response.json()
                for event in events[last_event_index:]:
                    self.handle_event(event)
                last_event_index = len(events)
            except requests.exceptions.RequestException as e:
                print(f"Error connecting to metadata repository: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
            finally:
                time.sleep(5)  # Always sleep before next iteration

    def handle_event(self, event):
        try:
            if not isinstance(event, dict):
                print(f"Invalid event format: {event}")
                return
                
            if 'event' not in event or 'source_id' not in event:
                print(f"Missing required fields in event: {event}")
                return
                
            if event['event'] == 'schema_changed':
                print(f"Schema changed detected for source: {event['source_id']}")
                # Trigger logic to update hubs, links, satellites
                self.update_data_vault(event['source_id'])
        except Exception as e:
            print(f"Error handling event: {e}")

    def update_data_vault(self, source_id):
        try:
            print(f"Updating data vault for source: {source_id}")
            # Logic to update hubs, links, satellites
            # TODO: Implement actual data vault update logic
        except Exception as e:
            print(f"Error updating data vault for source {source_id}: {e}")
