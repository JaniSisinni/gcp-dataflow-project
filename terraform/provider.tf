provider "google" {
  project = var.gcp-flight-data-project 
  region  = var.europe-west3      
}

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}
