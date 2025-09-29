terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }
}

provider "google" {
  project     = "database-proyecto-473020"
  region      = "us-central1"
  credentials = file("./key-etl.json")
}

resource "google_storage_bucket" "function_bucket" {
  name                        = var.bucket_name
  location                    = "US"                    # ← Debe ser "US", no "US-CENTRAL1"
  uniform_bucket_level_access = false                   # ← Debe ser false, como está ahora
  force_destroy               = false
  
  lifecycle {
    prevent_destroy = true
  }
}

# Empaquetar el código en ZIP
data "archive_file" "function_zip" {
  type        = "zip"
  output_path = "${path.module}/function.zip"
  source_dir  = "${path.module}/../ETL"

  excludes = [
    "__pycache__",
    "*.pyc",
    ".env",
    "*.sql"
  ]
}

# Subir ZIP al bucket
resource "google_storage_bucket_object" "function_archive" {
  name   = "etl-${data.archive_file.function_zip.output_md5}.zip"
  bucket = google_storage_bucket.function_bucket.name
  source = data.archive_file.function_zip.output_path
}

# Dataset de BigQuery (USA DATA SOURCE EN VEZ DE RESOURCE)
data "google_bigquery_dataset" "northwind" {
  dataset_id = var.dataset_id
  project    = var.project_id
}

# Cloud Function Gen 1 (más simple y estable)
resource "google_cloudfunctions2_function" "etl_function" {
  name        = var.function_name
  location    = var.region
  description = "ETL Northwind - Proyecto práctico minimalista"

  build_config {
    runtime     = "python311"
    entry_point = "etl_entrypoint"

    source {
      storage_source {
        bucket = google_storage_bucket.function_bucket.name
        object = google_storage_bucket_object.function_archive.name
      }
    }
  }

  service_config {
    available_memory = "512Mi"
    timeout_seconds  = 300

    environment_variables = {
      PROJECT_ID = var.project_id
      DATASET_ID = var.dataset_id
      TABLE_ID   = var.table_id
      DB_HOST    = var.db_host
      DB_NAME    = var.db_name
      DB_USER    = var.db_user
      DB_PASS    = var.db_password
    }
  }
  
  timeouts {
    create = "20m"
    update = "20m"
  }
}
# --- Outputs mínimos ---
output "function_uri" {
  description = "URL de la Cloud Function"
  value       = google_cloudfunctions2_function.etl_function.service_config[0].uri
}
output "bigquery_dataset" {
  description = "Dataset de BigQuery creado"
  value       = data.google_bigquery_dataset.northwind.dataset_id
}