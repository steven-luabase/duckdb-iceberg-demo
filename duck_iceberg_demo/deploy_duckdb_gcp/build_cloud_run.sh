SERVICE_NAME=duck-iceberg-demo
REGION=us-east1
PROJECT_ID=YOUR_PROJECT_ID
gcloud config set project ${PROJECT_ID}
gcloud run deploy ${SERVICE_NAME} \
  --source . \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --memory 8Gi \
  --cpu 2

