#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

YEAR=${1:-invalid}
DAY=day${2:-invalid}

if [[ "${YEAR}${DAY}" =~ .*"invalid".* ]]
then
  echo "Specify a year and day"
  exit 1
fi

DIR="${SCRIPT_DIR}/${YEAR}/${DAY}"

echo "It's a new day, ${DIR}"
mkdir -pv "${DIR}"

INPUT_TXT="${DIR}/input.txt"
touch "${INPUT_TXT}"
echo "Created ${INPUT_TXT}"

PART_1="${DIR}/${DAY}a.py"
PART_2="${DIR}/${DAY}b.py"

for filename in "${PART_1}" "${PART_2}"
do
  if [ -e "${filename}" ]
  then
    echo "Cowardly refusing to create ${filename}"
    continue
  fi
cat >"${filename}" <<EOF
import dataclasses

import numpy as np

example = """\\

"""

def parse(lines: str):

    return

def solve(lines: str):
    puzzle = parse(lines)
    return


if __name__ == '__main__':
    solve(example)
    # solve(open('input.txt').read())
EOF
done

PYCHARM_EXEC=$(ls ~/$(ls -tr ~ | grep pycharm- | tail -n 1)/bin/pycharm.sh)
echo "${PYCHARM_EXEC}" "${PART_2}" "${INPUT_TXT}" "${PART_1}"
