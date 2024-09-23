resource "google_service_account" "dataflow_sa" {
  account_id   = "dataflow-flight-account" 
  display_name = "Dataflow Service Account Flight"  
}

resource "google_project_iam_member" "dataflow_pubsub_subscriber" {
  project = var.gcp-flight-data-project  }
  role    = "roles/pubsub.subscriber"  
  member  = "serviceAccount:${google_service_account.dataflow_sa.email}"  


resource "google_pubsub_topic" "flight_data_topic" {
  name = var.flight-data-topic 
}

resource "google_pubsub_subscription" "flight_data_subscription" {
  name  = var.flight-data-subscription  
  topic = google_pubsub_topic.flight_data_topic.name  
}

resource "google_storage_bucket" "flight_data_bucket" {
  name     = "${var.project_id}-flight-data-bucket"  
  location = var.europe-west3  
}

resource "google_bigquery_dataset" "flight_data_dataset" {
  dataset_id = "flight_data"  
  location   = var.europe-west3  
}

resource "google_bigquery_table" "flight_data_table" {
  dataset_id = google_bigquery_dataset.flight_data_dataset.dataset_id  
  table_id   = "flight_data"  
  schema     = file("${path.module}/bigquery_schema.json")  
}

output "pubsub_topic" {
  value = google_pubsub_topic.flight_data_topic.name  
}

output "pubsub_subscription" {
  value = google_pubsub_subscription.flight_data_subscription.name  
}

output "storage_bucket" {
  value = google_storage_bucket.flight_data_bucket.name  
}

output "bigquery_table" {
  value = google_bigquery_table.flight_data_table.table_id  
}
