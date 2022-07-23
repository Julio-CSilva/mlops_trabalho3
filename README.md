# Construção de um Modelo de aprendizado de máquina com dataset relacionado a dados da Airbnb

![alt text](mlops.jpg)

Repositório relacionado ao trabalho final da matéria de tópicos especiais em inteligência computacional "D", esse repositório se trata de uma reprodução do trabalho do Professor:Ivanovitch Silva (https://github.com/ivanovitchm/mlops), na qual exploramos dados da Airbnb aplicando técnicas de MLops, onde nesse primeiro momento utilizamos ETL, Checagem e segregação dos dados.

You can download the data from the [Airbnb Data Application](https://drive.google.com/file/d/16zF4MHEP_bBxAEWpQgVocPupTjRRAgfP/view?usp=sharing).

## Ferramentas:


* Anaconda(Jupyter Lab)
* Pytest
* Pep8
* wandb
* MLflow
* Python (Bibliotecas: Pandas/Matplotlib/Numpy

## Criando o Ambiente de Versionalização

- Dentro da pasta principal:

```bash
  conda env create -f conda.yml
  
  conda activate envname
```

![alt text](Screenshot_4.png)

- [Apresentação - Loom]( #link da apresentação )

## EDA

- Com o ambiente criado podemos acessar pelo jupter-lab


- Dentro da pasta principal
```bash
	 mlflow run . -P hydra_options="main.execute_steps='download'"
	 mlflow run . -P hydra_options="main.execute_steps='preprocess'"
       	 mlflow run . -P hydra_options="main.execute_steps='check_data'"
         mlflow run . -P hydra_options="main.execute_steps='segregate'"
         mlflow run . -P hydra_options="main.execute_steps='decision_tree'"
	 mlflow run . -P hydra_options="main.execute_steps='evalute'"
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
