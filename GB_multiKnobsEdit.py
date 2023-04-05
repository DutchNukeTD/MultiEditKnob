## GB_multiKnobsEdit
## Select multiple nodes of the same class and start the function.
## node MultiKnobs is created. As long as the properties of this node is open the effect is running. 
## Close the MultiKnobs node to stop the link.
## 2022 11 16
## Golan
## Python 3 

## 16-03-2023
## Bug: Doesn't work with settings key frames! 

import nuke

my_code = """

selectedNodes = list(selNodes.split(" "))

nodeName = nuke.thisNode().name()
knobName = nuke.thisKnob().name()
knobValue = nuke.thisKnob().value()
print(str(nodeName) + ' ' + str(knobName) + ' ' +  str(knobValue))

multiKnobsNode = nuke.toNode('multiKnobs')

if multiKnobsNode.shown() == True:
    for n in selectedNodes:
        node = nuke.toNode(n)
        if node.name() is not nodeName:
            value = nuke.toNode(nodeName)[knobName].toScript()
            node.knob(knobName).fromScript(value)
"""

my_code_end = """

selectedNodes = list(selNodes.split(" "))

count = 0
for n in selectedNodes:
    node = nuke.toNode(n)
    node['knobChanged'].setValue('')
    print(node.name() + ' knobChanged turned off!')
    count = count + 1

this = nuke.thisNode()
nuke.delete(this)

"""
    

def multiKnobsEdit():

    selNodes = ''
    selectedNodes = nuke.selectedNodes()

    if len(selectedNodes) <= 1:
        print('Selected 2 or more nodes!')
        pass

    else: 
        x = 0
        for selected_node in selectedNodes:
            x += 1
            selected_node = selected_node['name'].value()
            if x == 1:
                selNodes += '' + selected_node
            else:
                selNodes += ' ' + selected_node


        # Create NoOp node named 'MultiKnobs'.
        multiKnobsNode = 'multiKnobs'
        if multiKnobsNode in nuke.allNodes():
            multiKnobsNode = node
            multiKnobsNode.showControlPanel(forceFloat = True)
        
        else:
            code_end = 'selNodes = "' + selNodes + '"' + my_code_end
            multiKnobsNode = nuke.nodes.NoOp(name='multiKnobs')
            multiKnobsNode.addKnob(nuke.PyScript_Knob('End', 'end', code_end))
            multiKnobsNode.showControlPanel(forceFloat = True)


    count = 0
    for i in selectedNodes:
        selectedNodes[count].knob('knobChanged').setValue('selNodes = "' + selNodes + '"' + my_code)
        count = count + 1


###########
## To add to nuke menu + hotkey (shift+e)
nuke.menu('Nuke').addCommand( 'Edit/Node/Multi Knobs Edit', lambda: multiKnobsEdit(), 'shift+e' )
###########


