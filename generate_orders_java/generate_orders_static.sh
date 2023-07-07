#!/usr/bin/env bash

# This script is used to only run iDFlakies

# The output is like 
# proj, module, test, # total tests of FIC, # total tests of Starts (selectMore=true), y/n, # total tests of Starts (selectMore=false), y/n, percentage  
# The default running time is 10 times.

# find . -d -name ".dtfixingtools*" | xargs rm -rf # remove all the dirty info

if [[ $1 == "" ]]; then
    echo "arg1 - full path to the test file (eg. input.csv)"
    exit
fi

currentDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

bash $currentDir/"collect_pairs.sh" $1

input=$1
inputProj=$currentDir"/projects"

inc_pom_modify_script=$currentDir/inc-pom-modify/modify-project.sh

IDFLAKIESOPTIONS="-Ddt.detector.roundsemantics.total=true -Ddetector.detector_type=tuscan -Ddt.randomize.rounds=0 -Ddt.detector.original_order.all_must_pass=false -Ddt.verify.rounds=0 -Ddt.detector.forceJUnit4=true"
MVNOPTIONS="-Ddependency-check.skip=true -Denforcer.skip=true -Drat.skip=true -Dmdep.analyze.skip=true -Dmaven.javadoc.skip=true -Dgpg.skip -Dlicense.skip=true -Dcheckstyle.skip=true -Dmaven.test.failure.ignore=true"
SKIPTESTSOPTIONS="-DskipTests=true"

if [[ ! -d $repos"/iDFlakies" ]]; then
(
    cd $repos
    cd iDFlakies
    mvn install -DskipTests
)
fi

while IFS= read -r line
do
  if [[ ${line} =~ ^\# ]]; then 
    continue
  fi

  slug=$(echo $line | cut -d',' -f1)
  module=$(echo $line | cut -d',' -f3)
  test=$(echo $line | cut -d',' -f4)
  fic_sha=$(echo $line | cut -d',' -f2)
  
  fic_short_sha=${fic_sha: 0: 7}

  if [[ $module == "." ]]; then
    PL=""
    PL0=""
  else
    PL="-pl $module -am"
    PL0="-pl $module,dependencies-bom"
  fi

  if [[ ! -d ${inputProj}/${slug}/${module}/.dtfixingtools_${fic_short_sha}_static ]]; then
    (
      cd ${inputProj}/${slug}
      find -name ".dtfixingtools" | xargs rm -rf
      git stash
      git checkout -f $fic_sha
      if [[ ${slug} == "doanduyhai/Achilles" ]]; then
        cp pom-bu.xml pom.xml
      fi
      initial_sha=`git rev-parse HEAD`
      mvn clean install ${PL} ${MVNOPTIONS} ${SKIPTESTSOPTIONS}
      $inc_pom_modify_script $inputProj/$slug
      cd ${inputProj}/${slug}
      if [[ ${slug} == "spring-projects/spring-data-envers" ]]; then
        cp pom-bu.xml pom.xml
      fi
      mvn idflakies:incdetect ${PL} ${MVNOPTIONS} ${IDFLAKIESOPTIONS} -Ddt.asm.module=${module} -Ddt.asm.pairsfile=pairs-${fic_short_sha} #  -X
      cd ${inputProj}/${slug}/${module}
      mv .dtfixingtools .dtfixingtools_${fic_short_sha}_static
      cd ${inputProj}/${slug}
      find -name ".dtfixingtools" | xargs rm -rf
    )
  fi
done < "$input"
# $pom_modify_script $inputProj/$slug
