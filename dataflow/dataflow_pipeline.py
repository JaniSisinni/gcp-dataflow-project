import apache_beam as beam
import json
from apache_beam.options.pipeline_options import PipelineOptions
from google.cloud import bigquery, storage

# Define the pipeline options
class DataflowOptions(PipelineOptions):
    project = "gcp-flight-data-project"
    region = "europe-west3"
    runner = "DataflowRunner"
    temp_location = "gs://gcp-flight-data-project/tmp/"
    staging_location = "gs://gcp-flight-data-project/staging/"

def parse_pubsub_message(message):
    # Parse the Pub/Sub message into a dictionary
    data = json.loads(message.decode('utf-8'))
    return {
        'flight_id': data.get('flight_id'),
        'departure_airport': data.get('departure_airport'),
        'arrival_airport': data.get('arrival_airport'),
        'departure_timestamp': data.get('departure_timestamp'),
        'arrival_timestamp': data.get('arrival_timestamp'),
        'delay_time': data.get('delay_time'),
        'cancelation': data.get('cancelation'),
        'passengers': data.get('passengers')
    }

def write_to_bigquery(row):
    client = bigquery.Client()
    table_id = 'gcp-flight-data-project:flight_data.test'
    errors = client.insert_rows_json(table_id, [row])
    if errors:
        print(f"Encountered errors while inserting rows: {errors}")
    else:
        print("New rows have been added.")

def write_to_gcs(row):
    client = storage.Client()
    bucket = client.bucket('flight-data-project')
    blob = bucket.blob(f"flight_data/{row['flight_id']}.json")
    blob.upload_from_string(json.dumps(row), content_type="application/json")
    print(f"Uploaded flight data for flight {row['flight_id']} to GCS.")

def run():
    options = DataflowOptions()
    p = beam.Pipeline(options=options)

    (p
     | 'Read from Pub/Sub' >> beam.io.ReadFromPubSub(topic='projects/gcp-flight-data-project/topics/flight-data-topic')
     | 'Parse Pub/Sub message' >> beam.Map(parse_pubsub_message)
     | 'Write to BigQuery' >> beam.Map(write_to_bigquery)
     | 'Write to GCS' >> beam.Map(write_to_gcs))

    p.run().wait_until_finish()

if __name__ == '__main__':
    run()
