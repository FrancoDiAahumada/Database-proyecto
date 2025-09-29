variable "project_id" {
  description = "ID del proyecto GCP"
  type        = string
  default     = "database-proyecto-473020"
}

variable "region" {
  description = "Región de GCP"
  type        = string
  default     = "US"
}
variable "function_name" {
  description = "Nombre de la Cloud Function"
  type        = string
  default     = "etl-northwind"
}

variable "dataset_id" {
  description = "Dataset de BigQuery"
  type        = string
  default     = "northwind_dataset"
}

variable "table_id" {
  description = "Tabla de destino en BigQuery"
  type        = string
  default     = "sales_summary"
}

variable "db_host" {
  description = "Host de la base de datos (IP o connection name)"
  type        = string
}

variable "db_name" {
  description = "Nombre de la base de datos"
  type        = string
  default     = "northwind"
}

variable "db_user" {
  description = "Usuario de la base de datos"
  type        = string
}

variable "db_password" {
  description = "Contraseña de la base de datos"
  type        = string
  sensitive   = true
}

variable "bucket_name" {
  description = "Nombre del bucket donde se subirá el código"
  type        = string
}

variable "bucket_location" {
  description = "Ubicación del bucket (debe coincidir con el existente)"
  type        = string
  default     = "US"
}