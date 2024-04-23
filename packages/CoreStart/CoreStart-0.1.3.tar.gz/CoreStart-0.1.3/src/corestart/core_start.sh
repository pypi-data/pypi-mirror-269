#!/bin/bash
#!/bin/bash

# Define the base directory
BASE_DIR="your_fullstack_project"

# Create the base structure
mkdir -p $BASE_DIR

# API structure
mkdir -p $BASE_DIR/api/{routers,controllers,models,services,utils,exceptions,config,logs}
touch $BASE_DIR/api/main.py
touch $BASE_DIR/api/dependencies.py
touch $BASE_DIR/api/routers/users.py
touch $BASE_DIR/api/routers/products.py
touch $BASE_DIR/api/controllers/userController.py
touch $BASE_DIR/api/controllers/productController.py
touch $BASE_DIR/api/models/userModel.py
touch $BASE_DIR/api/models/productModel.py
touch $BASE_DIR/api/services/userService.py
touch $BASE_DIR/api/services/productService.py
touch $BASE_DIR/api/utils/security.py
touch $BASE_DIR/api/utils/commonHelpers.py
touch $BASE_DIR/api/config/config.py
touch $BASE_DIR/api/logs/access.log
touch $BASE_DIR/api/logs/error.log

# Web structure
mkdir -p $BASE_DIR/web/{pages,components,styles,public}
touch $BASE_DIR/web/pages/index.js
touch $BASE_DIR/web/pages/about.js
mkdir -p $BASE_DIR/web/pages/users
touch $BASE_DIR/web/pages/users/[id].js
mkdir -p $BASE_DIR/web/pages/products
touch $BASE_DIR/web/pages/products/[id].js
touch $BASE_DIR/web/components/Header.js
touch $BASE_DIR/web/components/Footer.js
touch $BASE_DIR/web/components/Layout.js
touch $BASE_DIR/web/styles/globals.css
touch $BASE_DIR/web/styles/theme.css
touch $BASE_DIR/web/public/favicon.ico
touch $BASE_DIR/web/public/logo.png

# ML_AI structure
mkdir -p $BASE_DIR/ML_AI/{training,prediction,evaluation,experiments/{current,archive},models/{latest,archive},data/{processed,raw}}
touch $BASE_DIR/ML_AI/training/train_model.py
touch $BASE_DIR/ML_AI/training/hyperparameters.json
touch $BASE_DIR/ML_AI/prediction/predict_model.py
touch $BASE_DIR/ML_AI/evaluation/evaluate_model.py

# Data Engineering structure
mkdir -p $BASE_DIR/data_engineering/{ETL_scripts,batch_jobs,spark,kafka,connectors/{elasticsearch,clickhouse,postgres,rabbitmq}}

# DevOps structure
mkdir -p $BASE_DIR/devops/{docker,kubernetes,ci_cd,monitoring/{prometheus,grafana}}
touch $BASE_DIR/devops/docker/Dockerfile
touch $BASE_DIR/devops/docker/docker-compose.yml
touch $BASE_DIR/devops/kubernetes/deployment.yaml
touch $BASE_DIR/devops/kubernetes/service.yaml
touch $BASE_DIR/devops/ci_cd/github_actions.yaml
touch $BASE_DIR/devops/ci_cd/jenkinsfile

# Tests structure
mkdir -p $BASE_DIR/tests/{api_tests,ML_AI_tests,integration_tests,system_tests,web_tests}
touch $BASE_DIR/tests/api_tests/test_users.py
touch $BASE_DIR/tests/api_tests/test_products.py
touch $BASE_DIR/tests/ML_AI_tests/test_training.py
touch $BASE_DIR/tests/ML_AI_tests/test_prediction.py
touch $BASE_DIR/tests/integration_tests/test_data_flow.py
touch $BASE_DIR/tests/system_tests/test_system_performance.py
touch $BASE_DIR/tests/web_tests/test_pages.py
touch $BASE_DIR/tests/web_tests/test_components.py

# Database structure
mkdir -p $BASE_DIR/database/{schema,migrations}
touch $BASE_DIR/database/schema/userSchema.sql
touch $BASE_DIR/database/schema/productSchema.sql
touch $BASE_DIR/database/migrations/001_initial.sql
touch $BASE_DIR/database/migrations/002_updates.sql

# Scripts structure
mkdir -p $BASE_DIR/scripts
touch $BASE_DIR/scripts/setup_dev_env.sh
touch $BASE_DIR/scripts/deploy_prod.sh

echo "Project structure created successfully!"
