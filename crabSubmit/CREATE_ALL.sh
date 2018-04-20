mapfile -t myArray < TableData.txt
afterfix=".py"
for i in "${myArray[@]}"
  do
    JobName=${i}
    ReplaceJobName=${JobName//\//\\/}
    Name1=$(cut -d/ -f2 <<<"${JobName}")
    Middle="_"
    Name2=$(cut -d/ -f3 <<<"${JobName}")
    echo $Name2
    NameToKeep=${Name2}
    SubVersion="rawSkim"
    Name=$Name1$Middle$NameToKeep$SubVersion
    echo $Name2
    file="$Name2"$afterfix

    sed "s/NAME/$Name2/g" "crabDataTemplate.py" > $file
    sed -i "s/INPUTDATASET/$ReplaceJobName/g" $file
    #crab submit -c $file
  done
#crabDataTemplate.py or crabMCTemplate.py
#TableData.txt or TableMC.txt
#Comment or uncomment crab submit -c $file
