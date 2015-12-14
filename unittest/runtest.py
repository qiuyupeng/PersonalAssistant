import unittest
import importlib
import os
import sys

#parent dir of current folder
PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

#put PARENT_DIR in search path
sys.path.append(PARENT_DIR)


def load_class_from_module(dir_str):
    """
    dynamically load a class from a dictionary
    dir: the name of the dir containning the files
    return a list of testCase obj
    """

    output = []

    dir_module = importlib.import_module(dir_str)
    unittest_info = getattr(dir_module, 'UNITTEST_INFO', None)
    if unittest_info is None:
    	return output

    # unittest_info: dict containning the test 
    # key: file name 
    # value: list of class names
    for file_name, list_class in unittest_info.items():
    	module = importlib.import_module(dir_str + "." + file_name)
    	for class_str in list_class:
    		output.append(getattr(module, class_str))

    return output


def load_class():
	"""
	search all the unittest in the system and return a list of all the modules
	"""
	list_dir_str = os.listdir(PARENT_DIR)
	output = []
	for dir_str in list_dir_str:
		#if dir name start with '.' or is this unittest folder
		if '.' in dir_str or dir_str == os.path.dirname(__file__):
			continue
		output.extend(load_class_from_module(dir_str))

	return output


if __name__ == '__main__':
	#collect all the test cases
	all_test = load_class()

	loader = unittest.TestLoader()
	mysuite = unittest.TestSuite()
	text_runner = unittest.TextTestRunner()
	for test in all_test:
		mysuite.addTests(loader.loadTestsFromTestCase(test))

	text_runner.run(mysuite)

