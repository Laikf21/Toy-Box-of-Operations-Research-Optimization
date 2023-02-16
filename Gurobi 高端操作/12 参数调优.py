from gurobipy import *

model = read('neos-957323.mps')

model.Params.TuneResults = 1
model.Params.TuneTimeLimit = 40

model.tune()

if model.tuneResultCount > 0:

    # Load the best tuned parameters into the model
    model.getTuneResult(0)

    # Write tuned parameters to a file
    model.write('neosTuned.prm')