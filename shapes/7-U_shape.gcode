%
; U
; T1 D=0 CR=0 - ZMIN=0 - laser cutter
N10 G90
N11 G17
N12 G21
N13 G28 G91 Z0
N14 G90

; 2D Profile1
N15 T1
N16 M3
N17 G0 X57.37 Y32.114 F1000
N18 G0 Z15
N19 G1 Z0 S0
N20 G1 X282.509 S1
N21 G1 Y197.012
N22 G1 X282.516 Y197.037
N23 G1 X282.534 Y197.055
N24 G1 X282.559 Y197.062
N25 G1 X329.881
N26 G1 X329.906 Y197.055
N27 G1 X329.924 Y197.037
N28 G1 X329.931 Y197.012
N29 G1 Y1
N30 G1 X329.924 Y0.975
N31 G1 X329.906 Y0.957
N32 G1 X329.881 Y0.95
N33 G1 X1
N34 G1 X0.975 Y0.957
N35 G1 X0.957 Y0.975
N36 G1 X0.95 Y1
N37 G1 Y197.012
N38 G1 X0.957 Y197.037
N39 G1 X0.975 Y197.055
N40 G1 X1 Y197.062
N41 G1 X57.22
N42 G1 X57.245 Y197.055
N43 G1 X57.263 Y197.037
N44 G1 X57.27 Y197.012
N45 G1 Y32.114
N46 G1 X57.37
N47 G1 Z15 S0
N48 M5
N49 M5
N50 G28 G91 Z0
N51 G90
N52 G28 G91 X0 Y0
N53 G90
%
