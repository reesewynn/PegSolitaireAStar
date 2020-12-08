#!/bin/bash
echo "Beginning time test one. ETA: 1 second"
point_three="...,xx.,.xx.x.x,.xx..x.,xx...xx,.x.,..."
echo "Test case ${point_three}" > ./rotation_solutions
echo "Test case ${point_three}" > ./rotation_times
echo "With Rotation's Removed" >> ./rotation_solutions
echo "With Rotation's Removed" >> ./rotation_times
{ time ./Solitaire_Solver --astar --no_rotation $point_three 2> /dev/null >> ./rotation_solutions ; }  &>> ./rotation_times
echo "" >> ./rotation_solutions
echo "" >> ./rotation_times
echo "Keeping Rotations" >> ./rotation_solutions
echo "Keepting Rotations" >> ./rotation_times
{ time ./Solitaire_Solver --astar $point_three 2> /dev/null >> ./rotation_solutions ; }  &>> ./rotation_times
echo "" >> ./rotation_solutions
echo "" >> ./rotation_times

echo "Beginning time test two. ETA: 20 minutes"
eight_min=".xx,x.x,.....x.,..xxxxx,....x.x,.x.,xx."
echo "Test case ${eight_min}" > ./rotation_solutions
echo "Test case ${eight_min}" > ./rotation_times
echo "With Rotation's Removed" >> ./rotation_solutions
echo "With Rotation's Removed" >> ./rotation_times
{ time ./Solitaire_Solver --astar --no_rotation $eight_min 2> /dev/null >> ./rotation_solutions ; }  &>> ./rotation_times
echo "" >> ./rotation_solutions
echo "" >> ./rotation_times
echo "Keeping Rotations" >> ./rotation_solutions
echo "Keepting Rotations" >> ./rotation_times
{ time ./Solitaire_Solver --astar $eight_min 2> /dev/null >> ./rotation_solutions ; }  &>> ./rotation_times
echo "" >> ./rotation_solutions
echo "" >> ./rotation_times

