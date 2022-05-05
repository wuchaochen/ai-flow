#!/usr/bin/env bash
##
## Licensed to the Apache Software Foundation (ASF) under one
## or more contributor license agreements.  See the NOTICE file
## distributed with this work for additional information
## regarding copyright ownership.  The ASF licenses this file
## to you under the Apache License, Version 2.0 (the
## "License"); you may not use this file except in compliance
## with the License.  You may obtain a copy of the License at
##
##   http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing,
## software distributed under the License is distributed on an
## "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
## KIND, either express or implied.  See the License for the
## specific language governing permissions and limitations
## under the License.
##
set -e

current_dir=$(cd "$(dirname "$0")";pwd)
root_dir=${current_dir}/../..
echo $root_dir

PROTO_FILES=( "namespace.proto" "workflow.proto" "schedule.proto" "execution.proto")

# generate go file
protoc -I/usr/local/include -I. \
  -I$GOPATH/src \
  -I$GOPATH/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis \
  --go_out=Mgoogle/api/annotations.proto=github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis/google/api,plugins=grpc:../go \
  common.proto

for i in "${PROTO_FILES[@]}"
do
  protoc -I/usr/local/include -I. \
    -I$GOPATH/src \
    -I$GOPATH/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis \
    --go_out=Mgoogle/api/annotations.proto=github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis/google/api,plugins=grpc:../go \
    --grpc-gateway_out=logtostderr=true:../go \
    "${i}"
done


# generate python file
python3 -m grpc.tools.protoc -I. \
  -I/usr/local/include \
  -I$GOPATH/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis \
  --python_out=.. \
  common.proto

for i in "${PROTO_FILES[@]}"
do
  python3 -m grpc.tools.protoc -I. \
    -I/usr/local/include \
    -I$GOPATH/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis \
    --python_out=.. \
    --grpc_python_out=.. \
    "${i}"
done

cd ..

IMPORT_WORDS=( "common" "namespace" "workflow" "schedule" "execution" )
for i in "${IMPORT_WORDS[@]}"
do
  w="s/^import ${i}_pb2 as ${i}__pb2/from \. import ${i}_pb2 as ${i}__pb2/"
  echo $w
  sed -i -E $w *pb2*.py
done
rm -rf *.py-E
