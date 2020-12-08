#!/bin/bash
echo "Beginning time test one. ETA: A Few Minutes"
point_three="...,xx.,.xx.x.x,.xx..x.,xx...xx,.x.,..."
echo "Test case ${point_three}" > ./compare_solutions
echo "Test case ${point_three}" > ./compare_times
{ time ./Solitaire_Solver --astar --no_rotation $point_three 2> /dev/null >> ./compare_solutions ; }  &>> ./compare_times
echo "TEST WITH NAIVE BACKTRACK" >> ./compare_solutions
echo "TEST WITH NAIVE BACKTRACK" >> ./compare_times
{ time ./Solitaire_Solver --backtrack $point_three 2> /dev/null >> ./compare_solutions ; }  &>> ./compare_times
echo "" >> ./compare_solutions
echo "" >> ./compare_times

echo "Beginning time test two. ETA: An Hour or two"
eight_min=".xx,x.x,.....x.,..xxxxx,....x.x,.x.,xx."
echo "Test case ${eight_min}" >> ./compare_solutions
echo "Test case ${eight_min}" >> ./compare_times
{ time ./Solitaire_Solver --astar --no_rotation $eight_min 2> /dev/null >> ./compare_solutions ; }  &>> ./compare_times
echo "TEST WITH NAIVE BACKTRACK" >> ./compare_solutions
echo "TEST WITH NAIVE BACKTRACK" >> ./compare_times
{ time ./Solitaire_Solver --backtrack $eight_min 2> /dev/null >> ./compare_solutions ; }  &>> ./compare_times
echo "" >> ./compare_solutions
echo "" >> ./compare_times

echo "Beginning THE BIG TEST. ETA: SEVERAL HOURS"
big_boy="xxx,xxx,xxxxxxx,xxx.xxx,xxxxxxx,xxx,xxx"
echo "Test case ${big_boy}" >> ./compare_solutions
echo "Test case ${big_boy}" >> ./compare_times
{ time ./Solitaire_Solver --astar --no_rotation $big_boy 2> /dev/null >> ./compare_solutions ; }  &>> ./compare_times
echo "TEST WITH NAIVE BACKTRACK" >> ./compare_solutions
echo "TEST WITH NAIVE BACKTRACK" >> ./compare_times
{ time ./Solitaire_Solver --backtrack $big_boy 2> /dev/null >> ./compare_solutions ; }  &>> ./compare_times
echo "" >> ./compare_solutions
echo "" >> ./compare_times