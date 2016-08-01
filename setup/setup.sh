inst_dir=$( cd $(dirname $BASH_SOURCE)/..; pwd -P )
export SLCOSMO_DIR=${inst_dir}
export PYTHONPATH=${inst_dir}/python:${PYTHONPATH}
