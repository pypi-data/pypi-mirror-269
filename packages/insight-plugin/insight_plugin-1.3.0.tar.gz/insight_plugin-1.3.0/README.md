# Insight Plugin - CLI Tooling for plugin development

## Commands

### Create
Create a new plugin.

This command will generate the skeleton folder structure and 
code for a new plugin, based on the provided plugin.spec.yaml file.

### Export
Export a plugin Docker image to a tarball.

This tarball can be uploaded as a custom plugin 
via the import functionality in the InsightConnect UI.

### Refresh
Refresh the plugin.

This command will update the current plugin code, 
when updates are made in the plugin.spec.yaml file

### Validate
Validate / Run checks against the plugin. 

This command performs quality control checks on the current 
state of the plugin. 
This should be run before finalizing any new updates.

### Semver
Update the plugin versioning. 

This command should be run after finalizing any updates, 
defect fixes or new functionality, to update the versioning

### Samples
Create test samples for actions and triggers. 

This command will create new files under the 'tests' folder which can be 
used to test each new action/trigger. 
Note if a file already exists for a particular action/trigger, it will be overwritten.

### Run
Run an action/trigger from a json test file (created during sample generation)

### Server
Run the plugin in HTTP mode. 

This allows an external API testing program to be used to test a plugin 

### Shell
Run the plugin via the docker shell to enable advanced debugging

### View
Run a docker command to get an overview of a plugin.
