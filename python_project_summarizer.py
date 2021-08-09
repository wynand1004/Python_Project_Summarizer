# Python Project Summarizer
# By @TokyoEdtech
# This program will read a file/file directory with .py files
# And then summarize the file (classes, methods, variables, etc)

class ParsedFile():
    keywords = ["if", "elif", "else", "for", "while"]
    
    def __init__(self, filename):
        self.filename = filename
        self.internal_classes = []
        self.variables = []
        self.methods = []
        self.external_classes = []
        self.modules = []
        
        # Keep track of where we are in the parsing
        self.current = None
        
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
            
            # Ignore comments
            if line.find("#") > -1:
                continue
            
            # Check for modules
            if line.find("import ") != -1:
                tokens = line.split(" ")[1]
                tokens = tokens.split(",")
                for token in tokens:
                    if token != "":
                        self.add_module(token.strip())
                self.current = None
            
            # Check for methods
            elif line.find("def ") != -1:
                line = line.strip()
                # print("\n\nLine: " + line + "\n\n")
                token = line.split(" ",1)[1]
                if self.current == "class":
                    self.add_internal_class("    " + token.strip(), "", "")
                else:
                    self.add_method(token.strip()[0:-1])
                
            elif line.find("return ") != -1 and self.current == "def":
                self.add_method(line.strip())
                self.current = None
            
            # Check for internal classes
            elif line.find("class ") != -1:
                tokens = line.split(" ")[1]
                tokens = tokens.split("(");
                class_name = tokens[0]
                try:
                    parent = tokens[1][0:-3]
                except:
                    parent = "NO PARENT FOUND"
                init = "NOT IMPLEMENTED"
                self.add_internal_class(class_name, parent, init)
                self.current = "class"
                
            else: 
                keyword_found = False
                for keyword in ParsedFile.keywords:
                    if line.find(keyword) != -1:
                        keyword_found = True
                
                if not keyword_found and line.find("=") != -1 and self.current == None and line[0]!=" " and line[0]!="\t":
                    variable = line.strip().split("=")[0].split(" ")[0].strip()
                    if  variable !="" and variable not in self.variables:
                        self.add_variable(variable)
                
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
            print(f"    {module}")
            
        # Print variables
        print("\nGloblal Variables:")
        for variable in self.variables:
            print(f"    {variable}")
        
        # Print methods
        print("\nMethods:")
        for method in self.methods:
            print(f"    {method}")
            
        # Print classes
        print("\nInternal Classes:")
        for internal_class in self.internal_classes:
            print(f"    {internal_class}")
            
        # Print external classes
        print("\nExternal Classes:")
        for external_class in self.external_classes:
            print(f"    {external_class}")
            

# Clear screen
import os
os.system("clear")

# Choose filename
files = os.listdir()

for filename in files:
    if filename.find(".py") != -1:
    
        # Create ParsedFile Object
        parsed_file = ParsedFile(filename)

        # Parse the file
        parsed_file.parse_file();

        # Print file info
        parsed_file.print_info();
        
    print("\n\n")
