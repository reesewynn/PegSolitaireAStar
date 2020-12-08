#!/bin/bash
echo "Beginning time test one. ETA: 0.4 seconds"
point_three="...,xx.,.xx.x.x,.xx..x.,xx...xx,.x.,..."
echo "Test case ${point_three}" > ./solutions
echo "Test case ${point_three}" > ./times
{ time ./Solitaire_Solver --astar --no_rotation $point_three 2> /dev/null >> ./solutions ; }  &>> ./times
echo "" >> ./solutions
echo "" >> ./times

echo "Beginning time test two. ETA: 8.5 minutes"
eight_min=".xx,x.x,.....x.,..xxxxx,....x.x,.x.,xx."
echo "Test case ${eight_min}" >> ./solutions
echo "Test case ${eight_min}" >> ./times
{ time ./Solitaire_Solver --astar --no_rotation $eight_min 2> /dev/null >> ./solutions ; }  &>> ./times
echo "" >> ./solutions
echo "" >> ./times

echo "Beginning time test two. ETA: 10 minutes"
eight_min_too="...,x..,xxxxx..,xxxxxx.,x.xxx..,.x.,.xx"
echo "Test case ${eight_min_too}" >> ./solutions
echo "Test case ${eight_min_too}" >> ./times
{ time ./Solitaire_Solver --astar --no_rotation $eight_min_too 2> /dev/null >> ./solutions ; }  &>> ./times
echo "" >> ./solutions
echo "" >> ./times
