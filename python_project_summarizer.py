# Python Project Summarizer
# By @TokyoEdtech
# This program will read a file/file directory with .py files
# And then summarize the file (classes, methods, variables, etc)

class ParsedFile():
    def __init__(self, filename):
        self.filename = filename
        self.internal_classes = []
        self.variables = []
        self.methods = []
        self.external_classes = []
        self.modules = []
        
    def parse_file(self):
        # Open file and read data into list
        try:
            with open(filename, "r") as my_file:
                file_data = my_file.readlines()
        except:
            print("ERROR: Could not open/read file: {}")
            print("Are you sure the file exists? (Check the spelling.)")
            print("You may need to add the full path to the file.")
            print("Are you sure you have permission to access the file?")
        
        # Iterate through each line
        for line in file_data:
            line.strip()
            
            # Check for modules
            if line.find("import") != -1:
                tokens = line.split(" ")[1]
                tokens = tokens.split(",")
                for token in tokens:
                    self.add_module(token.strip())
            
            # Check for functions
            elif line.find("def") == 0:
                token = line.split(" ")[1]
                self.add_method(token.strip())
            
            # Check for internal classes
            elif line.find("class") != -1:
                tokens = line.split(" ")[1]
                tokens = tokens.split("(");
                class_name = tokens[0]
                parent = tokens[1][0:-3]
                init = "NOT IMPLEMENTED"
                self.add_internal_class(class_name, parent, init)
                
    def add_internal_class(self, name, parent, init):
        self.internal_classes.append(name + " " + parent + " " + init)
        # Add parent to external class list
        if parent not in self.internal_classes and parent not in self.external_classes and parent != "":
            self.external_classes.append(parent)
    
    def add_variable(self, variable):
        self.variables.append(variable)
        
    def add_method(self, method):
        self.methods.append(method)
        
    def add_external_class(self, external_class):
        self.external_classes.append(external_class)
        
    def add_module(self, module):
        self.modules.append(module)
        
    def print_info(self):
        print(self.filename)
        
        # Print modules
        print("\nModules:")
        for module in self.modules:
            print(module)
            
        # Print variables
        print("\nVariables:")
        for variable in self.variables:
            print(variable)
        
        # Print methods
        print("\nMethods:")
        for method in self.methods:
            print(method)
            
        # Print classes
        print("\nInternal Classes:")
        for internal_class in self.internal_classes:
            print(internal_class)
            
        # Print external classes
        print("\nExternal Classes:")
        for external_class in self.external_classes:
            print(external_class)
            
            
# Choose filename
filename = "spgl.py"

# Create ParsedFile Object
parsed_file = ParsedFile(filename)

# Parse the file
parsed_file.parse_file();

# Print file info
parsed_file.print_info();
