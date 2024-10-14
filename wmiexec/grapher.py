from collections import Counter
from scipy.stats import entropy
import plotly.graph_objects as go


def getEntropy(string):
    counts = Counter(string)
    probabilities = [count / len(string) for count in counts.values()]
    return entropy(probabilities, base=2)

def createBarchart(entropyValues, entropyLabels): # entropyValues -> list format    
    mockVals = []
    for v in range(0, len(entropyValues)):
        mockVals.append("cmd" + str(v))
    fig = go.Figure(data=[go.Bar(x=entropyLabels, y=entropyValues, hoverinfo='x+y')])
    fig.update_layout(title='Entropy', xaxis_title='Commands', yaxis_title='Entropy', xaxis=dict(showticklabels=False))
    fig.show()


def parseProcmon(location):
    f = open(location, 'r')
    data = f.readlines()
    
    entropyValues = []
    entropyLabels = []
    nonDupCommands = []

    for line in data:
        if "Process Start" in line:
            try:
                commandline = line.split(",")[7]
                if commandline not in nonDupCommands:
                    nonDupCommands.append(commandline)
                

            except:
                print("[!] Error encountered when attempting to find command line. Ignoring...")

    # Removing any duplicate commands to make sure bars aren't stacked on top of one another
    for cmd in nonDupCommands:
        cmdStrip = cmd.strip("Command line:")
        # Filtering only for cmd.exe for increased visibility into entropy difference in graph
        if cmdStrip.startswith("cmd.exe"):
            entropy = getEntropy(cmdStrip)
            entropyValues.append(entropy)
            entropyLabels.append(cmdStrip)
        


    print(entropyValues)
    print(entropyLabels)
    createBarchart(entropyValues, entropyLabels)



parseProcmon('<CSV Procmon file here>')
