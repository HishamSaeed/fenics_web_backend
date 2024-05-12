# fenics_web_fenics_backend
The backend for a web app for finite element simulation using fenics project

# Project Setup
## VM Setup
First update the VM by running the following commands 
```
sudo apt update
sudo apt upgrade
```

Then install the required python libraries, python3-pip and python3-venv, by running the following commands
```
sudo apt install python3-pip
sudo apt install python3-venv
```

## Install Fenics
legacy FEniCS  is used, no need to use FEniCSx, go to FEniCS download page  https://fenicsproject.org/download/, then go to
the page where legacy FEniCS can be installed https://fenicsproject.org/download/archive/.

Follow the instruction to install it on Ubuntu https://fenicsproject.org/download/archive/#:~:text=Ubuntu%20FEniCS%20on%20Ubuntu .
The Ubunut version used in development is Ubunut 22.04 Jammy

## Install Ngnix , supervisor and gunicorn
For production mode, a server application is required, the server application used in this project are ngnix and gunicorn

To install ngnix run the following command
```
sudo apt install nginx
sudo apt install supervisor
```

For gunicorn it should be installed in the next section since it is a python package, add it to the requirements.txt

## Set up nginx config file
/etc/nginx/sites-enabled
server {
    listen 80;
    server_name YOUR_IP_OR_DOMAIN;

    location / {
        proxy_pass http://localhost:8000;
        include /etc/nginx/proxy_params;
        proxy_redirect off;
    }
}

sudo systemctl restart nginx
sudo nginx -t
## Problems with supervisor
## Create virtual environement
Clone the repository in the chosen directory on local PC or Azure/AWS Cloud Deployment VM, by running the command
`git clone <ssh-project-key>`

After Cloning the project go to the project directory, then create the virtual environement, activate virtual environement, install requirements

```
cd fenics_web_backend
python3 -m venv fenicsWeb
source fenicsWeb/bin/activate
pip install -r requirements.txt
```

## FEniCS required packages to link
dolfin-bin
dolfin-doc 
fenics 
ksh 
ksh93u+m 
libdolfin-dev 
libdolfin-dev-common 
libdolfin2019.2gcc13 
libgraphblas-dev 
libgraphblas6 
libhypre-dev 
libldl2 
libmongoose2 
libmshr-dev 
libmshr-dev-common
libmshr2019.2 
libmumps-dev 
libmumps-headers-dev 
libparpack2 
libparpack2-dev 
libpetsc-real3.15-dev 
libpetsc3.15-dev-common 
libpetsc3.15-dev-examples 
libptscotch-dev 
librbio2 
libscalapack-mpi-dev
libscalapack-openmpi-dev 
libscotch-dev 
libslepc-real3.15 
libslepc-real3.15-dev 
libsliplu1 
libspqr2 
libsuitesparse-dev 
libsuperlu-dist-dev 
libtet1.5 
libtrilinos-aztecoo-dev 
libtrilinos-ml-dev
libtrilinos-trilinosss-dev 
libtrilinos-zoltan-dev 
libyaml-dev 
pybind11-dev 
                                                python-petsc4py-doc 
                                                python-ufl-legacy-doc 
                                                python3-dijitso 
                                                python3-dolfin 
                                                python3-dolfin-real 
                                                python3-ffc 
                                                python3-fiat
                                                python3-mshr 
                                                python3-mshr-real 
                                                python3-petsc4py 
                                                python3-petsc4py-real 
                                                python3-petsc4py-real3.15 
                                                python3-pkgconfig 
                                                python3-pybind11 
python3-slepc4py 
python3-slepc4py-real 
python3-slepc4py-real3.15
                                                python3-ufl-legacy 
swig 
swig4.0 
trilinos-dev


## Packages
fenics
fenics-dijitso      /usr/lib/python3/dist-packages            
fenics-dolfin     /usr/lib/python3/dist-packages            
fenics-ffc        /usr/lib/python3/dist-packages           
fenics-fiat       /usr/lib/python3/dist-packages              
fenics-ufl-legacy  /usr/lib/python3/dist-packages
pkgconfig /usr/lib/python3/dist-packages pkgconfig pkgconfig-1.5.5.egg-info
pybind11 /usr/lib/python3/dist-packages pybind11 pybind11-2.9.1.egg-info

mshr  /usr/lib/mshr/python3/dist-packages mshr mshr-2019.2.0.dev0.egg-info

petsc4py /usr/lib/petscdir/petsc3.15/x86_64-linux-gnu-real/lib/python3/dist-packages dolfin petsc4py petsc4py-3.15.1.egg-info
slepc4py /usr/lib/slepcdir/slepc3.15/x86_64-linux-gnu-real/lib/python3/dist-packages slepc4py slepc4py-3.15.1.egg-info
## Setup FEniCS to work with the virtual environement
Since FEniCS cannot be installed using pip since the avalaible packages are only meta packages and it can only be installed via apt on
Ubuntu, and when the virtual environement is activated, the FEniCS packages cannot be detected and ModuleNotFoundError: No module named ‘fenics’ is thrown when trying to import it. A link can be made to the virtual environement

Go to fenicsWeb/lib/python3.10/site-packages and link the required libraries through the command ln -s /usr/lib/fenics fenics, this can be achieved the following commands
```
ln -s /usr/lib/python3/dist-packages fenics
ln -s /usr/lib/python3/dist-packages fenics_dijitso-2019.2.0.dev0.egg-info &&
ln -s /usr/lib/python3/dist-packages fenics_dolfin-2019.2.0.13.dev0.egg-info &&
ln -s /usr/lib/python3/dist-packages fenics_ffc-2019.2.0.dev0.egg-info &&
ln -s /usr/lib/python3/dist-packages fenics_fiat-2019.2.0.dev0.egg-info &&
ln -s /usr/lib/python3/dist-packages fenics_ufl_legacy-2022.3.0.dist-info &&
```

This should link FEniCS to the created virtual environement, to make sure it worked, activate virtual environement and list installed packages using pip

```
source fenicsWeb/bin/activate
pip list
```

## Run the program in developement mode
set the main.py file as the entry point for the flask server by running the following command
`export FLASK_APP=main.py`
`flask run --host=0.0.0.0`

## For Running it in production mode
Go to the project directory and run the following command
`gunicorn -w 3 main:app`
where -w n is for setting the number of workers <file-name>:<app-name>
to determine number of workers (2 x num_cores) + 1
to see number of cores run nproc --all