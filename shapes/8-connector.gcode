%
; dick
; T1 D=0 CR=0 - ZMIN=0 - laser cutter
N10 G90
N11 G17
N12 G21
N13 G28 G91 Z0
N14 G90

; 2D Profile1
N15 T1
N16 M3
N17 G0 X0.965 Y162.483 F1000
N18 G0 Z15
N19 G1 Z0 S0
N20 G1 X0.954 Y162.499 S1
N21 G1 X0.95 Y162.518
N22 G1 Y221.663
N23 G2 X115.831 Y221.663 I57.44 J0
N24 G1 Y180.058
N25 G1 X411.829
N26 G2 X411.829 Y91.032 I0 J-44.513
N27 G1 X112.112
N28 G1 Y56.531
N29 G2 X0.95 Y56.531 I-55.581 J0
N30 G1 Y108.711
N31 G1 X0.954 Y108.73
N32 G1 X0.965 Y108.746
N33 G1 X27.832 Y135.545
N34 G1 X0.965 Y162.483
N35 G1 Z15 S0
N36 M5
N37 M5
N38 G28 G91 Z0
N39 G90
N40 G28 G91 X0 Y0
N41 G90
%