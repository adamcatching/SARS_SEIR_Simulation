#!/bin/bash

seeds=( 12 23 29 34 39 42 52 63 68 98 99 109 111 117 123 126 132 133 146 167 177 202 232 247 251 261 275 279 320 339 355 365 380 384 390 393 414 415 421 424 445 461 468 514 515 519 526 529 536 541 544 554 559 573 574 583 589 608 612 616 618 619 628 629 630 638 639 673 693 697 712 717 720 722 724 730 741 752 761 764 766 767 805 824 830 835 868 871 881 889 899 900 910 913 920 946 1137 1425 2718 3038)
i = 0
per_asympt = 75 
for iteration in "${seeds[@]}"
do
qsub -cwd -l h_rt=100:00:00 -pe smp 1 -o ~/SARS_sim/data/test_run/output.txt -e ~/SARS_sim/data/test_run/error.txt mask_and_social_distance_sim.sh 25 $iteration $i 
echo "qsub -cwd -l h_rt=100:00:00 -pe smp 1 -o ~/SARS_sim/data/test_run/output.txt -e ~/SARS_sim/data/test_run/error.txt mask_single_sim.sh 25 $iteration $i"
i=$(expr $i + 1)
done
exit 0
