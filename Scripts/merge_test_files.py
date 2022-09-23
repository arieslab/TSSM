# Import libraries
import pandas as pd
import numpy as np
import os.path

def GettingMetricsByMethod(file):

    # Loading file and removing production or test files
    try:

        # Loading the file
        fileMethod = pd.read_csv(pathInput+name+"_method.csv")

        # Formatting the methods name
        try:
            fileMethod.rename(columns = {'class': 'className'}, inplace = True)
            #fileMethod = fileMethod[~fileMethod.className.str.contains("\$")]
            fileMethod['className'] = fileMethod['className'].apply(lambda x: x.rpartition(".")[-1])

            # Getting test files
            onlyTest = fileMethod[fileMethod.className.str.contains("^Test|^test|Test$|test$|Tests$|tests$")]


            onlyTest['method'] = onlyTest['method'].apply(lambda x: x.rpartition("/")[0])
            onlyTest['method'] = onlyTest['method'].apply(lambda x: x.lower())

            onlyTest['className'] = onlyTest['className'].apply(lambda x: x.lower())

            onlyTest['file'] = onlyTest['file'].apply(lambda x: x.rpartition("Generator/")[-1])
            onlyTest['file'] = onlyTest['file'].apply(lambda x: x.lower())

            onlyTest['location'] = onlyTest['file'].astype(str)+'_'+onlyTest['className']+'_'+onlyTest['method']
            onlyTest.drop_duplicates()

            return onlyTest
        except KeyError:
            print("---------------------------------------------------  key Error ---------------------------------------------------")
        except AttributeError:
            print("------------------------------------------------  Attribute Error ------------------------------------------------")
    except pd.errors.EmptyDataError:
        print('---------------------------------------------------  Empty Data Error ---------------------------------------------------')
    except pd.errors.ParserError:
        print('------------------------------------------------------  Parse Error -----------------------------------------------------')


def GroupSmellsByMethod(file, change, array):

    # Loading the file
    try:
        smellF = pd.read_csv(file)

        try:
            smellF.rename(columns = {change: 'file'}, inplace = True)

            # Dropping Lazy Test as it occurs through several methods
            smellFile = smellF[~smellF.name.str.contains("Lazy Test")]

            # Concatenate Key
            smellFile['className'] = smellFile['className'].apply(lambda x: x.lower())
            smellFile['method'] = smellFile['method'].apply(lambda x: x.lower())
            smellFile['file'] = smellFile['file'].apply(lambda x: x.rpartition("Generator/")[-1])
            smellFile['file'] = smellFile['file'].apply(lambda x: x.lower())
            smellFile['location'] = smellFile['file'].astype(str)+'_'+smellFile['className']+'_'+smellFile['method']

            # Sum all test smells in a method
            allSmells = smellFile.groupby(['location','file', 'className','method'])['name'].count().reset_index(name="sumSmells")


            # Sum specific smell in a method
            for i in array:
                a = smellFile.query('name == @i').groupby(['location'])['range'].count().reset_index(name=i)
                allSmells = pd.merge(allSmells, a, on="location", how="left")

            return(allSmells)
        except KeyError:
            print("---------------------------------------------------  key Error ---------------------------------------------------")
        except AttributeError:
            print("------------------------------------------------  Attribute Error ------------------------------------------------")
    except pd.errors.EmptyDataError:
        print('---------------------------------------------------  Empty Data Error ---------------------------------------------------')
    except pd.errors.ParserError:
        print('------------------------------------------------------  Parse Error -----------------------------------------------------')

def MergeMethod(metrics, smells, array):

    # Columns of the dataframe
    joined_data = pd.merge(metrics, smells, on=["location"], how="inner")
    joined_data = pd.DataFrame.drop_duplicates(joined_data)

    return joined_data

def GettingMetricsByClass(file):

    # Loading file and selecting the test files
    try:

        fileMethod = pd.read_csv(pathInput+name+"_class.csv")
        try:
            fileMethod.rename(columns = {'class': 'className'}, inplace = True)
            #fileMethod = fileMethod.iloc[np.where(fileMethod.type == "class")]
            fileMethod['className'] = fileMethod['className'].apply(lambda x: x.rpartition(".")[-1])

            # Regular expression to get test classes and transform to lower case
            onlyTest = fileMethod[fileMethod.className.str.contains("^Test|^test|Test$|test$|Tests$|tests$")]
            onlyTest['className'] = onlyTest['className'].apply(lambda x: x.lower())

            # Establish a pattern in the files' names
            onlyTest['file'] = onlyTest['file'].apply(lambda x: x.rpartition("Generator/")[-1])
            onlyTest['file'] = onlyTest['file'].apply(lambda x: x.lower())

            return onlyTest
        except KeyError:
            print("---------------------------------------------------  key Error ---------------------------------------------------")
        except AttributeError:
            print("------------------------------------------------  Attribute Error ------------------------------------------------")
    except pd.errors.EmptyDataError:
        print('---------------------------------------------------  Empty Data Error ---------------------------------------------------')
    except pd.errors.ParserError:
        print('------------------------------------------------------  Parse Error -----------------------------------------------------')


def GroupSmellsByClass(file, change, array):

    # Loading the file
    try:
        smellF = pd.read_csv(file)

        try:
            smellF.rename(columns = {change: 'file'}, inplace = True)

            # Dopping Lazy Test as it occurs through several methods
            smellFile = smellF[~smellF.name.str.contains("Lazy Test")]

            smellFile['className'] = smellFile['className'].apply(lambda x: x.lower())
            smellFile['file'] = smellFile['file'].apply(lambda x: x.rpartition("Generator/")[-1])
            smellFile['file'] = smellFile['file'].apply(lambda x: x.lower())

            # Sum all test smells in a method
            allSmells = smellFile.groupby(['file'])['name'].count().reset_index(name="sumSmells")

            # Sum specific smell in a method
            for i in array:
                a = smellFile.query('name == @i').groupby(['file'])["range"].count().reset_index(name=i)
                allSmells = pd.merge(allSmells, a, on="file", how="left")

            return(allSmells)
        except KeyError:
            print("---------------------------------------------------  key Error ---------------------------------------------------")
        except AttributeError:
            print("------------------------------------------------  Attribute Error ------------------------------------------------")
    except pd.errors.EmptyDataError:
        print('---------------------------------------------------  Empty Data Error ---------------------------------------------------')
    except pd.errors.ParserError:
        print('------------------------------------------------------  Parse Error -----------------------------------------------------')

def MergeClass(metrics, smells, array):

    # Columns of the dataframe
    joined_data = pd.merge(metrics, smells, on=["file"], how="inner")
    joined_data = pd.DataFrame.drop_duplicates(joined_data)

    return joined_data

def Save(path, merged):
    if (os.path.isfile(path)):
        merged.to_csv(path, mode="a", index = False, header=False)
    else:
        merged.to_csv(path, mode="a", index = False, header=True)

def Read(fileName):
    fileObj = open(fileName, "r")
    words = fileObj.read().splitlines()
    fileObj.close()

    names = []

    for i in words:
        names.append(i.replace("/", "_"))

    return names


# Configure your paths
path = "/media/luana-martins/4805f023-fc6f-4893-b3f8-5f9f2d37cf70/home/luana-martins/Documentos/JSEP/"
pathInput = path+"files/"
pathProjectsList = path+"all.txt"
pathOutput = path+"TSSM/dataset_full/test_data/"

listSmells = ['Assertion Roulette', 'Conditional Test Logic', 'Constructor Initialization','Duplicate Assert',
         'Default Test', 'Dependent Test', 'EmptyTest', 'Eager Test', 'Exception Catching Throwing',
         'General Fixture','IgnoredTest', 'Magic Number Test', 'Mystery Guest', 'Print Statement',
         'Redundant Assertion', 'Resource Optimism', 'Sensitive Equality', 'Sleepy Test', 'Unknown Test', 'Verbose Test']


# Loop to merge the files of each project
projects = Read(pathProjectsList)


line = 0

for name in projects:
    try:
        ############################## Test files #########################################

        # Save test smells - method
        smellsTestMethod = GroupSmellsByMethod(pathInput+name+"_testsmells.csv", 'classPathFile', listSmells)
        if smellsTestMethod is not None:
            Save(pathOutput+"testMethodSmells.csv", smellsTestMethod)

        #Save test smells - class
        smellsTestClass = GroupSmellsByClass(pathInput+name+"_testsmells.csv",'classPathFile', listSmells)
        if smellsTestClass is not None:
            Save(pathOutput+"testClassSmells.csv", smellsTestClass)


        #Save test metrics - method
        metricsTestMethod = GettingMetricsByMethod(pathInput+name+"_method.csv")
        if metricsTestMethod is not None:
            Save(pathOutput+"testMethodMetrics.csv", metricsTestMethod)

        #Save test metrics - class
        metricsTestClass = GettingMetricsByClass(pathInput+name+"_class.csv")
        if metricsTestClass is not None:
            Save(pathOutput+"testClassMetrics.csv", metricsTestClass)


        #Merge test smells and test metrics - method
        if(smellsTestMethod is not None and metricsTestMethod is not None):
            merged = MergeMethod(metricsTestMethod, smellsTestMethod, listSmells)
            Save(pathOutput+"mergeTestMethod.csv", merged)

        #Merge test smells and test metrics - class
        if(smellsTestClass is not None and metricsTestClass is not None):
            merged = MergeClass(metricsTestClass, smellsTestClass, listSmells)
            Save(pathOutput+"mergeTestClass.csv", merged)

        line = line + 1
        print("\nLINE: ",line)
    except ValueError:
        print("Value Error")
