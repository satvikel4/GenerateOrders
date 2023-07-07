#! /bin/bash

if [[ $1 == "" ]]; then
  echo "No csv file passed"
  exit
fi

if [[ $2 == "" ]]; then
  echo "Specify method of order generation"
  exit
fi

while IFS="," read -r project sha module notneeded
do
    author=$(echo $project | cut -d "/" -f 1)
    repo=$(echo $project | cut -d "/" -f 2)
    short_sha=${sha: 0: 7}
    method=$2
    output_path=outputs/$method/${author}/${repo}/${module}/${short_sha}
    mkdir -p $output_path
    short_sha=${sha: 0: 7}
    javac -cp .:json-simple-1.1.1.jar GetTuscanOrders.java 
    java -cp .:json-simple-1.1.1.jar GetTuscanOrders $project $short_sha $module $method
done < $1
