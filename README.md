# TSSM Dataset

> **_NOTE:_** the dataset is temporarily available [here](https://drive.google.com/file/d/1sSTD-PdEnfdrgV4qhi62feHVGQ7v5s0b/view?usp=sharing).

## Creation Steps

### (1) List of Java projects
Mining the GitHub repository is a time-consuming activity because it has more than 8 million projects. Therefore, we used the 147,991 Java projects with more than five stars listed by [Loriot et al.](https://arxiv.org/abs/1904.01754) (2020) and [Durieux et al.](https://arxiv.org/abs/2103.09672) (2021). The list of projects is available at ```project_list.txt```. 

### (2) Filtering projects from Github
We established the following criteria to select projects that match the requirements of data extraction tools:
* **Open-source projects.** We limit our search to projects with a declared license
compliant with OSI (Open-Source Initiative) or FSF (Free Software Foundation) licensing;
* **Non-forked projects.** We removed the forked projects because they contain excerpts of code similar to the original ones, which return similar values in the data extraction, biasing the results.
* **Projects that use Java as the primary programming language.** Besides the initial list contains projects that use Java as the primary programming language, the projects evolved since the GitHub mining. Therefore, we checked whether the projects continue using Java as a primary language. 


### (3) Data extraction
We developed `MiningGitHub` to collect the following data of the projects:
* **Test Smells.** We used the [JNose Test](https://jnosetest.github.io/) to collect data of test smells in the test code. 
* **Structural metrics.** We used the [CK Metrics](https://github.com/mauricioaniche/ck) to collect structural metrics from the test and production code.
* **Metadata from GitHub.** We used the [GHRepository](https://github-api.kohsuke.org/apidocs/index.html) to collect the metadata of the projects sucessfully executed by JNose Test and CK Metrics. 

We made the files containing the data on test smells and metrics available in the folder ```TSSM```. It is structured as follows:

```
TSSM
│
├── Test Smells
│   ├── classSmells.csv: contains data of 18 test smells at class level
│   ├── methodSmells.csv: contains data of 18 test smells at method level
├── Metrics of the test code: 
│   ├── testClass.csv: contains data of 44 structural metrics at test class level
│   ├── testMethod.csv: contains data of 28 structural metrics at test method level 
├── Metrics of the production: 
│   ├── productionClass.csv: contains data of 44 structural metrics at production class level
│   ├── productionMethod.csv: contains data of 28 structural metrics at production method level 
|
```

## Mining GitHub 

Prerequisites:
 - JDK 1.8 
 - Maven 3 

The JNose Test requires the [jnose-core](https://github.com/tassiovirginio/jnose-core) dependency. Install the dependecy following the steps: 

```shell
git clone git@github.com:arieslab/jnose-core.git
cd jnose-core
mvn install
```
Clone the project to generate the dataset using the following command:

```shell
git clone git@github.com:arieslab/TSSM.git
```

Open the project ```MiningGitHub``` in the IDE as a Maven project (we used IntelliJ), configure and run the class ```Main.java``` with the information:
* **ghKey** receives a personal access token from GitHub. [Generating a ghKey](https://github.com/settings/tokens).
* **startNumberList** receives a initial lineID of a project from the ```project_list.txt``` to start the data collection. 
* **endNumberList** receives a final lineID of a project from the ```project_list.txt``` to start the data collection. 
