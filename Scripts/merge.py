# Import libraries
import pandas as pd

def GettingMetricsByMethod(file, mode):

    # Loading file and removing production or test files
    try:

        # Loading the file
        fileMethod = pd.read_csv(file)
        fileMethod.rename(columns = {'class': 'className'}, inplace = True)

        # Removing files: 0 - production, 1 - test
        if(mode == 0):
            a = fileMethod[fileMethod.className.str.contains("^Test|^test|Test.java$|test.java$|Tests.java$|tests.java$")]
        else:
            a = fileMethod[~fileMethod.className.str.contains("^Test|^test|Test.java$|test.java$|Tests.java$|tests.java$")]
        onlyTest = a[~a.className.str.contains("\$")]

        # Formatting the methods name
        try:
            onlyTest['method'] = onlyTest['method'].apply(lambda x: x.rpartition("/")[0])
            onlyTest['method'] = onlyTest['method'].apply(lambda x: x.lower())

            onlyTest['className'] = onlyTest['className'].apply(lambda x: x.rpartition(".")[-1])
            onlyTest['className'] = onlyTest['className'].apply(lambda x: x.lower())

            onlyTest['file'] = onlyTest['file'].apply(lambda x: x.rpartition("Generator/")[-1])
            onlyTest['file'] = onlyTest['file'].apply(lambda x: x.lower())

            onlyTest['location'] = onlyTest['file'].astype(str)+'_'+onlyTest['className']+'_'+onlyTest['method']
            return onlyTest
        except KeyError:
            print("---------------------------------------------------  Note: KeyError")
        except AttributeError:
            print("---------------------------------------------------  Note: AttributeError")

    except pd.errors.EmptyDataError:
        print('---------------------------------------------------  Note: filename.csv was empty. Skipping.')
    except pd.errors.ParserError:
        print('---------------------------------------------------  Note: Error tokenizing. Skipping.')


def GroupSmellsByMethod(file, change, array):

    # Loading the file
    try:
        smellF = pd.read_csv(file)

        smellF.rename(columns = {change: 'file'}, inplace = True)
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
    except pd.errors.EmptyDataError:
        print('---------------------------------------------------  Note: filename.csv was empty. Skipping.')
    except pd.errors.ParserError:
        print('---------------------------------------------------  Note: Error tokenizing. Skipping.')

def MergeMethod(metrics, smells, array):

    # Columns of the dataframe
    joined_data = pd.merge(metrics, smells, on=["location"], how="inner")
    joined_data = pd.DataFrame.drop_duplicates(joined_data)

    return joined_data

def GettingMetricsByClass(file, mode):

    # Loading file and removing production or test files
    try:

        # Loading the file
        fileMethod = pd.read_csv(file)
        fileMethod.rename(columns = {'class': 'className'}, inplace = True)


        # Removing files: 0 - production, 1 - test
        if(mode == 0):
            a = fileMethod[fileMethod.className.str.contains("^Test|^test|Test.java$|test.java$|Tests.java$|tests.java$")]
        else:
            a = fileMethod[~fileMethod.className.str.contains("^Test|^test|Test.java$|test.java$|Tests.java$|tests.java$")]
        onlyTest = a[~a.className.str.contains("\$")]

        print("-------------------------------------------------------------\n---------------------\n-------------")
        print(onlyTest)
        # Formatting the methods name
        onlyTest['className'] = onlyTest['className'].apply(lambda x: x.rpartition(".")[-1])
        onlyTest['className'] = onlyTest['className'].apply(lambda x: x.lower())

        onlyTest['file'] = onlyTest['file'].apply(lambda x: x.rpartition("Generator/")[-1])
        onlyTest['file'] = onlyTest['file'].apply(lambda x: x.lower())
        return onlyTest
    except pd.errors.EmptyDataError:
        print('---------------------------------------------------  Note: filename.csv was empty. Skipping.')
    except pd.errors.ParserError:
        print('---------------------------------------------------  Note: Error tokenizing. Skipping.')


def GroupSmellsByClass(file, change, array):

    # Loading the file
    try:
        smellF = pd.read_csv(file)

        smellF.rename(columns = {change: 'file'}, inplace = True)
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
    except pd.errors.EmptyDataError:
        print('---------------------------------------------------  Note: filename.csv was empty. Skipping.')
    except pd.errors.ParserError:
        print('---------------------------------------------------  Note: Error tokenizing. Skipping.')

def MergeClass(metrics, smells, array):

    # Columns of the dataframe
    joined_data = pd.merge(metrics, smells, on=["file"], how="inner")
    joined_data = pd.DataFrame.drop_duplicates(joined_data)

    return joined_data

def Save(path, merged, value):
    if value == 0:
        merged.to_csv(path, mode="a", index = False, header=True)
    else:
        merged.to_csv(path, mode="a", index = False, header=False)

def Read(fileName):
    fileObj = open(fileName, "r")
    words = fileObj.read().splitlines()
    fileObj.close()

    names = []

    for i in words:
        names.append(i.replace("/", "_"))

    return names

# Configure your paths
path = "/media/"
pathInput = path+"files/"
pathProjectsList = path+"project_list.txt"
pathOutput = path+"output/"

listSmells = ['Assertion Roulette', 'Conditional Test Logic', 'Constructor Initialization','Duplicate Assert',
         'Default Test', 'Dependent Test', 'EmptyTest', 'Eager Test', 'Exception Catching Throwing',
         'General Fixture','IgnoredTest', 'Magic Number Test', 'Mystery Guest', 'Print Statement',
         'Redundant Assertion', 'Resource Optimism', 'Sensitive Equality', 'Sleepy Test', 'Unknown Test', 'Verbose Test']


# Loop to merge the files of each project
projects = Read(pathProjectsList)

value = 0
line = 0

for name in projects:
    try:
        ############################## Test files #########################################

        # Save test smells - method
        smellsTestMethod = GroupSmellsByMethod(pathInput+name+"_testsmells.csv", 'classPathFile', listSmells)
        if smellsTestMethod is not None:
            Save(pathOutput+"methodSmells.csv", smellsTestMethod, value)

        #Save test smells - class
        smellsTestClass = GroupSmellsByClass(pathInput+name+"_testsmells.csv",'classPathFile', listSmells)
        if smellsTestClass is not None:
            Save(pathOutput+"classSmells.csv", smellsTestClass, value)


        #Save test metrics - method
        metricsTestMethod = GettingMetricsByMethod(pathInput+name+"_method.csv", 0)
        if metricsTestMethod is not None:
            Save(pathOutput+"testMethod.csv", metricsTestMethod, value)

        #Save test metrics - class
        metricsTestClass = GettingMetricsByClass(pathInput+name+"_class.csv", 0)
        if metricsTestClass is not None:
            Save(pathOutput+"testClass.csv", metricsTestClass, value)


        #Merge test smells and test metrics - method
        if(smellsTestMethod is not None and metricsTestMethod is not None):
            merged = MergeMethod(metricsTestMethod, smellsTestMethod, listSmells)
            Save(pathOutput+"mergeTestMethod.csv", merged, value)

        #Merge test smells and test metrics - class
        if(smellsTestClass is not None and metricsTestClass is not None):
            merged = MergeClass(metricsTestClass, smellsTestClass, listSmells)
            Save(pathOutput+"mergeTestClass.csv", merged, value)

        ############################## Production files #########################################

        #Save production metrics - method
        metricsProductionMethod = GettingMetricsByMethod(pathInput+name+"_method.csv", 1)
        if metricsProductionMethod is not None:
            Save(pathOutput+"productionMethodMetrics.csv", metricsProductionMethod, value)

        #Save production metrics - class
        metricsProductionClass = GettingMetricsByClass(pathInput+name+"_class.csv", 1)
        if metricsProductionClass is not None:
            Save(pathOutput+"productionClassMetrics.csv", metricsProductionClass, value)

        #Merge test smells and production metrics - class
        if(smellsTestMethod is not None and metricsProductionClass is not None):
            merged = MergeClass(metricsProductionClass, smellsTestMethod, listSmells)
            Save(pathOutput+"mergeProductionClass.csv", merged, value)

        #Merge test smells and production metrics - method
        if(smellsTestMethod is not None and metricsProductionMethod is not None):
            merged = MergeMethod(metricsProductionMethod, smellsTestMethod, listSmells)
            Save(pathOutput+"mergeProductionMethod.csv", merged, value)

        #print(name)
        value = 1
        line = line + 1

    except ValueError:
        print("Please enter a valid input.")
    except TypeError:
        print()
