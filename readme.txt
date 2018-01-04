Usage:
1. Put your yaml file into the 'yaml' folder of this project
2. Reach the directory of the project and run "python YamlGraphBuilder.py yourfilename", for example, "python YamlGraphBuilder.py jack_qa.yaml"
3. graph can be generated in pdf format and stored in "graph-output folder"

Pay attention to:
- This builder ignores all answer layers or prediction layers
- For configure file without model, it will return an empty graph
- all configure files in 'qa' and 'snli' folder have been tested, refer to the results in 'graph-output'

For further improvement:
1. Enrich the style of graphs to look gracefully
2. Show more information in configure files like model parameters
2. For making interactive graph, I think it is worthy to attempt but can not ensure 