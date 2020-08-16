#!/usr/bin/env bash

BACKUP_PATH=s3://backups.sandbox.stackhawk.com/devkube/zconger/postgres/beak.sql
SERVICE_ACCOUNT=devkube-db

function pg-patch-content() {
  cat << EOF
spec:
  template:
    spec:
      volumes:
        - name: init-dir
          emptyDir: {}
      initContainers:
        - name: postgres-init
          image: amazon/aws-cli
          command: ["aws"]
          args:
            - s3
            - cp
            - ${BACKUP_PATH}
            - /docker-entrypoint-initdb.d/
          volumeMounts:
            - mountPath: /docker-entrypoint-initdb.d
              name: init-dir
      containers:
      - name: postgres-beak
        volumeMounts:
          - mountPath: /docker-entrypoint-initdb.d
            name: init-dir
      serviceAccountName: ${SERVICE_ACCOUNT}
EOF
}

# Merge the deployment file with the patch file into a "merged" file
#yq m postgres-beak-deployment.yaml postgres-beak-deployment-patch.yaml > postgres-beak-deployment-merged.yaml

pg-patch-content | yq m postgres-beak-deployment.yaml -
