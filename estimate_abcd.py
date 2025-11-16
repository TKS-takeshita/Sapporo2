import re
import numpy as np

# ====== ログをここにコピペ ======
raw_data = r"""
t = 14.701, u = -0.03913, Enc1: theta=0.414 rad, omega=0.000 rad/s | Enc2: theta=1.170 rad, omega=0.047 rad/s
t = 14.801, u = 0.04035, Enc1: theta=0.414 rad, omega=0.000 rad/s | Enc2: theta=1.170 rad, omega=0.001 rad/s
t = 14.901, u = -0.04155, Enc1: theta=0.696 rad, omega=4.668 rad/s | Enc2: theta=1.181 rad, omega=1.438 rad/s
t = 15.001, u = 0.04274, Enc1: theta=0.386 rad, omega=-6.857 rad/s | Enc2: theta=1.251 rad, omega=0.211 rad/s
t = 15.101, u = -0.04397, Enc1: theta=0.438 rad, omega=4.755 rad/s | Enc2: theta=1.251 rad, omega=-0.058 rad/s
t = 15.202, u = 0.04516, Enc1: theta=0.271 rad, omega=-6.035 rad/s | Enc2: theta=1.256 rad, omega=-0.439 rad/s
t = 15.302, u = -0.04636, Enc1: theta=0.353 rad, omega=5.157 rad/s | Enc2: theta=1.251 rad, omega=0.000 rad/s
t = 15.402, u = 0.04758, Enc1: theta=0.181 rad, omega=-5.764 rad/s | Enc2: theta=1.254 rad, omega=-1.155 rad/s
t = 15.502, u = -0.04878, Enc1: theta=0.251 rad, omega=4.880 rad/s | Enc2: theta=1.251 rad, omega=-0.009 rad/s
t = 15.602, u = 0.04997, Enc1: theta=0.083 rad, omega=-5.778 rad/s | Enc2: theta=1.250 rad, omega=-0.295 rad/s
t = 15.702, u = -0.05120, Enc1: theta=0.159 rad, omega=5.044 rad/s | Enc2: theta=1.251 rad, omega=-0.077 rad/s
t = 15.802, u = 0.05239, Enc1: theta=-0.013 rad, omega=-5.764 rad/s | Enc2: theta=1.251 rad, omega=-0.007 rad/s
t = 15.902, u = -0.05362, Enc1: theta=0.063 rad, omega=4.702 rad/s | Enc2: theta=1.253 rad, omega=0.074 rad/s
t = 16.002, u = 0.05476, Enc1: theta=-0.111 rad, omega=-5.786 rad/s | Enc2: theta=1.251 rad, omega=-0.379 rad/s
t = 16.102, u = -0.05311, Enc1: theta=-0.036 rad, omega=4.723 rad/s | Enc2: theta=1.253 rad, omega=0.075 rad/s
t = 16.202, u = 0.05147, Enc1: theta=-0.204 rad, omega=-5.392 rad/s | Enc2: theta=1.251 rad, omega=-0.074 rad/s
t = 16.302, u = -0.04983, Enc1: theta=-0.131 rad, omega=5.300 rad/s | Enc2: theta=1.253 rad, omega=0.143 rad/s
t = 16.402, u = 0.04822, Enc1: theta=-0.295 rad, omega=-5.816 rad/s | Enc2: theta=1.251 rad, omega=0.015 rad/s
t = 16.502, u = -0.04655, Enc1: theta=-0.221 rad, omega=4.968 rad/s | Enc2: theta=1.251 rad, omega=-0.002 rad/s
t = 16.602, u = 0.04493, Enc1: theta=-0.384 rad, omega=-5.582 rad/s | Enc2: theta=1.251 rad, omega=-0.007 rad/s
t = 16.701, u = -0.04332, Enc1: theta=-0.677 rad, omega=-0.562 rad/s | Enc2: theta=1.251 rad, omega=-0.120 rad/s
t = 16.801, u = 0.04165, Enc1: theta=-0.686 rad, omega=0.289 rad/s | Enc2: theta=1.253 rad, omega=0.234 rad/s
t = 16.901, u = -0.04004, Enc1: theta=-0.687 rad, omega=-0.147 rad/s | Enc2: theta=1.251 rad, omega=-0.066 rad/s
t = 17.001, u = 0.03836, Enc1: theta=-0.686 rad, omega=0.153 rad/s | Enc2: theta=1.253 rad, omega=0.104 rad/s
t = 17.101, u = -0.03675, Enc1: theta=-0.686 rad, omega=0.210 rad/s | Enc2: theta=1.251 rad, omega=-0.266 rad/s
t = 17.201, u = 0.03508, Enc1: theta=-0.687 rad, omega=-0.083 rad/s | Enc2: theta=1.251 rad, omega=-0.108 rad/s
t = 17.301, u = -0.03346, Enc1: theta=-0.687 rad, omega=-0.050 rad/s | Enc2: theta=1.253 rad, omega=0.225 rad/s
t = 17.401, u = 0.03185, Enc1: theta=-0.686 rad, omega=0.199 rad/s | Enc2: theta=1.253 rad, omega=0.200 rad/s
t = 17.501, u = -0.03018, Enc1: theta=-0.687 rad, omega=-0.094 rad/s | Enc2: theta=1.251 rad, omega=-0.009 rad/s
t = 17.601, u = 0.02856, Enc1: theta=-0.686 rad, omega=0.245 rad/s | Enc2: theta=1.253 rad, omega=0.149 rad/s
t = 17.701, u = -0.02689, Enc1: theta=-0.687 rad, omega=-0.039 rad/s | Enc2: theta=1.251 rad, omega=-0.045 rad/s
t = 17.801, u = 0.02528, Enc1: theta=-0.686 rad, omega=0.108 rad/s | Enc2: theta=1.251 rad, omega=-0.100 rad/s
t = 17.901, u = -0.02360, Enc1: theta=-0.687 rad, omega=-0.015 rad/s | Enc2: theta=1.253 rad, omega=0.271 rad/s
t = 18.001, u = 0.02199, Enc1: theta=-0.687 rad, omega=-0.212 rad/s | Enc2: theta=1.251 rad, omega=-0.044 rad/s
t = 18.101, u = -0.02037, Enc1: theta=-0.687 rad, omega=-0.016 rad/s | Enc2: theta=1.253 rad, omega=0.170 rad/
t = 18.201, u = 0.01870, Enc1: theta=-0.687 rad, omega=-0.039 rad/s | Enc2: theta=1.253 rad, omega=0.133 rad/s
t = 18.301, u = -0.01709, Enc1: theta=-0.687 rad, omega=-0.060 rad/s | Enc2: theta=1.251 rad, omega=-0.113 rad/s
t = 18.401, u = 0.01541, Enc1: theta=-0.687 rad, omega=-0.171 rad/s | Enc2: theta=1.251 rad, omega=-0.071 rad/s
t = 18.500, u = -0.01380, Enc1: theta=-0.687 rad, omega=-0.002 rad/s | Enc2: theta=1.251 rad, omega=-0.086 rad/s
t = 18.600, u = 0.01218, Enc1: theta=-0.687 rad, omega=-0.075 rad/s | Enc2: theta=1.253 rad, omega=0.191 rad/s

# t = 0.099, u = 0.90888, Enc1: theta=1.181 rad, omega=-7.059 rad/s | Enc2: theta=1.797 rad, omega=0.267 rad/s
# t = 0.199, u = -0.54381, Enc1: theta=0.368 rad, omega=-5.722 rad/s | Enc2: theta=1.788 rad, omega=-0.000 rad/s
# t = 0.299, u = -0.57279, Enc1: theta=0.704 rad, omega=6.733 rad/s | Enc2: theta=1.796 rad, omega=0.041 rad/s
# t = 0.399, u = 0.89780, Enc1: theta=1.153 rad, omega=-2.098 rad/s | Enc2: theta=1.796 rad, omega=-0.155 rad/s
# t = 0.499, u = 0.01796, Enc1: theta=0.366 rad, omega=-7.136 rad/s | Enc2: theta=1.785 rad, omega=0.012 rad/s
# t = 0.599, u = -0.90890, Enc1: theta=0.133 rad, omega=5.554 rad/s | Enc2: theta=1.796 rad, omega=0.136 rad/s
# t = 0.699, u = 0.54373, Enc1: theta=0.794 rad, omega=4.049 rad/s | Enc2: theta=1.796 rad, omega=0.013 rad/s
# t = 0.799, u = 0.57288, Enc1: theta=0.348 rad, omega=-7.631 rad/s | Enc2: theta=1.794 rad, omega=-0.125 rad/s
# t = 0.899, u = -0.89776, Enc1: theta=-0.223 rad, omega=-0.591 rad/s | Enc2: theta=1.796 rad, omega=0.293 rad/s
# t = 0.999, u = -0.01807, Enc1: theta=0.388 rad, omega=5.716 rad/s | Enc2: theta=1.794 rad, omega=-0.107 rad/s
# t = 1.099, u = 0.90890, Enc1: theta=0.422 rad, omega=-7.203 rad/s | Enc2: theta=1.796 rad, omega=0.079 rad/s
# t = 1.199, u = -0.54381, Enc1: theta=-0.382 rad, omega=-5.222 rad/s | Enc2: theta=1.791 rad, omega=-0.034 rad/s
# t = 1.299, u = -0.57272, Enc1: theta=-0.062 rad, omega=6.471 rad/s | Enc2: theta=1.794 rad, omega=-0.066 rad/s
# t = 1.399, u = 0.89786, Enc1: theta=0.363 rad, omega=-2.309 rad/s | Enc2: theta=1.796 rad, omega=-0.071 rad/s
# t = 1.499, u = 0.01765, Enc1: theta=-0.416 rad, omega=-7.176 rad/s | Enc2: theta=1.793 rad, omega=-0.101 rad/s
# t = 1.599, u = -0.90878, Enc1: theta=-0.588 rad, omega=5.577 rad/s | Enc2: theta=1.796 rad, omega=-0.094 rad/s
# t = 1.699, u = 0.54415, Enc1: theta=0.084 rad, omega=4.141 rad/s | Enc2: theta=1.791 rad, omega=-0.276 rad/s
# t = 1.799, u = 0.57238, Enc1: theta=-0.352 rad, omega=-7.544 rad/s | Enc2: theta=1.786 rad, omega=-0.083 rad/s
# t = 1.899, u = -0.89800, Enc1: theta=-0.706 rad, omega=3.137 rad/s | Enc2: theta=1.797 rad, omega=0.347 rad/s
# t = 1.999, u = -0.01724, Enc1: theta=0.040 rad, omega=6.296 rad/s | Enc2: theta=1.790 rad, omega=-0.018 rad/s
# t = 2.099, u = 0.90872, Enc1: theta=0.101 rad, omega=-6.877 rad/s | Enc2: theta=1.793 rad, omega=-0.520 rad/s
# t = 2.199, u = -0.54415, Enc1: theta=-0.680 rad, omega=-4.267 rad/s | Enc2: theta=1.783 rad, omega=-0.248 rad/s
# t = 2.299, u = -0.57256, Enc1: theta=-0.694 rad, omega=0.220 rad/s | Enc2: theta=1.797 rad, omega=0.026 rad/s
# t = 2.399, u = 0.89786, Enc1: theta=-0.692 rad, omega=0.010 rad/s | Enc2: theta=1.796 rad, omega=-0.188 rad/s
# t = 2.499, u = 0.01788, Enc1: theta=-0.692 rad, omega=0.000 rad/s | Enc2: theta=1.796 rad, omega=-0.261 rad/s

# t = 1.299, u = -0.54874, Enc1: theta=0.173 rad, omega=-4.272 rad/s | Enc2: theta=2.412 rad, omega=-0.000 rad/s
# t = 1.399, u = -0.90709, Enc1: theta=0.518 rad, omega=8.217 rad/s | Enc2: theta=2.412 rad, omega=-0.005 rad/s
# t = 1.499, u = -0.01177, Enc1: theta=1.316 rad, omega=5.856 rad/s | Enc2: theta=2.412 rad, omega=-0.005 rad/s
# t = 1.599, u = 0.89982, Enc1: theta=1.583 rad, omega=-3.768 rad/s | Enc2: theta=2.414 rad, omega=0.050 rad/s
# t = 1.699, u = 0.56779, Enc1: theta=0.712 rad, omega=-8.084 rad/s | Enc2: theta=2.412 rad, omega=-0.000 rad/s
# t = 1.799, u = -0.54897, Enc1: theta=-0.045 rad, omega=-4.408 rad/s | Enc2: theta=2.414 rad, omega=0.232 rad/s
# t = 1.899, u = -0.90701, Enc1: theta=0.300 rad, omega=8.160 rad/s | Enc2: theta=2.412 rad, omega=0.057 rad/s
# t = 1.999, u = -0.01149, Enc1: theta=1.093 rad, omega=5.820 rad/s | Enc2: theta=2.412 rad, omega=0.179 rad/s
# t = 2.099, u = 0.89986, Enc1: theta=1.342 rad, omega=-4.192 rad/s | Enc2: theta=2.412 rad, omega=-0.017 rad/s
# t = 2.199, u = 0.56779, Enc1: theta=0.465 rad, omega=-8.393 rad/s | Enc2: theta=2.412 rad, omega=-0.000 rad/s
# t = 2.299, u = -0.54885, Enc1: theta=-0.298 rad, omega=-4.472 rad/s | Enc2: theta=2.411 rad, omega=-0.174 rad/s
# t = 2.399, u = -0.90709, Enc1: theta=0.056 rad, omega=8.175 rad/s | Enc2: theta=2.414 rad, omega=0.118 rad/s
# t = 2.499, u = -0.01192, Enc1: theta=0.857 rad, omega=6.007 rad/s | Enc2: theta=2.414 rad, omega=0.250 rad/s
# t = 2.599, u = 0.89972, Enc1: theta=1.098 rad, omega=-4.509 rad/s | Enc2: theta=2.414 rad, omega=0.133 rad/s
# t = 2.699, u = 0.56814, Enc1: theta=0.208 rad, omega=-8.443 rad/s | Enc2: theta=2.412 rad, omega=-0.185 rad/s
# t = 2.799, u = -0.54850, Enc1: theta=-0.502 rad, omega=-2.616 rad/s | Enc2: theta=2.374 rad, omega=-0.597 rad/s
# t = 2.899, u = -0.90722, Enc1: theta=-0.048 rad, omega=8.139 rad/s | Enc2: theta=2.313 rad, omega=0.022 rad/s
# t = 2.999, u = -0.01235, Enc1: theta=0.748 rad, omega=5.822 rad/s | Enc2: theta=2.313 rad, omega=-0.025 rad/s
# t = 3.099, u = 0.89958, Enc1: theta=1.018 rad, omega=-2.338 rad/s | Enc2: theta=2.313 rad, omega=-0.118 rad/s
# t = 3.199, u = 0.56848, Enc1: theta=0.937 rad, omega=-0.039 rad/s | Enc2: theta=2.313 rad, omega=0.130 rad/s
# t = 3.299, u = -0.54814, Enc1: theta=0.935 rad, omega=-0.003 rad/s | Enc2: theta=2.314 rad, omega=0.238 rad/s

# t = 0.099, u = 0.89974, Enc1: theta=2.486 rad, omega=-3.923 rad/s | Enc2: theta=3.167 rad, omega=-0.221 rad/s
# t = 0.199, u = 0.56801, Enc1: theta=1.695 rad, omega=-7.493 rad/s | Enc2: theta=3.167 rad, omega=0.100 rad/s
# t = 0.299, u = -0.54869, Enc1: theta=1.026 rad, omega=-4.108 rad/s | Enc2: theta=3.167 rad, omega=0.165 rad/s
# t = 0.399, u = -0.90713, Enc1: theta=1.376 rad, omega=7.658 rad/s | Enc2: theta=3.167 rad, omega=0.016 rad/s
# t = 0.499, u = -0.01197, Enc1: theta=2.184 rad, omega=6.347 rad/s | Enc2: theta=3.167 rad, omega=0.026 rad/s
# t = 0.599, u = 0.89973, Enc1: theta=2.468 rad, omega=-3.575 rad/s | Enc2: theta=3.169 rad, omega=0.026 rad/s
# t = 0.699, u = 0.56806, Enc1: theta=1.684 rad, omega=-7.447 rad/s | Enc2: theta=3.167 rad, omega=0.000 rad/s
# t = 0.799, u = -0.54863, Enc1: theta=1.008 rad, omega=-4.116 rad/s | Enc2: theta=3.167 rad, omega=-0.045 rad/s
# t = 0.899, u = -0.90715, Enc1: theta=1.360 rad, omega=7.597 rad/s | Enc2: theta=3.166 rad, omega=-0.295 rad/s
# t = 0.999, u = -0.01205, Enc1: theta=2.172 rad, omega=6.325 rad/s | Enc2: theta=3.167 rad, omega=0.003 rad/s
# t = 1.099, u = 0.89973, Enc1: theta=2.457 rad, omega=-3.511 rad/s | Enc2: theta=3.169 rad, omega=0.008 rad/s
# t = 1.199, u = 0.56801, Enc1: theta=1.667 rad, omega=-7.451 rad/s | Enc2: theta=3.167 rad, omega=-0.001 rad/s
# t = 1.299, u = -0.54874, Enc1: theta=0.983 rad, omega=-4.003 rad/s | Enc2: theta=3.169 rad, omega=0.307 rad/s
# t = 1.399, u = -0.90709, Enc1: theta=1.336 rad, omega=7.628 rad/s | Enc2: theta=3.167 rad, omega=0.065 rad/s
# t = 1.499, u = -0.01177, Enc1: theta=2.146 rad, omega=6.308 rad/s | Enc2: theta=3.167 rad, omega=0.103 rad/
# t = 1.599, u = 0.89982, Enc1: theta=2.433 rad, omega=-3.344 rad/s | Enc2: theta=3.169 rad, omega=0.007 rad/s
# t = 1.699, u = 0.56779, Enc1: theta=1.643 rad, omega=-7.388 rad/s | Enc2: theta=3.167 rad, omega=0.120 rad/s
# t = 1.799, u = -0.54897, Enc1: theta=0.955 rad, omega=-4.152 rad/s | Enc2: theta=3.167 rad, omega=-0.046 rad/s
# t = 1.899, u = -0.90701, Enc1: theta=1.308 rad, omega=7.519 rad/s | Enc2: theta=3.166 rad, omega=-0.227 rad/s
# t = 1.999, u = -0.01149, Enc1: theta=2.115 rad, omega=6.317 rad/s | Enc2: theta=3.167 rad, omega=0.017 rad/s
# t = 2.099, u = 0.89986, Enc1: theta=2.399 rad, omega=-3.520 rad/s | Enc2: theta=3.167 rad, omega=-0.322 rad/s
# t = 2.199, u = 0.56779, Enc1: theta=1.604 rad, omega=-7.326 rad/s | Enc2: theta=3.167 rad, omega=0.040 rad/s
# t = 2.299, u = -0.54885, Enc1: theta=0.905 rad, omega=-3.985 rad/s | Enc2: theta=3.167 rad, omega=0.000 rad/s
# t = 2.399, u = -0.90709, Enc1: theta=1.258 rad, omega=7.961 rad/s | Enc2: theta=3.167 rad, omega=0.015 rad/s
# t = 2.499, u = -0.01192, Enc1: theta=2.064 rad, omega=6.390 rad/s | Enc2: theta=3.167 rad, omega=0.017 rad/s
# t = 2.599, u = 0.89972, Enc1: theta=2.347 rad, omega=-3.713 rad/s | Enc2: theta=3.169 rad, omega=0.063 rad/s
# t = 2.699, u = 0.56814, Enc1: theta=1.548 rad, omega=-7.714 rad/s | Enc2: theta=3.166 rad, omega=-0.187 rad/s
# t = 2.799, u = -0.54850, Enc1: theta=0.843 rad, omega=-3.979 rad/s | Enc2: theta=3.167 rad, omega=0.060 rad/s
# t = 2.899, u = -0.90722, Enc1: theta=1.192 rad, omega=7.896 rad/s | Enc2: theta=3.167 rad, omega=0.047 rad/s
# t = 2.999, u = -0.01235, Enc1: theta=1.991 rad, omega=5.934 rad/s | Enc2: theta=3.167 rad, omega=0.000 rad/s
# t = 3.099, u = 0.89958, Enc1: theta=2.270 rad, omega=-3.540 rad/s | Enc2: theta=3.169 rad, omega=-0.072 rad/s
# t = 3.199, u = 0.56848, Enc1: theta=1.471 rad, omega=-7.635 rad/s | Enc2: theta=3.167 rad, omega=0.065 rad/s
# t = 3.299, u = -0.54814, Enc1: theta=0.762 rad, omega=-4.238 rad/s | Enc2: theta=3.167 rad, omega=-0.038 rad/s
# t = 3.399, u = -0.90735, Enc1: theta=1.109 rad, omega=7.643 rad/s | Enc2: theta=3.167 rad, omega=0.047 rad/s
# t = 3.499, u = -0.01279, Enc1: theta=1.908 rad, omega=6.122 rad/s | Enc2: theta=3.169 rad, omega=0.258 rad/s
# t = 3.599, u = 0.89944, Enc1: theta=2.184 rad, omega=-3.485 rad/s | Enc2: theta=3.167 rad, omega=-0.164 rad/s
# t = 3.699, u = 0.56883, Enc1: theta=1.368 rad, omega=-8.167 rad/s | Enc2: theta=3.167 rad, omega=0.092 rad/s
# t = 3.799, u = -0.54779, Enc1: theta=0.656 rad, omega=-4.454 rad/s | Enc2: theta=3.167 rad, omega=0.090 rad/s
# t = 3.899, u = -0.90748, Enc1: theta=1.004 rad, omega=7.763 rad/s | Enc2: theta=3.167 rad, omega=0.010 rad/s
# t = 3.999, u = -0.01322, Enc1: theta=1.796 rad, omega=6.142 rad/s | Enc2: theta=3.167 rad, omega=0.001 rad/s
# t = 4.099, u = 0.89930, Enc1: theta=2.066 rad, omega=-3.306 rad/s | Enc2: theta=3.169 rad, omega=0.149 rad/s
# t = 4.199, u = 0.56917, Enc1: theta=1.235 rad, omega=-7.924 rad/s | Enc2: theta=3.167 rad, omega=0.052 rad/s
# t = 4.299, u = -0.54744, Enc1: theta=0.511 rad, omega=-4.197 rad/s | Enc2: theta=3.167 rad, omega=-0.045 rad/s
# t = 4.399, u = -0.90760, Enc1: theta=0.866 rad, omega=7.961 rad/s | Enc2: theta=3.167 rad, omega=0.121 rad/s
# t = 4.499, u = -0.01365, Enc1: theta=1.656 rad, omega=5.866 rad/s | Enc2: theta=3.167 rad, omega=-0.127 rad/s
# t = 4.599, u = 0.89917, Enc1: theta=1.933 rad, omega=-3.634 rad/s | Enc2: theta=3.169 rad, omega=0.040 rad/s
# t = 4.699, u = 0.56952, Enc1: theta=1.100 rad, omega=-7.673 rad/s | Enc2: theta=3.167 rad, omega=-0.043 rad/s
# t = 4.799, u = -0.54709, Enc1: theta=0.383 rad, omega=-2.893 rad/s | Enc2: theta=3.139 rad, omega=-0.395 rad/s
# t = 4.899, u = -0.90773, Enc1: theta=0.762 rad, omega=8.360 rad/s | Enc2: theta=3.153 rad, omega=0.145 rad/s
# t = 4.999, u = -0.01408, Enc1: theta=1.549 rad, omega=6.031 rad/s | Enc2: theta=3.153 rad, omega=-0.004 rad/s
# t = 5.099, u = 0.89903, Enc1: theta=1.971 rad, omega=1.526 rad/s | Enc2: theta=3.155 rad, omega=0.069 rad/s
# t = 5.199, u = 0.56986, Enc1: theta=2.034 rad, omega=0.004 rad/s | Enc2: theta=3.153 rad, omega=-0.061 rad/s
# t = 5.299, u = -0.54673, Enc1: theta=2.034 rad, omega=0.026 rad/s | Enc2: theta=3.153 rad, omega=0.023 rad/s
# ENC2
# t = 1.599, u = -0.01464, Enc1: theta=0.055 rad, omega=-0.001 rad/s | Enc2: theta=1.909 rad, omega=-5.444 rad/s
# t = 1.699, u = 0.94989, Enc1: theta=0.055 rad, omega=0.000 rad/s | Enc2: theta=1.757 rad, omega=4.454 rad/s
# t = 1.799, u = 0.01450, Enc1: theta=0.055 rad, omega=-0.157 rad/s | Enc2: theta=2.503 rad, omega=6.711 rad/s
# t = 1.899, u = -0.94989, Enc1: theta=0.066 rad, omega=-0.765 rad/s | Enc2: theta=2.730 rad, omega=-5.588 rad/s
# t = 1.999, u = -0.01436, Enc1: theta=0.055 rad, omega=-0.001 rad/s | Enc2: theta=1.986 rad, omega=-5.268 rad/s
# t = 2.099, u = 0.94989, Enc1: theta=0.055 rad, omega=0.000 rad/s | Enc2: theta=1.826 rad, omega=4.720 rad/s
# t = 2.199, u = 0.01458, Enc1: theta=0.055 rad, omega=0.001 rad/s | Enc2: theta=2.584 rad, omega=6.592 rad/s
# t = 2.299, u = -0.94989, Enc1: theta=0.104 rad, omega=0.152 rad/s | Enc2: theta=2.727 rad, omega=-6.515 rad/s
# t = 2.399, u = -0.01479, Enc1: theta=0.098 rad, omega=0.059 rad/s | Enc2: theta=1.954 rad, omega=-5.700 rad/s
# t = 2.499, u = 0.94988, Enc1: theta=0.096 rad, omega=-0.001 rad/s | Enc2: theta=1.737 rad, omega=4.041 rad/s
# t = 2.599, u = 0.01501, Enc1: theta=0.098 rad, omega=0.214 rad/s | Enc2: theta=2.445 rad, omega=6.155 rad/s
# t = 2.699, u = -0.94988, Enc1: theta=0.096 rad, omega=-0.066 rad/s | Enc2: theta=2.690 rad, omega=-4.961 rad/s
# t = 2.799, u = -0.01522, Enc1: theta=0.093 rad, omega=-0.061 rad/s | Enc2: theta=1.957 rad, omega=-5.526 rad/s
# t = 2.899, u = 0.94988, Enc1: theta=0.093 rad, omega=0.000 rad/s | Enc2: theta=1.744 rad, omega=3.802 rad/s
# t = 2.999, u = 0.01544, Enc1: theta=0.093 rad, omega=0.130 rad/s | Enc2: theta=2.446 rad, omega=6.256 rad/s
# t = 3.099, u = -0.94987, Enc1: theta=0.092 rad, omega=-0.109 rad/s | Enc2: theta=2.693 rad, omega=-4.756 rad/s
# t = 3.199, u = -0.01566, Enc1: theta=0.092 rad, omega=0.000 rad/s | Enc2: theta=1.960 rad, omega=-5.241 rad/s
# t = 3.299, u = 0.94987, Enc1: theta=0.092 rad, omega=0.000 rad/s | Enc2: theta=1.747 rad, omega=3.791 rad/s
# t = 3.399, u = 0.01587, Enc1: theta=0.092 rad, omega=0.061 rad/s | Enc2: theta=2.454 rad, omega=6.408 rad/s
# t = 3.499, u = -0.94987, Enc1: theta=0.093 rad, omega=-0.081 rad/s | Enc2: theta=2.701 rad, omega=-4.897 rad/s
# t = 3.599, u = -0.01609, Enc1: theta=0.092 rad, omega=0.002 rad/s | Enc2: theta=1.966 rad, omega=-5.335 rad/s
# t = 3.699, u = 0.94986, Enc1: theta=0.092 rad, omega=0.000 rad/s | Enc2: theta=1.754 rad, omega=3.878 rad/s
# t = 3.799, u = 0.01631, Enc1: theta=0.092 rad, omega=0.007 rad/s | Enc2: theta=2.461 rad, omega=6.145 rad/s
# t = 3.899, u = -0.94986, Enc1: theta=0.095 rad, omega=0.069 rad/s | Enc2: theta=2.708 rad, omega=-5.059 rad/s
# t = 3.999, u = -0.01652, Enc1: theta=0.090 rad, omega=-0.004 rad/s | Enc2: theta=1.974 rad, omega=-5.412 rad/s
# t = 4.099, u = 0.94985, Enc1: theta=0.090 rad, omega=-0.000 rad/s | Enc2: theta=1.760 rad, omega=3.897 rad/s
# t = 4.199, u = 0.01674, Enc1: theta=0.090 rad, omega=0.022 rad/s | Enc2: theta=2.458 rad, omega=6.139 rad/s
# t = 4.299, u = -0.94985, Enc1: theta=0.090 rad, omega=0.118 rad/s | Enc2: theta=2.636 rad, omega=-5.706 rad/s
# t = 4.399, u = -0.01695, Enc1: theta=0.089 rad, omega=-0.000 rad/s | Enc2: theta=1.886 rad, omega=-5.815 rad/s
# t = 4.499, u = 0.94985, Enc1: theta=0.089 rad, omega=0.000 rad/s | Enc2: theta=1.668 rad, omega=3.984 rad/s
# t = 4.599, u = 0.01717, Enc1: theta=0.089 rad, omega=0.009 rad/s | Enc2: theta=2.368 rad, omega=6.040 rad/s
# t = 4.699, u = -0.94984, Enc1: theta=0.089 rad, omega=0.000 rad/s | Enc2: theta=2.612 rad, omega=-4.875 rad/s
# t = 4.799, u = -0.01739, Enc1: theta=0.087 rad, omega=-0.000 rad/s | Enc2: theta=1.894 rad, omega=-5.526 rad/s
# t = 4.899, u = 0.94984, Enc1: theta=0.087 rad, omega=-0.045 rad/s | Enc2: theta=1.679 rad, omega=4.048 rad/s
# t = 4.999, u = 0.01760, Enc1: theta=0.087 rad, omega=-0.003 rad/s | Enc2: theta=2.379 rad, omega=6.380 rad/s
# t = 5.099, u = -0.94983, Enc1: theta=0.087 rad, omega=-0.000 rad/s | Enc2: theta=2.623 rad, omega=-5.137 rad/s
# t = 5.199, u = -0.01782, Enc1: theta=0.087 rad, omega=0.000 rad/s | Enc2: theta=1.903 rad, omega=-5.709 rad/s
# t = 5.299, u = 0.94983, Enc1: theta=0.087 rad, omega=0.000 rad/s | Enc2: theta=1.688 rad, omega=3.940 rad/s
# t = 5.399, u = 0.01804, Enc1: theta=0.087 rad, omega=0.027 rad/s | Enc2: theta=2.386 rad, omega=6.059 rad/s
# t = 5.499, u = -0.94983, Enc1: theta=0.087 rad, omega=0.000 rad/s | Enc2: theta=2.632 rad, omega=-4.768 rad/s
# t = 5.599, u = -0.01825, Enc1: theta=0.086 rad, omega=-0.307 rad/s | Enc2: theta=1.911 rad, omega=-5.439 rad/s
# t = 5.699, u = 0.94982, Enc1: theta=0.087 rad, omega=0.000 rad/s | Enc2: theta=1.696 rad, omega=4.035 rad/s
# t = 5.799, u = 0.01847, Enc1: theta=0.087 rad, omega=0.095 rad/s | Enc2: theta=2.394 rad, omega=5.889 rad/s
# t = 5.899, u = -0.94982, Enc1: theta=0.087 rad, omega=0.001 rad/s | Enc2: theta=2.641 rad, omega=-4.892 rad/s
# t = 5.999, u = -0.01868, Enc1: theta=0.086 rad, omega=-0.125 rad/s | Enc2: theta=1.920 rad, omega=-5.553 rad/s
# t = 6.099, u = 0.94981, Enc1: theta=0.087 rad, omega=0.069 rad/s | Enc2: theta=1.759 rad, omega=4.672 rad/s
# t = 6.199, u = 0.01890, Enc1: theta=0.087 rad, omega=0.002 rad/s | Enc2: theta=2.503 rad, omega=6.842 rad/s
# t = 6.299, u = -0.94981, Enc1: theta=0.092 rad, omega=-0.678 rad/s | Enc2: theta=2.747 rad, omega=-5.474 rad/s
# t = 6.399, u = -0.01912, Enc1: theta=0.084 rad, omega=-0.013 rad/s | Enc2: theta=1.998 rad, omega=-5.437 rad/s
# t = 6.499, u = 0.94981, Enc1: theta=0.083 rad, omega=-0.307 rad/s | Enc2: theta=1.782 rad, omega=3.811 rad/s
# t = 6.599, u = 0.01933, Enc1: theta=0.083 rad, omega=-0.004 rad/s | Enc2: theta=2.500 rad, omega=6.259 rad/s
# t = 6.699, u = -0.94980, Enc1: theta=0.087 rad, omega=-1.115 rad/s | Enc2: theta=2.742 rad, omega=-5.432 rad/s
# t = 6.799, u = -0.01955, Enc1: theta=0.080 rad, omega=-0.297 rad/s | Enc2: theta=1.998 rad, omega=-5.279 rad/s
# t = 6.899, u = 0.94980, Enc1: theta=0.080 rad, omega=-0.025 rad/s | Enc2: theta=1.833 rad, omega=4.782 rad/s
# t = 6.999, u = 0.01976, Enc1: theta=0.080 rad, omega=-0.001 rad/s | Enc2: theta=2.593 rad, omega=6.900 rad/s
# t = 7.099, u = -0.94979, Enc1: theta=0.132 rad, omega=0.273 rad/s | Enc2: theta=2.799 rad, omega=-5.090 rad/s
# t = 7.199, u = -0.01998, Enc1: theta=0.126 rad, omega=-0.084 rad/s | Enc2: theta=2.027 rad, omega=-5.676 rad/s
# t = 7.299, u = 0.94979, Enc1: theta=0.126 rad, omega=0.064 rad/s | Enc2: theta=1.810 rad, omega=3.891 rad/s
# t = 7.399, u = 0.02020, Enc1: theta=0.126 rad, omega=0.013 rad/s | Enc2: theta=2.529 rad, omega=6.625 rad/s
# t = 7.499, u = -0.94978, Enc1: theta=0.129 rad, omega=-0.557 rad/s | Enc2: theta=2.776 rad, omega=-5.343 rad/s
# t = 7.599, u = -0.02041, Enc1: theta=0.121 rad, omega=-0.152 rad/s | Enc2: theta=2.023 rad, omega=-5.553 rad/s
# t = 7.699, u = 0.94978, Enc1: theta=0.121 rad, omega=0.146 rad/s | Enc2: theta=1.862 rad, omega=4.716 rad/s
# t = 7.799, u = 0.02063, Enc1: theta=0.121 rad, omega=0.090 rad/s | Enc2: theta=2.630 rad, omega=6.904 rad/s
# t = 7.899, u = -0.94977, Enc1: theta=0.210 rad, omega=1.226 rad/s | Enc2: theta=2.965 rad, omega=-0.694 rad/s
# t = 7.999, u = -0.02085, Enc1: theta=0.270 rad, omega=0.001 rad/s | Enc2: theta=2.972 rad, omega=-0.134 rad/s
# t = 8.099, u = 0.94978, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.974 rad, omega=0.268 rad/s
# t = 8.199, u = 0.01966, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.974 rad, omega=0.166 rad/s
# t = 8.299, u = -0.94981, Enc1: theta=0.270 rad, omega=-0.000 rad/s | Enc2: theta=2.974 rad, omega=0.082 rad/s
# t = 8.399, u = -0.01844, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.972 rad, omega=-0.188 rad/s
# t = 8.499, u = 0.94983, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.972 rad, omega=-0.036 rad/s
# t = 8.599, u = 0.01723, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.972 rad, omega=-0.036 rad/s
# t = 8.699, u = -0.94985, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.974 rad, omega=0.146 rad/s
# t = 8.799, u = -0.01604, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.972 rad, omega=-0.021 rad/s
# t = 8.899, u = 0.94987, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.974 rad, omega=0.202 rad/s
# t = 8.999, u = 0.01482, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.972 rad, omega=-0.096 rad/s
# t = 9.099, u = -0.94989, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.974 rad, omega=0.129 rad/s
# t = 9.199, u = -0.01361, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.972 rad, omega=-0.131 rad/s
# t = 9.299, u = 0.94991, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.972 rad, omega=-0.265 rad/s
# t = 9.399, u = 0.01242, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.974 rad, omega=0.230 rad/s
# t = 9.499, u = -0.94993, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.972 rad, omega=-0.114 rad/s
# t = 9.599, u = -0.01120, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.974 rad, omega=0.235 rad/s
# t = 9.699, u = 0.94994, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.974 rad, omega=0.241 rad/s
# t = 9.799, u = 0.00999, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.974 rad, omega=0.170 rad/s
# t = 9.899, u = -0.94995, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.974 rad, omega=0.124 rad/s
# t = 9.999, u = -0.00878, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.974 rad, omega=0.294 rad/s
# t = 10.099, u = 0.94996, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.972 rad, omega=-0.167 rad/s
# t = 10.199, u = 0.00758, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.972 rad, omega=-0.065 rad/s
# t = 10.300, u = -0.94997, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.974 rad, omega=0.159 rad/s
# t = 10.400, u = -0.00637, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.974 rad, omega=0.158 rad/s
# t = 10.500, u = 0.94998, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.972 rad, omega=-0.021 rad/s
# t = 10.600, u = 0.00516, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.974 rad, omega=0.193 rad/s
# t = 10.700, u = -0.94999, Enc1: theta=0.270 rad, omega=0.000 rad/s | Enc2: theta=2.974 rad, omega=0.140 rad/s

# t = 1.599, u = -0.01464, Enc1: theta=0.055 rad, omega=-0.001 rad/s | Enc2: theta=1.909 rad, omega=-5.444 rad/s
# t = 1.699, u = 0.94989, Enc1: theta=0.055 rad, omega=0.000 rad/s | Enc2: theta=1.757 rad, omega=4.454 rad/s
# t = 1.799, u = 0.01450, Enc1: theta=0.055 rad, omega=-0.157 rad/s | Enc2: theta=2.503 rad, omega=6.711 rad/s
# t = 1.899, u = -0.94989, Enc1: theta=0.066 rad, omega=-0.765 rad/s | Enc2: theta=2.730 rad, omega=-5.588 rad/s
# t = 1.999, u = -0.01436, Enc1: theta=0.055 rad, omega=-0.001 rad/s | Enc2: theta=1.986 rad, omega=-5.268 rad/s
# t = 2.099, u = 0.94989, Enc1: theta=0.055 rad, omega=0.000 rad/s | Enc2: theta=1.826 rad, omega=4.720 rad/s
# t = 2.199, u = 0.01458, Enc1: theta=0.055 rad, omega=0.001 rad/s | Enc2: theta=2.584 rad, omega=6.592 rad/s
# t = 2.299, u = -0.94989, Enc1: theta=0.104 rad, omega=0.152 rad/s | Enc2: theta=2.727 rad, omega=-6.515 rad/s
# t = 2.399, u = -0.01479, Enc1: theta=0.098 rad, omega=0.059 rad/s | Enc2: theta=1.954 rad, omega=-5.700 rad/s
# t = 2.499, u = 0.94988, Enc1: theta=0.096 rad, omega=-0.001 rad/s | Enc2: theta=1.737 rad, omega=4.041 rad/s
# t = 2.599, u = 0.01501, Enc1: theta=0.098 rad, omega=0.214 rad/s | Enc2: theta=2.445 rad, omega=6.155 rad/s
# t = 2.699, u = -0.94988, Enc1: theta=0.096 rad, omega=-0.066 rad/s | Enc2: theta=2.690 rad, omega=-4.961 rad/s
# t = 2.799, u = -0.01522, Enc1: theta=0.093 rad, omega=-0.061 rad/s | Enc2: theta=1.957 rad, omega=-5.526 rad/s
# t = 2.899, u = 0.94988, Enc1: theta=0.093 rad, omega=0.000 rad/s | Enc2: theta=1.744 rad, omega=3.802 rad/s
# t = 2.999, u = 0.01544, Enc1: theta=0.093 rad, omega=0.130 rad/s | Enc2: theta=2.446 rad, omega=6.256 rad/s
# t = 3.099, u = -0.94987, Enc1: theta=0.092 rad, omega=-0.109 rad/s | Enc2: theta=2.693 rad, omega=-4.756 rad/s
# t = 3.199, u = -0.01566, Enc1: theta=0.092 rad, omega=0.000 rad/s | Enc2: theta=1.960 rad, omega=-5.241 rad/s
# t = 3.299, u = 0.94987, Enc1: theta=0.092 rad, omega=0.000 rad/s | Enc2: theta=1.747 rad, omega=3.791 rad/s
# t = 3.399, u = 0.01587, Enc1: theta=0.092 rad, omega=0.061 rad/s | Enc2: theta=2.454 rad, omega=6.408 rad/s
# t = 3.499, u = -0.94987, Enc1: theta=0.093 rad, omega=-0.081 rad/s | Enc2: theta=2.701 rad, omega=-4.897 rad/s
# t = 3.599, u = -0.01609, Enc1: theta=0.092 rad, omega=0.002 rad/s | Enc2: theta=1.966 rad, omega=-5.335 rad/s
# t = 3.699, u = 0.94986, Enc1: theta=0.092 rad, omega=0.000 rad/s | Enc2: theta=1.754 rad, omega=3.878 rad/s
# t = 3.799, u = 0.01631, Enc1: theta=0.092 rad, omega=0.007 rad/s | Enc2: theta=2.461 rad, omega=6.145 rad/s
# t = 3.899, u = -0.94986, Enc1: theta=0.095 rad, omega=0.069 rad/s | Enc2: theta=2.708 rad, omega=-5.059 rad/s
# t = 3.999, u = -0.01652, Enc1: theta=0.090 rad, omega=-0.004 rad/s | Enc2: theta=1.974 rad, omega=-5.412 rad/s
# t = 4.099, u = 0.94985, Enc1: theta=0.090 rad, omega=-0.000 rad/s | Enc2: theta=1.760 rad, omega=3.897 rad/s
# t = 4.199, u = 0.01674, Enc1: theta=0.090 rad, omega=0.022 rad/s | Enc2: theta=2.458 rad, omega=6.139 rad/s
# t = 4.299, u = -0.94985, Enc1: theta=0.090 rad, omega=0.118 rad/s | Enc2: theta=2.636 rad, omega=-5.706 rad/s
# t = 4.399, u = -0.01695, Enc1: theta=0.089 rad, omega=-0.000 rad/s | Enc2: theta=1.886 rad, omega=-5.815 rad/s
# t = 4.499, u = 0.94985, Enc1: theta=0.089 rad, omega=0.000 rad/s | Enc2: theta=1.668 rad, omega=3.984 rad/s
# t = 4.599, u = 0.01717, Enc1: theta=0.089 rad, omega=0.009 rad/s | Enc2: theta=2.368 rad, omega=6.040 rad/s
# t = 4.699, u = -0.94984, Enc1: theta=0.089 rad, omega=0.000 rad/s | Enc2: theta=2.612 rad, omega=-4.875 rad/s
# t = 4.799, u = -0.01739, Enc1: theta=0.087 rad, omega=-0.000 rad/s | Enc2: theta=1.894 rad, omega=-5.526 rad/s
# t = 4.899, u = 0.94984, Enc1: theta=0.087 rad, omega=-0.045 rad/s | Enc2: theta=1.679 rad, omega=4.048 rad/s
# t = 4.999, u = 0.01760, Enc1: theta=0.087 rad, omega=-0.003 rad/s | Enc2: theta=2.379 rad, omega=6.380 rad/s
# t = 5.099, u = -0.94983, Enc1: theta=0.087 rad, omega=-0.000 rad/s | Enc2: theta=2.623 rad, omega=-5.137 rad/s
# t = 5.199, u = -0.01782, Enc1: theta=0.087 rad, omega=0.000 rad/s | Enc2: theta=1.903 rad, omega=-5.709 rad/s
# t = 5.299, u = 0.94983, Enc1: theta=0.087 rad, omega=0.000 rad/s | Enc2: theta=1.688 rad, omega=3.940 rad/s
# t = 5.399, u = 0.01804, Enc1: theta=0.087 rad, omega=0.027 rad/s | Enc2: theta=2.386 rad, omega=6.059 rad/s
# t = 5.499, u = -0.94983, Enc1: theta=0.087 rad, omega=0.000 rad/s | Enc2: theta=2.632 rad, omega=-4.768 rad/s
# t = 5.599, u = -0.01825, Enc1: theta=0.086 rad, omega=-0.307 rad/s | Enc2: theta=1.911 rad, omega=-5.439 rad/s
# t = 5.699, u = 0.94982, Enc1: theta=0.087 rad, omega=0.000 rad/s | Enc2: theta=1.696 rad, omega=4.035 rad/s
# t = 5.799, u = 0.01847, Enc1: theta=0.087 rad, omega=0.095 rad/s | Enc2: theta=2.394 rad, omega=5.889 rad/s
# t = 5.899, u = -0.94982, Enc1: theta=0.087 rad, omega=0.001 rad/s | Enc2: theta=2.641 rad, omega=-4.892 rad/s
# t = 5.999, u = -0.01868, Enc1: theta=0.086 rad, omega=-0.125 rad/s | Enc2: theta=1.920 rad, omega=-5.553 rad/s
# t = 6.099, u = 0.94981, Enc1: theta=0.087 rad, omega=0.069 rad/s | Enc2: theta=1.759 rad, omega=4.672 rad/s
# t = 6.199, u = 0.01890, Enc1: theta=0.087 rad, omega=0.002 rad/s | Enc2: theta=2.503 rad, omega=6.842 rad/s
# t = 6.299, u = -0.94981, Enc1: theta=0.092 rad, omega=-0.678 rad/s | Enc2: theta=2.747 rad, omega=-5.474 rad/s
# t = 6.399, u = -0.01912, Enc1: theta=0.084 rad, omega=-0.013 rad/s | Enc2: theta=1.998 rad, omega=-5.437 rad/s
# t = 6.499, u = 0.94981, Enc1: theta=0.083 rad, omega=-0.307 rad/s | Enc2: theta=1.782 rad, omega=3.811 rad/s
# t = 6.599, u = 0.01933, Enc1: theta=0.083 rad, omega=-0.004 rad/s | Enc2: theta=2.500 rad, omega=6.259 rad/s
# t = 6.699, u = -0.94980, Enc1: theta=0.087 rad, omega=-1.115 rad/s | Enc2: theta=2.742 rad, omega=-5.432 rad/s
# t = 6.799, u = -0.01955, Enc1: theta=0.080 rad, omega=-0.297 rad/s | Enc2: theta=1.998 rad, omega=-5.279 rad/s
# t = 6.899, u = 0.94980, Enc1: theta=0.080 rad, omega=-0.025 rad/s | Enc2: theta=1.833 rad, omega=4.782 rad/s
# t = 6.999, u = 0.01976, Enc1: theta=0.080 rad, omega=-0.001 rad/s | Enc2: theta=2.593 rad, omega=6.900 rad/s
# t = 7.099, u = -0.94979, Enc1: theta=0.132 rad, omega=0.273 rad/s | Enc2: theta=2.799 rad, omega=-5.090 rad/s
# t = 7.199, u = -0.01998, Enc1: theta=0.126 rad, omega=-0.084 rad/s | Enc2: theta=2.027 rad, omega=-5.676 rad/s
# t = 7.299, u = 0.94979, Enc1: theta=0.126 rad, omega=0.064 rad/s | Enc2: theta=1.810 rad, omega=3.891 rad/s
# t = 7.399, u = 0.02020, Enc1: theta=0.126 rad, omega=0.013 rad/s | Enc2: theta=2.529 rad, omega=6.625 rad/s
# t = 7.499, u = -0.94978, Enc1: theta=0.129 rad, omega=-0.557 rad/s | Enc2: theta=2.776 rad, omega=-5.343 rad/s
# t = 7.599, u = -0.02041, Enc1: theta=0.121 rad, omega=-0.152 rad/s | Enc2: theta=2.023 rad, omega=-5.553 rad/s
# t = 7.699, u = 0.94978, Enc1: theta=0.121 rad, omega=0.146 rad/s | Enc2: theta=1.862 rad, omega=4.716 rad/s
# t = 7.799, u = 0.02063, Enc1: theta=0.121 rad, omega=0.090 rad/s | Enc2: theta=2.630 rad, omega=6.904 rad/s

# t = 0.099, u = 0.78066, Enc1: theta=1.615 rad, omega=0.054 rad/s | Enc2: theta=2.357 rad, omega=6.477 rad/s
# t = 0.199, u = -0.89683, Enc1: theta=1.624 rad, omega=0.201 rad/s | Enc2: theta=2.942 rad, omega=-0.971 rad/s
# t = 0.299, u = 0.27362, Enc1: theta=1.620 rad, omega=-0.377 rad/s | Enc2: theta=2.273 rad, omega=-5.058 rad/s
# t = 0.399, u = 0.57519, Enc1: theta=1.609 rad, omega=0.005 rad/s | Enc2: theta=2.432 rad, omega=6.708 rad/s
# t = 0.499, u = -0.94977, Enc1: theta=1.623 rad, omega=0.025 rad/s | Enc2: theta=2.822 rad, omega=-4.167 rad/s
# t = 0.599, u = 0.54129, Enc1: theta=1.621 rad, omega=-0.064 rad/s | Enc2: theta=2.136 rad, omega=-4.455 rad/s
# t = 0.699, u = 0.31347, Enc1: theta=1.609 rad, omega=0.014 rad/s | Enc2: theta=2.491 rad, omega=6.272 rad/s
# t = 0.799, u = -0.90978, Enc1: theta=1.617 rad, omega=0.024 rad/s | Enc2: theta=2.715 rad, omega=-6.032 rad/s
# t = 0.899, u = 0.75600, Enc1: theta=1.609 rad, omega=-0.419 rad/s | Enc2: theta=2.095 rad, omega=-2.179 rad/s
# t = 0.999, u = 0.02108, Enc1: theta=1.610 rad, omega=0.129 rad/s | Enc2: theta=2.629 rad, omega=6.246 rad/s
# t = 1.099, u = -0.78071, Enc1: theta=1.617 rad, omega=0.011 rad/s | Enc2: theta=2.675 rad, omega=-6.944 rad/s
# t = 1.199, u = 0.89683, Enc1: theta=1.604 rad, omega=-0.328 rad/s | Enc2: theta=2.184 rad, omega=0.378 rad/s
# t = 1.299, u = -0.27372, Enc1: theta=1.609 rad, omega=-0.000 rad/s | Enc2: theta=2.888 rad, omega=6.877 rad/s
# t = 1.399, u = -0.57501, Enc1: theta=1.610 rad, omega=0.287 rad/s | Enc2: theta=2.739 rad, omega=-6.818 rad/s
# t = 1.499, u = 0.94978, Enc1: theta=1.604 rad, omega=0.034 rad/s | Enc2: theta=2.376 rad, omega=3.554 rad/s
# t = 1.599, u = -0.54168, Enc1: theta=1.609 rad, omega=0.000 rad/s | Enc2: theta=3.202 rad, omega=6.875 rad/s
# t = 1.699, u = -0.31290, Enc1: theta=1.606 rad, omega=-0.005 rad/s | Enc2: theta=2.850 rad, omega=-6.411 rad/s
# t = 1.799, u = 0.90957, Enc1: theta=1.606 rad, omega=0.061 rad/s | Enc2: theta=2.664 rad, omega=6.286 rad/s
# t = 1.899, u = -0.75652, Enc1: theta=1.604 rad, omega=-0.087 rad/s | Enc2: theta=3.524 rad, omega=3.913 rad/s
# t = 1.999, u = -0.02011, Enc1: theta=1.606 rad, omega=0.000 rad/s | Enc2: theta=3.001 rad, omega=-6.608 rad/s
# t = 2.099, u = 0.78030, Enc1: theta=1.607 rad, omega=0.022 rad/s | Enc2: theta=3.047 rad, omega=9.233 rad/s
# t = 2.199, u = -0.89699, Enc1: theta=1.606 rad, omega=0.155 rad/s | Enc2: theta=3.805 rad, omega=2.052 rad/s
# t = 2.299, u = 0.27394, Enc1: theta=1.607 rad, omega=0.268 rad/s | Enc2: theta=3.136 rad, omega=-6.036 rad/s
# t = 2.399, u = 0.57502, Enc1: theta=1.609 rad, omega=0.127 rad/s | Enc2: theta=3.405 rad, omega=8.058 rad/s
# t = 2.499, u = -0.94977, Enc1: theta=1.607 rad, omega=-0.000 rad/s | Enc2: theta=3.940 rad, omega=-4.471 rad/s
# t = 2.599, u = 0.54126, Enc1: theta=1.607 rad, omega=0.051 rad/s | Enc2: theta=3.001 rad, omega=-6.040 rad/s
# t = 2.699, u = 0.31362, Enc1: theta=1.607 rad, omega=-0.109 rad/s | Enc2: theta=3.394 rad, omega=6.811 rad/s
# t = 2.799, u = -0.90986, Enc1: theta=1.606 rad, omega=0.002 rad/s | Enc2: theta=3.956 rad, omega=1.358 rad/s

# t = 0.099, u = 0.02984, Enc1: theta=2.445 rad, omega=0.080 rad/s | Enc2: theta=3.100 rad, omega=7.733 rad/s
# t = 0.199, u = -0.02983, Enc1: theta=2.448 rad, omega=-0.007 rad/s | Enc2: theta=3.037 rad, omega=-5.957 rad/s
# t = 0.299, u = 0.02985, Enc1: theta=2.439 rad, omega=1.317 rad/s | Enc2: theta=3.189 rad, omega=6.636 rad/s
# t = 0.399, u = -0.02989, Enc1: theta=2.448 rad, omega=-0.001 rad/s | Enc2: theta=3.097 rad, omega=-5.994 rad/s
# t = 0.499, u = 0.02993, Enc1: theta=2.433 rad, omega=0.386 rad/s | Enc2: theta=3.250 rad, omega=8.199 rad/s
# t = 0.599, u = -0.02996, Enc1: theta=2.451 rad, omega=-0.009 rad/s | Enc2: theta=3.159 rad, omega=-6.040 rad/s
# t = 0.699, u = 0.03000, Enc1: theta=2.448 rad, omega=1.633 rad/s | Enc2: theta=3.308 rad, omega=6.489 rad/s
# t = 0.799, u = -0.03004, Enc1: theta=2.450 rad, omega=-0.001 rad/s | Enc2: theta=3.218 rad, omega=-6.162 rad/s
# t = 0.899, u = 0.03008, Enc1: theta=2.442 rad, omega=0.784 rad/s | Enc2: theta=3.360 rad, omega=6.391 rad/s
# t = 0.999, u = -0.03012, Enc1: theta=2.443 rad, omega=-0.630 rad/s | Enc2: theta=3.274 rad, omega=-6.084 rad/s
# t = 1.099, u = 0.02998, Enc1: theta=2.445 rad, omega=0.928 rad/s | Enc2: theta=3.422 rad, omega=6.617 rad/s
# t = 1.199, u = -0.02984, Enc1: theta=2.448 rad, omega=-0.016 rad/s | Enc2: theta=3.334 rad, omega=-6.395 rad/s
# t = 1.299, u = 0.02970, Enc1: theta=2.446 rad, omega=1.281 rad/s | Enc2: theta=3.486 rad, omega=7.429 rad/s
# t = 1.399, u = -0.02956, Enc1: theta=2.450 rad, omega=0.000 rad/s | Enc2: theta=3.391 rad, omega=-6.995 rad/s
# t = 1.499, u = 0.02942, Enc1: theta=2.442 rad, omega=1.066 rad/s | Enc2: theta=3.552 rad, omega=6.874 rad/s
# t = 1.599, u = -0.02928, Enc1: theta=2.450 rad, omega=-0.025 rad/s | Enc2: theta=3.454 rad, omega=-6.746 rad/s
# t = 1.699, u = 0.02914, Enc1: theta=2.437 rad, omega=0.593 rad/s | Enc2: theta=3.618 rad, omega=7.588 rad/s
# t = 1.799, u = -0.02900, Enc1: theta=2.450 rad, omega=0.039 rad/s | Enc2: theta=3.515 rad, omega=-6.645 rad/s
# t = 1.899, u = 0.02886, Enc1: theta=2.439 rad, omega=0.936 rad/s | Enc2: theta=3.678 rad, omega=7.462 rad/s
# t = 1.999, u = -0.02872, Enc1: theta=2.448 rad, omega=-0.050 rad/s | Enc2: theta=3.578 rad, omega=-6.712 rad/s
# t = 2.099, u = 0.02893, Enc1: theta=2.442 rad, omega=0.922 rad/s | Enc2: theta=3.738 rad, omega=7.194 rad/s
# t = 2.199, u = -0.02915, Enc1: theta=2.448 rad, omega=-0.018 rad/s | Enc2: theta=3.629 rad, omega=-6.951 rad/s
# t = 2.299, u = 0.02936, Enc1: theta=2.443 rad, omega=1.086 rad/s | Enc2: theta=3.782 rad, omega=7.031 rad/s
# t = 2.399, u = -0.02958, Enc1: theta=2.448 rad, omega=0.000 rad/s | Enc2: theta=3.653 rad, omega=-6.831 rad/s
# t = 2.499, u = 0.02980, Enc1: theta=2.443 rad, omega=0.970 rad/s | Enc2: theta=3.791 rad, omega=6.706 rad/s
# t = 2.599, u = -0.03001, Enc1: theta=2.448 rad, omega=-0.009 rad/s | Enc2: theta=3.650 rad, omega=-7.101 rad/s
# t = 2.699, u = 0.03023, Enc1: theta=2.442 rad, omega=0.974 rad/s | Enc2: theta=3.788 rad, omega=7.127 rad/s
# t = 2.799, u = -0.03045, Enc1: theta=2.448 rad, omega=-0.013 rad/s | Enc2: theta=3.653 rad, omega=-7.024 rad/s
# t = 2.899, u = 0.03066, Enc1: theta=2.443 rad, omega=1.135 rad/s | Enc2: theta=3.787 rad, omega=6.664 rad/s
# t = 2.999, u = -0.03088, Enc1: theta=2.448 rad, omega=0.159 rad/s | Enc2: theta=4.008 rad, omega=-0.555 rad/s
"""

# 空行ごとにブロック分割（位置条件ごとに分けてある前提）
blocks = [b for b in raw_data.strip().split("\n\n") if b.strip()]
print(f"検出したデータセット数: {len(blocks)}")

# Enc2 の値（theta, omega）を使う想定
# Enc1 を使いたければ group(3) を使うように少し書き換えればOK
# line_pattern = re.compile(
#     r"t\s*=\s*([0-9.]+)\s*,\s*"
#     r"u\s*=\s*([-0-9.]+).*?"
#     r"Enc2:\s*theta=([-0-9.]+)\s*rad,\s*omega=([-0-9.]+)\s*rad/s"
# )
# Enc1の場合
line_pattern = re.compile(
    r"t\s*=\s*([0-9.]+)\s*,\s*"
    r"u\s*=\s*([-0-9.]+).*?"
    r"Enc1:\s*theta=([-0-9.]+)\s*rad,\s*omega=([-0-9.]+)\s*rad/s"
)

def parse_block(block_text):
    t_list, u_list, theta_list, omega_list = [], [], [], []
    for line in block_text.splitlines():
        m = line_pattern.search(line)
        if not m:
            continue
        t = float(m.group(1))
        u = float(m.group(2))
        theta2 = float(m.group(3))
        omega2 = float(m.group(4))

        t_list.append(t)
        u_list.append(u)
        theta_list.append(theta2)
        omega_list.append(omega2)

    if len(t_list) < 3:
        return None
    return (np.array(t_list),
            np.array(u_list),
            np.array(theta_list),
            np.array(omega_list))

all_X = []
all_y = []

for i, block in enumerate(blocks):
    parsed = parse_block(block)
    if parsed is None:
        print(f"[ブロック {i}] データ不足でスキップ")
        continue

    t, u, theta, omega = parsed

    # 微分近似 (中央差分っぽく: 中点に合わせる)
    dt = np.diff(t)
    domega = np.diff(omega)
    omega_dot = domega / dt

    # t[1:], u[1:], theta[1:], omega[1:] を対応させる
    u_mid     = u[1:]
    theta_mid = theta[1:]
    omega_mid = omega[1:]

    sign_omega = np.sign(omega_mid)
    sin_theta  = np.sin(theta_mid)
    ones       = np.ones_like(u_mid)

    # モデル: ω_dot = a*u + b*ω + c*sign(ω) + d*sin(θ)
    X = np.column_stack([u_mid, omega_mid, sign_omega, sin_theta])
    y = omega_dot

    # ごく小さい |omega| は sign がうるさいので除外しても良い
    mask = np.abs(omega_mid) > 1e-3
    X = X[mask]
    y = y[mask]

    if len(y) < 4:
        print(f"[ブロック {i}] サンプル不足でスキップ")
        continue

    params, residuals, rank, s = np.linalg.lstsq(X, y, rcond=None)
    a, b, c, d = params
    print(f"[ブロック {i}] a={a:.4e}, b={b:.4e}, c={c:.4e}, d={d:.4e}, 残差={residuals}")

    all_X.append(X)
    all_y.append(y)

# 全データをまとめてグローバル a,b,c,d を同定
if all_X:
    all_X = np.vstack(all_X)
    all_y = np.concatenate(all_y)

    global_params, global_res, rank, s = np.linalg.lstsq(all_X, all_y, rcond=None)
    a, b, c, d = global_params
    print("\n=== 全ブロックまとめて同定した結果 ===")
    print(f"a = {a:.4e}  (入力→加速度ゲイン)")
    print(f"b = {b:.4e}  (粘性摩擦項)")
    print(f"c = {c:.4e}  (クーロン摩擦項)")
    print(f"d = {d:.4e}  (重力係数; ~ mgL/I)")
    print(f"残差ノルム = {global_res}")
else:
    print("有効なデータがありませんでした。")
