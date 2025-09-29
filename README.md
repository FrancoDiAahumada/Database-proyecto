# Database-proyecto

Proyecto ETL minimalista que extrae datos desde PostgreSQL, transforma ventas por cliente y carga resultados a BigQuery. Diseñado para ejecutarse localmente o desplegarse como Cloud Function mediante Terraform.

Badges
- Estado: draft
- Tecnología: Python, Terraform, Google Cloud

Contenido
- Resumen
- Arquitectura
- Ejecutar localmente
- Despliegue (Terraform)
- Estructura del repositorio
- Archivos clave
- Buenas prácticas

Resumen
Proyecto educativo / práctico que implementa un pipeline ETL:
- Extracción: [`extract_data`](ETL/extract.py)
- Transformación: [`calculate_sales_by_customer`](ETL/transform.py)
- Carga: [`load_to_bigquery`](ETL/load.py)
- Entrypoint Cloud Function: [`etl_entrypoint`](ETL/main.py)

Arquitectura
1. PostgreSQL (source) -> 2. ETL (Python) -> 3. BigQuery (dest)
El código de la función se empaqueta en ZIP y se sube a un bucket GCS mediante la configuración en [terraform/main.tf](terraform/main.tf).

Ejecutar localmente
1. Crear y activar virtualenv:
```sh
python -m venv env
# Windows
env\Scripts\activate
# Unix
source env/bin/activate
```
pip install -r [requirements.txt](http://_vscodecontentref_/0)
functions-framework --target=etl_entrypoint --port=8080

cd terraform
terraform init
terraform apply

Archivos importantes: terraform/main.tf, terraform/variables.tf, terraform/terraform.tfvars.

Estructura del repositorio (resumen)

ETL/: código Python del pipeline — ver ETL/main.py
terraform/: infra como código para deploy — ver terraform/main.tf
.env: variables locales — ver .env
Archivos clave y símbolos

etl_entrypoint — handler HTTP (Cloud Functions)
main — flujo ETL principal
extract_data — conexión y extracción desde PostgreSQL
calculate_sales_by_customer — transformación de negocio
load_to_bigquery — carga y diagnóstico de BigQuery
Buenas prácticas

Nunca commitear credenciales; ya están en .gitignore.
Guardar secretos en Secret Manager en producción.
Versionar requirements y probar compatibilidades (pandas / pyarrow).
Contribuir Abrir issues o PRs con cambios y pruebas claras. Ejecutar tests y linter antes de enviar PR.

Licencia Añadir LICENSE según corresponda. Franco Ahuamada sepulveda