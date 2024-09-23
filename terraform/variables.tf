variable "project_id" {
  description = "GCP project ID"
  type        = string
  default     = "gcp-flight-data-project"
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "europe-west3"  
}

variable "pubsub_topic_name" {
  description = "Pub/Sub topic name"
  type        = string
  default     = "flight-data-topic"
}

variable "pubsub_subscription_name" {
  description = "Pub/Sub subscription name"
  type        = string
  default     = "flight-data-subscription"
}
