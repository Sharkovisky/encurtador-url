## encurtador-url
Projeto de TCC que consiste em um Encurtador de URL, desenvolvido no framework Python Flask.

Este projeto foi inteiramanete desenvolvido em um ambiente baseado em Linux, por isso, todos os passos da instalação provém de comandos no Terminal.

Para realizar a implantação do projeto, primeiro é necessário ter instalado na máquina a versão 3 do Python e o banco de dados MariaDB.

A instalação do MariaDB é relativamente fácil, só tendo um detalhe de que: se houve a instalação do banco de dados MySQL anteriormente, causa alguns erros assim que é realizada a instalação do MariaDB. Para driblar toda essa dor de cabeça, é extremamente recomendado fazer a instalação num sistema recém instalado. Para instalar o MariaDB, abre-se o Terminal e digite o seguinte comando:

# sudo apt install mariadb-server

Algumas versões de Linux já vem com o Python instalado, sendo somente necessário a consulta da versão instalada:

# python3 --version

Caso não tenha uma versão de Python3 instalada, abre-se o Terminal do Linux e digite o comando para instalação do Python3:

# sudo apt-get install python3.8 python3-pip

Instalaremos junto o pip, que é um gerenciador de pacotes do próprio Python3.

Após realizar todas as instalações, consulte novamente a versão do Python3 para ver se foi corretamente instalada, voltando ao passo retrasado.

Realizaremos a abertura do Terminal do Pip, com o comando:

# pipenv shell

Agora, instalaremos todas as dependências com o seguinte comando, que instalará tudo automaticamente nas versões corretas:

# pipenv install

Após ter feito a instalação de todas as dependências, vamos realizar a criação automática de todas as tabelas de nosso banco de dados, assim, utilizaremos o comando em .py para isso:

# python3 tables.py

Depois de criado as tabelas, realizaremos as migrações

# python3 migrations.py db init