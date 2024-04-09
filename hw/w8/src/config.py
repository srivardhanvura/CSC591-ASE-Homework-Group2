the = {}

help = """
OPTIONS:
  -b --bins   initial number of bins      = 16
  -B --Bootstraps number of bootstraps    = 512
  -c --cohen  parametric small delta      = .35
  -C --Cliffs  non-parametric small delta = 0.2385 
  -d --d      frist cut                       = 32
  -D --D      second cut                      = 4
  -f --file   where to read data          = hw/w8/data/auto93.csv
  -F --Far    distance to  distant rows   = .925
  -g --go     start up action             = "help"
  -H --Half #examples used in halving   = 512
  -p --p      distance coefficient        = 2
  -S --seed   random number seed          = 1234567891
  -m --min    minimum size               = .5
  -r --rest   |rest| is |best|*rest         = 3
  -T --Top    max. good cuts to explore   = 10 
  -BB --Beam   max number of ranges        = 10
  -SS --Support coeffecient on best        = 2
  -C --Cut    ignore ranges less than C*max   = .1
  -k --k low class frequency kludge = 1
  -m --m low attribute frequency kludge = 2
   """
egs = {}

Seed = 31210