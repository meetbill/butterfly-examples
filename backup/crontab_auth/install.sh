#!/bin/bash
#########################################################################
# File Name: install.sh
# Author: meetbill
# mail: meetbill@163.com
# Created Time: 2019-11-10 10:34:15
#
# src/static/js/config.router.js
# src/static/js/controllers/crontab.js
# src/static/tpl/crontab.html
# src/handlers/__init__.py
# src/handlers/api/__init__.py
# src/handlers/api/persistent.py
#########################################################################

CUR_DIR=`S=$(readlink "$0"); [ -z "$S"  ] && S=$0; cd $(dirname $S);pwd`
cd ${CUR_DIR}

butterfly_dir=$1
[[ -z "${butterfly_dir}" ]] && echo "usage:bash ./install.sh butterfly_dir" && exit -1
[[ -d "${butterfly_dir}" ]] && echo "butterfly dir is exists" && exit -1

mkdir -p ${butterfly_dir}

local_butterfly_dir=~/meetbill/github/butterfly
local_angulr_dir=~/meetbill/github/pine-Angulr
if [[ -d "${local_butterfly_dir}"  ]];then
    cp -rf ${local_butterfly_dir}/butterfly/* $butterfly_dir
fi
if [[ -d "${local_angulr_dir}"  ]];then
    cp -rf ${local_angulr_dir}/src/static $butterfly_dir
    cp -rf ${local_angulr_dir}/src/templates $butterfly_dir
fi


[[ ! -d "${butterfly_dir}/handlers"  ]] && echo "the dir is not a butterfly dir" && exit -1
[[ ! -d "${butterfly_dir}/static"  ]] && echo "the dir is not install angulr" && exit -1


for src_file in $(find * | grep -v third |grep -E '\.py|\.js|\.html')
do
    dest_file=${butterfly_dir}${src_file#*src}
    dest_dir=$(dirname ${dest_file})
    mkdir -p ${dest_dir}
    echo "[exe]:cp $src_file ${dest_dir}"
    cp $src_file ${dest_dir}
done

# third
mkdir -p ${butterfly_dir}/third
cp -rf src/third/* ${butterfly_dir}/third/

