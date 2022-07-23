# Construção de um Modelo de aprendizado de máquina com dataset relacionado a dados da Airbnb

![alt text](mlops.jpg)

Repositório relacionado ao trabalho 2 da segunda unidade da matéria de tópicos especiais em inteligência computacional "D", esse repositório se trata de uma reprodução do trabalho do Professor:Ivanovitch Silva (https://github.com/ivanovitchm/mlops), na qual exploramos dados da Airbnb aplicando técnicas de MLops, onde nesse primeiro momento utilizamos ETL, Checagem e segregação dos dados.

You can download the data from the [Airbnb Data Application](https://drive.google.com/file/d/16zF4MHEP_bBxAEWpQgVocPupTjRRAgfP/view?usp=sharing).

## Ferramentas:


* Anaconda(Jupyter Lab)
* Pytest
* Pep8
* wandb
* MLflow
* Python (Bibliotecas: Pandas/Matplotlib/Numpy

## Criando o Ambiente de Versionalização

- Dentro da pasta EDA:

```bash
  conda env create -f conda.yml
  
  conda activate envname
```

![alt text](Screenshot_4.png)

- [Apresentação - Loom]( #link da apresentação )

## EDA

- Com o ambiente criando utilizamos o comando a seguir para executar o jupyterlab onde será aberto um arquivo notebook onde é realizado alguns processos do EDA)

```bash
mlflow run .
```

## Preprocessing

- Dentro da pasta Preprocessing (realizamos o processo de limpeza da base de dados, retirandos valores repetidos/invalidos e etc):

```bash
	 mlflow run . -P input_artifact="trabalho_2/raw_data.csv:latest" \
                -P artifact_name="preprocessed_data.csv" \
                -P artifact_type="clean_data" \
                -P artifact_description="Data after preprocessing"
```

## Data Segregation

- Dentro da pasta Data_segregation (nesse momento criamos os artefatos de train e test):

```bash
	 mlflow run . -P input_artifact="trabalho_2_preprocessing/preprocessed_data.csv:latest" \
                -P artifact_root="data" \
                -P artifact_type="trainvaltest_data" \
                -P test_size=0.3 \
                -P stratify="instant_bookable" \
                -P random_state="13"
```

## Data Validation

- Dentro da pasta Data_validation (aqui realizamos alguns testes gerais dos dados):
```bash
    pytest . -vv
```

- Dentro da pasta Deterministic_tests (aqui realizamos testes especificos, onde verificamos os tipos dos dados e seu range de valores):

```bash
    mlflow run .
```
- Dentro da pasta Multiple_hypothesis_testing_in_pytest (nesse passo executamos alguns scripts para realizar testes com os artefatos tanto de train como de test):

Test_data.csv:v0             |  Train_data.csv:v0
:-------------------------:|:-------------------------:
![test_data](test_data.png)  |  ![train_data](train_data.png)

```bash
   mlflow run . -P reference_artifact="trabalho_2_segregation/train_data.csv:latest" \
                -P sample_artifact="trabalho_2_segregation/test_data.csv:latest" \
                -P ks_alpha=0.05
```

## In case of errors

When you make an error writing your ``conda.yml`` file, you might end up with an environment for the pipeline or one of the components that is corrupted. Most of the time ``mlflow`` realizes that and creates a new one every time you try to fix the problem. However, sometimes this does not happen, especially if the problem was in the ``pip`` dependencies. In that case, you might want to clean up all conda environments created by ``mlflow`` and try again. In order to do so, you can get a list of the environments you are about to remove by executing:

```bash
conda info --envs | grep mlflow | cut -f1 -d" "
```

If you are ok with that list, execute this command to clean them up:

**NOTE**: this will remove ALL the environments with a name starting with mlflow. Use at your own risk

```bash
for e in $(conda info --envs | grep mlflow | cut -f1 -d" "); do conda uninstall --name $e --all -y;done
```

This will iterate over all the environments created by mlflow and remove them.


## Authors

<a href="https://github.com/Julio-CSilva">
 <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/57691025?s=400&u=15893c15d3d42c7737e91cc4f11dcbd7751b7565&v=4" width="100px;" alt=""/>
 <br />
 <sub><b>Julio Silva</b></sub></a> <a href="https://github.com/Julio-CSilva" title="Foguete não tem ré">🚀</a>
 
Clique para saber mais!

[![Linkedin Badge](https://img.shields.io/badge/-Julio-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/julio-csilva/)](https://www.linkedin.com/in/julio-csilva/) 
[![Gmail Badge](https://img.shields.io/badge/-juliocesarfilho0112@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:juliocesarfilho0112@gmail.com)](mailto:juliocesarfilho0112@gmail.com)

---

<a href="https://github.com/Benhurds12">
 <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/90663589?v=4" width="100px;" alt=""/>
 <br />
 <sub><b>Jose Ben Hur</b></sub></a> <a href="https://github.com/Julio-CSilva" title="Foguete não tem ré">🚀</a>
 
Clique para saber mais!

[![Linkedin Badge](https://img.shields.io/badge/-Benhur-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/josé-ben-hur-nascimento-de-oliveira-385bb8238/)](https://www.linkedin.com/in/josé-ben-hur-nascimento-de-oliveira-385bb8238/) 
[![Gmail Badge](https://img.shields.io/badge/-benhurdsufrn@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:benhurdsufrn@gmail.com)](mailto:benhurdsufrn@gmail.com)
