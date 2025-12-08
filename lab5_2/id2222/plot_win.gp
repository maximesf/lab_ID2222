# Gnuplot script for Windows
set term png small size 1024,786
set output 'graph.png'

# Style definitions
set style line 1 lc rgb "#1a9850" lw 1.5
set style line 2 lc rgb "black" lw 1.5
set style line 3 lc rgb "brown" lw 1.5

# Layout configuration
set multiplot layout 3,1 title filename font ",14"
set yrange [0:]

# Graph 1: Edge Cut
set ylabel "Edge Cut" 
set xlabel "Rounds" 
plot filename using 1:2 with l ls 1 title "Edge-Cut"

# Graph 2: Swaps
set ylabel "Swaps" 
set xlabel "Rounds" 
plot filename using 1:3 with l ls 2 title "Swaps"

# Graph 3: Migrations
set ylabel "Migrations" 
set xlabel "Rounds" 
plot filename using 1:4 with l ls 3 title "Migrations"

unset multiplot