#!/bin/bash

function parse {
        objdump -D read.o -M intel
        sc=$(objdump -D $1 | cut -c -28 | grep '_start' -A 9999999 |tail -n +2 | grep -Poz "[a-fA-F0-9]{2} {1}" | sed  -re  's/[ ]+$//g' -e 's/.*/ &/g' -e 's/ /\\x/g' -e 's/...$//g')
        echo $sc
        echo -ne $sc |wc -c
}

parse $1
