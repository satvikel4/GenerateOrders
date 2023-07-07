#!/usr/bin/env bash

# This script is used to run RTS on iDFlakies

# The output is like 
# proj, module, test, # total tests of FIC, # total tests of Starts (selectMore=true), y/n, # total tests of Starts (selectMore=false), y/n, percentage  
# The default running time is 10 times.

# find . -d -name ".dtfixingtools*" | xargs rm -rf # remove all the dirty info

if [[ $1 == "" ]]; then
    echo "arg1 - full path to the test file (eg. input.csv)"
    exit
fi

currentDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PY=${currentDir}/p.py

input=$1
inputProj=$currentDir"/projects"

pom_modify_script=$currentDir/asm-pom-modify/modify-project.sh

IDFLAKIESOPTIONS="-Ddt.detector.roundsemantics.total=true -Ddetector.detector_type=random-class-method -Ddt.randomize.rounds=10 -Ddt.detector.original_order.all_must_pass=false"
MVNOPTIONS="-Ddependency-check.skip=true -Denforcer.skip=true -Drat.skip=true -Dmdep.analyze.skip=true -Dmaven.javadoc.skip=true -Dgpg.skip -Dlicense.skip=true -Dcheckstyle.skip=true"

ROOT=`(echo ~)`
repos=$currentDir"/repos"

if [[ ! -d $repos ]]; then
    mkdir -p $repos
fi

if [[ -d $repos"/testrunner" ]]; then
(
    cd $repos
    cd testrunner
    mvn install -DskipTests
)
fi

AGENT_JAR="${ROOT}/.m2/repository/edu/illinois/cs/testrunner-running/1.3-SNAPSHOT/testrunner-running-1.3-SNAPSHOT.jar"

while IFS= read -r line
do
  if [[ ${line} =~ ^\# ]]; then 
    continue
  fi

  slug=$(echo $line | cut -d',' -f1)
  fic_sha=$(echo $line | cut -d',' -f2)
  module=$(echo $line | cut -d',' -f3)
  
  fic_short_sha=${fic_sha: 0: 7}

  if [[ $module == "." ]]; then
    PL=""
    PL0=""
  else
    PL="-pl $module -am"
    PL0="-pl $module,dependencies-bom"
  fi
  
  PAIRSFILE=${inputProj}/${slug}/${module}/pairs-${fic_short_sha}
  TESTSFILE=${inputProj}/${slug}/${module}/tests-${fic_short_sha}
  LOGFILE=${inputProj}/${slug}/${module}/log-${fic_short_sha}
  STATSFILE=${inputProj}/${slug}/${module}/stats-${fic_short_sha}
  if [ ! -f ${PAIRSFILE} -o ! -f ${TESTSFILE} -o ! -f ${LOGFILE} -o ! -f ${STATSFILE} ]; then
  ( 
    if [[ ! -d ${inputProj}/${slug} ]]; then
        git clone "https://github.com/$slug" $inputProj/$slug
    fi 
    cd ${inputProj}/${slug}
    git stash
    git checkout -f $fic_sha
    mvn clean install -DskipTests ${PL} ${MVNOPTIONS} ${SKIPTESTSOPTIONS}
    $pom_modify_script $inputProj/$slug/${module} ${AGENT_JAR}
    cd ${module}
    mvn clean test ${MVNOPTIONS} | tee log-${fic_short_sha}
    grep "PAIR: " log-${fic_short_sha}| cut -d: -f2 | cut -d' ' -f2 > pairs-${fic_short_sha}
    grep "Test started: " log-${fic_short_sha} | cut -d: -f2 | cut -d' ' -f2 > tests-${fic_short_sha}
    python3 ${PY} pairs-${fic_short_sha} tests-${fic_short_sha} > stats-${fic_short_sha}
    mvn clean
  )
  fi
done < "$input"
# $pom_modify_script $inputProj/$slug
