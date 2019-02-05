Install party
*************

The simplest way to install **party** is by creating a Docker image that sets up the required environment.

Note that the *./install_party.sh* script maps the $HOME directory of the host machine to the $HOME folder of the Docker container. This means that the $HOME folder of the
host machine and the $HOME of the party Docker container share the same files and folders.

Installation steps
------------------

- Install `Docker <https://docs.docker.com/install/>`_ for your platform

- *git clone https://github.com/osv-team/party* somewhere under $HOME

- *cd party*

- *./install_party.sh*

- *./start_party.sh*

Now you can execute examples from party or write your own examples.


Development environment
-----------------------

After launching the party Docker container (*./start_party.sh* command) you can type the following command at the container prompt:

*export PYTHONPATH="${PYTHONPATH}:/home/<user>/path/to/party/"*

This will allow you to have changes to the party package code taken into account for tests and examples.