aixblock ml
pip install -e .
aixblock-ml create my_ml_backend
aixblock-ml start my_ml_backend
aixblock-ml start my_ml_backend -p 9091

aixblock-ml deploy gcp {ml-backend-local-dir} \
--from={model-python-script} \
--gcp-project-id {gcp-project-id} \
--label-studio-host {https://aixblock.org} \
--label-studio-api-key {YOUR-AIXBLOCK-API-KEY}