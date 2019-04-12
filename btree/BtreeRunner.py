# import sys
# from Btree import Btree
#
#
# # Btree Runner
# class BtreeRunner(object):
#     # Init with order - it will load the console file based on command line arguments
#     def __init__(self, order):
#         self._order = order
#         self._btree = Btree(order)
#
#         if len(sys.argv) > 0:
#             command_file_name = sys.argv[1]
#             self.run(command_file_name)
#
#         else:
#             print "Error: No command line arguments"
#
#     # Run the command line file
#     # Input: command_file: name of the command file
#     def run(self, command_file):
#         runner_file = open(command_file, 'r')
#
#         print "Starting B-Tree runner."
#
#         for line in runner_file:
#             line = line.rstrip()
#             action = line.split(" ")
#             if len(action) > 0:
#                 command = action[0]
#                 if command == "L:":
#                     if len(action) > 1:
#                         self.load(action[1])
#                     else:
#                         "Error: no file name given"
#                 elif command == "A:":
#                     if len(action) > 1:
#                         self.insert(action[1])
#                     else:
#                         "Error: no value given to add"
#                 elif command == "D:":
#                     if len(action) > 1:
#                         self.delete(action[1])
#                     else:
#                         "Error: no value given to delete"
#                 elif command == "S:":
#                     if len(action) > 1:
#                         print "Found key: " + action[1] + "? " + str(self.find(action[1]))
#                     else:
#                         "Error: no value given to find"
#                 elif command == "P:":
#                     self.print_tree()
#                 elif command == "T:":
#                     print "\nQuiting B-Tree runner. Goodbye."
#
#     # insert - key - ensures it can convert to an int before adding
#     def insert(self, key):
#         try:
#             float_val = float(key)
#             if float_val % 1 == 0:
#                 return self._btree.insert(int(float_val))
#             else:
#                 return self._btree.insert(float_val)
#         except ValueError:
#             return self._btree.insert(key)
#
#     # find - key - ensures it can convert to an int before searching
#     def find(self, key):
#         try:
#             float_val = float(key)
#             if float_val % 1 == 0:
#                 return self._btree.find(int(float_val))
#             else:
#                 return self._btree.find(float_val)
#         except ValueError:
#             return self._btree.find(key)
#
#     # delete - key - ensures it can convert to an int before deleting
#     def delete(self, key):
#         try:
#             float_val = float(key)
#             if float_val % 1 == 0:
#                 self._btree.delete(int(float_val))
#             else:
#                 self._btree.delete(float_val)
#         except ValueError:
#             self._btree.delete(key)
#
#     # print the tree
#     def print_tree(self):
#         print "\nPrinting B-tree:"
#         self._btree.print_tree()
#         print "\n"
#
#     # load - file_name - name of the file to load - adds all the values to the Btree
#     def load(self, file_name):
#         file_tree = open(file_name, 'r')
#
#         for line in file_tree:
#             values = line.split(" ")
#             for value in values:
#                 try:
#                     float_val = float(value)
#                     if float_val % 1 == 0:
#                         self.insert(int(float_val))
#                     else:
#                         self.insert(float_val)
#                 except ValueError:
#                     self.insert(value)
#
#         file_tree.close()
#
#
# runner = BtreeRunner(5)  # starts up the program
#
